
import os
import json
import pandas as pd
from .graph import CityGraph
from .algorithms import astar, bfs, dfs
from .clustering import cluster_deliveries
from .routing import nearest_neighbor_route, route_cost
from .visualize import draw_graph, draw_clusters

def run(data_dir, out_dir, k_clusters=3, depot_name="Centro"):
    nodes_csv = os.path.join(data_dir, "nodes.csv")
    edges_csv = os.path.join(data_dir, "edges.csv")
    deliveries_csv = os.path.join(data_dir, "deliveries.csv")

    G = CityGraph(nodes_csv, edges_csv)
    nodes_df = pd.read_csv(nodes_csv)
    # depot e um node com nome fornecido
    depot_id = int(nodes_df[nodes_df["name"]==depot_name]["id"].iloc[0])

    # demonstração rápida do caminho mais curto com A*
    goal_id = int(nodes_df["id"].iloc[-1])
    cost_astar, path_astar = astar(depot_id, goal_id, G.neighbors, lambda a,b: G.cost(a,b,weight="time"), lambda a,b: G.heuristic(a,b))
    # Caminhos BFS/DFS (não ponderados)
    path_bfs = bfs(depot_id, goal_id, G.neighbors)
    path_dfs = dfs(depot_id, goal_id, G.neighbors)

    # visualizar gráfico base e caminho A*
    draw_graph(G, path=path_astar, save_path=os.path.join(out_dir, "graph_astar.png"), title="Grafo e Caminho A*")

    # clustering de entregas
    df_deliv, centers = cluster_deliveries(deliveries_csv, k=k_clusters)
    df_deliv.to_csv(os.path.join(out_dir, "deliveries_clustered.csv"), index=False)
    draw_clusters(df_deliv, centers, save_path=os.path.join(out_dir, "clusters.png"))

    # entregas de mapas para o node mais próximo (paradas)
    stops_by_cluster = {}
    for c, grp in df_deliv.groupby("cluster"):
        stops_by_cluster[c] = sorted(set(int(n) for n in grp["node_id"].tolist()))

    # Construir rotas por cluster a partir do depot
    routes = {}
    costs = {}
    total_cost = 0.0
    for c, stops in stops_by_cluster.items():
        if depot_id not in stops:
            route = nearest_neighbor_route(G, stops, start=depot_id)
        else:
            route = nearest_neighbor_route(G, [s for s in stops if s != depot_id], start=depot_id)
        routes[c] = route
        rcost = route_cost(G, route, weight="time")
        costs[c] = rcost
        total_cost += rcost

    # linha de base: ordem por ID do node
    unique_stops = sorted(set(int(n) for n in df_deliv["node_id"].tolist()))
    baseline_route = [depot_id] + unique_stops
    baseline_cost = route_cost(G, baseline_route, weight="time")

    # salvar métricas
    results = {
        "astar_demo": {"from": int(depot_id), "to": int(goal_id), "cost_time": float(cost_astar), "path": [int(x) for x in path_astar]},
        "bfs_demo_path": [int(x) for x in path_bfs],
        "dfs_demo_path": [int(x) for x in path_dfs],
        "cluster_routes": {int(k): [int(x) for x in v] for k, v in routes.items()},
        "cluster_costs_time": {int(k): float(v) for k, v in costs.items()},
        "optimized_total_cost_time": float(total_cost),
        "baseline_route": [int(x) for x in baseline_route],
        "baseline_total_cost_time": float(baseline_cost),
        "improvement_percent": float((baseline_cost - total_cost)/baseline_cost * 100.0) if baseline_cost > 0 else 0.0
    }
    with open(os.path.join(out_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # retornar string de resumo
    return (
        f"A* custo (tempo) de {depot_id} para {goal_id}: {cost_astar:.2f}\n"
        f"Baseline tempo total: {baseline_cost:.2f}\n"
        f"Otimizado tempo total: {total_cost:.2f}\n"
        f"Melhoria: {results['improvement_percent']:.2f}%"
    )
