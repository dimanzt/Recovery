
import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
from scipy import stats
from my_lib import *
from my_flows_lib import *
from my_lib_optimal_recovery import *
from test_random_lib import *

#load a particular graph from file
H=nx.MultiGraph(nx.read_gml('network topologies/Abilene.gml'))  #grafo supply
prepare_graph(H)
seed= random.randint(0,sys.maxint)
seed=1
print 'seed: %d'%(seed)
random.seed(seed)

green_edges=[]
path_to_demand,green_edges=generate_demand(H,0.05,'DemandGenerated')

#green_edges,sequence1=subset(H)

print 'green selezionati'
print green_edges

#print 'sequence 1'
#print sequence1

random.shuffle(green_edges)
print 'shuffle'
print green_edges

destroy_graph(H,29,-95,10) #per abilene


H=nx.MultiGraph(nx.read_gml('network topologies/random_graphs_generated/random_graph_20_nodes_34_edges.gml'))

prepare_graph(H)

my_draw(H,'provagrafo')