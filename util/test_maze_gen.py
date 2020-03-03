from adventure.models import Maze

maze = Maze()
maze.title = "My First Maze"
maze.generate_connections()
maze.save()