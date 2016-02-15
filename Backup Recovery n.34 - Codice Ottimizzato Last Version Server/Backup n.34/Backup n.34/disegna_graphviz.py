
__author__ = 'Stefano'
import networkx as nx


#Gm=nx.MultiGraph ([(1,2),(1,2),(1,2),(3,1),(3,2)])
#nx.write_dot(Gm,'multi.dot')

G=nx.MultiGraph()
G.add_edge(0,1)
G.add_edge(1,0)
#G.add_edge(3,1)
#G.add_edge(1,3)
#G.add_edge(2,3)
nx.write_dot(G,'multi.dot')

#neato -Tps multi.dot >multi.png
#nx.draw_graphviz(G,prog='neato')
#dot -Tps multi.dot -o outfile.ps

#dot -Tps input.dot > output.eps
#dot -Tpng input.dot > output.png