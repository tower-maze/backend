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
    dirs = {"y"-1: "north", "y"+1: "south", "x"+1: "east", "x"-1: "west"}
    reverse_dirs = {"y"-1: "south", "y"+1: "north",
                    "x"+1: "west", "x"-1: "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    next_room_id = None
    if direction == "n":
        next_room_id = room.n_to
    elif direction == "s":
        next_room_id = room.s_to
    elif direction == "e":
        next_room_id = room.e_to
    elif direction == "w":
        next_room_id = room.w_to
    if next_room_id is not None and next_room_id > 0:
        next_room = Room.objects.get(id=next_room_id)
        player.current_room = next_room_id
        player.save()
        players = next_room.player_names(player_id)
        current_player_uuids = room.player_uuids(player_id)
        next_player_uuids = next_room.player_uuids(player_id)
        # for p_uuid in current_player_uuids:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in next_player_uuids:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title': next_room.title, 'description': next_room.description, 'players': players, 'error_msg': ""}, safe=True)
    else:
        players = room.player_names(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


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
