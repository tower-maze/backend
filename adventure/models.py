from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import random

from util.stack import Stack

class Maze(models.Model):
    title = models.CharField(max_length=127, default="Default Title")

    def initialize(self):
        """returns 2D array grid of maze rooms, creating them if missing"""
        # [
        #     [Room(x=0,y=0), Room(x=1,y=0), ...],
        #     [Room(x=0,y=1), Room(x=1,y=1), ...],
        #     ...
        # ]
        if not self.id:
            self.save()
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
        assert(True, False)
        return [[rooms[i] for i in range(j*32, (j+1)*32)] for j in range(32)]

    def generate_connections(self):
        rooms = self.initialize()
        maze_start = random.choice(rooms[31]) # bottom row
        maze_exit = random.choice(rooms[0]) # top row
        maze_stack = Stack()
        maze_stack.push(maze_start)
        # repeat until stack is empty
        while len(maze_stack):
            # assert(True, False)
            room = maze_stack.get_head()
            # pick a random, available direction
            available_rooms = room.get_available_rooms()
            if len(available_rooms):
                next_room = random.choice(available_rooms)
                # connect and add next room to stack
                room.connect(next_room)
                maze_stack.push(next_room)
            # if dead end, go back through stack
            else:
                maze_stack.pop()


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

    def count_connections(self):
        count = 0
        count += self.north_connection
        count += self.east_connection
        count += self.south_connection
        count += self.west_connection
        return count

    def get_available_rooms(self):
        rooms = [self.get_room_north(), self.get_room_east(),
                 self.get_room_south(), self.get_room_west()]
        return filter(lambda room: room and room.count_connectons() == 0, rooms)

    def get_room_north(self):
        try:
            return Room.objects.get(maze=self.maze, x=self.x, y=self.y-1)
        except Room.DoesNotExist:
            return None

    def get_room_east(self):
        try:
            return Room.objects.get(maze=self.maze, x=self.x+1, y=self.y)
        except Room.DoesNotExist:
            return None

    def get_room_south(self):
        try:
            return Room.objects.get(maze=self.maze, x=self.x, y=self.y+1)
        except Room.DoesNotExist:
            return None

    def get_room_west(self):
        try:
            return Room.objects.get(maze=self.maze, x=self.x-1, y=self.y)
        except Room.DoesNotExist:
            return None


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
