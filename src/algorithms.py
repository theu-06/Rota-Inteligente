
import math
import heapq

def astar(start, goal, neighbors_fn, cost_fn, heuristic_fn):
    """Generic A* search returning (cost, path)."""
    open_set = [(0, start)]
    came_from = {start: None}
    g = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            # path reconstruído
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return g[path[-1]], path

        for nxt in neighbors_fn(current):
            tentative_g = g[current] + cost_fn(current, nxt)
            if nxt not in g or tentative_g < g[nxt]:
                g[nxt] = tentative_g
                priority = tentative_g + heuristic_fn(nxt, goal)
                heapq.heappush(open_set, (priority, nxt))
                came_from[nxt] = current

    return float("inf"), []

def bfs(start, goal, neighbors_fn):
    """BFS for unweighted graphs, returns path (ignores weights)."""
    from collections import deque
    q = deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        if u == goal: break
        for v in neighbors_fn(u):
            if v not in parent:
                parent[v] = u
                q.append(v)
    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return list(reversed(path))

def dfs(start, goal, neighbors_fn):
    """DFS returns path if found."""
    stack = [start]
    parent = {start: None}
    while stack:
        u = stack.pop()
        if u == goal: break
        for v in neighbors_fn(u):
            if v not in parent:
                parent[v] = u
                stack.append(v)
    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return list(reversed(path))
