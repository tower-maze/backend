from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(['GET'])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    # players = room.playerNames(player_id)
    return JsonResponse({'x': room.x, 'y': room.y, 'maze': room.maze.id}, safe=True)


# @csrf_exempt
@api_view(['POST'])
def move(request):
    data = request.data
    direction = data['direction']
    player = request.user.player
    try:
        new_room = player.move(direction)
        return JsonResponse({'x': new_room.x, 'y': new_room.y})
    except:
        return JsonResponse({'message': 'Invalid Direction'}, status=400)


@csrf_exempt
@api_view(['POST'])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': 'Not yet implemented'}, safe=True, status=500)
