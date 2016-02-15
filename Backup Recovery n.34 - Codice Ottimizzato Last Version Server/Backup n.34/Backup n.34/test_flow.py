__author__ = 'Utente'
from my_flows_lib import *


a=Vertex(0)
b=Vertex(1)
c= Vertex(2)
d= Vertex(3)
e= Vertex(4)
f= Vertex(5)
g=Vertex(6)
z=Vertex(7)

vertices=[a,b,c,d,e,f,g,z]
edges = [(0,1,2),(0,3,4),(1,2,5),(2,3,3),(3,6,6),(3,4,3),(6,5,2),(4,5,4)]
buildGraph(vertices, edges)
source = vertices[0]
sink = vertices[7]
#path=source.find(sink,[])

#path=source.find(sink,[])
#pino=[]
#pino=my_find(source,sink,[])
#print pino
maxFlow = maxFlow(source, sink)
print 'maxFlow: '+str(maxFlow)
