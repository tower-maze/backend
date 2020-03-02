from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(x=1, y=1, maze=0)

r_outside.save()

players = Player.objects.all()
for p in players:
    p.current_room = r_outside.id
    p.save()