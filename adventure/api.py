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
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.player_names(player_id)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    player = request.user.player
    data = json.loads(request.body)
    direction = data['direction']
    new_room = player.move(direction)
    return JsonResponse({'x': new_room.x, 'y': new_room.y})


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)


# @csrf_exempt
# @api_view(["GET"])
# def rooms(request):
#     user = request.user
#     player = user.player
#     player_id = player.id
#     return JsonResponse([{
#         'room_id': index,
#         'north': room.y-1_to != 0,
#         'south': room.y+1_to != 0,
#         'east': room.x+1_to != 0,
#         'west': room.x-1_to != 0,
#         'title': room.title,
#         'description': room.description,
#         'players': room.allPlayerNames()
#     } for index, room in enumerate(Room.objects.all())], safe=False)
