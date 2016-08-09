__author__ = 'Utente'

import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
from scipy import stats
from my_lib import *
from my_flows_lib import *
from my_lib_optimal_recovery import *





def subset(H):
    selected=[]
    sequence=[]
    p=0.15
    for source in H.nodes():
        for target in H.nodes():
            id_source=H.node[source]['id']
            id_target=H.node[target]['id']
            value_rand=random.random()
            sequence.append(value_rand)
            if value_rand <= p:
                edge=(id_source,id_target)
                selected.append(edge)

    return selected,sequence


