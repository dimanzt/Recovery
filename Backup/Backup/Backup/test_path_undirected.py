__author__ = 'Utente'

import networkx as nx
from my_lib import *
G= nx.MultiGraph()

G.add_node('a',id='a')
G.add_node('b',id='b')
G.add_node('c',id='c')
G.add_node('d',id='d')
G.add_node('m',id='m')
G.add_node('n',id='n')

for i in G.nodes():
    print i

G.add_edge('a','b',capacity=3)
G.add_edge('b','n',capacity=5)
G.add_edge('b','m',capacity=5)
G.add_edge('b','c',capacity=2)
G.add_edge('m','c',capacity=5)
G.add_edge('c','d',capacity=3)
G.add_edge('n','d',capacity=5)

for edge in G.edges():
    print edge
#my_draw(G,'test_undirected')

def find_path(G,source,sink):

        if(str(source)==str(sink)):
            return path
        #print '--------------Archi del nodo : '+str(source.name)+'-------------------------'

        for edge in source.edges:
            residual= edge.capacity
            if(residual >0 or edge.inf):
                if (edge not in path and edge.oppositeEdge not in path):
                        path.append(edge)
                        toVertex=edge.toVertex
                        result=my_find(toVertex,sink,path)
                        if result !=None:
                            return result

                        #print 'archi non trovati,elimino ultimo elemento di path:'
                        lenght=len(path)
                        elem=path[lenght-1]
                        path.remove(elem)
        return None