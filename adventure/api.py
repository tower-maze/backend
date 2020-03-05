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
    return JsonResponse({'maze': room.maze.id, 'x': room.x, 'y': room.y}, safe=True)


@csrf_exempt
@api_view(['GET'])
def get_maze(request):
    maze = request.user.player.maze()
    rooms = maze.get_rooms(callback=lambda room: dict(room))
    start_room = dict(maze.get_room_by_id(maze.start_room))
    exit_room = dict(maze.get_room_by_id(maze.exit_room))
    return JsonResponse({'title': maze.title, 'rooms': rooms, 'startRoom': start_room, 'exitRoom': exit_room}, safe=True)


@csrf_exempt
@api_view(['GET'])
def other_players(request):
    user = request.user
    player = user.player
    others = player.see_others()
    return JsonResponse({'others': others})


@csrf_exempt
@api_view(['POST'])
def move(request):
    data = request.data
    direction = data['direction']
    directions = ['n', 's', 'e', 'w']
    player = request.user.player
    for i in range(1, 101):
        player.move(directions['n'])
        player.move(directions['s'])
        player.move(directions['e'])
        player.move(directions['w'])

        try:
            new_room = player.move(direction)
            return JsonResponse({'maze': new_room.maze.id, 'x': new_room.x, 'y': new_room.y})
        except:
            return JsonResponse({'message': 'Invalid Direction'}, safe=True, status=400)


@csrf_exempt
@api_view(['POST'])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': 'Not yet implemented'}, safe=True, status=500)
