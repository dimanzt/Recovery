__author__ = 'Utente'

from my_lib import *
import os

filename_graph= 'KDL_Random_Capacity'
filename_graph= 'Abilene'
filename_graph='1866_2464_Random_Capacity'
path_to_graph= 'network topologies/'
path_to_folder_couple='distance_between_couples/'

print 'here'
if not os.path.exists(path_to_folder_couple):
    os.makedirs(path_to_folder_couple)

if sys.argv[1]!=None:
    filename_graph=str(sys.argv[1])

path_to_graph=path_to_graph+filename_graph+'.gml'

H=nx.MultiGraph(nx.read_gml(path_to_graph))

check_if_have_multiple_edges(H)

compute_and_save_distance_couples(H,path_to_folder_couple,filename_graph)


#print mylist