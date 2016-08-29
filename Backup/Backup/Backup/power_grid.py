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


