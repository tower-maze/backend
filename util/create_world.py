from django.contrib.auth.models import User
from adventure.models import Player, Room, Maze

Maze.objects.all().delete()
Room.objects.all().delete()

for i in range(1, 10):
    maze = Maze()
    maze.generate_connections()
    maze.title = f"Floor {i}"
    maze.save()


players = Player.objects.all()
for player in players:
    player.initialize()
