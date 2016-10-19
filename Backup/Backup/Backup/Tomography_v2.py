import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
import sys
#import winsound
import time
from scipy import stats
import numpy as np
from numpy.linalg import svd
from my_lib import *
from my_flows_lib import *
from my_lib_optimal_recovery import *
from my_lib_optimal_expected_recovery import *
from my_lib_optimal_approx_max_flow import *
from my_lib_optimal_expected_recovery_max_flow import *
from my_lib_optimal_approx_recovery import *
from my_lib_optimal_recovery_multicommodity import *
from my_lib_optimal_recovery_multicommodity_maxFlow import *
from my_lib_optimal_recovery_multicommodity_worst import *
from my_lib_optimal_recovery_multicommodity_best import *
from my_lib_check_routability import *
from my_lib_compute_max_demand_in_the_graph import *
from my_lib_optimal_tomography import *
#from my_lib_optimal_risk_averse_expected_recovery import *
from my_lib_optimal_risk_behavior_expected_recovery import *
#https://www.diffchecker.com/efddo0xv

work_dir=os.getcwd()

path_to_dot_dir='../../../image_graph_dot/DotFile/'
path_to_image_dir='../../../image_graph_dot/immagini_generate/'
path_to_image_store='../../../image_graph_dot/store_images/'
path_to_stats='../../../image_graph_dot/stats/statistiche/'
path_to_file_simulation='../../../image_graph_dot/current_simulation.txt'
path_to_stat_prog='../../../image_graph_dot/stats/progress_iteration/'
path_to_stat_times='../../../image_graph_dot/stats/times/'


print "Number of runs: "+sys.argv[5]+ "/"+sys.argv[4]
print "Simulation Parameters: "
print "Seed: "+sys.argv[1]
print "Alpha demand: "+sys.argv[2]
print "Prob edge green: "+sys.argv[3]
print "Distance metric: "+sys.argv[6]
print "Type of betweeness: "+sys.argv[7]

seed_passed=sys.argv[1]
alpha_passed=sys.argv[2]
prob_edge_passed=sys.argv[3]
distance_metric_passed=sys.argv[6]
type_of_bet_passed=sys.argv[7]
flow_c_fixed=sys.argv[8]
flow_c_value=int(sys.argv[9])
number_of_couple=int(sys.argv[10])
Percentage = float(sys.argv[18])
#fixed_distruption=str(sys.argv[11])
#var_distruption=float(sys.argv[12])
#K_HOPS=int(sys.argv[14])
#always_split=int(sys.argv[15])
#random_disruption=int(sys.argv[16])
#disruption_value=int(sys.argv[17])
#error=float(sys.argv[18])
#Gap=float(sys.argv[19])
#risk=int(sys.argv[20])

if sys.argv[13]!=None:
    filename_graph=str(sys.argv[13])
    print 'Graph: ' + filename_graph


path_to_graph= 'network topologies/'
path_to_graph=path_to_graph+filename_graph+'.gml'
path_to_folder_couple='distance_between_couples/'


H=nx.MultiGraph(nx.read_gml(path_to_graph))

print 'Dimensions of the Graph'
print "Nodes: %d"%H.number_of_nodes()
print "Edges: %d"%H.number_of_edges()
print "Total: %d"%(H.number_of_nodes()+H.number_of_edges())
seed_random=int(seed_passed)
random.seed(seed_random)

print 'Seed Utilized: %f: '%seed_random


list_of_couples=get_list_distance_couples(path_to_folder_couple,filename_graph)
list_of_couples=subset_of_list(list_of_couples,50)
list_of_couples=select_random_couples_from_list(list_of_couples,number_of_couple)
#list_of_couples = [(16, 38, 10),(35, 44, 10)]

print 'Subset of Random Couples:'
print list_of_couples


green_edges=[]
filename_graph=path_to_graph[path_to_graph.find('/')+1:-4]
print filename_graph
filename_demand=filename_graph+'DemandGenereted'


prepare_graph(H)
my_draw(H,'1-initial'+'_Seed_'+str(seed_random)+'_'+'Prob_edge_'+str(prob_edge_passed)+'_')

#GENERATE FEASIBLE DEMAND ON SUPPLY GRAPH
prob_edge=float(prob_edge_passed)

alfa=float(alpha_passed)
#select the distance metric used to calculate the length of a path: 'capacity', 'one-hop', 'broken'
#distance_metric='broken'
distance_metric=distance_metric_passed
#feasible_solution=check_if_istance_is_feasible(H,list_of_couples,flow_c_value)

if not os.path.exists(path_to_stat_times):
    os.makedirs(path_to_stat_times)
path_to_file_times=path_to_stat_times+filename_graph+'_times_'+str(number_of_couple)+'_couple.txt'

if not os.path.exists(path_to_file_times):
    file=open(path_to_file_times,'w')
    file.close()

#if feasible_solution==False:
#    #per la coppia selezionata none' possibile assegnare la quantita flow_c. SCARTO IL SEED
#    #write_stat_time_simulation(path_to_stat_times,'ISP',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed)
#    write_stat_time_simulation(path_to_stat_times,'Infeasible',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,0)
#    sys.exit('Seed Discarded - Solution Infeasible')



#sys.exit(0)
#genera la domanda casuale partendo da una lista di coppie ordinata per distanza maggiore (lo shortest piu alto)
#path_to_demand,green_edges=generate_demand_from_list_of_couple(H,list_of_couples,prob_edge,filename_demand,alfa,seed_random,path_to_stats,distance_metric)

#genera la domanda in base ad una quantita' di flusso FISSATA (flow_c_value_ da assegnare a tutte le coppie
path_to_demand,green_edges_old=generate_demand_of_fixed_value_from_list_of_couple(H,list_of_couples,flow_c_value,prob_edge,filename_demand,alfa,seed_random,path_to_stats,distance_metric)
my_monitors,green_edges = generate_random_monitors(H,Percentage,seed_random)
print 'DIMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN'
print my_monitors
print green_edges
print 'Couples of Green Edges Seclected:'
#per passare archi particolari
#green_edges=[(3,6,3)]
print green_edges

#sys.exit(0)
copy_of_green_edges=[]
copy_of_green_edges=deepcopy(green_edges)
#decommentare se si passano archi verdi manuali
#compute_paths(H,green_edges)

#generare una demand casuale dal grafo

D=nx.MultiGraph(nx.read_gml(path_to_demand))

my_draw(H, '2-prepared-new_bet_alpha_%f'%alfa)

if not os.path.exists(path_to_stat_prog):
    os.makedirs(path_to_stat_prog)
file=open(path_to_stat_prog+filename_graph+'_progress.txt','w')
file.close()





#if random_disruption !=1:
#    #nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) 
#    nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,disruption_value,error,seed_passed) 
#    #nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray_real(H,29,-95,disruption_value,error,seed_passed)     
#
#    #nodes_destroyed_1,nodes_really_dest_1,edges_destroyed_1,edges_really_dest_1=destroy_graph_gray(H1,29,-95,disruption_value,error,seed_passed)
#else:
#    nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_random_graph_gray(H,var_distruption,error)

H1=nx.MultiGraph(H)
H2=nx.MultiGraph(H)

merge_graphs(H,D)
##select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)

coor_x=45
coor_y=-75

#path_to_real_distruption=write_really_destroyed_graph(nodes_really_dest,edges_really_dest,filename_graph,path_to_stats)
#path_to_real_distruption=write_destroyed_graph(nodes_really_dest,edges_really_dest,filename_graph,path_to_stats)

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#dict_bet,temp_shortest_set,end_time_bet=select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)
#my_draw(H,'3-destroyed')
#CREO UNA COPIA DEL SET DI SHORTEST PATH INZIALI SU GRAFO DISTRUTTO PER UTILIZZARLO NELL'ALGORITMO SHORTESTS SET
#global shortest_set_algo
##shortest_set_algo=deepcopy(temp_shortest_set)

#------------------------------------------tomography shortest path---------------------------------
#my_dijkstra_shortest_path(supply_graph,0,8,'weight')
#del H
#H = nx.MultiGraph(nx.read_gml(path_to_graph)) # Supply graph
prepare_graph(H1)
merge_graphs(H1,D)
my_draw(H1, 'real_Graph_%f'%alfa)
#green_edges= deepcopy(copy_of_green_edges)
nodes_included=[]
edges_included=[]
distance_metric = "one-hop"
#Start adding edges and nodes to the solution set
print 'Green edges'
print green_edges
#i=0
# This is the routing matrix
R= np.zeros(shape=(len(green_edges),H2.number_of_edges()))
print ' A zero matrix'
print R
# Counts the number of equations
Path_Index =0
for edge in green_edges:
  #residual_graph=nx.MultiGraph(supply_graph)
  source=edge[0]
  target=edge[1]
  #demand= edge[2]
  arc=(source,target)
  (length, path) = my_prob_single_source_dijkstra(H2,distance_metric, source, target)
  print 'Diman'
  #print i
  #print path
  #print 'Length'
  #print length 
  #i = i+1
  #print patih
  try:
    print path[target]

    print type(path[target]), len(path[target]), path[target]
    a = np.asarray(path[target])
    #print type(a), a.shape, "\n", a
    #keydict=H[id_source][id_target]
    #for k in keydict:
    #  if H2[source][target][k]['type']=='normal':
    #    #H.add_edge(source,target,key=k, true_status='destroyed')
    #    edges_destroyed.append((id_source,id_target))
    i=0
    #my_path = path[target].tolist()
    print a
    for node in a:
      if i < (len(path[target])-1):
        id_source= a[i]
        i = i+1      
        id_target= a[i]
        #i= i+1
        #keydict=H2[id_source][id_target]
        #for k in keydict:
        #  if H2[source]
        my_edge=(id_source,id_target)
        if my_edge not in edges_included:
          edges_included.append(my_edge)
        #Set up the routing matrix R: 
        edge_number=0
        for e in H2.edges():
          #print 'Number of H2 edges'
          #print H2.edges()
          my_source=e[0]
          my_target=e[1]
          graph_edge=(my_source, my_target)
          graph_edge_reverse= (my_target, my_source)
          if (my_edge == graph_edge) or (my_edge== graph_edge_reverse):
            #print 'Hahahaaaaa'
            R[Path_Index][edge_number]=1#.item((Path_Index,edge_number))= 1
          edge_number=edge_number + 1
          #Increase by the number of edges in the graph
      #Add nodes in each path to the solution set    
      if node not in nodes_included:
        nodes_included.append(node)
        
  except KeyError:
    raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))

  Path_Index= Path_Index +1
#Print the results
print 'Nodes included'
print nodes_included
print 'Edges included'
print edges_included
print 'Edges in the graph'
print H2.edges()
print 'Routing matrix'
print R
#C = np.array([[1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
#[1,1,0;0,1,1;1,0,1]
my_null = null(R)
print 'Null space of R'
print my_null
rows= len(my_null)
columns = len(my_null.T)
print 'Rows'
print rows
print 'Columns'
print columns
routing_rows = len(R)
routing_columns = len(R.T)
print 'Routing rows'
print routing_rows
print 'Routing Columns'
print routing_columns
iden =1
Num_Identi_link =0
#for i in range(0,len(green_edges)-1):
#  for j in range(0,len(my_null.T)-1):
for i in range(0,rows):
  #print 'I ro print kon'
  #print i
  for j in range(0,columns):
    #print 'J ro print kon'
    #print j
    if (-1e-12 <my_null[i][j] < 1e-12) and (iden==1):
      iden=1
    else:
      iden=0
  if (iden == 1):
    Num_Identi_link = Num_Identi_link +1 
    #print 'Which Row?'
    #print i
  iden=1
print 'Number of Identofiable links:'
#if (not my_null):
#  Num_Identi_link = len(green_edges)
print Num_Identi_link
print "Nodes: %d"%H2.number_of_nodes()
print "Edges: %d"%H2.number_of_edges()


