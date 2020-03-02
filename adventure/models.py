from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import random

from ..util.stack import Stack

class Maze(models.Model):
    title = models.CharField(max_length=127)

    def initialize(self):
        """returns 2D array grid of maze rooms, creating them if missing"""
        # [
        #     [Room(x=0,y=0), Room(x=1,y=0), ...],
        #     [Room(x=0,y=1), Room(x=1,y=1), ...],
        #     ...
        # ]
        rooms = Room.objects.filter(maze=self.id)
        if len(rooms) != 32*32:
            for y in range(32):
                for x in range(32):
                    room = Room.objects.create()
                    room.x = x
                    room.y = y
                    room.maze = self.id
                    room.save()
            rooms = Room.objects.filter(maze=self.id)
        return [[rooms[i] for i in range(j*32, (j+1)*32)] for j in range(32)]

    def generate_connections(self):
        rooms = self.initialize()
        maze_start = random.choice(rooms[31]) # bottom row
        maze_exit = random.choice(rooms[0]) # top row
        maze_stack = Stack()
        maze_stack.push(maze_start)
        while len(maze_stack):
            pass
            # pick a random, available direction
            # add next room to stack
            # move to next room
            # repeat until no more available directions 
                # (edge of map or already has 2 connections)
            # pop from stack until you have available directions
            # repeat until stack is empty


class Room(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    north_connection = models.BooleanField(default=False)
    east_connection = models.BooleanField(default=False)
    south_connection = models.BooleanField(default=False)
    west_connection = models.BooleanField(default=False)
    maze = models.IntegerField(default=0)

    def connect(self, room):
        if self.y < room.y:
            self.north_connection = True
            room.south_connection = True
        elif self.y > room.y:
            self.south_connection = True
            room.north_connection = True
        elif self.x < room.x:
            self.east_connection = True
            room.west_connection = True
        elif self.x > room.x:
            self.west_connection = True
            room.east_connection = True
        self.save()
        room.save()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.current_room == 0:
            self.current_room = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.current_room)
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
