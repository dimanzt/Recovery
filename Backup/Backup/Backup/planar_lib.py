__author__ = 'ciavarellas'

import networkx as nx
import itertools as it
from networkx.algorithms import bipartite

def is_planar(G):
    """
    function checks if graph G has K(5) or K(3,3) as minors,
    returns True /False on planarity and nodes of "bad_minor"
    """
    result=True
    bad_minor=[]
    n=len(G.nodes())
    iterazione=0
    if n>5:
        print 'N >5'

        for subnodes in it.combinations(G.nodes(),6):
            iterazione+=1
            print 'iterazione %d'%iterazione
            subG=G.subgraph(subnodes)
            if bipartite.is_bipartite(G):# check if the graph G has a subgraph K(3,3)
                X, Y = bipartite.sets(G)
                if len(X)==3:
                    result=False
                    bad_minor=subnodes
                    return result,bad_minor
    iterazione=0
    if n>4 and result:
        print 'N >4'

        for subnodes in it.combinations(G.nodes(),5):
            print 'iterazione %d'%iterazione
            subG=G.subgraph(subnodes)
            if len(subG.edges())==10:# check if the graph G has a subgraph K(5)
                result=False
                bad_minor=subnodes
                return result,bad_minor

    return result,bad_minor


#create random planar graph with n nodes and p probability of growing
"""
n=8
p=0.6
while True:
    G=nx.gnp_random_graph(n,p)
    if is_planar(G)[0]:
        break
"""

path_to_graph='network topologies/BellCanada.gml'
#'network topologies/BellCanada.gml'
#random_graph_48_nodes_60_edges.gml'

H=nx.MultiGraph(nx.read_gml(path_to_graph))

print is_planar(H)
