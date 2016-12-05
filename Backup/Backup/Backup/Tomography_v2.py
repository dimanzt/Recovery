# Author: Diman Zad Tootaghaj
import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
import sys
#import winsound
import time
import itertools
from scipy import stats
import numpy as np
import copy
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
#from my_lib_optimal_tomography import *
from my_lib_optimal_ILP_tomography import *
from my_lib_optimal_LP_Relax_tomography import *
from my_lib_Max_rank import *
#from my_lib_optimal_risk_averse_expected_recovery import *
from my_lib_optimal_risk_behavior_expected_recovery import *
from numpy.linalg import matrix_rank

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
Monitors = int(sys.argv[17])
#fixed_distruption=str(sys.argv[11])
#var_distruption=float(sys.argv[12])
#K_HOPS=int(sys.argv[14])
#always_split=int(sys.argv[15])
#random_disruption=int(sys.argv[16])
#disruption_value=int(sys.argv[17])
#error=float(sys.argv[18])
#Gap=float(sys.argv[19])
ProbeCost = int(sys.argv[19])
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
if (len(my_monitors) < Monitors):
    Monitors = len(my_monitors)
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
Cost_routing= np.zeros(shape=(len(green_edges), 1))
#Green_Edges= np.zeros
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
            Cost_routing[Path_Index][0] = len(length)
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
#C = np.array([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
#[1,1,0;0,1,1;1,0,1]
my_null = null(R)
MatrixRank= matrix_rank(R)
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
print 'Number of monitors'
print len(my_monitors)
print 'Number of Identofiable links:'
#if (not my_null):
#  Num_Identi_link = len(green_edges)
print Num_Identi_link
print "Nodes: %d"%H2.number_of_nodes()
print "Edges: %d"%H2.number_of_edges()
print '********************************'
##############################################################################################################
########################START Greedy-Min-Prob Algorithm#######################################################
##Description: The algorithm starts by adding a path to the set of path that increase the rank most###########
RMin=[]
temp=[]
IncreaseInRank=0
currentRank =0
Max_Increase =0
sort_index = np.argsort(Cost_routing[:,0])
Cost=0
print 'Diman Sort naKarde'
print Cost_routing
print 'Diman Sort Karde!'
print sort_index
for i in sort_index:
  print 'I ro print kon'
  print i
  temp= copy.deepcopy(RMin)
  temp.append(i)
  IncreaseInRank=  matrix_rank(R[temp,:]) - currentRank
  print 'Rank of R'
  print matrix_rank(R[temp,:])
  print 'IncreaseInRank'
  print IncreaseInRank
  print 'currentRank'
  print currentRank
  if i in RMin:
    RMin.remove(i)
  #temp.remove(i)
  if (IncreaseInRank > 0):
    #Print 'Yaftam!'
    #Max_Increase = IncreaseInRank
    RMin.append(i)
    currentRank= matrix_rank(R[temp,:])
    Cost = Cost + Cost_routing[i,0]
  temp.remove(i)
print 'Found R'
print RMin
#for x in RMin:
print 'Rank:'
print matrix_rank(R[RMin,:])
MinProbMonitors=[]
for i in RMin:
  print 'This is which index'
  print i
  if green_edges[i][0] not in MinProbMonitors:
    print 'Source:'
    print green_edges[i][0]
    MinProbMonitors.append(green_edges[i][0])
  if green_edges[i][1] not in MinProbMonitors:
    print 'Destination:'
    print green_edges[i][1]
    MinProbMonitors.append(green_edges[i][1])
################################################################################
TotalCost=0
for i in sort_index:
  TotalCost = TotalCost + Cost_routing[i,0]
#################################################################################
MinProbeNull = null(R[RMin,:])
print 'Null space of RMin'
print MinProbeNull
rows= len(MinProbeNull)
columns = len(MinProbeNull.T)
print 'Rows'
print rows
print 'Columns'
print columns
routing_rows = len(R[RMin,:])
routing_columns = len(R[RMin,:].T)
print 'Routing rows'
print routing_rows
print 'Routing Columns'
print routing_columns
iden =1
MinProbe_Identi_link =0
#for i in range(0,len(green_edges)-1):
#  for j in range(0,len(my_null.T)-1):
for i in range(0,rows):
  #print 'I ro print kon'
  #print i
  for j in range(0,columns):
    #print 'J ro print kon'
    #print j
    if (-1e-12 <MinProbeNull[i][j] < 1e-12) and (iden==1):
      iden=1
    else:
      iden=0
  if (iden == 1):
    MinProbe_Identi_link = MinProbe_Identi_link +1
    #print 'Which Row?'
    #print i
  iden=1
#################################################################################
print 'Number of Identofiable links:'
print MinProbe_Identi_link
print 'Rank of matrix:'
print matrix_rank(R[temp,:])
#################################################################################
print 'Preserving rank, we have this many monitors:'
print len(MinProbMonitors)
print 'Minimum Number of Probes to preserve Rank:'
print len(RMin)
print 'Cost of Preserving Rank (Hop count):'
print Cost
print 'Total Cost if using all paths:'
print TotalCost
print '####################FINISHED MIN-Prob algorithm ######################' 
#############################################################################
print '####################Start Min-Prob with minimum monitors##############'
RMinMon=[]
ListofR=[]
#ListofCost=[]
TempList=[]
IncreaseInRank=0
currentRank =0
Max_Increase =0
sort_index = np.argsort(Cost_routing[:,0])
CostMinMon=0
Previous_Cost =0
PrevProb=[]
#print 'Diman Sort naKarde'
#print Cost_routing
#print 'Diman Sort Karde!'
#print sort_index
for i in sort_index:
  #temp.remove(i)
  #print 'Temp List in the beginning:'
  #print TempList
  #if (TempList):
  #  ListofR=TempList
  #print 'ListofR in the beginning:'
  #print ListofR
  ThisCost=Cost_routing[i,0]
  #print 'This Cost:'
  #print ThisCost
  #print 'PPPPRevious Cost'
  #print Previous_Cost
  if (ThisCost != Previous_Cost): 
      if (len(ListofR) ==0):
          #print 'NO EQUAL COST EMPTY'
          temp= []
          temp.append(i)
          IncreaseInRank = matrix_rank(R[temp,:]) - currentRank
          #print 'Rank of R'
          #print matrix_rank(R[temp,:])
          #print 'Incease in Rank'
          #print IncreaseInRank
          #print 'current Rank'
          #print currentRank
          if (IncreaseInRank >0):
            ListofR.append(temp)
            currentRank= matrix_rank(R[temp,:])
            CostMinMon = CostMinMon + Cost_routing[i,0]
            PrevProb=i
            Previous_Cost = ThisCost
            #ListofCost.append(CostMinMon)

      else:
        k=0
        for Probes in ListofR:
          #print 'NO EQUAL COST NO EMPTY'
          #print Probes
          temp= copy.deepcopy(Probes)
          currentRank=matrix_rank(R[temp,:])
          temp.append(i)
          IncreaseInRank = matrix_rank(R[temp,:]) - currentRank
          #print 'Rank of R'
          #print matrix_rank(R[temp,:])
          #print 'Incease in Rank'
          #print IncreaseInRank
          #print 'current Rank'
          #print currentRank
          if i in Probes:
            Probes.remove(i)
          if (IncreaseInRank >0):
            Probes.append(i)
            currentRank= matrix_rank(R[temp,:])
            CostMinMon = CostMinMon + Cost_routing[i,0]
            PrevProb=i
            Previous_Cost = ThisCost
            #ListofCost[k]= ListofCost[k] + Cost_routing[i,0]
          k=k+1
  elif (ThisCost == Previous_Cost):
    #if (TempList):
    #  ListofR=TempList
    #ListofR = copy.deepcopy(TempList)
    print 'TempList Here:'
    print TempList
    #print 'Prev Cost'
    #print Previous_Cost
    #print 'this cost'
    #print ThisCost
    k=0
    for Probes in ListofR:
      #print 'Probes Here'
      #print Probes
      TempList = copy.deepcopy(ListofR)
      temp = copy.deepcopy(Probes)
      currentRank = matrix_rank(R[temp,:])
      temp.append(i)
      IncreaseInRank = matrix_rank(R[temp,:]) - currentRank
      if i in Probes:
        Probes.remove(i)
      if (IncreaseInRank > 0):
        Probes.append(i)
        #print ListofR
        currentRank = matrix_rank(R[temp,:])
        #ListofCost[k]=ListofCost[k]+ Cost_routing[i,0]
        CostMinMon = CostMinMon + Cost_routing[i,0]
        PrevProb = i
        TempList = []
        Previous_Cost = ThisCost
      else:
        #print 'Probes'
        #print Probes
        #print 'Temp:'
        #print temp
        #print 'I:'
        #print i
        temp.remove(i)
        #temp.remove(temp[len(temp)-1])
        OldProb= temp[len(temp)-1]
        temp.remove(OldProb)
        OldRank= matrix_rank(R[temp,:])
        temp.append(i)
        IncreaseInRank = matrix_rank(R[temp,:]) - OldRank
        if (IncreaseInRank >0):
          TempList.append(temp)
          #ListofCost.append(ListofCost[k-1] +Cost_routing[i,0])
          currentRank = matrix_rank(R[temp,:])
          Previous_Cost = ThisCost
        else: 
          temp.append(OldProb)
      k=k+1
    if (TempList):
      ListofR = TempList
  #temp.remove(i)
  #Previous_Cost= ThisCost
print 'Found ListofR'
print ListofR
ProbMinMon=[]
MinimumMonitors=1000000
MinProbeLen=0
ListofCost= np.zeros(shape=(len(ListofR), 1))
J=0
CostMinMon =0
for x in ListofR:
  print 'Rank'
  print matrix_rank(R[x,:])
  for p in x:
    ListofCost[J] = ListofCost[J] + Cost_routing[p,0]
  J = J +1
  if (ListofCost[J-1] > CostMinMon):
    CostMinMon = ListofCost[J-1][0]
for c in ListofCost:
  print 'Cost of Elements:'
  print c
  #if (c > CostMinMon):
  #  CostMinMon = c
OPT_Prob=[]
for Probes in ListofR:
  MinProbMinMon= []
  for i in Probes:
    if green_edges[i][0] not in MinProbMinMon:
      #print 'Source:'
      #print green_edges[i][0]
      MinProbMinMon.append(green_edges[i][0])
    if green_edges[i][1] not in MinProbMinMon:
      #print 'Destination:'
      #print green_edges[i][1]
      MinProbMinMon.append(green_edges[i][1])
  if (len(MinProbMinMon) < MinimumMonitors):
    MinimumMonitors = len(MinProbMinMon)
    ProbMinMon = MinProbMinMon
    MinProbeLen = len(Probes)
    OPT_Prob = Probes
###############################################################################################################################
#################################################################################
MinProbMinMonNull = null(R[OPT_Prob,:])
rows= len(MinProbMinMonNull)
columns = len(MinProbMinMonNull.T)
print 'Rows'
print rows
print 'Columns'
print columns
routing_rows = len(R[OPT_Prob,:])
routing_columns = len(R[OPT_Prob,:].T)
print 'Routing rows'
print routing_rows
print 'Routing Columns'
print routing_columns
iden =1
MinProb_MinMon_Identi_link =0
#for i in range(0,len(green_edges)-1):
#  for j in range(0,len(my_null.T)-1):
for i in range(0,rows):
  #print 'I ro print kon'
  #print i
  for j in range(0,columns):
    #print 'J ro print kon'
    #print j
    if (-1e-12 < MinProbMinMonNull[i][j] < 1e-12) and (iden==1):
      iden=1
    else:
      iden=0
  if (iden == 1):
    MinPron_MinMon_Identi_link = MinProb_MinMon_Identi_link +1
    #print 'Which Row?'
    #print i
  iden=1
#################################################################################
print 'Number of Identofiable links:'
print MinProb_MinMon_Identi_link
#################################################################################
#################################################################################################################################    
#print 'Green Edges'
#for edge in green_edges:
#  print 'Source'
#  print edge[0]
#  print 'Destination'
#  print edge[1]
print 'Preserving rank, we have this many monitors:'
print MinimumMonitors
print 'Minimum Number of Probes to preserve Rank:'
print MinProbeLen
print 'Cost of Preserving Rank (Hop count):'
print CostMinMon
print '####################FINISHED MIN-Prob with minimum monitors algorithm: Similar to finding all spanning trees ######################'
#################################################################################################################################
##############Start Greedy-Max-Rank Algorithm####################################################################################
print '#################################Start Greedy-Max-Rank Algorithm #######################################################'
#MaxRank_Identi_link, MaxRank,MaxRankMonitors, RMaxRank, CostMaxRank = Greedy_Max_Rank_Unbounded(Cost_routing, R, ProbeCost, green_edges)
print '####################FINISHED MAX-rank algorithm ######################'
###################################################################################
#################Started Max-Rank Alg 1: This algorithm gauranteed (1-1/e)/2 approximation######################################
Alg1MaxRank_Identi_link, Alg1MaxRank, Alg1MaxRankMonitors, Alg1RMaxRank, Alg1CostMaxRank = Greedy_Max_Rank_Alg1(Cost_routing, R, ProbeCost, green_edges)
MaxRank_Identi_link, MaxRank,MaxRankMonitors, RMaxRank, CostMaxRank = Greedy_Max_Rank_Alg2(Cost_routing, R, ProbeCost, green_edges)
#################STARTED Min Monitor's Algorithm###################################
print '##################STARTED Min Monitor Max Rank Algorithm#######################'
RMinMonMaxRank=[]
temp=[]
Added =[]
AddedCost = []
IncreaseInRank=0
IncreaseWeight=0
MaxWeight =0
currentRank =0
Max_Increase =0
sort_index = np.argsort(Cost_routing[:,0])
Sorted=[]
MinMonMaxRankSet=[]
CostofMon = 0
Sorted = list(sort_index)
#sort_index.tolist()
#sort_index = Cost_routing
#Sorted = copy.deepcopy(sort_index)
CostMinMonMaxRank=0
#while (CostMaxRank < ProbeCost):
for j in Sorted:#sort_index:
  for i in Sorted:#sort_index:
    #print 'I ro print kon'
    #print i
    #print 'RMaxRank'
    #print RMaxRank
    temp= copy.deepcopy(RMinMonMaxRank)
    if (temp):
      currentRank = matrix_rank(R[temp,:])
    else:
      currentRank = 0
    if i not in temp:
      temp.append(i)
    IncreaseInRank=  matrix_rank(R[temp,:]) - currentRank
    CostofMon = 0
    if green_edges[i][0] not in MinMonMaxRankSet:
      CostofMon= CostofMon + 1
    if green_edges[i][1] not in MinMonMaxRankSet:
      CostofMon= CostofMon + 1
    IncreaseWeight = IncreaseInRank / (CostofMon+0.1)
    #print 'Rank of R'
    #print matrix_rank(R[temp,:])
    #print 'IncreaseInRank'
    #print IncreaseInRank
    #print 'currentRank'
    #print currentRank
    #print 'IncreaseWeight'
    #print IncreaseWeight
    #if i in RMaxRank:
    #  RMaxRank.remove(i)
    #temp.remove(i)
    if (IncreaseWeight > MaxWeight) and ((CostofMon + CostMinMonMaxRank) < Monitors):
      #Print 'Yaftam!'
      #Max_Increase = IncreaseInRank
      #RMaxRank.append(i)
      MaxWeight = IncreaseWeight
      Added=i
      AddedCost = CostofMon
      #print 'Added:'
      #print Added
      #print 'ProbeCossssssssssssssst'
      #print ProbeCost
      #print 'Added Probe Cost:'
      #print (Cost_routing[i,0]+Cost)
      #print 'AddedCost:'
      #print AddedCost
      #currentRank= matrix_rank(R[temp,:])
      #CostMaxRank = CostMaxRank + Cost_routing[i,0]
    if i != Added:
      temp.remove(i)
  if Added not in RMinMonMaxRank:
    RMinMonMaxRank.append(Added)
    print 'RMinMonMaxRank Found:'
    print RMinMonMaxRank
    CostMinMonMaxRank = CostMinMonMaxRank + AddedCost
    if green_edges[Added][0] not in MinMonMaxRankSet:
      MinMonMaxRankSet.append(green_edges[Added][0])
    if green_edges[Added][1] not in MinMonMaxRankSet:
      MinMonMaxRankSet.append(green_edges[Added][1])
    #print 'CostMaxRank of Rmin:'
    #print CostMaxRank
    temp.append(Added)
    currentRank = matrix_rank(R[temp,:])
    #temp.remove(Added)
    #sort_index = np.delete(sort_index, Added)
    Sorted.remove(Added)
    #print 'HHHHHHHHHHHHEEEEEEEEEEEEEYYY Print SortIndex'
    #print Sorted
    MaxWeight =0
    IncreaseWeight =0
    #del sort_index[Added]
    #sort_index.delete(Added)
    #Sorted.remove(Added)
#####################################
print 'Found R'
print RMinMonMaxRank
#for x in RMaxRank:
print 'Maximum Rank:'
print matrix_rank(R[RMinMonMaxRank,:])
MinMonMaxRankMonitors=[]
for i in RMinMonMaxRank:
  #print 'This is which index'
  #print i
  if green_edges[i][0] not in MinMonMaxRankMonitors:
    #print 'Source:'
    #print green_edges[i][0]
    MinMonMaxRankMonitors.append(green_edges[i][0])
  if green_edges[i][1] not in MinMonMaxRankMonitors:
    #print 'Destination:'
    #print green_edges[i][1]
    MinMonMaxRankMonitors.append(green_edges[i][1])
print 'Preserving rank, we have this many monitors:'
print len(MinMonMaxRankMonitors)
print 'Minimum Number of Probes to preserve Rank:'
print len(RMinMonMaxRank)
#for x in RMaxRank:
print 'Rank:'
print matrix_rank(R[RMinMonMaxRank,:])
MinMonMaxRankMonitors=[]
for i in RMinMonMaxRank:
  #print 'This is which index'
  print i
  if green_edges[i][0] not in MinMonMaxRankMonitors:
    #print 'Source:'
    #print green_edges[i][0]
    MinMonMaxRankMonitors.append(green_edges[i][0])
  if green_edges[i][1] not in MinMonMaxRankMonitors:
    #print 'Destination:'
    #print green_edges[i][1]
    MinMonMaxRankMonitors.append(green_edges[i][1])
MinMonMaxRank = matrix_rank(R[RMinMonMaxRank,:])
###########################################################
#################################################################################
MinMonMaxRankNull = null(R[RMinMonMaxRank,:])
rows= len(MinMonMaxRankNull)
columns = len(MinMonMaxRankNull.T)
print 'Rows'
print rows
print 'Columns'
print columns
routing_rows = len(R[RMinMonMaxRank,:])
routing_columns = len(R[RMinMonMaxRank,:].T)
print 'Routing rows'
print routing_rows
print 'Routing Columns'
print routing_columns
iden =1
MinMonMaxRank_Identi_link =0
#for i in range(0,len(green_edges)-1):
#  for j in range(0,len(my_null.T)-1):
for i in range(0,rows):
  #print 'I ro print kon'
  #print i
  for j in range(0,columns):
    #print 'J ro print kon'
    #print j
    if (-1e-12 < MinMonMaxRankNull[i][j] < 1e-12) and (iden==1):
      iden=1
    else:
      iden=0
  if (iden == 1):
    MinMonMaxRank_Identi_link = MinMonMaxRank_Identi_link +1
    #print 'Which Row?'
    #print i
  iden=1
#################################################################################
print 'Number of Identofiable links:'
print MinMonMaxRank_Identi_link
#################################################################################
#################################################################################
print 'Maximum Rank is:'
print MinMonMaxRank
print 'With this rank, we have this many monitors:'
print CostMinMonMaxRank#len(MinMonMaxRankMonitors)
print 'Minimum Number of Probes to for maximum Rank:'
print len(RMinMonMaxRank)
print 'Cost of Preserving Rank (Hop count):'
print CostMinMonMaxRank
print '##################DIMAAAAAAAAAAAAAAN Finished Min Monitor Max Rank Algorithm######################'
################FINISHED Min Monitor Max Rank Algorithm####################################
###########################################################
#In this section, we want to find solutions of each variable:
# Use brute force to find the equations that solve e1 e2, ...
# Suppose I only want to choose k/M monitors.
#X1= R[0][:] 
#X2= R[1][:]
#X3= [X1; X2]#np.concatenate([X1; X2])
#X3= [X1 X2]
#print 'Concatinate'
#print X3
#R2= R
#R_enumurate=[]
#N= len(R)
#for k in range(0,N-2)
#  #find all c(n,k) combination of rows
########################OPTIMAL##########################################
#COMPUTE all combinations:
#class Combination:
#     def __init__(s,d, comb_monitors):
#         edge= (s,d)
#         Combination.e = edge
#         Combination.m = comb_monitors

#class Combination:
#    def __init__(edge):
#        edge.self = []
#
#    def add(edge, s,d):
#        e=(s,d)
#        edge.self.append(e)        
#
#    #def addtwice(self, x):
#    #    self.add(x)
#    #    self.add(x

class Combination():#(s,d,m):
    def __init__(self, s, d, m,number, monitor_number):
        edge=(s, d)
        self.e = edge
        self.m = m
        self.n = number
        self.mon_num = monitor_number
    #def AddComb(self, m):
    #    self.m = m
class Monitors_Perm():
    def __init__(self,edges,m,number):
        self.ident= edges
        self.num=number
        self.monitors= m
        

my_objects = []
Edge_index=0

for links in H2.edges():
    my_objects.append(Combination(Edge_index,links,[],Edge_index,[]))
    Edge_index = Edge_index +1
    #my_objects.AddComb(
my_monitor_comb=[]
# later

#for obj in my_objects:
#    print obj.e
#    print obj.m
#    print obj.n

print 'All chosen monitors'
print my_monitors
print '##############################'
stuff = my_monitors
Max_Ident=0
Selected_Links=[]
Selected_monitors=[]
x = (int)(Monitors+1)
index=0
#if 1> 0:
#for L in range(x, x+1):
#for L in range(2, len(stuff)+1):
for L in range(len(stuff), len(stuff)+1):
  #L = x
  for subset in itertools.combinations(stuff, L):
    #print(subset)
    enum_green_edges= my_green_edges(subset)
    Rx= Routing_matrix(H2, enum_green_edges)
    Num_Iden, Iden= Identifiable_links(Rx)
    #print ' Deeeeeeeeeeeeeeeeeeeeeeee'
    #print Iden
    my_monitor_comb.append(Monitors_Perm(Iden,subset,index))
    #index= index+1
    for n in Iden:
      for obj in my_objects:
        if (str(obj.n) == str(n)):
          #print 'YEEEEEYYYYYYYYYYYYYYYYYEEEEEEEEEEEEEEEEs'
          obj.m.append(subset)
          obj.mon_num.append(index)
    index= index+1
    #print Iden 
    if (Num_Iden > Max_Ident):
      if (L < x):
        #print 'L:'
        #print L
        #print 'Monitors'
        #print x
        #print 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
        Max_Ident = Num_Iden
        Selected_Links=Iden
        Selected_monitors = subset
      #if (float(Num_Iden)/(L) >  )
    #print len(subset)
    #add to the list of e1 or e2 ....eN which can be identified using this list

#print type(Monitors)
#print type(L)
print 'Best Solution:'
print 'Maximum number of links:'
print Max_Ident
print 'Selected Links:'
print Selected_Links
print 'Selected_Monitors'
print Selected_monitors
print '##########################OPT Finished############################'
print '##########################Start Greedy ###########################'
#########################GREEEDY BASED APPROACH###############################
Best_greedy=0
Best_greedy_monitors=[]
Identified_links=[]
for obj in my_objects:
    print obj.e
    print obj.m
    print obj.n
    #print obj.m[0]
    #if (float(len(obj.m[0]))/len() > Best_greedy)
print '########################START MONITOR LISTS###################'
Add_more_monitors =0#1
Added_monitors =0
temp_monitors=[]
temp_mon=[]
temp_Identifiable_links=[]
temp_mon_ident=[]
Identified_links=[]
temp_num_Identifiable= []
while (Add_more_monitors):
  for mon in my_monitor_comb:
      ##print 'Identifiable_Links:'
      ##print mon.ident
      ##print 'Number:'
      ##print mon.num
      ##print 'Monitor Combination:'
      ##print mon.monitors
      Num_Identifiable=len(mon.ident)
      Num_Selected_Mon =0
      Selected_mon=[]
      for m in mon.monitors:
        if m not in Best_greedy_monitors:
           Num_Selected_Mon= Num_Selected_Mon + 1
           Selected_mon.append(m)
      for e in mon.ident:
        if e in Identified_links:
           Num_Identifiable = Num_Identifiable -1
      if ((Added_monitors+ len(Selected_mon)) > Monitors):
          Add_more_monitors =0
      if ((float(float(Num_Identifiable)/len(Selected_mon))) > float(Best_greedy)) and ((Added_monitors+ len(Selected_mon) -1) < Monitors):
          print 'Length of selected monitors:'
          print (Added_monitors+ len(Selected_mon)) 
          #Added_monitors= Added_monitors + len(Selected_mon)
          Best_greedy = float(float(Num_Identifiable)/len(Selected_mon))
          temp_monitors=Selected_mon
          #temp_selected_mon= len(Selected_mon)
          #temp_selected_mon=Selected_mon
          temp_num_Identifiable= Num_Identifiable
          temp_mon=mon.monitors
          temp_Identifiable_links= Identifiable_links
          temp_mon_ident= mon.ident
          #Best_greedy_monitors.append(Selected_mon)
          #print 'Found the best greedy monitor combinations:'
          #print mon.monitors
          #print 'Those which were not included before:'
          #print Selected_mon
          #print 'Best greedy number:'
          #print Best_greedy
          #print 'Num identifiable links:'
          #print Num_Identifiable
          #print 'Length of monitors:'
          #print len(mon.monitors)
          #for edge in mon.ident:
          #  if edge not in Identified_links:
          #    Identified_links.append(edge)
  Added_monitors= Added_monitors + len(temp_mon)
  #Best_greedy = float(float(Num_Identifiable)/len(temp_selected_mon))
  Best_greedy_monitors.append(temp_mon)
  print '##################Start printing the stats:#############'
  print 'Found the best greedy monitor combinations:'
  print Best_greedy_monitors
  print 'Those which were not included before:'
  print temp_mon
  print 'Best greedy number:'
  print Best_greedy
  print 'Num identifiable links:'
  print temp_num_Identifiable
  print 'Length of monitors:'
  print len(temp_mon)
  for edge in temp_mon_ident:
    if edge not in Identified_links:
      Identified_links.append(edge)
  print 'Links which were identified:'
  print Identified_links 
  print 'Selected Monitors:'
  print Best_greedy_monitors 
  print 'Number of Selected Monitors'
  print Added_monitors     
####################### Finished with the Greedy Algorithm#####################
####################### Start writing the ILP formulation for Branch and Bound ######################
#Max sum xl s.t xl <= sum zs for s: l \in I(Ms) and sum_{v \in V} yv <= k nad Zs <= yv ####
Best_ILP_monitors, ILP_identifiable_links = optimal_ILP_tomography(my_monitor_comb,my_objects,Monitors, my_monitors) 
####################### Finished OPT ILP, start the LP relaxation of the problem####################
Best_LP_relaxation_monitors, LP_relaxation_identifiable_links = optimal_LP_tomography(my_monitor_comb,my_objects,Monitors, my_monitors)
####################### Writing the Stats#######################################
filename_stat='stat_simulations_'+filename_graph+"_Max_Monitors_"+str(Monitors)+"_Percentage_"+str(Percentage)+"_Alpha_"+str(alfa)+".txt"
#numero della simulazione corrente e scrivo statistiche
num_sim=get_num_simulation(path_to_file_simulation)

Nodes= H2.number_of_nodes()
Edges= H2.number_of_edges()
Edges= H2.number_of_edges()
write_stat_monitors(path_to_stats,filename_stat,seed_random,alfa,
                          len(my_monitors), Num_Identi_link, MatrixRank, TotalCost, #Random generated monitor with a maximum of Monitors, Number of Identifiable links using shortest path 
                          Monitors, #Limit on Maximum number of monitors
                          len(Selected_Links), len(Selected_monitors), #Brute Force: The identifiable links, , Selected number of monitors
                          len(Identified_links), Added_monitors, # Greedy algorithm: The identifiable links, Selected number of monitors,
                          len(ILP_identifiable_links), len(Best_ILP_monitors), # ILP solution: The identifiable links, Selected number of monitors,
                          len(LP_relaxation_identifiable_links),len(Best_LP_relaxation_monitors), # LP relaxation of ILP: The identifiable links, Selected number of monitors
                          len(MinProbMonitors), len(RMin), Cost, MinProbe_Identi_link,  #Min-prob algorithm that preserves the rank: Minimum number of Monitors, Number of probes is OPT, Cost (hop-count), Number of identifiable links
                          MinimumMonitors, MinProbeLen, CostMinMon, MinProb_MinMon_Identi_link, #Min-prob algorithm that preserves the rank: Minimum number of Monitors, Number of probes is OPT, Cost (hop-count), Number of identifiable links
                          MaxRank, len(MaxRankMonitors), len(RMaxRank), CostMaxRank, ProbeCost, MaxRank_Identi_link,  #Matrix maximum rank is, number of monitors for the max rank, Minimum number of probes, Cost of probes for the max rank, Limit on the probe cost, Number of identifiable links using max Rank algorithm
                          Alg1MaxRank, len(Alg1MaxRankMonitors), len(Alg1RMaxRank), Alg1CostMaxRank, ProbeCost, Alg1MaxRank_Identi_link,  #Matrix maximum rank is, number of monitors for the max rank, Minimum number of probes, Cost of probes for the max rank, Limit on the probe cost, Number of identifiable links using max Rank algorithm
                          MinMonMaxRank, CostMinMonMaxRank, len(RMinMonMaxRank), MinMonMaxRank_Identi_link, #Matrix maximum Rank when having a bound on number of monitors, Number of Monitors that maximizes the rank, Number of Probes for Min Mon Max Rank Algorithm, Number of identifiable links using MaxRankMin Mon Algorithm
                          Nodes, Edges) # Number of nodes in the graph, Number of edges in the graph

#print 'Maximum Rank is:'
#print matrix_rank(R[RMaxRank,:])
#print 'With this rank, we have this many monitors:'
#print len(MaxRankMonitors)
#print 'Minimum Number of Probes to for maximum Rank:'
#print len(RMaxRank)
#print 'Cost of Preserving Rank (Hop count):'
#print CostMaxRank
#print '####################FINISHED MIAX-rank algorithm ######################'

#################################################################################
#print 'Number of Identofiable links:'
#print MinMonMaxRank_Identi_link
#################################################################################
#################################################################################
#print 'Maximum Rank is:'
#print MinMonMaxRank
#print 'With this rank, we have this many monitors:'
#print CostMinMonMaxRank#len(MinMonMaxRankMonitors)
#print 'Minimum Number of Probes to for maximum Rank:'
#print len(RMinMonMaxRank)
#print 'Cost of Preserving Rank (Hop count):'
#print CostMinMonMaxRank
#print '##################DIMAAAAAAAAAAAAAAN Finished Min Monitor Max Rank Algorithm######################'
