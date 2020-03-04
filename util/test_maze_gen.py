from adventure.models import Maze

maze = Maze()
maze.title = "My First Maze"
maze.initialize(8)
for row in maze.rooms:
    print(row)

