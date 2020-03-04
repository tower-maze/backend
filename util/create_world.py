from django.db import transaction
from django.contrib.auth.models import User
from adventure.models import Player, Room, Maze

Maze.objects.all().delete()
players = Player.objects.all()

with transaction.atomic():
    for i in range(1, 101):
        maze = Maze()
        maze.title = f"Floor {i}"
        maze.initialize()
        if i == 1:
            print('')
        print(maze.title, 'created')

with transaction.atomic():
    for player in players:
        player.initialize()
