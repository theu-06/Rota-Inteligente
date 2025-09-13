
import pandas as pd
import math

class CityGraph:
    def __init__(self, nodes_csv, edges_csv):
        self.nodes = pd.read_csv(nodes_csv)
        self.edges = pd.read_csv(edges_csv)
        self._build()

    def _build(self):
        self.pos = {int(r.id):(r.x, r.y) for _, r in self.nodes.iterrows()}
        self.adj = {int(nid): {} for nid in self.nodes.id}
        for _, e in self.edges.iterrows():
            u, v = int(e.source), int(e.target)
            self.adj[u][v] = {"distance": float(e.distance), "time": float(e.time)}
            self.adj[v][u] = {"distance": float(e.distance), "time": float(e.time)}

    def neighbors(self, u):
        return list(self.adj[u].keys())

    def cost(self, u, v, weight="time"):
        return self.adj[u][v][weight]

    def heuristic(self, u, v, expected_speed=0.4):
        # distância euclidiana / velocidade esperada (em unidades consistentes)
        (ux, uy) = self.pos[u]
        (vx, vy) = self.pos[v]
        return math.hypot(ux-vx, uy-vy)/expected_speed
