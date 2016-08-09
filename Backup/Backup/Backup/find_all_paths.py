__author__ = 'Utente'
import networkx as nx
from my_lib import *

def convert_graph_to_dict(G):
        graph={}
        for node in G.nodes():
            if not graph.has_key(node):
                graph[node]=[]

        print 'my_graph'
        print graph

        for edge in G.edges():
            source=edge[0]
            target=edge[1]
            #print str(source) +'-'+str(target)
            if graph[source]==None:
                graph.update({source:target})
                #print graph
            else:
                graph[source].append(target)

            if graph[target]==None:
                graph.update({target:source})
                #print graph
            else:
                #print graph[target]
                graph[target].append(source)

        return graph

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths




def feasible_path2(G,paths):
    #G is a graph
    #paths is a list of all path in G between two nodes
    paths_to_remove=[]
    lenght_paths=len(paths)

    for path in paths:
        minCap=sys.maxint
        print 'selected:'
        print path

        for i in range(0,(len(path)-1),1):
            id_source=path[i]
            id_target=path[(i+1)]

            if G.has_edge(id_source,id_target,key=0):
                cap_edge=G[id_source][id_target][0]['capacity']
                if(cap_edge<minCap):
                    minCap=cap_edge
            else: # edge mising
                paths_to_remove.append(path)
                minCap=-1
                break   #i want stop the for index loop


        if(minCap != -1):
            index=0
            for index in range(0,(len(path)-1),1):
                id_source=path[index]
                id_target=path[index+1]
                if G.has_edge(id_source,id_target,key=0):
                    old_capacity=G[id_source][id_target][0]['capacity']
                    new_capacity=old_capacity-minCap
                    G[id_source][id_target][0]['capacity']=new_capacity
                    if(new_capacity==0):
                        G.remove_edge(id_source,id_target,key=0)
                else:
                    print 'ERRORE ??????'


    print 'path to remove'
    print paths_to_remove
    for path in paths_to_remove:
        if path in paths:
            print 'rimuovo path'
            print path
            paths.remove(path)
    return paths

G= nx.MultiGraph()

G.add_node('a',id='a')
G.add_node('b',id='b')
G.add_node('c',id='c')
G.add_node('d',id='d')
G.add_node('m',id='m')
G.add_node('n',id='n')


G.add_edge('a','b',capacity=3)
G.add_edge('b','n',capacity=5)
G.add_edge('b','m',capacity=5)
G.add_edge('b','c',capacity=2)
G.add_edge('m','c',capacity=5)
G.add_edge('c','d',capacity=2)
G.add_edge('n','d',capacity=5)

for edge in G.edges():
    id_source=edge[0]
    id_target=edge[1]
    print str(id_source) + str(id_target)

new_graph=convert_graph_to_dict(G)

print new_graph
paths= find_all_paths(new_graph,'a','d')
print 'path trovati:'
print paths
path_feasible=feasible_path2(G,paths)
print 'path feasible:'
print path_feasible