import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as nrand

class PercolationNetwork2D(object):
    def __init__(self, dim, prob):
        self.prob = prob
        self.data = nx.Graph()
        self.data.add_nodes_from([(i, j) for i in range(dim) for j in range(dim)])
        def neighbour(node1, node2):
            def same_row(node1, node2):
                return node1[0]==node2[0]
            def same_col(node1, node2):
                return node1[1]==node2[1]
            return ((same_row(node1, node2) or same_col(node1, node2)) and node1!=node2) and abs(node1[0]-node2[0])%(dim-1) <= 1 and abs(node1[1]-node2[1])%(dim-1) <= 1
        for node1 in self.data:
            for node2 in self.data:
                if neighbour(node1, node2):
                    if node1 == (0, 5):
                        if node2 == (5, 5):
                            print('hello')
                    self.data.add_edge(node1, node2)
        self.edges = self.data.add_edges_from([(node1, node2) for node1 in self.data.nodes() for node2 in self.data.nodes() if neighbour(node1, node2)])
    def draw(self):
        nx.draw(self.data)

    def kill_rand_edges(self):
        for edge in self.data.edges():
            if nrand.uniform() > self.prob:
                self.data.remove_edge(*edge)

net = PercolationNetwork2D(5, 0.6)
net.kill_rand_edges()
net.draw()
plt.show()

