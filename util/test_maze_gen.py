from adventure.models import Maze

maze = Maze()
maze.generate_connections()
maze.title = "My First Maze"
maze.save()