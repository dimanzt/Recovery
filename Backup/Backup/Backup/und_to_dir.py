__author__ = 'Utente'
import networkx as nx
import matplotlib.pyplot as plt

H=nx.MultiGraph(nx.read_gml('network topologies/multiGraph.gml'))

G=nx.DiGraph(H)

#pos = nx.random_layout(G)
#nx.draw(G, pos)
#plt.show()
graphDot=H.to_directed()
graphDot.write_png('prova_conversione.png')
