# Import pygraphviz
import pygraphviz as gv
import networkx as nx
# Graph creation
gr = nx.Graph()

G=nx.MultiGraph()

G.add_edge(1,2)

G.add_edge(1,2)

# Draw as PNG
dot = nx.write_dot(G,'multi.dot')
gvv = gv.readstring(dot)
gv.layout(gvv,'dot')
gv.render(gvv,'png','europe.png')