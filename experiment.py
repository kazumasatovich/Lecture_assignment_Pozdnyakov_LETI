import os, time
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.matrix_graph.matrix_multiplies import prepare, power_linear, power_binary, identity
from src.matrix_graph.graphs import petersen_random_orientation, random_digraph, draw_graph

os.makedirs("figures", exist_ok=True)
KINDS = ("ОБЫЧ", "БИН", "ТРОП")


def matrix_for(A, kind):
    n = len(A)
    if kind == "ОБЫЧ":
        return (A != 0).astype(np.int64)
    if kind == "БИН":
        return prepare(A, "БИН") | np.eye(n, dtype=bool)
    return prepare(A, "ТРОП", zero_diag=True)

def best_time(f, *args, repeat=3):
    result = f(*args)
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        f(*args)
        times.append(time.perf_counter() - t0)
    return min(times), result

# 1. Граф Петерсена со случайно ориентацией
SEED = 174
A = petersen_random_orientation(np.random.default_rng(SEED), weights=(1, 9))
n = len(A)
p = n - 1
G = nx.from_numpy_array(A, create_using=nx.DiGraph)
draw_graph(A, "figures/1_petersen.png", f"Граф Петерсена со случайной ориентацией по сиду {SEED}",
           weighted=True)

oracles = {
    "ОБЫЧ": np.linalg.matrix_power(matrix_for(A, "ОБЫЧ"), p),
    "БИН": nx.to_numpy_array(nx.transitive_closure(G, reflexive=True), nodelist=range(n), dtype=bool),
    "ТРОП": nx.floyd_warshall_numpy(G, nodelist=range(n)),
}

print(f"Граф Петерсена, сид: {SEED}, степень p = {p}")
for kind in KINDS:
    R = power_binary(matrix_for(A, kind), p, kind)
    print(f"\n{kind}: совпало с эталоном? - {np.array_equal(R, oracles[kind])}")
    print(np.array2string(R.astype(int) if kind == "БИН" else R, max_line_width=120))

# 2. Обычное и быстрое возведение в степень p = n - 1
NS = (50, 100, 200, 400)
rng = np.random.default_rng(7)
rows = []
for n in NS:
    A = random_digraph(n , 3 / n, rng, weights=(1, 9))
    row = {"n": n}
    for kind in KINDS:
        M = matrix_for(A, kind)
        if kind == "ОБЫЧ":
            M = M.astype(float)
        t_lin, R_lin = best_time(power_linear, M, n - 1, kind)
        t_bin, R_bin = best_time(power_binary, M, n - 1, kind)
        assert np.allclose(R_lin, R_bin, rtol=1e-9), f"{kind}, n={n}: способы разошлись"
        row[kind] = (t_lin, t_bin)
    rows.append(row)

print("Время возведения в степень n - 1, c")
print(f"{'n':>4} | " + " | ".join(f"{k + ', p умн.':>13} | {k + ', быстро':>13}" for k in KINDS))
for row in rows:
    cells = " | ".join(f"{row[k][0]:>13.4f} | {row[k][1]:>13.4f}" for k in KINDS)
    print(f"{row['n']:>4} | {cells}")

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
colors = {"ОБЫЧ": "#2b2cb2", "БИН": "#2f888a", "ТРОП": "#c05621"}
for kind in KINDS:
    ax.plot(NS, [r[kind][0] for r in rows], "--o", color=colors[kind], label=f"{kind}, p умножения")
    ax.plot(NS, [r[kind][1] for r in rows], "-o", color=colors[kind], label=f"{kind}, быстрое")
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_xticks(NS, labels=[str(n) for n in NS])
ax.set_xlabel("n (число вершин), p = n − 1")
ax.set_ylabel("время, с")
ax.set_title("Возведение в степень n − 1")
ax.grid(alpha=0.3, which="both")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("figures/2_timing.png")
plt.close(fig)
