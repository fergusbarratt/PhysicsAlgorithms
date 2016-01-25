import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import random
import networkx as nx
from copy import copy

class Network(object):
    def __init__(self, n_nodes):
        self.nodes = list(range(n_nodes))
        self.edges = {node:set() for node in self.nodes}

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        if not node in self.nodes:
            self.nodes.add(node)

    def add_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes:
            self.edges[node1].add(node2)
            self.edges[node2].add(node1)
        else:
            self.nodes.add(node1)
            self.nodes.add(node2)
            self.add_edge(node1, node2)

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return [(node1, node2) for node1, other_nodes in self.edges.items() for node2 in other_nodes]

    def get_neighbours(node):
        return [other_node in self.edges[node]]

    def draw(self):
        G = nx.Graph()
        G.add_nodes_from(self.get_nodes())
        G.add_edges_from(self.get_edges())
        nx.draw(G)
        plt.show()

class SmallWorldNetwork(Network):
    def __init__(self, N_nodes, N_joins, p):
        super().__init__(N_nodes)
        # connect n to it's n nearest neighbours (global)
        for node_skip in range(1, N_joins+1):
            for ind, node in enumerate(self.nodes):
                self.edges[node].add(self.nodes[(ind+node_skip)%len(self.nodes)])
        # add number of random edges

        for _ in range(int(p*N_nodes*(N_joins/2))):
            self.add_random_edge()

    def add_random_edge(self):
        '''add a new unique random edge (speedup: select from nodes with old node removed, deal with recursion'''
        rand_node_1 = random.choice(self.nodes)
        rand_node_2 = copy(rand_node_1)
        while rand_node_2==rand_node_1:
            rand_node_2 = random.choice(self.nodes)
        if rand_node_2 in self.edges[rand_node_1] or rand_node_1 in self.edges[rand_node_2]:
            self.add_random_edge()
        else:
            self.edges[rand_node_1].add(rand_node_2)
            self.edges[rand_node_2].add(rand_node_1)

    def find_path_lengths_from_node(self, node):
        pass

def test_small_world_network(L=20, Z=4, p=0.2):
    test_net = SmallWorldNetwork(L, Z, p)
    assert len(test_net.get_edges()) == L*Z+int(p*L*(Z))
    test_net.draw()

def test_network():
    new_net = Network(5)
    new_net.add_edge(1, 2)
    new_net.draw()

test_small_world_network()
