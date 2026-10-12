# demo.py
import numpy as np
import graphs as g

rng = np.random.default_rng(0)
A = g.petersen_undirected()
g.draw_graph(A, "petersen_undirected.png", title="Petersen (undirected)", directed=False)

D = g.petersen_random_orientation(rng)
g.draw_graph(D, "petersen_directed.png", title="Petersen (random orientation)", directed=True)

W = g.petersen_random_orientation(rng, weights=(1, 9))
g.draw_graph(W, "petersen_weighted.png", title="Petersen (weighted)", directed=True, weighted=True)
