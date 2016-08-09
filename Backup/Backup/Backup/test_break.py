__author__ = 'Utente'

count=0
for x in xrange(10):
    print 'external iteration: '+str(x)
    for y in xrange(10):
        print 'internal: '+str(y)
        print 'sum'+ str(x+y)
        if x+y > 3:
            print 'i want exit from the inner loop and continue the external loop'
            count+=1
            break

print count

def feasible_path(G,paths):
    #G is a graph
    #paths is a list of all path in G between two nodes
    paths_to_remove=[]
    lenght_paths=len(paths)

    for i in range(0,lenght_paths-1,1):
        minCap=sys.maxint
        print 'selected:'
        print paths[i]
        index=0
        lenght_path=len(paths[i])

        for index in range(0,len(paths[i])-1,1):
            id_source=(paths[i])[index]
            id_target=(paths[i])[index+1]

            if G.has_edge(id_source,id_target,key=0):
                cap_edge=G[id_source][id_target][0]['capacity']
                if(cap_edge<minCap):
                    minCap=cap_edge

                else: # edge mising
                    #paths.remove(paths[i])
                    path_to_remove.append(paths[i])
                    minCap=-1
                    break

        if(minCap != -1):
            index=0
            for index in range(0,len(paths[i])-1,1):
                id_source=(paths[i])[index]
                id_target=(paths[i])[index+1]
                if G.has_edge(id_source,id_target,key=0):
                    old_capacity=G[id_source][id_target][0]['capacity']
                    new_capacity=old_capacity-minCap
                    G[id_source][id_target][0]['capacity']=new_capacity
                    if(new_capacity==0):
                        G.remove_edge(id_source,id_target,key=0)


    print path_to_remove
    return paths