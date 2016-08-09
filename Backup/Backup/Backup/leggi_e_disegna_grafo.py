__author__ = 'novella'


import networkx as nx
import matplotlib.pyplot as plt
H=nx.read_gml('network topologies/Abilene.gml')

num_nodes = H.number_of_nodes()
print 'number of nodes: ' + str(num_nodes)


pos = nx.random_layout(H)
nx.draw(H, pos)
plt.show()