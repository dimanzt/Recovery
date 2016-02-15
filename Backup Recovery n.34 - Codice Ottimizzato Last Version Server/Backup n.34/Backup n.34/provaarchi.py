__author__ = 'Utente'

import networkx as nx

H=nx.MultiGraph()
H=nx.read_gml('network topologies/test_archi.gml')  #grafo supply

for i in H.edges(data=True):
    print i

#H.add_edge(0,1,weight='5')
H.add_edge(0,1,key=1,value='blue')
H.add_edge(0,1,key=2,value='red')

print 'archi nuovi'
for i in H.edges(data=True):
    print i

#print H.edge[0][1]