import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def petersen_edges():
    outer = [(i, (i + 1) % 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    return outer + inner + spokes

def petersen_undirected():
    A = np.zeros((10, 10), dtype=np.int64)
    for u, v in petersen_edges():
        A[u, v] = A[v, u] = 1
    return A

def petersen_random_orientation(rng, weights=None):
    A = np.zeros((10,10), dtype=np.int64)
    flips = rng.random(15) < 0.5
    for (u, v), f in zip(petersen_edges(), flips):
        if f:
            u, v = v, u
        A[u, v] = 1
    if weights is not None:
        A = A * rng.integers(weights[0], weights[1] + 1, size=(10,10))
    return A

def random_digraph(n, prob, rng, weights=None):
    A = (rng.random((n, n)) < prob).astype(np.int64)
    np.fill_diagonal(A, 0)
    if weights is not None:
        A = A * rng.integers(weights[0], weights[1] + 1, size=(n, n))
    return A

def is_strongly_connected(A):
    return nx.is_strongly_connected(nx.from_numpy_array((A != 0).astype(int), create_using=nx.DiGraph))

def draw_graph(A, path, title="", directed=True, weighted=False, pos=None, highlight=None):
    A = np.asarray(A)
    G = nx.from_numpy_array(A, create_using=nx.DiGraph if directed else nx.Graph)
    if pos is None:
        if len(A) == 10:
            ang = np.pi / 2 + 2 * np.pi * np.arange(5) / 5
            pos = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(ang)}
            pos.update({5 + i: (0.5 * np.cos(a), 0.5 * np.sin(a)) for i, a in enumerate(ang)})
        else:
            pos = nx.spring_layout(G, seed=1)
    fig, ax = plt.subplots(figsize=(6,6), dpi=150)
    hl = set(highlight or [])
    colors = ["#d1488b" if (u, v) in hl else "#4a5567" for u, v in G.edges()]
    widths = [2.6 if (u, v) in hl else 1.4 for u, v in G.edges()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#edae52", node_size=520, edgecolors="#313b46")
    nx.draw_networkx_labels(G, pos, ax=ax, labels={i: str(i + 1) for i in G.nodes()}, font_size=11)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=colors, width=widths,
                           node_size=520, **({"arrows": True, "arrowsize": 18} if directed else {}))

    if weighted:
        lbl = {(u, v): int(d["weight"]) for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=lbl, ax=ax, font_size=9,
                                     label_pos=0.5, rotate=False)
    ax.set_title(title, fontsize=12)
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)