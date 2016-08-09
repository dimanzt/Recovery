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
        self.capacity = capacity+0.0
        self.flow = 0
        self.inf = False
        if(capacity == -1):
            self.inf = True
    def __repr__(self):
        return str(self.fromVertex.name) + " - " + str(self.toVertex.name)

def buildGraph(vertices, edges):

    for edge in edges:
        #print  edge[0]
        sourceVertex = get_Vertex(vertices,edge[0])
        #print 'source'+str(sourceVertex.name)
        sinkVertex = get_Vertex(vertices,edge[1])
        #print 'target'+str(sinkVertex.name)
        #if edge[2]==0.5:
        #    capacity=0.5
        #else:
        capacity = edge[2]
        edge1 = Edge(sourceVertex, sinkVertex, capacity)
        edge2 = Edge(sinkVertex, sourceVertex, capacity)
        edge1.oppositeEdge = edge2
        edge2.oppositeEdge = edge1
        sourceVertex.edges.append(edge1)
        sinkVertex.edges.append(edge2)


def get_Vertex(vertices,name):
    for node in vertices:
        if str(node.name)==str(name):
            return node

def my_find(source,sink,path,node_visited):

        if source.name not in node_visited:
            node_visited.append(source.name)

        if(str(source.name)==str(sink.name)):
            return path
        #print '--------------Archi del nodo : '+str(source.name)+'-------------------------'

        for edge in source.edges:
            residual= edge.capacity
            #print 'esamino arco '
            #print edge
            #print residual
            if(residual >0 or edge.inf):
                toVertex=edge.toVertex
                if toVertex.name not in node_visited:
                    node_visited.append(toVertex.name)
                    if (edge not in path and edge.oppositeEdge not in path):
                        path.append(edge)
                        result=my_find(toVertex,sink,path,node_visited)
                        if result !=None:
                            return result

                        #print 'archi non trovati,elimino ultimo elemento di path:'
                        lenght=len(path)
                        elem=path[lenght-1]
                        path.remove(elem)
            #else:
                #print 'scarto'
        return None


def maxFlow(source, sink):
    all_paths={}
    path=my_find(source,sink,[],[])
    # 'path trovato'
    #print path
    while path != None:

        #print 'path da analizzare'
        #print path
        minCap = sys.maxint
        for e in path:
            #print e
            #print 'capacita arco> %f'%e.capacity
            if(e.capacity < minCap and not e.inf):
                minCap = e.capacity
                #print 'capacita minima: '+str(minCap)
        for edge in path:
            edge.flow += minCap
            edge.oppositeEdge.flow -= minCap
            edge.capacity -=minCap
            if (edge.capacity<0):
                print 'errore capacita NEGATIVAAAAA'
                sys.exit('maxfLOW LIB: CAPACITA NEGATIVA')

        if not all_paths.has_key(minCap):
            list_paths=[path]
            all_paths.update({minCap:list_paths})

        else:
            all_paths[minCap].append(path)

        #print 'prova'
        #print all_paths
        path=my_find(source,sink,[],[])

    #all_paths_updated=update_all_flow(all_paths)

    return (sum(e.flow for e in source.edges))


def update_all_paths(all_paths):
        new_dict_paths={}

        for minCap in all_paths:
            for path in minCap:
                for edge in path:
                    residual=edge.capacity-edge.flow
                    if(edge.capacity < minCap and not e.inf):
                        minCap = e.capacity


def clean_edges(vertices):

    for node in vertices:
        del node.edges[:]

def get_index_vertex(vertices,id_node):

    for i in range(0,len(vertices),1):
        if str(vertices[i].name) == str(id_node):
            return i