__author__ = 'Utente'
from my_lib_optimal_recovery import optimal_recovery
import networkx as nx

G=nx.MultiGraph()

G.add_node(0,id=0,status='on')
G.add_node(1,id=1,status='destroyed')
G.add_node(2,id=2,status='on')
G.add_node(3,id=3,status='on')
G.add_node(7,id=7,status='on')


G.add_edge(0,1,type='normal',status='on',capacity=3)
G.add_edge(7,2,type='normal',status='destroyed',capacity=4)
G.add_edge(1,3,type='normal',status='destroyed',capacity=5)
#,(7,2,4)
green_edges=[(3,0,2)]
#print G.edges()
#print green_edges
#edges_repaired=[]
#nodes_repaired=[]
nodes_repaired,edges_repaired=optimal_recovery(G,green_edges)

#print nodes_repaired
#print edges_repaired