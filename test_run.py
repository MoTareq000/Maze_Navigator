from maze_generator import generate_maze
from search_algorithms import bfs, a_star
from helpers import plot_maze
import matplotlib.pyplot as plt

maze = generate_maze(10, 10, wall_prob=0.3)

# Run BFS and A*
path_bfs, visited_bfs = bfs(maze)
path_a, visited_a = a_star(maze)

# Compare in one figure
fig = plot_maze(
    maze, 
    paths=[path_bfs, path_a], 
    visited_nodes_list=[visited_bfs, visited_a], 
    labels=['BFS', 'A*']
)
plt.show()
input("Press Enter to exit...")
