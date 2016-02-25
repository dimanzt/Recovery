
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
from my_lib_optimal_recovery_multicommodity import *
from my_lib_optimal_recovery_multicommodity_worst import *
from my_lib_optimal_recovery_multicommodity_best import *
from my_lib_check_routability import *
from my_lib_compute_max_demand_in_the_graph import *


work_dir=os.getcwd()


path_to_dot_dir='../../../image_graph_dot/DotFile/'
path_to_image_dir='../../../image_graph_dot/immagini_generate/'
path_to_image_store='../../../image_graph_dot/store_images/'
path_to_stats='../../../image_graph_dot/stats/statistiche/'
path_to_file_simulation='../../../image_graph_dot/current_simulation.txt'
path_to_stat_prog='../../../image_graph_dot/stats/progress_iteration/'
path_to_stat_times='../../../image_graph_dot/stats/times/'


#path_to_dot_dir='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\DotFile\\'
#path_to_image_dir='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\immagini_generate\\'
#path_to_image_store='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\store_images\\'
#path_to_stats='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\stats\\statistiche'
#path_to_file_simulation='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\current_simulation.txt'
#path_to_stat_prog='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\stats\\progress_iteration\\'
#path_to_stat_times='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\stats\\times\\'

#path_to_dot_dir='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/DotFile/'
#path_to_image_dir='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/immagini_generate/'
##path_to_image_store='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/store_images/'
#path_to_stats='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/stats/statistiche/'
#path_to_file_simulation='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/current_simulation.txt'
#path_to_stat_prog='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/stats/progress_iteration/'
#path_to_stat_times='/usr/local/home/'+user_name+'/Desktop/image_graph_dot/stats/times/'

#print path_to_file_simulation
#'/usr/local/home/ciavarellas/Documents/'



"""
for arg in sys.argv:
    print 'Parametro passato: '+str(arg)
"""

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
var_distruption=int(sys.argv[12])

#load a particular graph from file
#path_to_graph= 'network topologies/Abilene - High Capacity_Random_Capacity.gml'
#path_to_graph= 'network topologies/Abilene.gml'
#path_to_graph='network topologies/BellCanada_Random_Capacity - High Capacity - 2 backbone - eterogeneous.gml'
#path_to_graph='network topologies/BellCanada - Connettivity.gml'
#path_to_graph= 'network topologies/Europe - Connettivity.gml'
#path_to_graph= 'network topologies/DeltaCom - Connettivity.gml'
#path_to_graph= 'network topologies/Tw - Connettivity.gml'
#path_to_graph= 'network topologies/xpedius - Connettivity.gml'

#filename_graph= '600_800_Random_Capacity'
#filename_graph='Abilene'
#filename_graph='KDL_Random_Capacity'
#filename_graph='erdos_renyi_graph_100_nodes_231_edges'
#filename_graph='erdos_renyi_graph_100_nodes_524_edges'
if sys.argv[13]!=None:
    filename_graph=str(sys.argv[13])
    print 'Graph: ' + filename_graph


path_to_graph= 'network topologies/'
path_to_graph=path_to_graph+filename_graph+'.gml'
path_to_folder_couple='distance_between_couples/'

"""
max_nodes=50
max_x=500
max_y=500
prob_edge_random=0.025
path_to_graph=generate_random_graph(max_nodes,prob_edge_random,max_x,max_y)

H=nx.MultiGraph(nx.read_gml(path_to_graph))
flag=True


while (flag):
    path_to_graph=generate_random_graph(max_nodes,prob_edge_random,max_x,max_y)
    del H
    H=nx.MultiGraph(nx.read_gml(path_to_graph))
    if nx.is_connected(H):
        flag=True
        diameter=compute_diameter_of_graph(H)
        print diameter
        if diameter>6:
            break


#generate_erdos_renyi_graph(50,0.05)

#sys.exit(0)
"""


#path_to_graph= 'network topologies/test_path_ramification.gml'
#path_to_graph='network topologies/random_graph_48_nodes_60_edges.gml'
#path_to_graph='network topologies/multiGraph.gml'
#path_to_graph='network topologies/BellCanada_Random_Capacity.gml'
#path_to_graph='network topologies/BellCanada - No capacity.gml'
#path_to_graph='network topologies/BellCanada_Random_Capacity - High Capacity.gml'
#path_to_graph='network topologies/BellCanada_Random_Capacity -  One capacity.gml'
#path_to_graph='network topologies/BellCanada_Random_Capacity - Backbone.gml'
#path_to_graph='network topologies/BellCanada.gml'
#path_to_graph='network topologies/Barabasi_graph_30_nodes_56_edges.gml'

#print path_to_graph
#load graph from path
#H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply

#or generate graph with model Barabasi
#path_to_graph=generate_graph_barabasi(30,2,1)


H=nx.MultiGraph(nx.read_gml(path_to_graph))

#print H.nodes()[1]

print 'Dimensions of the Graph'
print "Nodes: %d"%H.number_of_nodes()
print "Edges: %d"%H.number_of_edges()
print "Total: %d"%(H.number_of_nodes()+H.number_of_edges())
#sys.exit(0)
#imposto il seed della simulazione con uno particolare
#seed_random= random.randint(0,sys.maxint)
#commentare questa riga se si vuole seed random
seed_random=2
#seed passato per argomento
seed_random=int(seed_passed)
random.seed(seed_random)

print 'Seed Utilized: %f: '%seed_random


print 'Diameter of the Graph: %d'%(compute_diameter_of_graph(H))

print 'Flow Variation: %s'%(flow_c_fixed)
if flow_c_fixed=='False':
    print 'Quantity of Flow Assigned: %d'%(flow_c_value)
else:
    print 'Vario il numero di coppie fissando il flusso: %d'%(flow_c_value)
    print 'Number of Pairs Selected: %d'%(number_of_couple)

if fixed_distruption=='True':
    print 'Fixed Disruption'
    #var_distruption=0
else:
    print 'Varied Disruption'
    print 'Variance of Disruption: %d '%(var_distruption)

#prendi la lista delle distanze da file
list_of_couples=get_list_distance_couples(path_to_folder_couple,filename_graph)

list_of_couples=subset_of_list(list_of_couples,50)

list_of_couples=select_random_couples_from_list(list_of_couples,number_of_couple)
print 'Subset of Random Couples:'
print list_of_couples

#sys.exit(0)

#my_draw(H,'1-initial'+'_Seed_'+str(seed_random)+'_'+'Prob_edge_'+str(prob_edge_passed)+'_')
#sys.exit('stop')

#generate a random graphs
"""
max_nodes=50
max_capacity=10
max_x=500
max_y=500
prob_edge_random=0.25
path_to_graph=generate_random_graph(max_nodes,max_capacity,prob_edge_random,max_x,max_y)
H=nx.MultiGraph(nx.read_gml(path_to_graph))
"""


#sys.exit(0)
green_edges=[]
filename_graph=path_to_graph[path_to_graph.find('/')+1:-4]
print filename_graph
filename_demand=filename_graph+'DemandGenereted'

#change the graph by assigning random values to the capacity of the edges
#assign_random_capacity_to_edges(H,filename_graph)
#sys.exit(0)

prepare_graph(H)
my_draw(H,'1-initial'+'_Seed_'+str(seed_random)+'_'+'Prob_edge_'+str(prob_edge_passed)+'_')
#sys.exit(0)

#--------Calculate maximum radius value for the total disruption of the graph
"""
max_var_distruption=0
#Coordinate centrali per bell canada: nodo 13, x=45.41117, y=-75.69812
coor_x=45
coor_y=-75
max_var_distruption=find_max_radius_destruction_of_graph(H,coor_x,coor_y)

print 'Max_var_distruption: %d'%(max_var_distruption)
"""

#GENERATE FEASIBLE DEMAND ON SUPPLY GRAPH
#prob_edge=0.05
#Probability green edge passed in argument
prob_edge=float(prob_edge_passed)

#Value of flow in proportion to alfa (put alfa=0.0 if you want the random question between 0 and max flow)
#alfa=0.70
alfa=float(alpha_passed)
#select the distance metric used to calculate the length of a path: 'capacity', 'one-hop', 'broken'
#distance_metric='broken'
distance_metric=distance_metric_passed

#genera la domanda casuale (coppie casuali)
#path_to_demand,green_edges=generate_demand(H,prob_edge,filename_demand,alfa,seed_random,path_to_stats,distance_metric)

#passare lista di coppia manualmente
#list_of_couples=[(0,10),(19,6),(18,6)]
#list_of_couples=[(0,3),(9,4)]
#QUESTO SERVE PER TROVARE IL MAX VALUE OF FLOW C. DOPO AVERLO TROVATO PER IL GRAFO PARTICOLARE, VA COMMENTATO
#print 'Calcolo del max value of flow c:'
#max_flow_c=compute_max_value_of_fixed_flow_from_list_of_couple(H,list_of_couples,prob_edge,alfa,filename_demand,seed_random,path_to_stats,distance_metric)

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
    #per la coppia selezionata non e' possibile assegnare la quantita flow_c. SCARTO IL SEED
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
#green_edges=[(3,6,5)]
print green_edges

#sys.exit(0)
copy_of_green_edges=[]
copy_of_green_edges=deepcopy(green_edges)
#decommentare se si passano archi verdi manuali
#compute_paths(H,green_edges)

#generare una demand casuale dal grafo

D=nx.MultiGraph(nx.read_gml(path_to_demand))

#caricare una demand da file
#D=nx.MultiGraph(nx.read_gml('network topologies/abileneDemand.gml'))

merge_graphs(H,D)
H1=nx.MultiGraph(H)
H2=nx.MultiGraph(H)
H3=nx.MultiGraph(H)
H4=nx.MultiGraph(H)
H5=nx.MultiGraph(H)
H6=nx.MultiGraph(H)
H7=nx.MultiGraph(H)

#old_bet_dict=compute_my_betweeness(H,green_edges,'reciproco')
#my_draw(H, '2-prepared-old_bet')

#betweeeness basata sui flussi
#new_bet_dict=compute_my_betweeness_2(H, green_edges,'reciproco')

#centralita approssimata
#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)

#centralita esatta
#new_bet_dict=compute_my_betweeness_4(H, green_edges,distance_metric)

select_betweeness(H,green_edges,distance_metric,type_of_bet_passed)


#print new_bet_dict
my_draw(H, '2-prepared-new_bet_alpha_%f'%alfa)
#print H.nodes(),H.edges()
#supply_graph=get_supply_graph(H,green_edges)
#nx.single_source_dijkstra(supply_graph,0,4,'weight')
#print 'my versione'
#my_dijkstra_shortest_path(supply_graph,0,4,'weight')

#---------------pulisco il file delle stat progr e times
if not os.path.exists(path_to_stat_prog):
    os.makedirs(path_to_stat_prog)
file=open(path_to_stat_prog+filename_graph+'_progress.txt','w')
file.close()

#print check_routability(H,green_edges)

#print compute_max_demand_in_the_graph(H,green_edges)


#manual destroy from file
#path_to_distruption='C:\Users\Utente\Desktop\image_graph_dot\stats\Abilene_Destroyed.txt'
#path_to_distruption='C:\Users\Utente\Desktop\image_graph_dot\stats\Abilene_all_destroyed.txt'
#path_to_distruption='C:\Users\Utente\Desktop\image_graph_dot\stats\\test_ramification_destroyed.txt'
#destroy_graph_manual(H,path_to_distruption)

#casual destroy
nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,12) #per abilene




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
total_demand_of_graph=compute_total_demand_of_graph(H)

#START Iteritive Split and Prune
#"""---------------------------------------------------------------------------------

graph_built=get_graph_from_destroyed_graph(H)

resolve_one_hop_nodes(H, graph_built, owned_nodes)
my_draw(graph_built,'grafo_costruito')

#sys.exit(0)

#Gather Information


print '*********************************************'
print 'Start Iteritive Split and Prune'
print '*********************************************'
cnt = 0
K_HOPS = 1

while ( check_routability(graph_built,copy_of_green_edges)==False  ):

    #Begin Seamus Additions
    for node in nodes_recovered_isp: 
        if node not in owned_nodes:
             owned_nodes.append(node)
        
    print '########################################################'
    print owned_nodes

    information_gain(H, graph_built, owned_nodes, 1);
    
    #resolve_onwed_node_edges(H,graph_built, owned_nodes)
    #resolve_one_hop_nodes(H, graph_built, owned_nodes)
        
    write_progress_algorithm_on_file(path_to_stat_prog,filename_graph,'ISP',number_of_couple,int(sys.argv[5]),int(sys.argv[4]),int(sys.argv[1]),len(nodes_recovered_isp),len(edges_recovered_isp),len(nodes_recovered_all),len(edges_recovered_all))
    
    #print 'post'
    #aggiorna eventuali nodi verdi che non hanno piu archi
    #check_if_are_green(temp_graph_supply)
    #split(H,temp_graph_supply,id_bc,i)

    #counter iteration multiple pruning
    counter_pruning=0
    #print couples_to_prune

    recovered_one_hop_flag=False
    pruning_flag=True


    while(pruning_flag==True):
        #quantita di flusso da ridurre
        #flow_to_prune=1
        #ritorna lo shortest path attuale tra la coppia di cui fare lo split dell'arco
        #shortest_path_selected_for_pruning=get_shortest_path_to_prune(H,couple_selected)

        #ritorna tutti gli shortest path fra coppie di nodi verdi senza ramificazioni su cui fare il pruning (SU TUTTO IL GRAFO)
        #multiple_paths_to_prune,edges_to_prune=get_multiple_shortest_path_no_ramification_to_prune(H,distance_metric)

        #ho ripristinato alcuni archi ad un hop, devo fare il pruning
        if (len(recovered_edges_one_hop)>0):
            print 'pre pruning one hop'
            counter_isp+=1
            counter_starvation=0
            couple_pruned=[]
            #print recovered_edges_one_hop
            #print_edge_graph(temp_graph_supply)
            couple_pruned=pruning_one_hop(temp_graph_supply,recovered_edges_one_hop,distance_metric,counter_isp,type_of_bet_passed)
            #print_edge_graph(temp_graph_supply)
            recovred_edges_one_hop=[]
            update_couple_to_prune(couples_to_prune,couple_pruned)

        #costruisce il grafo rimanente senza la distruzione
        only_graph_destroyed=nx.MultiGraph(get_graph_from_destroyed_graph(temp_graph_supply))
        #only_graph_truely_destroyed=nx.MultiGraph(get_graph_from_truely_destroyed_graph(temp_graph_supply))
		
        #my_draw(only_graph_destroyed,'4-grafo_distrutto')

        if couples_to_prune==None:
            #print 'entro'
            #non ho fatto split, calcolo se posso fare pruning su tutti
            #ritorna tutti i path fra coppie di nodi verdi senza ramificazioni  e senza nodi verdi (sul grafo Originale) intermedi su cui fare il pruning (Grafo distruttyo) --> TEOREMA PRUNING
            multiple_paths_to_prune,edges_to_prune=get_multiple_path_no_ramification_to_prune(H,temp_graph_supply,only_graph_destroyed,distance_metric)
            #multiple_paths_to_prune,edges_to_prune=get_multiple_path_no_ramification_to_prune(H,temp_graph_supply,only_graph_truely_destroyed,distance_metric)

        else:
            #ho fatto split, controllo il pruning solo per le due nuove coppie splittate
            print 'controllo se lo split ha creato qualcosa per fare pruning'
            multiple_paths_to_prune,edges_to_prune=get_multiple_path_no_ramification_to_prune_after_split(H,temp_graph_supply,only_graph_destroyed,distance_metric,couples_to_prune)

        if (len(multiple_paths_to_prune)>0):
            pruning_flag=True
            counter_pruning=counter_pruning+1
            #singolo pruning basato sullo shortest della coppia splittata
            #pruning(H,path_for_pruning,flow_to_prune,couples_to_prune,number_of_prune,distance_metric)
            #pruning multiple basato sugli shortest path senza ramificazioni

            print 'multiple path to prune'
            print multiple_paths_to_prune

            pruning_multiple(temp_graph_supply,multiple_paths_to_prune,counter_isp,counter_pruning,distance_metric,type_of_bet_passed)

            if couples_to_prune==None:
               print 'PRUNING DEI PATH:'
            else:
                print 'PRUNING COPPIA SPLITTATA'
                couples_to_prune=None

            print multiple_paths_to_prune

            counter_starvation=0

        elif len(multiple_paths_to_prune)==0:
            pruning_flag=False
            #counter_starvation+=1
        else:
            sys.exit('Errore pruning_flag: lunghezza array dei path prunable <0 !!!')

        #print 'Controllo one hop'
        recovered_edges_one_hop=[]
        recovered_edges_one_hop,recovered_one_hop_flag = recover_one_hop_edge_green(temp_graph_supply,edges_recovered_isp,nodes_recovered_isp,edges_truely_recovered_isp,nodes_truely_recovered_isp)

        if recovered_one_hop_flag:
            add_edges_recovered_to_graph_gray(H,graph_built,recovered_edges_one_hop)
        print recovered_one_hop_flag

        

    ################################################################
        my_draw(temp_graph_supply,'5-isp-%d-recover-one-hop'%(counter_isp))

        #se non dovevo fare il pruning la prossima iterazione, controllo se ho ripristinato almeno un link.  Se si allora faro di nuovo pruning
        #if pruning_flag==False:
        if recovered_one_hop_flag==True:
            pruning_flag=True
            counter_isp=counter_isp+1

    #sys.exit('stop')
    #ritorna l'arco verde splittato e le due nuove coppie di archi verdi con il bc
    #couple_selected,couples_to_prune,flag_no_split=split_by_one(temp_graph_supply,i,distance_metric)


    #if check_routability(temp_graph_supply,green_edges)
    #ritorna l'arco verde splittato e le due nuove coppie di archi verdi con il bc
    #temp_green=get_green_edges(temp_graph_supply)
    #check_routability(temp_graph_supply,temp_green)
    #couple_selected,couples_to_prune,flag_no_split,bc=split_by_capacity_path(temp_graph_supply,counter_isp,distance_metric,nodes_recovered_isp)

    couple_selected,couples_to_prune,flag_no_split,bc=split_by_capacity_path_and_ranking_max_split(temp_graph_supply,counter_isp,distance_metric,nodes_recovered_isp,nodes_truely_recovered_isp,type_of_bet_passed)

    #couple_selected,couples_to_prune,flag_no_split,bc=split_by_capacity_path_and_demand(temp_graph_supply,counter_isp,distance_metric,nodes_recovered_isp,type_of_bet_passed)

    if bc!=None:
        add_node_to_graph_recovered_gray(H,graph_built,bc)
        #owned_nodes.append(bc)

    #my_draw(graph_built,'5-isp-%d-graph_built'%(counter_isp))
    #sys.exit()
    counter_isp=counter_isp+1

    if flag_no_split==True:
        counter_starvation+=1
        print '---------COUNTER STARVATION %d: '%(counter_starvation)

    #sys.exit(0)

    my_draw(graph_built,'ISP%d'%cnt)
    cnt = cnt + 1

    if counter_starvation>=10:
        #sto in stallo
        #winsound.Beep(500,500)
        #winsound.Beep(500,500)
        my_draw(temp_graph_supply,'5-isp-STALLO')
        #sys.exit('ERRORE ISP: possibile stallo dell algoritmo')
        print 'Stallo: vedo se bastano le riparazioni gia fatte per instradare la domanda iniziale'
        graph_recovered=build_graph_repaired(H,nodes_recovered_isp,edges_recovered_isp)
        prepare_graph(graph_recovered)
        merge_graphs(graph_recovered,D)
        my_draw(graph_recovered,'5-STALLO-grafo_riparato_stallo')
        if check_routability(graph_recovered,copy_of_green_edges):
            print 'Riparazioni sufficienti ad instradare tutte le domande'
        else:
            print 'Riparazioni non sufficienti ad istradare tutte l domande'
            #ricorro al multicommodity sul grafo e sulla domanda rimanente
            print 'Ricorro al MCG'
            flag_starvation=True
            green_edges_remaining=get_green_edges(temp_graph_supply)
            print 'Archi rimanenti'
            print green_edges_remaining
            my_draw(temp_graph_supply,'5-isp-STALLO-grafo_passato_MCG')
            nodes_to_recover_for_mcg, edges_to_recover_for_mcg=optimal_recovery_multicommodity(temp_graph_supply,green_edges_remaining)
            flag_solution_MCG=True
            #exit from while

        break
print '*********************************************'
print 'END Iteritive Split and Prune'
print '*********************************************'
my_draw(graph_built,'ISP%d'%cnt)
#---------------------End Iteritive Split and Prune Phase---------------------------------------------------

print 'soluzione parziale ISP'
print nodes_recovered_isp
print edges_recovered_isp
print 'soluzione rimanenete MCG'
print nodes_to_recover_for_mcg
print edges_to_recover_for_mcg
#add nodes and edges from mcg solution
for id_node in nodes_to_recover_for_mcg:
    if id_node not in nodes_recovered_isp:
        nodes_recovered_isp.append(id_node)

for edge in edges_to_recover_for_mcg:
    edge_reverse=(edge[1],edge[0])
    if edge not in edges_recovered_isp and edge_reverse not in edges_recovered_isp:
        edges_recovered_isp.append(edge)


print 'Soluzione algoritmo ISP: '
print 'Nodi ripristinati'
nodes_recovered_isp.sort()
print nodes_recovered_isp

print 'Archi ripristinati'
print edges_recovered_isp

num_rip_isp_nodes=len(nodes_recovered_isp)
num_rip_truely_isp_nodes=len(Find_truely_recovered_nodes(H,nodes_recovered_isp))
#len(nodes_truely_recovered_isp)
num_rip_isp_edges=len(edges_recovered_isp)
num_rip_truely_isp_edges=len(Find_truely_recovered_edges(H,edges_recovered_isp))
#len(edges_truely_recovered_isp)
print num_rip_isp_nodes
print num_rip_isp_edges
print num_rip_truely_isp_nodes
print num_rip_truely_isp_edges

#add_edges_recovered_to_graph(H,temp_graph_supply,edges_recovered_isp)

#recovery_supply_graph(H,temp_graph_supply,nodes_recovered_isp,edges_recovered_isp)
#recover_gray(H,nodes_recovered_isp,edges_recovered_isp, owned_nodes)
recover_gray(H,nodes_recovered_isp,edges_recovered_isp, owned_nodes, K_HOPS)

my_draw(H,'6-final_algorithm')

#winsound.Beep(500,1000)
time_elapsed=round(time.time() - start_time,3)
print("--- %s seconds ---" % str(time_elapsed))
write_stat_time_simulation(path_to_stat_times,'ISP',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed)

#sys.exit(0)

#"""
#----------------------------------------------------------OPTIMAL-------------------------------------------------------
print 'Inizio algoritmo OPTIMAL recovery'
#Diman Commented these
#del H

#H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
#prepare_graph(H)
#merge_graphs(H,D)
#Diman Commented these

#distruggi di nuovo e recover whit multicommodity
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
print path_to_distruption
#Diman
#prepare_graph(H1)
#merge_graphs(H1,D)
#Diman
destroy_graph_manual(H1,path_to_real_distruption)
my_draw(H1,'Diman_optimal')

#nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
#Diman
#destroy_graph_manual(H,path_to_distruption)
#Diman
#green_edges=get_green_edges(temp_graph_supply_optimal)
green_edges=deepcopy(copy_of_green_edges)
#print 'Archi verdi :'
#print green_edges

#all_graph_paths={}
#compute_paths(H,green_edges)
#all_graph_paths=deepcopy(all_graph_paths_copy)


#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H1,'7-destroyed_for_optimal')
#calcola recovery ottimo
nodes_recovered_optimal=[]
edges_recovered_optimal=[]

start_time_optimal=time.time()

#optimal classico
nodes_recovered_optimal,edges_recovered_optimal=optimal_recovery(H1,green_edges)
num_rip_optimal_nodes=len(nodes_recovered_optimal)
num_rip_optimal_edges=len(edges_recovered_optimal)
print num_rip_optimal_nodes
print num_rip_optimal_edges
#ripristina e disegna
recover(H1,nodes_recovered_optimal,edges_recovered_optimal)
#set_betwenness_from_dict(H,old_bet_dict)
#my_draw(H,'4-recovered_optimal_old_bet')
#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H1,'8-recovered_optimal_new_bet')

time_elapsed_optimal=round(time.time() - start_time_optimal,3)
print("--- %s seconds ---" % str(time_elapsed_optimal))
write_stat_time_simulation(path_to_stat_times,'OPT',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed_optimal)
#sys.exit(0)

"""
"""
#------------------------------------Multicommodity generale-------------------------------

print 'Inizio algoritmo Multicommodity Generale'
#Diman Commented
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)
#Diman Commented

#distruggi di nuovo e recover whit multicommodity
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
#Diman
destroy_graph_manual(H,path_to_distruption)
#nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
#Diman

#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)
#all_graph_paths={}
#compute_paths(H,green_edges)
#all_graph_paths=deepcopy(all_graph_paths_copy)
#print 'Archi verdi :'
#print green_edges

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'9-destroyed_multy')


#soluzione con multicommodity generale
nodes_recovered_general=[]
edges_recovered_general=[]
nodes_recovered_general,edges_recovered_general=optimal_recovery_multicommodity(H,green_edges)
num_rip_mult_nodes=len(nodes_recovered_general)
num_rip_truely_mult_nodes=len(Find_truely_recovered_nodes(H,nodes_recovered_general))

num_rip_mult_edges=len(edges_recovered_general)
num_rip_truely_mult_edges=len(Find_truely_recovered_edges(H,edges_recovered_general))

#ripristina e disegna
print 'Soluzione Multicommodity Generale: '
print 'Nodi da ripristinare'
print nodes_recovered_general
print 'Archi da ripristinare'
print edges_recovered_general
print num_rip_mult_nodes
print num_rip_mult_edges
recover(H,nodes_recovered_general,edges_recovered_general)
#set_betwenness_from_dict(H,old_bet_dict)
#my_draw(H,'4-recovered_multi_old_bet')

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'10-recovered_multy_general_new_bet')

#disegnaPDF()
#disegna_3d()

#-------------------------------------------Multicommodity WORST------------------------------------------------------
print 'Inizio algoritmo Multicommodity WORST'
#Diman Commented
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)
#Diman Commented

#distruggi di nuovo e recover whit multicommodity worst
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
#Diman
#nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
destroy_graph_manual(H,path_to_distruption)
#Diman

#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)

#all_graph_paths={}
#compute_paths(H,green_edges)
#all_graph_paths=deepcopy(all_graph_paths_copy)
#print 'Archi verdi :'
#print green_edges

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'11-destroyed_multy_worst')


#recover con multicommodity worst
nodes_recovered_mcw=[]
edges_recovered_mcw=[]
nodes_recovered_mcw,edges_recovered_mcw=optimal_recovery_multicommodity_worst(H,green_edges)
num_rip_mult_worst_nodes=len(nodes_recovered_mcw)
num_rip_mult_worst_edges=len(edges_recovered_mcw)
#ripristina e disegna
print 'Soluzione algoritmo Multicommodity WORST'
print 'Nodi da ripristinare'
print nodes_recovered_mcw
print 'Archi da ripristinare'
print edges_recovered_mcw
print num_rip_mult_worst_nodes
print num_rip_mult_worst_edges
recover(H,nodes_recovered_mcw,edges_recovered_mcw)
#set_betwenness_from_dict(H,old_bet_dict)
#my_draw(H,'4-recovered_multi_old_bet')

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'11-recovered_multy_worst_new_bet')

#-------------------------------------------Multicommodity BEST------------------------------------------------------
print 'Inizio algoritmo Multicommodity BEST'
#Diman Commented
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)
#Diman Commented
#distruggi di nuovo e recover whit multicommodity best
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
#Diman
#nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
destroy_graph_manual(H,path_to_distruption)
#Diman
#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)

#all_graph_paths={}
#compute_paths(H,green_edges)

#all_graph_paths=deepcopy(all_graph_paths_copy)
#print 'Archi verdi :'
#print green_edges
#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'12-destroyed_multy_best')


#recover con multicommodity
nodes_recovered_mcb=[]
edges_recovered_mcb=[]
nodes_recovered_mcb,edges_recovered_mcb=optimal_recovery_multicommodity_best(H,green_edges)
num_rip_mult_best_nodes=len(nodes_recovered_mcb)
num_rip_mult_best_edges=len(edges_recovered_mcb)
#ripristina e disegna
print 'Soluzione algoritmo Multicommodity Best'
print 'Nodi da ripristinare'
print nodes_recovered_mcb
print edges_recovered_mcb
print num_rip_mult_best_nodes
print num_rip_mult_best_edges
recover(H,nodes_recovered_mcb,edges_recovered_mcb)
#set_betwenness_from_dict(H,old_bet_dict)
#my_draw(H,'4-recovered_multi_old_bet')

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'12-recovered_multy_best_new_bet')

#sys.exit(0)
#"""
#------------------------------------------------Recovery based on Shortest path (tom la porta)---------------------
print 'Inizio algoritmo Shortest path recovery'
#Diman Commented
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)
#Diman Commented

#distruggi di nuovo e recover whit multicommodity best
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
#Diman
#nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
destroy_graph_manual(H,path_to_distruption)
#Diman
#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)
#compute_paths(H,green_edges)
#all_graph_paths={}
#compute_paths(H,green_edges)

#all_graph_paths=deepcopy(all_graph_paths_copy)
#print 'Archi verdi :'
#print green_edges

#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'13-destroyed_recovery_shortest_based')

#grapho supply di appoggio per l'algoritmo iterativo basato su shortest
temp_graph_supply_shortest_based=nx.MultiGraph(H)
#recovery shortest_based algorithm
nodes_recovered_sb=[]
edges_recovered_sb=[]
demand_not_satisfied_sb=0.0
start_time_srt=time.time()
#nodes_recovered_sb,edges_recovered_sb=recovery_algorithm_based_on_shortest(temp_graph_supply_shortest_based,distance_metric)
#nodes_recovered_sb,edges_recovered_sb,demand_not_satisfied_sb=recovery_algorithm_based_on_shortest_no_routability(temp_graph_supply_shortest_based,distance_metric)
nodes_recovered_sb,edges_recovered_sb=recovery_algorithm_based_on_shortest_set_opt(temp_graph_supply_shortest_based,shortest_set_algo,distance_metric)

#ripristina e disegna
print 'Soluzione algoritmo Shortest Based Recovery - No commitment'
print 'Nodi da ripristinare'
print nodes_recovered_sb
print 'Archi da ripristinare'
print edges_recovered_sb
#print FINITO
num_rip_shortest_nodes=len(nodes_recovered_sb)
num_rip_truely_shortest_nodes=len(Find_truely_recovered_nodes(H,nodes_recovered_sb))

num_rip_shortest_edges=len(edges_recovered_sb)
num_rip_truely_shortest_edges=len(Find_truely_recovered_edges(H,edges_recovered_sb))

print num_rip_shortest_nodes
print num_rip_shortest_edges
recover(H,nodes_recovered_sb,edges_recovered_sb)
#new_bet_dict=compute_my_betweeness_3(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'13-recovered_shortest_solution_final')
temp_destroyed=get_graph_from_destroyed_graph(H)
#my_draw(temp_destroyed,'13-z_solo_riparato')
demand_satisfied_sb=compute_max_demand_in_the_graph(temp_destroyed)
demand_not_satisfied_sb=total_demand_of_graph-demand_satisfied_sb
time_elapsed_srt=(time.time()-start_time_srt)+end_time_bet
time_elapsed_srt=round(time_elapsed_srt,3)
write_stat_time_simulation(path_to_stat_times,'SRT',filename_graph,int(sys.argv[5]),int(sys.argv[4]),seed_passed,number_of_couple,time_elapsed_srt)

#sys.exit(0)
#----------------------------------------------------------PATHS RANKING BASED RECOVERY (old version betweeness)-------------------------

#-------------------------------------------------------------------
#"""
"""
print 'Inizio algoritmo Paths ranking based recovery'
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)

policy_sort='reverse'
#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)

#compute_paths(H,green_edges)
all_graph_paths={}
compute_paths(H,green_edges)

#all_graph_paths=deepcopy(all_graph_paths_copy)
print 'Archi verdi :'
print green_edges

#new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'14-1_intial_recovery_ranking_based')

#distruggi di nuovo e recover whit multicommodity best
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
destroy_graph_manual(H,path_to_distruption)

print 'compute betweeness_1'
new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'14-destroyed_recovery_ranking_based')
print 'fine betw'

#sys.exit(0)

#recovery shortest_based algorithm
nodes_recovered_rb=[]
edges_recovered_rb=[]
print 'inzio fase ranking recovery'
nodes_recovered_rb,edges_recovered_rb=recovery_algorithm_ranking_path(H,distance_metric,policy_sort)
#ripristina e disegna
#sys.exit('stop')
print 'Soluzione algoritmo Ranking Based Recovery'
print 'Nodi da ripristinare'
print nodes_recovered_rb
print 'Archi da ripristinare'
print edges_recovered_rb
num_rip_ranked_nodes=len(nodes_recovered_rb)
num_rip_ranked_edges=len(edges_recovered_rb)
print num_rip_ranked_nodes
print num_rip_ranked_edges
#print FINITO
my_draw(H,'14-recovered_ranking_solution_final')

#sys.exit(0)
"""

#num_rip_ranked_nodes=48
#num_rip_ranked_edges=64
#-------------------------------------Algoritmo Upper Bound: Riparare tutto cio che e distrutto-----------------------#

#"""----------------------------------------------------------------------
print 'Inizio algoritmo Ripara tutto'
#Diman Commented
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)
#Diman Commented
my_draw(H,'16-repair_all_initial')

#distruggi di nuovo e recover whit multicommodity best
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
#Diman
#nodes_destroyed,nodes_really_dest,edges_destroyed,edges_really_dest=destroy_graph_gray(H,29,-95,100) #per abilene
destroy_graph_manual(H,path_to_distruption)
#Diman

#new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'16-repair_all_destroyed')


#recovery all nodes and links algorithm
nodes_recovered_all=[]
edges_recovered_all=[]
print 'inzio recovery all'
nodes_recovered_all,edges_recovered_all=recovery_all_graph_algorithm(H)
#ripristina e disegna
#sys.exit('stop')
print 'Soluzione algoritmo Recovery All'
print 'Nodi da ripristinare'
print nodes_recovered_all
print 'Archi da ripristinare'
print edges_recovered_all
num_rip_all_nodes=len(nodes_recovered_all)
num_rip_all_edges=len(edges_recovered_all)
print num_rip_all_nodes
print num_rip_all_edges
recover(H,nodes_recovered_all,edges_recovered_all)
#print FINITO
my_draw(H,'16-repair_all_final_solution')

num_rip_ranked_nodes=num_rip_all_nodes
num_rip_ranked_edges=num_rip_all_edges

#-------------------------------------------------------------
#Diman Commented
"""
#Diman Commented
#----------------------------------------------------------PATHS RANKING BASED COMMITMENT-------------------------


print 'Inizio algoritmo Knapsack COMMITMENT'
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)

policy_sort='sort'
#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)

#compute_paths(H,green_edges)
all_graph_paths={}
compute_paths(H,green_edges)

#all_graph_paths=deepcopy(all_graph_paths_copy)
print 'Archi verdi :'
print green_edges

#new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'14-1_intial_recovery_ranking_based_commitment')

#distruggi di nuovo e recover whit multicommodity best
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
destroy_graph_manual(H,path_to_distruption)


my_draw(H,'14-destroyed_recovery_ranking_based_commitment')
#print 'fine betw'

#sys.exit(0)
temp_graph_supply_rank_comm=nx.MultiGraph(H)
#recovery shortest_based algorithm
nodes_recovered_rb_comm=[]
edges_recovered_rb_comm=[]
print 'inzio fase Knapsack Commitment'
demand_not_satisfied_rb_comm=0
#nodes_recovered_rb_comm,edges_recovered_rb_comm,demand_not_satisfied_rb_comm=recovery_algorithm_ranking_path_commitment_3(temp_graph_supply_rank_comm,distance_metric,policy_sort)
#nodes_recovered_rb_comm,edges_recovered_rb_comm,demand_not_satisfied_rb_comm=recovery_algorithm_ranking_path_commitment_3(temp_graph_supply_rank_comm,distance_metric,policy_sort)
nodes_recovered_rb_comm,edges_recovered_rb_comm,demand_not_satisfied_rb_comm=knapsack_commitment(temp_graph_supply_rank_comm,distance_metric,policy_sort)


#ripristina e disegna
#sys.exit('stop')
print 'Soluzione algoritmo Ranking Based Recovery Commitment'
print 'Nodi da ripristinare'
print nodes_recovered_rb_comm
print 'Archi da ripristinare'
print edges_recovered_rb_comm
num_rip_ranked_comm_nodes=len(nodes_recovered_rb_comm)
num_rip_ranked_comm_edges=len(edges_recovered_rb_comm)
print num_rip_ranked_comm_nodes
print num_rip_ranked_comm_edges
#print FINITO
recover(H,nodes_recovered_rb_comm,edges_recovered_rb_comm)
my_draw(H,'14-recovered_ranking_solution_final_commitment')

#sys.exit(0)

#num_rip_ranked_nodes=48
#num_rip_ranked_edges=64

#Diman Uncommented
#"""
#Diman Uncommented
#----------------------------------------------------------PATHS RANKING BASED NO - COMMITMENT-------------------------

"""
print 'Inizio algoritmo Knapsack recovery NO-COMMITMENT'
del H

H=nx.MultiGraph(nx.read_gml(path_to_graph))  #grafo supply
prepare_graph(H)
merge_graphs(H,D)

policy_sort='sort'
#green_edges=get_green_edges(H)
green_edges=deepcopy(copy_of_green_edges)

#compute_paths(H,green_edges)
all_graph_paths={}
compute_paths(H,green_edges)

#all_graph_paths=deepcopy(all_graph_paths_copy)
print 'Archi verdi :'
print green_edges

#new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
#set_betwenness_from_dict(H,new_bet_dict)
my_draw(H,'15-1_intial_recovery_ranking_based_NO_commitment')

#distruggi di nuovo e recover whit multicommodity best
#nodes_destroyed,edges_destroyed=destroy_graph(H,29,-95,10) #per abilene
destroy_graph_manual(H,path_to_distruption)


my_draw(H,'15-destroyed_recovery_ranking_based_commitment')
#print 'fine betw'

#sys.exit(0)

#recovery shortest_based algorithm
nodes_recovered_rb_no_comm=[]
edges_recovered_rb_no_comm=[]
print 'inzio fase knapsack recovery NO - commitment'
#nodes_recovered_rb_no_comm,edges_recovered_rb_no_comm=recovery_algorithm_ranking_path_no_commitment(H,distance_metric,policy_sort)
nodes_recovered_rb_no_comm,edges_recovered_rb_no_comm=knapsack_no_commitment(H,distance_metric,policy_sort)

#ripristina e disegna
#sys.exit('stop')
print 'Soluzione algoritmo Knapsack NO-Commitment'
print 'Nodi da ripristinare'
print nodes_recovered_rb_no_comm
print 'Archi da ripristinare'
print edges_recovered_rb_no_comm
num_rip_ranked_no_comm_nodes=len(nodes_recovered_rb_no_comm)
num_rip_ranked_no_comm_edges=len(edges_recovered_rb_no_comm)
print num_rip_ranked_no_comm_nodes
print num_rip_ranked_no_comm_edges
#print FINITO
my_draw(H,'15-recovered_ranking_solution_final_NO_commitment')

#sys.exit(0)

#num_rip_ranked_nodes=48
#num_rip_ranked_edges=64


#"""

#sys.exit(0)
# SIMULAZIONE FINITA --->SCRIVERE STATISTICHE SU FILE (NODI RIPARATI E ARCHI RIPARATI PER OGNI ALGORITMO)


filename_stat='stat_simulations_'+filename_graph+"_Prob_"+str(prob_edge)+"_Alpha_"+str(alfa)+".txt"

#numero della simulazione corrente e scrivo statistiche
number_sim=get_num_simulation(path_to_file_simulation)

#"""
#Commentato per statistiche su alcuni algo
write_stat_num_reparation(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          num_rip_isp_nodes,num_rip_isp_edges,num_rip_truely_isp_nodes,num_rip_truely_isp_edges,    #ISP
                          num_rip_optimal_nodes,num_rip_optimal_edges,#OPTIMAL
                          num_rip_mult_nodes,num_rip_mult_edges,num_rip_truely_mult_nodes,num_rip_truely_mult_edges,       #Multicommodity generale
                          num_rip_mult_worst_nodes,num_rip_mult_worst_edges, #Multicommodity worst
                          num_rip_mult_best_nodes,num_rip_mult_best_edges,    #Multicommodity best
                          num_rip_shortest_nodes,num_rip_shortest_edges,num_rip_truely_shortest_nodes, num_rip_truely_shortest_edges,    #Shortest Based
                          num_rip_all_nodes,num_rip_all_edges,          #Ranked based
                          num_rip_all_nodes,num_rip_all_edges,                #All repairs algortim
                          number_sim,                                         #Numero della simulazione
                          flag_solution_MCG,                                  #True se ho dovuto usare il MCG per terminare l'algoritmo
                          total_demand_of_graph,                                #Domanda totale sul grafo
                          demand_not_satisfied_sb,                             #Domanda non soddisfatta da shortest based
                          num_rip_all_nodes,num_rip_all_edges,
                          num_rip_all_nodes,num_rip_all_edges,
                          0,
                          flow_c_value,                                        #valore di flusso fixed assegnato per questa run
                          number_of_couple,                                     #numero di coppie scelto per rappresentare la domanda
                          var_distruption)                                      #varianza della distruzione


#"""
"""
write_stat_num_reparation(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          num_rip_isp_nodes,num_rip_isp_edges,num_rip_truely_isp_nodes,num_rip_truely_isp_edges,    #ISP
                          num_rip_optimal_nodes,num_rip_optimal_edges,#OPTIMAL
                          num_rip_all_nodes,num_rip_all_edges,num_rip_truely_mult_nodes,num_rip_truely_mult_edges,       #Multicommodity generale
                          num_rip_all_nodes,num_rip_all_edges, #Multicommodity worst
                          num_rip_all_nodes,num_rip_all_edges,    #Multicommodity best
                          num_rip_shortest_nodes,num_rip_shortest_edges,num_rip_truely_shortest_nodes, num_rip_truely_shortest_edges,    #Shortest Based
                          num_rip_all_nodes,num_rip_all_edges,          #Ranked based
                          num_rip_all_nodes,num_rip_all_edges,                #All repairs algortim
                          number_sim,                                         #Numero della simulazione
                          flag_solution_MCG,                                  #True se ho dovuto usare il MCG per terminare l'algoritmo
                          total_demand_of_graph,                                #Domanda totale sul grafo
                          demand_not_satisfied_sb,                                                    #Domanda non soddisfatta da shortest based
                          num_rip_all_nodes,num_rip_all_edges,              #knap comm
                          num_rip_all_nodes,num_rip_all_edges,              #knap no_comm
                          1,                                                #demand not satisfied by knap comm
                          flow_c_value,                                        #valore di flusso fixed assegnato per questa run
                          number_of_couple,                                     #numero di coppie scelto per rappresentare la domanda
                          var_distruption)

#"""


#winsound.Beep(500,3000)
