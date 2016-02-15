__author__ = 'Utente'

import networkx as nx
import pydot
from my_lib import *

graph= nx.MultiGraph()

#add 4 nodes in the vertexs of a square
graph.add_node(1,x=100,y=100)
graph.add_node(2,x=100,y=200)
graph.add_node(3,x=200,y=100)
graph.add_node(4,x=200,y=200)
graph.add_edge(1,2)
graph.add_edge(2,3)
graph.add_edge(3,4)
graph.add_edge(4,1)

for n in graph:
    graph.node[n]['pos'] = '"%d,%d!"'%(graph.node[n]['x'], graph.node[n]['y'])

#for node in graphDot.get_nodes():

  #      node.set_shape('circle')
   #     #getAttrDot is a function that returns the value of attribute passed
    #    pos_string='\''+ get_attrDot(node,'x')+','+get_attrDot(node,'y')+'!\''
    #    print 'coordinate: ' + pos_string  #the pos_string is correct: 'x,y!'
     #   node.set('pos',pos_string)


graphDot=nx.to_pydot(graph)
for i in graphDot.get_nodes():
    print 'color' + str(get_attrDot(i,'color'))
    print 'style' + str(get_attrDot(i,'style'))
    #print 'color' + get_attrDot(i,'color')

print graphDot.to_string()
graphDot.write('graphDot.dot')

graphDot.write_png('test_position.png')

