__author__ = 'Utente'
from my_flows_lib import *
from my_lib import *
a=Vertex(0)
b=Vertex(1)
c= Vertex(2)
d= Vertex(3)
e= Vertex(4)
f= Vertex(5)
g=Vertex(6)


#print a
vertices=[a,b,c,d,e,f,g]
edges = [(0,1,2),(0,3,4),(1,2,5),(2,3,3),(3,6,6),(3,4,3),(6,5,2),(4,5,4)]

for node in vertices:
    print node.name

for edge in edges:
    print edge
buildGraph(vertices, edges)
source = vertices[0]
sink = vertices[1]
paths={}
maxFlow,paths = maxFlow(source, sink)
print 'maxFlow: '+str(maxFlow)

print 'tutti gli archi'
for i in vertices:
    print 'archi nodo: '+str(i.name)
    for edge in i.edges:
        print edge
        #print edge.oppositeEdge

print 'provo a cancellare'

clean_edges(vertices)
print 'stampa archi rimanenti'
for i in vertices:
    for edge in i.edges:
        print edge

print 'nodi'
for node in vertices:
    print node.name

print 'cancellazione nodi'
#for node in vertices:
#    vertices.pop(node)
#del vertices
#del edges

print 'nuovo graph'

a=Vertex(10)
b=Vertex(11)
c= Vertex(12)
d= Vertex(13)
e= Vertex(14)
f= Vertex(15)
g=Vertex(16)


#print a
vertices=[a,b,c,d,e,f,g]
edges = [(10,11,2),(10,13,4),(11,12,5),(12,13,3),(13,16,6),(13,14,3),(16,15,2),(14,15,4)]

for node in vertices:
    print node.name

for edge in edges:
    print edge
buildGraph(vertices, edges)

print 'tutti gli archi'
for i in vertices:
    print 'archi nodo: '+str(i.name)
    for edge in i.edges:
        print edge
        #print edge.oppositeEdge

print 'provo a cancellare'

clean_edges(vertices)
print 'stampa archi rimanenti'
for i in vertices:
    for edge in i.edges:
        print edge

print 'nodi'
for node in vertices:
    print node.name

print 'cancellazione nodi'
#for node in vertices:
#    vertices.pop(node)
del vertices
del edges