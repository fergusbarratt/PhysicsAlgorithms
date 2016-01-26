'''does small world networks like in Entropy Order Parameters & Complexity, JP Sethna'''
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

    def find_path_lengths_from_node(self, target_node):
        distances = {(target_node, target_node):0}
        currentShell = [target_node]
        dep=0
        while currentShell!=[]:
            nextShell=[]
            for node in currentShell:
                for neighbour in self.edges[node]:
                    if (target_node, neighbour) not in distances:
                        nextShell.append(neighbour)
                        distances[(target_node, neighbour)] = dep+1
            dep+=1
            currentShell=copy(nextShell)
        return distances

    def find_all_path_lengths(self):
        all_distances={}
        for node in self.edges:
            all_distances.update(self.find_path_lengths_from_node(node))
        return all_distances

    def find_average_path_length(self):
        return np.mean(list(self.find_all_path_lengths().values()))

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


def test_small_world_network(L=100, Z=2, p=0.1, draw=False):
    test_net = SmallWorldNetwork(L, Z, p)
    assert len(test_net.get_edges()) == L*Z+int(p*L*(Z))
    print(test_net.find_average_path_length())
    if draw:
        # draw the network
        test_net.draw()

        # histogram
        vals = np.array(list(test_net.find_all_path_lengths().values()))
        plt.hist(vals, 20)

        # strogatz plot
        Y = np.linspace(0.001, 1, 100)
        X = np.array([SmallWorldNetwork(L, Z, p).find_average_path_length()/SmallWorldNetwork(L, Z, 0).find_average_path_length() for p in Y])
        plt.semilogx(Y, X)

        plt.ylim([0, 1.5])

        plt.show()
    return test_net

def test_network():
    new_net = Network(5)
    new_net.add_edge(1, 2)
    new_net.draw()

test_small_world_network()

