
import matplotlib.pyplot as plt

def draw_graph(G, path=None, save_path=None, title="Grafo da Cidade"):
    xs = [G.pos[n][0] for n in G.pos]
    ys = [G.pos[n][1] for n in G.pos]
    plt.figure(figsize=(7,5))
    # nodes
    plt.scatter(xs, ys)
    # edges
    for u in G.adj:
        for v in G.adj[u]:
            if u < v:
                x = [G.pos[u][0], G.pos[v][0]]
                y = [G.pos[u][1], G.pos[v][1]]
                plt.plot(x, y)
    
    for nid, (x, y) in G.pos.items():
        plt.text(x, y, str(nid), fontsize=9)
    # path
    if path:
        px = [G.pos[u][0] for u in path]
        py = [G.pos[u][1] for u in path]
        plt.plot(px, py, linewidth=2)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def draw_clusters(df, centers, save_path=None, title="Entregas por Cluster"):
    plt.figure(figsize=(7,5))
    plt.scatter(df["addr_x"], df["addr_y"])
    plt.scatter(centers[:,0], centers[:,1], marker="x", s=100)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.close()
