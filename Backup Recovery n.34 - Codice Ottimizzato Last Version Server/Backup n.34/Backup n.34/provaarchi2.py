__author__ = 'Utente'
import networkx as nx

G = nx.MultiGraph()

#G.add_edge(1,2,color='red')
G=nx.read_gml('network topologies/multiGraph.gml')

print G.edges(data=True)

if G.has_edge(0,1):
    keydict=G.edge[0][1]
    print len(keydict)
    G.add_edge(0,1,color='blue')

print 'aggiunto'
print G.edges(data=True)


#print G.edges(data=True,keys=True)


G.add_edge(0,1,key=0,color='blue')
print 'valore color aggiunto al primo'
print G.edges(data=True)


print G[0][1]

G[0][1][0]['color']='green'

#print G.edges(data=True,keys=True)
