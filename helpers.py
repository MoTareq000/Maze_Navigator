# helpers.py
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

def plot_maze(maze, paths=None, visited_nodes_list=None,
              agent_img=None, goal_img=None, goal_pos=None):
    """
    Draw maze using imshow for walls and overlay agent/goal images using AnnotationBbox.
    - maze: 2D list (0=open, 1=wall)
    - paths: list of path lists (each path is list of (r,c))
    - visited_nodes_list: list of visited node lists (each is list of (r,c))
    - agent_img, goal_img: PIL.Image or numpy array (will be converted)
    - goal_pos: tuple (r,c)
    Returns matplotlib.figure.Figure
    """
    maze = np.array(maze)
    rows, cols = maze.shape
    # Convert maze 0=open, 1=wall into a numpy array for plotting

    grid = np.array([[0 if maze[r][c]==0 else 1 for c in range(len(maze[0]))] for r in range(len(maze))])
    fig, ax = plt.subplots(figsize=(cols/2, rows/2))
  # dynamically scale
    ax.imshow(grid, cmap='Blues', origin='upper')           # nicer colors


    # Draw grid: show walls as 1 and free as 0 (binary colormap)
    ax.imshow(maze, cmap="Greys", interpolation='nearest', origin='upper')

    # Ensure equal aspect and exact cell coordinates
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)  # invert y to match matrix indexing
    ax.set_aspect('equal')

    # Draw visited nodes (small dots)
    if visited_nodes_list:
        for visited in visited_nodes_list:
            if not visited:
                continue
            vr = [v[0] for v in visited]
            vc = [v[1] for v in visited]
            ax.scatter(vc, vr, s=20, alpha=0.5, marker='s')

    # Draw all paths (lines)
    if paths:
        for path in paths:
            if not path:
                continue
            pr = [p[0] for p in path]
            pc = [p[1] for p in path]
            ax.plot(pc, pr, linewidth=2)

    # Helper to create OffsetImage from PIL or numpy
    def _make_offset(img):
        if img is None:
            return None
        arr = np.asarray(img)  # works if img is PIL.Image or np.array
        return OffsetImage(arr, zoom=1.0)

    # Plot goal image centered on its cell using AnnotationBbox
    if goal_img is not None and goal_pos is not None:
        off = _make_offset(goal_img)
        if off is not None:
            ab = AnnotationBbox(off, (goal_pos[1], goal_pos[0]), frameon=False, pad=0.0)
            ax.add_artist(ab)

    # Plot agent image at last position of last path
    if agent_img is not None and paths and len(paths) > 0 and paths[-1]:
        last = paths[-1][-1]
        off = _make_offset(agent_img)
        if off is not None:
            ab = AnnotationBbox(off, (last[1], last[0]), frameon=False, pad=0.0)
            ax.add_artist(ab)

    # Start marker (green) — optional but useful
    ax.scatter(0, 0, color='green', s=80, edgecolors='black', zorder=5)

    # Remove ticks and margins
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    return fig
