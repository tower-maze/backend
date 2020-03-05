from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from util.stack import Stack
import uuid
import random


class Maze(models.Model):
    title = models.CharField(max_length=127, default="Default Title")
    start_room = models.IntegerField(default=-1)
    exit_room = models.IntegerField(default=-1)
    seed = models.CharField(max_length=1024, default='')
    rooms = None

    def __iter__(self):
        yield 'title', self.title
        yield 'rooms', self.get_rooms(callback=lambda room: dict(room))
        yield 'startRoom',  dict(self.get_room_by_id(self.start_room))
        yield 'exitRoom', dict(self.get_room_by_id(self.exit_room))

    def initialize(self, n=32):
        """loads the maze rooms into memory, generating new rooms if seed is missing"""
        # [
        #     [Room(x=0,y=0), Room(x=1,y=0), ...],
        #     [Room(x=0,y=1), Room(x=1,y=1), ...],
        #     ...
        # ]
        if not self.id:
            self.save()
        if not self.rooms:
            # generate room objects O(n^2) n=32
            self.rooms = [[Room(x + n*y, x, y, self) for x in range(n)]
                          for y in range(n)]
            if self.exit_room < 0 or self.start_room < 0:
                # select start and exit, save as (x,y) tuples
                x, y = random.randint(0, n-1), 0
                self.exit_room = x + n*y
                x, y = random.randint(0, n-1), n-1
                self.start_room = x + n*y
            # generate connections
            maze_start = self.get_room_by_id(self.start_room)
            maze_stack = Stack()
            maze_stack.push(maze_start)
            seed = self.seed
            if not seed:
                seed = ['0' for i in range(n**2)]
            i = 0
            # repeat until stack is empty O(n^2) n=32
            while len(maze_stack):
                room = maze_stack.get_head()
                # pick a random, available direction
                available_rooms = room.get_available_rooms()
                if len(available_rooms):
                    if self.seed:
                        index = int(self.seed[i])
                    else:
                        index = random.choice(range(len(available_rooms)))
                        seed[i] = str(index)
                    next_room = available_rooms[index]
                    # connect and add next room to stack
                    room.connect(next_room)
                    maze_stack.push(next_room)
                    i += 1
                # if dead end, go back through stack
                else:
                    maze_stack.pop()
            # save seed, start, and exit
            if not self.seed:
                self.seed = ''.join(seed)
            self.save()

    def get_rooms(self, callback=None):
        if not self.rooms:
            self.initialize()
        if not callback:
            return self.rooms
        else:
            return [[callback(room) for room in row] for row in self.rooms]

    def get_room(self, x, y):
        """returns Room or None"""
        if not self.rooms:
            self.initialize()
        if x < 0 or y < 0:
            return None
        try:
            return self.rooms[y][x]
        except IndexError:
            return None

    def get_room_by_id(self, room_id):
        if not self.rooms:
            self.initialize()
        y = room_id // len(self.rooms)
        x = room_id % len(self.rooms)
        return self.get_room(x, y)


class Room():
    north_connection = 0
    east_connection = 0
    south_connection = 0
    west_connection = 0

    def __init__(self, n, x, y, maze, **kwargs):
        self.id = n
        self.x = x
        self.y = y
        self.maze = maze
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __iter__(self):
        yield 'x', int(self.x)
        yield 'y', int(self.y)
        yield 'n', int(self.north_connection)
        yield 'e', int(self.east_connection)
        yield 's', int(self.south_connection)
        yield 'w', int(self.west_connection)

    def connect(self, room):
        if self.y > room.y:
            self.north_connection = 1
            room.south_connection = 1
        elif self.y < room.y:
            self.south_connection = 1
            room.north_connection = 1
        elif self.x < room.x:
            self.east_connection = 1
            room.west_connection = 1
        elif self.x > room.x:
            self.west_connection = 1
            room.east_connection = 1

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

        def is_available(room):
            if room:
                return room.count_connections() == 0
            return False

        return [*filter(is_available, rooms)]

    def get_room_north(self):
        return self.maze.get_room(self.x, self.y-1)

    def get_room_east(self):
        return self.maze.get_room(self.x+1, self.y)

    def get_room_south(self):
        return self.maze.get_room(self.x, self.y+1)

    def get_room_west(self):
        return self.maze.get_room(self.x-1, self.y)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_maze = models.IntegerField(default=-1)
    current_room = models.IntegerField(default=-1)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __iter__(self):
        room = self.room()
        yield 'player', self.id
        yield 'x', room.x
        yield 'y', room.y

    def initialize(self):
        first_maze = Maze.objects.first()
        self.current_maze = first_maze.id
        self.current_room = first_maze.start_room
        self.save()

    def room(self):
        maze = self.maze()
        room = maze.get_room_by_id(self.current_room)
        if room:
            return room
        else:
            self.initialize()
            return self.room()

    def maze(self):
        try:
            return Maze.objects.get(id=self.current_maze)
        except Maze.DoesNotExist:
            self.initialize()
            return self.maze()

    def set_room(self, room):
        self.current_room = room.id
        maze = self.maze()
        if self.current_room == maze.exit_room and self.current_maze != Maze.objects.last().id:
            self.current_maze += 1
            self.current_room = self.maze().start_room
        elif self.current_room == maze.start_room and self.current_maze != Maze.objects.first().id:
            self.current_maze -= 1
            self.current_room = self.maze().exit_room
        self.save()

    def move(self, direction):
        room = self.room()
        if direction == 'n' and room.north_connection:
            new_room = room.get_room_north()
        elif direction == 's' and room.south_connection:
            new_room = room.get_room_south()
        elif direction == 'e' and room.east_connection:
            new_room = room.get_room_east()
        elif direction == 'w' and room.west_connection:
            new_room = room.get_room_west()
        else:
            raise Exception('Invalid Direction')
        self.set_room(new_room)
        return self.room()

    def see_others(self):
        players = Player.objects.filter(current_maze=self.current_maze)
        players = players.exclude(id=self.id)
        player_positions = [dict(player) for player in players]
        return player_positions


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
