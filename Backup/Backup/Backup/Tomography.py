import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
import sys
#import winsound
import time
from scipy import stats
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
fixed_distruption=str(sys.argv[11])
var_distruption=float(sys.argv[12])
K_HOPS=int(sys.argv[14])
always_split=int(sys.argv[15])
random_disruption=int(sys.argv[16])
disruption_value=int(sys.argv[17])
error=float(sys.argv[18])
Gap=float(sys.argv[19])
risk=int(sys.argv[20])

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



print 'Flow Variation: %s'%(flow_c_fixed)
if flow_c_fixed=='False':
    print 'Quantity of Flow Assigned: %d'%(flow_c_value)
else:
    print 'Vario il numero di coppie fissando il flusso: %d'%(flow_c_value)
    print 'Number of Pairs Selected: %d'%(number_of_couple)

if fixed_distruption=='True':
    print 'Fixed Disruption'
else:
    print 'Varied Disruption'
    print 'Variance of Disruption: %d '%(var_distruption)

#prendi la lista delle distanze da file
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
feasible_solution=check_if_istance_is_feasible(H,list_of_couples,flow_c_value)

print feasible_solution

#crea file se non esiste dei tempi delle simulazioni
if not os.path.exists(path_to_stat_times):
    os.makedirs(path_to_stat_times)
path_to_file_times=path_to_stat_times+filename_graph+'_times_'+str(number_of_couple)+'_couple.txt'

if not os.path.exists(path_to_file_times):
    file=open(path_to_file_times,'w')
    file.close()

if feasible_solution==False:
    #per la coppia selezionata none' possibile assegnare la quantita flow_c. SCARTO IL SEED
    #write_stat_time_simulation(path_to_stat_times,'ISP',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed)
    write_stat_time_simulation(path_to_stat_times,'Infeasible',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,0)
    sys.exit('Seed Discarded - Solution Infeasible')



#sys.exit(0)
#genera la domanda casuale partendo da una lista di coppie ordinata per distanza maggiore (lo shortest piu alto)
#path_to_demand,green_edges=generate_demand_from_list_of_couple(H,list_of_couples,prob_edge,filename_demand,alfa,seed_random,path_to_stats,distance_metric)

#genera la domanda in base ad una quantita' di flusso FISSATA (flow_c_value_ da assegnare a tutte le coppie
path_to_demand,green_edges=generate_demand_of_fixed_value_from_list_of_couple(H,list_of_couples,flow_c_value,prob_edge,filename_demand,alfa,seed_random,path_to_stats,distance_metric)


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





if random_disruption !=1:
    #nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) 
    nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,disruption_value,error,seed_passed) 
    #nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray_real(H,29,-95,disruption_value,error,seed_passed)     

    #nodes_destroyed_1,nodes_really_dest_1,edges_destroyed_1,edges_really_dest_1=destroy_graph_gray(H1,29,-95,disruption_value,error,seed_passed)


else:
    nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_random_graph_gray(H,var_distruption,error)

H1=nx.MultiGraph(H)
H2=nx.MultiGraph(H)
H3=nx.MultiGraph(H)
H4=nx.MultiGraph(H)



H6=nx.MultiGraph(H)
H7=nx.MultiGraph(H)
nodes_destroyed_6= nodes_destroyed
nodes_really_destroyed_6=nodes_really_dest
edges_destroyed_6=edges_destroyed
edges_really_destroyed_6=edges_really_dest


H9=nx.MultiGraph(H)
H8=nx.MultiGraph(H)
merge_graphs(H,D)
select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)

#destroy_graph_manual(H,path_to_real_distruption)

#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,12) #per abilene

#path_to_distruption='C:\Users\Seamus\Documents\LabWork\image_graph_dot\stats\statistiche\DimanTestDisruption.txt'
#path_to_distruption='C:\Users\Seamus\Documents\LabWork\image_graph_dot\stats\statistiche\seamus_disruption.txt'
#nodes_destroyed,edges_destroyed = destroy_graph_manual_gray(H,path_to_distruption)
#nodes_really_dest = nodes_destroyed
#edges_really_dest = edges_destroyed

#print nodes_destroyed
#print edges_destroyed
#Per bellcanada nodo 13
coor_x=45
coor_y=-75

#nodes_destroyed,edges_destroyed=destroy_graph(H,coor_x,coor_y,var_distruption) #per grafo random
#nodes_destroyed,edges_destroyed=destroy_graph_gray(H,300,300,300) #per BellCanada
#nodes_destroyed,edges_destroyed=destroy_all_graph(H)
#nodes_destroyed,edges_destroyed=destroy_graph_random(H,50, 90)


#destroy_graph(H,50,300,10) #per multigraph.gml

#memorizza distruzione per ripeterla COMMENTARE SE SI PASSA LA DISTRUZIONE MANUALE
path_to_distruption=write_destroyed_graph(nodes_destroyed,edges_destroyed,filename_graph,path_to_stats)
path_to_real_distruption=write_really_destroyed_graph(nodes_really_dest,edges_really_dest,filename_graph,path_to_stats)
#path_to_real_distruption=write_destroyed_graph(nodes_really_dest,edges_really_dest,filename_graph,path_to_stats)

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
dict_bet,temp_shortest_set,end_time_bet=select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)
my_draw(H,'3-destroyed')
#CREO UNA COPIA DEL SET DI SHORTEST PATH INZIALI SU GRAFO DISTRUTTO PER UTILIZZARLO NELL'ALGORITMO SHORTESTS SET
global shortest_set_algo
shortest_set_algo=deepcopy(temp_shortest_set)

#print shortest_set_algo
#sys.exit(0)

#print 'Post distruzione'
#supply_graph=get_supply_graph(H,green_edges)
#my_dijkstra_shortest_path(supply_graph,0,8,'weight')
#sys.exit(0)
#----------------------------------------------------------------------Eseguo ALL per conoscere il num di nodi rotti e archi rotti
nodes_recovered_all=[]
edges_recovered_all=[]
#print 'inzio recovery all'
nodes_recovered_all,edges_recovered_all=recovery_all_graph_algorithm(H)
#-----------------------------------------------------------------------

temp_graph_supply_optimal=nx.MultiGraph(H)

start_time = time.time()

nodes_recovered_isp=[]
nodes_truely_recovered_isp=[]
nodes_recovered_isp=recover_all_green_nodes_destroyed(H)
nodes_truely_recovered_isp=recover_all_green_nodes_really_destroyed(H)
my_draw(H,'4-recovery_green_nodes')
edges_recovered_isp=[]
edges_truely_recovered_isp=[]

#list for mcg riparations
nodes_to_recover_for_mcg=[]
edges_to_recover_for_mcg=[]


#SPLIT AND PRUNE
#for i in range(1,100,1):
#counter iterazioni algoritmo ISP
counter_isp=0

#temp_graph su cui fare split/pruning e recovery
temp_graph_supply=nx.MultiGraph(H)
#flag per controllare se al passo precedente ho fatto pruning e posso aver svincolato qualche altra domanda che e' ora pruneble
pruning_flag=True
flag_starvation=False
flag_solution_MCG=False
counter_starvation=0
recovered_edges_one_hop=[]
pruning_after_split=False
couples_to_prune=None

#seamus
owned_nodes = init_owned_nodes(green_edges)
green_nodes = list(owned_nodes)
total_demand_of_graph=compute_total_demand_of_graph(H)

#----------------------------------------------------------OPTIMAL-------------------------------------------------------
print 'Inizio algoritmo OPTIMAL recovery'
del H
#Diman commented two comments
H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)

#distruggi di nuovo e recover whit multicommodity
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene

destroy_graph_manual(H,path_to_real_distruption)

my_draw(H, 'really_destroyed')

#green_edges=get_green_edges(temp_graph_supply_optimal)
green_edges=deepcopy(copy_of_green_edges)

my_draw(H,'7-destroyed_for_optimal')
#calcola recovery ottimo
nodes_recovered_optimal=[]
edges_recovered_optimal=[]
total_nodes_sol=[]
total_edges_sol=[]
start_time_optimal=time.time()

#optimal classico
#nodes_recovered_optimal,edges_recovered_optimal=optimal_recovery(H,green_edges)
nodes_recovered_optimal, edges_recovered_optimal, total_nodes_sol, total_edges_sol=optimal_recovery_tomography(H,green_edges)

#nodes_recovered_optimal, edges_recovered_optimal, total_nodes_sol, total_edges_sol=optimal_recovery_tomography(H,green_edges)
print 'INJAAAAAAAAAAAAAAAAAAAA'
print total_nodes_sol
print total_edges_sol
print nodes_recovered_optimal
print edges_recovered_optimal
#nodes_recovered_optimal,edges_recovered_optimal=optimal_approx_recovery(H,green_edges)

num_rip_optimal_nodes=len(nodes_recovered_optimal)
num_rip_optimal_edges=len(edges_recovered_optimal)
print num_rip_optimal_nodes
print num_rip_optimal_edges
print 'Total nodes and edges in the solution'
num_rip_optimal_total_nodes=len(total_nodes_sol)
num_rip_optimal_total_edges=len(total_edges_sol)
print total_edges_sol
print total_nodes_sol


#ripristina e disegna
recover(H,nodes_recovered_optimal,edges_recovered_optimal)
#set_betwenness_from_dict(H,old_bet_dict)
#my_draw(H,'4-recovered_optimal_old_bet')
#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'8-recovered_optimal_new_bet')

time_elapsed_optimal=round(time.time() - start_time_optimal,3)
print("--- %s seconds ---" % str(time_elapsed_optimal))
write_stat_time_simulation(path_to_stat_times,'OPT',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed_optimal)

#ADD NUMBER of TOTAL NODES and EDGES in the solution to the stats
#################################################################################################################
#----------------------------------------------------------OPTIMAL GRAY-------------------------------------------------------
print 'Inizio algoritmo OPTIMAL recovery'
del H
#Diman commented two comments
H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)

#distruggi di nuovo e recover whit multicommodity
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene

destroy_graph_manual(H,path_to_distruption)

my_draw(H, 'gray_really_destroyed')

#green_edges=get_green_edges(temp_graph_supply_optimal)
green_edges=deepcopy(copy_of_green_edges)

my_draw(H,'7-destroyed_for_gray_optimal')
#calcola recovery ottimo
nodes_recovered_optimal=[]
edges_recovered_optimal=[]
total_nodes_sol=[]
total_edges_sol=[]

start_time_optimal=time.time()

#optimal classico
nodes_recovered_optimal, edges_recovered_optimal, total_nodes_sol, total_edges_sol=optimal_recovery_tomography(H,green_edges)
print 'INJAAAAAA GRAAAAY'
print nodes_recovered_optimal
print edges_recovered_optimal
print total_nodes_sol
print total_edges_sol

#nodes_recovered_optimal,edges_recovered_optimal=optimal_recovery(H,green_edges)
#nodes_recovered_optimal,edges_recovered_optimal=optimal_approx_recovery(H,green_edges)

num_rip_optimal_gray_nodes=len(nodes_recovered_optimal)
num_rip_optimal_gray_edges=len(edges_recovered_optimal)
print num_rip_optimal_gray_nodes
print num_rip_optimal_gray_edges
#ripristina e disegna
recover(H,nodes_recovered_optimal,edges_recovered_optimal)
#set_betwenness_from_dict(H,old_bet_dict)
#my_draw(H,'4-recovered_optimal_old_bet')
#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'8-recovered_gray_optimal_new_bet')

time_elapsed_optimal=round(time.time() - start_time_optimal,3)
print("--- %s seconds ---" % str(time_elapsed_optimal))
write_stat_time_simulation(path_to_stat_times,'OPT',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed_optimal)
#################################################################################################################

filename_stat='stat_simulations_'+filename_graph+"_Prob_"+str(prob_edge)+"_Alpha_"+str(alfa)+"_KHOP_"+str(K_HOPS)+"_distance_metric_"+str(distance_metric_passed)+"_type_of_bet_"+str(type_of_bet_passed)+"_always_put_monitor_"+str(always_split)+"_randomDisruption_"+str(random_disruption)+"_disruption_value_"+str(disruption_value)+"_error_"+str(error)+"_Gap"+str(Gap)+"risk"+str(risk)+".txt"

#numero della simulazione corrente e scrivo statistiche
num_sim=get_num_simulation(path_to_file_simulation)
################################################################################################################
#-------------------------------------------------------- Iterative Branch and Bound -Expected -OPTIMAL-------------------------------------------------------
print ' Iterative Branch and Bound  recovery'
#del H2
#if random_disruption !=1:
#    nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H3,29,-95,100)
#else:
#    nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_random_graph_gray(H3,0.2)


my_draw(H9, 'really_destroyed_expected')
temp_graph_supply_4=nx.MultiGraph(H9)
graph_built_4=get_graph_from_destroyed_graph(H9)

#my_draw(graph_built,'ExpectedIterative')



green_edges=deepcopy(copy_of_green_edges)
my_draw(H9,'7-destroyed_for_expected_optimal')
#calcola recovery ottimo
nodes_recovered_expected_optimal=[]
edges_recovered_expected_optimal=[]

start_time_expected_optimal=time.time()
repaired_nodes=[]
repaired_edges=[]
owned_nodes=[]
#seamus
owned_nodes = init_owned_nodes(green_edges)
green_nodes = list(owned_nodes)

edges_removed_exp = []
edges_recovered_exp=[]
#optimal classico
node_selected=[]
routability_flag=False
counter=0
my_draw(temp_graph_supply_4,'Diman_expected_optimal_%d'%counter)
max_prob=0
min_prob= 1
counter=counter+1
#information_gain(H9, graph_built_4, owned_nodes, edges_removed_exp+edges_recovered_exp,K_HOPS)
information_gain(H9, temp_graph_supply_4, owned_nodes, edges_removed_exp+edges_recovered_exp, K_HOPS)
my_draw(temp_graph_supply_4,'Diman_expected_optimal_%d'%counter)
counter=counter+1
#risk = 0
#nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_expected_recovery(temp_graph_supply_4,green_edges,Gap)
while (routability_flag==False):
  nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_risk_behavior_expected_recovery(temp_graph_supply_4,green_edges,Gap,risk)
  ##nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_expected_recovery(temp_graph_supply_4,green_edges,Gap)
  #nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_approx_recovery(temp_graph_supply_4,green_edges)
  #nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_recovery_multicommodity_max_flow(temp_graph_supply_4,green_edges)
  #nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_expected_recovery_max_flow(temp_graph_supply_4,green_edges,Gap)
  #nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_approx_max_flow(temp_graph_supply_4,green_edges)


  #nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_expected_recovery(H3,green_edges,Gap)
  print 'Diman joooooooooooooooooooooooooon'
  print nodes_recovered_expected_optimal
  print edges_recovered_expected_optimal
  #if (nodes_recovered_expected_optimal==[]):
  #  routability_flag=True

  for node in nodes_recovered_expected_optimal:
    if H9.node[node]['prob']>=max_prob:
     #if H9.node[node]['prob'] <= min_prob:
      max_prob=H9.node[node]['prob']
      #node_selected = []
      node_selected=node
      print 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
      print max_prob
      #print min_prob

  if (node_selected==[]):
    routability_flag=True
    break
  if node_selected not in repaired_nodes:
    #repaired_nodes.append(node_selected)
    #temp_graph_supply_4.node[node_selected]['prob']=0

    if (temp_graph_supply_4.has_node(node_selected)):
      H9.node[node_selected]['prob']=0
      temp_graph_supply_4.node[node_selected]['prob']=0
      repaired_nodes.append(node_selected)

    #temp_graph_supply_4.node[node_selected]['status']='on'
      if H9.node[node_selected]['true_status']=='destroyed':
        H9.node[node_selected]['color']='blue'
        H9.node[node_selected]['status']='on'
        temp_graph_supply_4.node[node_selected]['color']='blue'
        temp_graph_supply_4.node[node_selected]['status']='on'

      elif H9.node[node_selected]['status']=='destroyed':
        temp_graph_supply_4.node[node_selected]['status']='on'
        temp_graph_supply_4.node[node_selected]['color']='""'


      if H9.node[node_selected]['true_status']=='on' or H9.node[node_selected]['true_status']=='repaired':
        H9.node[node_selected]['color']='""'
        H9.node[node_selected]['status']=='on'
        temp_graph_supply_4.node[node_selected]['color']='""'
        temp_graph_supply_4.node[node_selected]['status']=='on'
  #counter=counter+1
  for node in repaired_nodes:
    if node not in owned_nodes:
      owned_nodes.append(node)
  repair_first_hop_edges(H9, temp_graph_supply_4, node_selected, repaired_edges,edges_recovered_expected_optimal)
  #information_gain(H9, graph_built_4, owned_nodes, edges_removed+edges_recovered_isp,K_HOPS)
  #for edge in repaired_edges:
  #  if edge not in repaired_edges:
  #    repaired_edges.append(edge) 
  information_gain(H9, temp_graph_supply_4, owned_nodes, edges_removed_exp+edges_recovered_exp, K_HOPS)
  print 'DEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEMI'
  print owned_nodes
  if len(nodes_recovered_expected_optimal)==0:# and len(edges_recovered_expected_optimal)==0:
    routability_flag=True
  my_draw(temp_graph_supply_4,'Diman_BB_optimal_%d'%counter)
  counter=counter+1

  max_prob = 0


nodes_recovered_expected_optimal,edges_recovered_expected_optimal=optimal_expected_recovery(temp_graph_supply_4,green_edges,Gap)
#for edge in repaired_edges:
#  if edge not in edges_recovered_expected_optimal:
#    edges_recovered_expected_optimal.append(edge) 

for edge in edges_recovered_expected_optimal:
  if edge not in repaired_edges:
    repaired_edges.append(edge)

num_rip_one_shot_expected_optimal_nodes=len(repaired_nodes)#len(nodes_recovered_expected_optimal)
num_rip_one_shot_expected_optimal_edges=len(repaired_edges)
print num_rip_one_shot_expected_optimal_nodes
print num_rip_one_shot_expected_optimal_edges
#########################################################
real_expected_node_repairs = []
for node in  repaired_nodes:
    if node in nodes_really_destroyed_6:
        real_expected_node_repairs.append(node)


real_expected_edge_repairs = []
for edge in repaired_edges:
    if edge in edges_really_destroyed_6:
        real_expected_edge_repairs.append(edge)

num_rip_BB_expected_truely_optimal_nodes=len(real_expected_node_repairs)
num_rip_BB_expected_truely_optimal_edges=len(real_expected_edge_repairs)
############################################################
#ripristina e disegna
recover(H9,repaired_nodes,repaired_edges)
recover(temp_graph_supply_4,repaired_nodes,repaired_edges)

my_draw(temp_graph_supply_4,'Diman_BB_expected_optimal_Final_%d'%counter)
counter=counter+1
my_draw(H9,'Diman_BB_expected_optimal_Final_%d'%counter)

time_elapsed_BB_expected_optimal=round(time.time() - start_time_expected_optimal,3)
print("--- %s seconds ---" % str(time_elapsed_BB_expected_optimal))
write_stat_time_simulation(path_to_stat_times,'BB_EXP_ITER_OPT',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed_BB_expected_optimal)
#sys.exit(0)
#################################################################################################################
write_stat_tomo(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          num_rip_optimal_nodes,num_rip_optimal_edges,#OPTIMAL
                          num_rip_optimal_gray_nodes,num_rip_optimal_gray_edges,#Gray OPTIMAL
                          num_rip_one_shot_expected_optimal_nodes,num_rip_one_shot_expected_optimal_edges,num_rip_BB_expected_truely_optimal_nodes,num_rip_BB_expected_truely_optimal_edges,#IBB Expected,
                          num_rip_optimal_total_nodes,num_rip_optimal_total_edges,#OPTIMAL total nodes and edges in the solution
                          num_sim,                        
                          flow_c_value,                                        #valore di flusso fixed assegnato per questa run
                          number_of_couple,                                     #numero di coppie scelto per rappresentare la domanda
                          var_distruption)

"""


write_stat_num_reparation(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          num_rip_isp_nodes,num_rip_isp_edges,nodes_truely_recovered_isp,edges_truely_recovered_isp, num_not_needed,        #ISP
                          num_rip_optimal_nodes,num_rip_optimal_edges,#OPTIMAL
                          num_rip_expected_optimal_nodes,num_rip_expected_optimal_edges,num_rip_expected_truely_optimal_nodes,num_rip_expected_truely_optimal_edges,#Expected,
                          num_rip_one_shot_expected_optimal_nodes,num_rip_one_shot_expected_optimal_edges,num_rip_one_shot_expected_truely_optimal_nodes,num_rip_one_shot_expected_truely_optimal_edges,#One Shot Expected,
                          num_rip_one_shot_expected_optimal_nodes,num_rip_one_shot_expected_optimal_edges,num_rip_BB_expected_truely_optimal_nodes,num_rip_BB_expected_truely_optimal_edges,#BB Expected,
                          num_rip_mult_nodes,num_rip_mult_edges,num_rip_truely_mult_nodes,num_rip_truely_mult_edges,       #Multicommodity generale
                          num_rip_mult_worst_nodes,num_rip_mult_worst_edges, #Multicommodity worst
                          num_rip_mult_best_nodes,num_rip_mult_best_edges,    #Multicommodity best
                          num_rip_shortest_nodes,num_rip_shortest_edges,num_rip_truely_shortest_nodes, num_rip_truely_shortest_edges,      #Shortest Based
                          num_rip_ranked_nodes,num_rip_ranked_edges,          #Ranked based
                          num_rip_all_nodes,num_rip_all_edges,                #All repairs algorithm
                          num_sim,
                          flag_solution_MCG,                                  #True se ho dovuto usare il MCG per terminare l'algoritmo
                          total_demand_of_graph,                                #Domanda totale sul grafo
                          demand_not_satisfied_sb,                             #Domanda non soddisfatta da shortest based
                          num_rip_all_nodes,num_rip_all_edges,
                          num_rip_all_nodes,num_rip_all_edges,
                          0,
                          flow_c_value,                                        #valore di flusso fixed assegnato per questa run
                          number_of_couple,                                     #numero di coppie scelto per rappresentare la domanda
                          var_distruption)

"""


#winsound.Beep(500,3000)
