__author__ = 'Utente'

from lib_global import *
import lib_global as lib_g
import networkx as nx

graph=nx.MultiGraph(nx.read_gml('network topologies/multiGraph.gml'))  #grafo supply
prepare_graph(graph)
#calcola_paths(graph)
# all_graph_paths
generate_demand(graph,0.15,"prova")

print lib_g.all_graph_paths
print lib_g.all_paths_feasible