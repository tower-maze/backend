from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from .models import *
from rest_framework.decorators import api_view

# instantiate pusher
pusher = Pusher(
    app_id=config('PUSHER_APP_ID'),
    key=config('PUSHER_KEY'),
    secret=config('PUSHER_SECRET'),
    cluster=config('PUSHER_CLUSTER')
)


@api_view(['GET'])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    return JsonResponse({'maze': room.maze.id, 'x': room.x, 'y': room.y}, safe=True)


@api_view(['GET'])
def get_maze(request):
    maze = dict(request.user.player.maze())
    return JsonResponse(maze, safe=True)


@api_view(['GET'])
def other_players(request):
    user = request.user
    player = user.player
    others = player.see_others()
    return JsonResponse({'others': others})


@api_view(['POST'])
def move(request):
    player = request.user.player
    prev_maze = player.current_maze
    try:
        room = player.move(request.data['direction'])
        maze = dict(player.maze()) if prev_maze != room.maze.id else None
        position = {'x': room.x, 'y': room.y}
        pusher.trigger('Tower-Maze', 'movement',
                       {'player': player.id, 'position': position})
        return JsonResponse({'player': {**position, 'maze': room.maze.id}, 'nextMaze': maze}, safe=True)
    except:
        return JsonResponse({'detail': 'Invalid Direction'}, safe=True, status=400)


@api_view(['POST'])
def say(request):
    # IMPLEMENT
    return JsonResponse({'detail': 'Not yet implemented'}, safe=True, status=500)
