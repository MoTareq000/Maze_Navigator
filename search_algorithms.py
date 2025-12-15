from collections import deque
import heapq

# -------------------------
# BFS Step-by-Step
# -------------------------
from collections import deque

def bfs_steps(maze, start=(0, 0), goal=None):
    if goal is None:
        raise ValueError("Goal must be provided to BFS")

    rows, cols = len(maze), len(maze[0])
    visited = set()

    queue = deque([[(start, 0)]])  # path = [(pos, cost)]

    while queue:
        path = queue.popleft()
        current, _ = path[-1]

        if current in visited:
            continue

        visited.add(current)

        cost = sum(c for _, c in path)
        yield [pos for pos, _ in path], cost, visited.copy()

        if current == goal:
            return

        r, c = current
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and neighbor not in visited:
                    queue.append(path + [(neighbor, 1)])


# -------------------------
# A* Step-by-Step
# -------------------------
import heapq
import time

def a_star_steps(maze, start=(0, 0), goal=None):
    if goal is None:
        raise ValueError("Goal must be provided to A*")

    rows, cols = len(maze), len(maze[0])
    visited = set()

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), [(start, 0)]))
    expanded_states = 0

    while open_set:
        f, path = heapq.heappop(open_set)
        expanded_states += 1

        current, _ = path[-1]

        if current in visited:
            continue

        visited.add(current)

        g = sum(cost for _, cost in path)
        yield [pos for pos, _ in path], g, visited.copy()

        if current == goal:
            return

        r, c = current
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and neighbor not in visited:
                    new_path = path + [(neighbor, 1)]
                    g_new = g + 1
                    f_new = g_new + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_new, new_path))
def dfs_steps(maze, start=(0, 0), goal=None):
    if goal is None:
        raise ValueError("Goal must be provided to DFS")

    rows, cols = len(maze), len(maze[0])
    visited = set()

    stack = [[(start, 0)]]  # path = [(pos, cost)]

    while stack:
        path = stack.pop()
        current, _ = path[-1]

        if current in visited:
            continue

        visited.add(current)

        cost = sum(c for _, c in path)
        yield [pos for pos, _ in path], cost, visited.copy()

        if current == goal:
            return

        r, c = current

        # Reverse order so DFS visually matches typical expectations
        for dr, dc in reversed([(-1,0), (1,0), (0,-1), (0,1)]):
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and neighbor not in visited:
                    stack.append(path + [(neighbor, 1)])
