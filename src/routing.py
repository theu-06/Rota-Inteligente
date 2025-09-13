
import math
from .algorithms import astar

def pairwise_astar_matrix(G, nodes, weight="time"):
    # pré-calcular os custos A* entre todos os nodes na lista
    costs = {}
    paths = {}
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            u, v = nodes[i], nodes[j]
            c, p = astar(u, v, G.neighbors, lambda a,b: G.cost(a,b,weight=weight), lambda a,b: G.heuristic(a,b))
            costs[(u,v)] = costs[(v,u)] = c
            paths[(u,v)] = p
            paths[(v,u)] = list(reversed(p))
    return costs, paths

def nearest_neighbor_route(G, stops, start):
    """Nearest-neighbor heuristic to visit all 'stops' starting from 'start'."""
    remaining = set(stops)
    route = [start]
    cur = start
    while remaining:
        
        best = None
        best_cost = float("inf")
        for v in list(remaining):
            c, _ = astar(cur, v, G.neighbors, lambda a,b: G.cost(a,b,weight="time"), lambda a,b: G.heuristic(a,b))
            if c < best_cost:
                best_cost = c
                best = v
        route.append(best)
        cur = best
        remaining.remove(best)
    return route

def route_cost(G, route, weight="time"):
    total = 0.0
    for i in range(len(route)-1):
        c, _ = astar(route[i], route[i+1], G.neighbors, lambda a,b: G.cost(a,b,weight=weight), lambda a,b: G.heuristic(a,b))
        total += c
    return total
