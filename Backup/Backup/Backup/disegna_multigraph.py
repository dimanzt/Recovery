import networkx as nx
import pygraphviz
import graphviz


G=nx.MultiGraph()

G.add_edge(1,2)

G.add_edge(1,2)

nx.write_dot(G,'multi.dot')

#neato -T png multi.dot > multi.png

nx.draw_graphviz(G,prog='neato')