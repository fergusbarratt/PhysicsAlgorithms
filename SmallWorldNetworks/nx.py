import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from([1, 2])
nx.draw(G)
plt.show()
