__author__ = 'Utente'

var_locale={}

all_graph_paths={}

from my_lib import *


def prendi_valore_globale():

    global var_locale
    for x in range(0,9,1):
        var_locale.update({x:[]})
        for j in range(1,5,1):
            var_locale[x].append(j)

    return var_locale


def modifica_var_globale():
    global var_locale

    print 'pre modifica'
    print var_locale

    var_locale[4].reverse()
    var_locale.pop(1)

    return var_locale

def calcola_paths(H):

    global all_graph_paths

    for i in H.nodes():
        for j in H.nodes():
            edge=(i,j)
            edge_reverse=(j,i)
            graph_dict=convert_graph_to_dict(H)
            paths=find_all_paths(graph_dict,i,j,[])
            print 'path tra %d%d'%(i,j)
            print paths
            if not all_graph_paths.has_key(edge) and not all_graph_paths.has_key(edge_reverse):
                all_graph_paths.update({edge:paths})

    print all_graph_paths