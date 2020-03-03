from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    maze = models.IntegerField(default=0)


def connectRooms(self, upcomingRoom, direction):
    upcomingRoomID = upcomingRoom.id
    try:
        upcomingRoom = Room.objects.get(id=upcomingRoomID)
    except Room.DoesNotExist:
        print("You have reached a dead-end")
    else:
        if direction == "y"-1:
            self.n_to = upcomingRoomID
        elif direction == "y"+1:
            self.s_to = upcomingRoomID
        elif direction == "x"+1:
            self.e_to = upcomingRoomID
        elif direction == "x"-1:
            self.w_to = upcomingRoomID
        else:
            print("Invalid direction")
            return
        self.save()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = player.currentRoom = upcomingRoomID
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
