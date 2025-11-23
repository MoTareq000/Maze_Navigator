import random

def generate_maze(rows, cols, wall_prob=0.3):
    """Generates a maze (0=open, 1=wall) and returns (maze, goal_position)."""

    maze = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(1 if random.random() < wall_prob else 0)
        maze.append(row)

    # Start always open
    maze[0][0] = 0

    # Random goal not equal to start
    while True:
        gr = random.randint(0, rows - 1)
        gc = random.randint(0, cols - 1)
        if (gr, gc) != (0, 0) and maze[gr][gc] == 0:
            return maze, (gr, gc)
