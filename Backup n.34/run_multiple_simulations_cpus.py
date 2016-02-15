__author__ = 'ciavarellas'


import os
import sys
from subprocess import Popen
array_graphs=['524','1029','1503','1942','2474','2977','3431','3982','4413','4950']
#graph_name='Abilene'
#graph_name='erdos_renyi_graph_100_nodes_"+curr_edges+"_edges'

i=-1
for curr_edges in array_graphs:
        #esegui una simulazione
        #os.system("taskset -c +python "+name_of_program_simulation +" "+str(seed_elem)+" "+str(alpha)+" "+str(prob_edge)+" "+str(num_simulations)+" "+str(i+1)+" "+distance_metric+" "+type_of_bet+" "+str(flow_fixed)+" "+str(flow_c)+" "+str(number_of_couple)+" "+str(fixed_distruption)+" "+str(var_distruption)+" "+filename_graph)
    i=i+1
    Popen("taskset -c "+str(i)+" python multiple_simulations_opt_only_1.py 5 erdos_renyi_graph_100_nodes_"+curr_edges+"_edges", shell=True)
    i=i+1
    Popen("taskset -c "+str(i)+" python multiple_simulations_opt_only_2.py 5 erdos_renyi_graph_100_nodes_"+curr_edges+"_edges", shell=True)
    i=i+1
    Popen("taskset -c "+str(i)+" python multiple_simulations_opt_only_3.py 5 erdos_renyi_graph_100_nodes_"+curr_edges+"_edges", shell=True)
    i=i+1
    Popen("taskset -c "+str(i)+" python multiple_simulations_opt_only_4.py 5 erdos_renyi_graph_100_nodes_"+curr_edges+"_edges", shell=True)

    #sys.exit(0)