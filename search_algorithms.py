from collections import deque
import heapq

# -------------------------
# BFS Step-by-Step
# -------------------------
def bfs_steps(maze, start=(0, 0), goal=None):
    if goal is None:
        raise ValueError("Goal must be provided to BFS")

    rows, cols = len(maze), len(maze[0])
    visited = set()
    queue = deque([(start, [start], 0)])  # (pos, path, cost)
    visited.add(start)

    while queue:
        (r, c), path, cost = queue.popleft()

        yield path, cost, visited.copy()

        if (r, c) == goal:
            return

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)], cost + 1))


# -------------------------
# A* Step-by-Step
# -------------------------
def a_star_steps(maze, start=(0, 0), goal=None):
    if goal is None:
        raise ValueError("Goal must be provided to A*")

    rows, cols = len(maze), len(maze[0])
    visited = set()

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, 0, start, [start]))  # (f, g, current, path)

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)
        yield path, g, visited.copy()

        if current == goal:
            return

        r, c = current
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    g_new = g + 1
                    f_new = g_new + heuristic((nr, nc), goal)
                    heapq.heappush(open_set, (f_new, g_new, (nr, nc), path + [(nr, nc)]))
