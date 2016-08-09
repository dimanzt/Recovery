__author__ = 'Utente'

from my_lib import check_if_have_multiple_edges
import networkx as nx
import time
import numpy as np
import ast
import sys
import os


#-----------------------------MAIN HERE--------------------------------
#filename_graph='400_500'
#path_to_graph= 'network topologies/internet_routers-22july06.gml'
#path_to_graph= 'network topologies/DeltaCom - Connettivity.gml'
filename_graph= 'Abilene'
path_to_graph= 'network topologies/'+filename_graph+'.gml'

print path_to_graph
H=nx.MultiGraph(nx.read_gml(path_to_graph))




dijstra_paths=nx.dijkstra_path(H,source=4,target=0)
print dijstra_paths
sys.exit(0)
paths=nx.all_shortest_paths(H,source=4,target=0)
for p in paths:
    print p

sys.exit(0)



check_if_have_multiple_edges(H)
#sys.exit()
number_of_nodes=nx.number_of_nodes(H)
print 'Nodes: %d'%(number_of_nodes)
print 'Edges: %d'%(nx.number_of_edges(H))

list_couples=[(1,8)]
compute_flag=False

if compute_flag==True:
    for couple in list_couples:
        id_source=couple[0]
        id_target=couple[1]
        couple_name='%d-%d'%(id_source,id_target)
        dir_save='precomputed_path/'+filename_graph+'/'
        if not os.path.exists(dir_save):
            os.makedirs(dir_save)

        file_save_paths=dir_save+filename_graph+'_'+couple_name+'.txt'
        file=open(file_save_paths,'w')
        file.close()
        len_shortest=nx.shortest_path_length(H,source=id_source,target=id_target)
        print 'Min k: %d'%(len_shortest)
        for i in range(len_shortest,number_of_nodes,1):
            start_time=time.time()
            all_simple_paths=list(nx.all_simple_paths(H,source=id_source,target=id_target,cutoff=i))
            end_time=time.time()
            total_time=end_time-start_time
            print 'Paths lenght %d finished in %s seconds!'%(i,total_time)
            #print all_simple_paths
            #print 'Time: %s'%(end_time-start_time)
            file=open(file_save_paths,'a')
            iteration=str('K= %d Time: %s'%(i,total_time))
            file.write(iteration+'\n')
            file.write(str(all_simple_paths))
            file.write('\n')
            #file.write('----------------------------------------------------------------------------------------------'+'\n')
            #file.write('----------------------------------------------------------------------------------------------'+'\n')
            #file.write('\n')
            file.close()
            print 'Paths lenght %d Saved!'%(i)

read_from_file_flag=True
if read_from_file_flag==True:
    filename='precomputed_path/600_800/600_800_1-8'
    file=open(filename+'.txt','r')
    number_of_lines=0
    #for line in file.readlines():
    #    number_of_lines+=1

    #print number_of_lines
    last_line=(file.readlines())[21]
    last_line=ast.literal_eval(last_line)
    print type(last_line)
    print last_line[0]

