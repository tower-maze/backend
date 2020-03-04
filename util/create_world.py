from django.contrib.auth.models import User
from django.db import transaction
from adventure.models import Player, Room, Maze

Maze.objects.all().delete()
Room.objects.all().delete()

with transaction.atomic():
    for i in range(1, 10):
        maze = Maze()
        maze.generate_connections()
        maze.title = f"Floor {i}"
        maze.save()

    players = Player.objects.all()
    for player in players:
        player.current_room = Room.objects.first().id
        player.save()
