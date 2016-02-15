__author__ = 'Utente'


import sys
import fileinput

class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.edges = []

class Edge(object):
    def __init__(self, fromVertex, toVertex, capacity):
        self.fromVertex = fromVertex
        self.toVertex = toVertex
        self.capacity = capacity
        self.flow = 0
        self.inf = False
        if(capacity == -1):
            self.inf = True
    def __repr__(self):
        return str(self.fromVertex.name) + " - " + str(self.toVertex.name)

def buildGraph(vertices, edges):

    for edge in edges:
        sourceVertex = vertices[int(edge[0])]
        sinkVertex = vertices[int(edge[1])]
        capacity = int(edge[2])
        edge1 = Edge(sourceVertex, sinkVertex, capacity)
        edge2 = Edge(sinkVertex, sourceVertex, capacity)
        edge1.oppositeEdge = edge2
        edge2.oppositeEdge = edge1
        sourceVertex.edges.append(edge1)
        sinkVertex.edges.append(edge2)

def my_find(source,sink,path):

        if(str(source.name)==str(sink.name)):
            return path
        #print '--------------Archi del nodo : '+str(source.name)+'-------------------------'

        for edge in source.edges:
            residual= edge.capacity-edge.flow
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


def maxFlow(source, sink):
    path=my_find(source,sink,[])
    while path != None:
        print 'path da analizzare'
        print path
        minCap = sys.maxint
        for e in path:
            if(e.capacity < minCap and not e.inf):
                minCap = e.capacity
        #print 'capacita minima: '+str(minCap)
        for edge in path:
            edge.flow += minCap
            edge.oppositeEdge.flow -= minCap
        path=my_find(source,sink,[])
    return sum(e.flow for e in source.edges)

def clean_edges(vertices):

    for node in vertices:
        node.edges=[]

a=Vertex(0)
b=Vertex(1)
c= Vertex(2)
d= Vertex(3)
e= Vertex(4)
f= Vertex(5)
g=Vertex(6)
z=Vertex(7)

#print a
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

for i in vertices:
    for edge in i.edges:
        print edge

clean_edges(vertices)
print 'stampa archi ripuliti'
for i in vertices:
    for edge in i.edges:
        print edge

for node in vertices:
    print node.name

vertices=[]

for node in vertices:
    print node.name