#variabile globale che per ogni coppia di nodi (verdi) salva la lista dei path tra di essi
all_graph_paths={}

#variabile globale che per ogni coppia di nodi (verdi) salva la lista dei path feasible
all_paths_feasible={}

all_graph_paths_copy={}

shortest_paths_for_bet={}
betwenness_dict={}

shortest_set_algo={}

#dizionario globale delle prenotazioni degli shortest
reservation_dict={}

path_counter=0

user_name='Seamus'

import networkx as nx
import pydot
import numpy as np
import matplotlib.pyplot as plt
from my_lib_optimal_recovery import *
from scipy.integrate import dblquad
from scipy.stats import multivariate_normal
from matplotlib.mlab import bivariate_normal
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from copy import deepcopy
import random
from heapq import heappush, heappop
from itertools import count

from my_flows_lib import *
from my_lib_check_routability import *
from operator import itemgetter
from find_max_value_of_split import *

import os
import shutil
import re
import math
import collections
import time



def my_draw(H,file_name):
    #print 'DRAWING************************'
    #imposto le coordinate del nodo per il formato .dot "x,y!"
    for i in H.nodes():
        #print i
        H.node[i]['pos'] = '"%d,%d!"'%(H.node[i]['Longitude'], H.node[i]['Latitude'])

    H.graph['graph']={'size':'"20,20!"','ratio':'expand','overlap':'false'}
    graphDot=nx.to_pydot(H)
    #graphDot.__setattr__('size',"1000,1000!")
    #graphDot.__setattr__('ratio',"expand")
    #dict={'size':"1000,1000!"}
    #graphDot.set_graph_defaults(dict)

    #print graphDot.__get_attribute__('size')
    #print graphDot.__get_attribute__('ratio')


    #colora e disegna i nodi
    for node in graphDot.get_nodes():
        #print 'id_nodo:' + str (i.get_id())
        betweeness=str(get_attrDot(node,'betweeness'))
        id=str(get_attrDot(node,'id'))
        label=str(id)+'/'+betweeness
        node.set_label( label )
        node.set_shape('circle')

        #pos_string='\''+ get_attrDot(node,'Longitude')+','+get_attrDot(node,'Latitude')+'!\''
        #print 'coordinate: ' + pos_string
        #node.set('pos',pos_string)

        type_node = str(get_attrDot(node,'type'))
        status_node=str(get_attrDot(node,'status'))
        color_node=str(get_attrDot(node,'color'))
        if color_node == '""' or color_node=='None':
            node.set_color('""')
            node.set_style('""')
            node.set_shape('circle')

        else:
            node.set_style('filled')
        if status_node=='on' or status_node=='repaired':   #nodo attivo o ripristinato
            if color_node =='green':
                node.set_color('green')
            if color_node=='blue':
                node.set_color('blue')
        if status_node == 'destroyed':
            if color_node =='green':
                node.set_color('green')
                node.set_style('')
            elif color_node == 'red':
                node.set_color('red')

    #colora e disegna archi

    for elem in graphDot.get_edges():
        value_demand=str(get_attrDot(elem,'demand'))
        value_capacity=str(get_attrDot(elem,'capacity'))
        if str(value_demand) != 'None':
            elem.set_color('green')  #    add_edge(pydot.Edge(u ,v, color='green', label=demand))
            elem.set_label(value_demand)
            elem.set_fontcolor('green')
        elif str(value_capacity) !='None':
            #elem.set_color('green')  #    add_edge(pydot.Edge(u ,v, color='green', label=demand))
            elem.set_label(value_capacity)
            #elem.set_fontcolor('green')


    #for node in graphDot.get_nodes():
     #   print str(get_attrDot(node,'pos'))
    path='../../../image_graph_dot/DotFile/' + file_name    

    #path='c:\\Users\\'+user_name+'\\Documents\LabWork\\image_graph_dot\\DotFile' + file_name
    #print path
    graphDot.write(path+'Dot.dot')
    graphDot.write_png(file_name +'.png')


def set_attrDot(elem,attr,value):
    elem.__set_attribute__(attr,value)

def get_attrDot(elem, attr):
    value=elem.__get_attribute__(attr)

    return value

def add_attribute_Nodes(H):
    
    for i in H.nodes():
    
        #aggiunta attributi mancanti
        if 'type' not in H.node[i]:
            H.node[i]['type']='normal'
           # print 'aggiunto type a ' + str(H.node[i]['id'])
        if 'status' not in H.node[i]:
            H.node[i]['status']='on'
           # print 'aggiunto on' + str(H.node[i]['id'])
        if 'color' not in H.node[i]:
            H.node[i]['color']='""'
        if 'betweeness' not in H.node[i]:
            H.node[i]['betweeness']=0
        if 'weight' not in H.node[i]:
            H.node[i]['weight']=0
        if 'Longitude' not in H.node[i]:
            H.node[i]['Longitude']=random.randint(0,300)
        if 'Latitde' not in H.node[i]:
            H.node[i]['Latitude']=random.randint(0,300)
        if 'true_status' not in H.node[i]:
            H.node[i]['true_status']='on'

def add_attribute_Edges(H):

    #for i in H.nodes():
     #   for j in H.nodes():
     #       id_source = H.node[i]['id']
      #      id_target = H.node[j]['id']
      #      if( H.has_edge(id_source,id_target)):
      #          if 'key' not in H.edge[id_source][id_target]:
       #             H.add_edge(id_source,id_target, key='0')

    #for i in H.edges(data=True,keys=True):
     #   print i

    

    for i in H.nodes():
        for j in H.nodes():
            id_source = H.node[i]['id']
            id_target = H.node[j]['id']
            #if (H.node[i]['type']=='green' and H.node[j]['type']=='green'):
            
            if( H.has_edge(id_source,id_target)):
                    #print 'Here'
                    #sys.exit(0)
                    #print str(id_source)+str(id_target)
                    keydict =H[id_source][id_target]
                    #print len(H[id_source][id_target])
                    number_edges=H.number_of_edges(id_source,id_target)
                    if number_edges ==1 and len(keydict)>1:
                        #print 'foopu'
                        if 'type' not in H.edge[id_source][id_target]:
                            H.add_edge(id_source,id_target, type='normal')
                        #print 'prestatus'
                        if 'status' not in H.edge[id_source][id_target]:
                            H.add_edge(id_source,id_target, status='on')
                        #print 'precolor'
                        if 'color' not in H.edge[id_source][id_target]:
                            H.add_edge(id_source,id_target, color='black')

                        if 'weight' not in H.edge[id_source][id_target]:
                            cap=H[id_source][id_target]['capacity']
                            H.add_edge(id_source,id_target, weight=0.1/cap)
                        if 'true_status' not in H.edge[id_source][id_target]:
                            H.add_edge(id_source,id_target, true_status='on')
                    else:
                        #print 'barpa'
                        key=len(keydict)
                        for k in keydict:
                            #print len(keydict)
                            if 'type' not in H.edge[id_source][id_target][k]:
                                H.add_edge(id_source,id_target,key=k, type='normal')
                            #print 'prestatus'
                            if 'status' not in H.edge[id_source][id_target][k]:
                                H.add_edge(id_source,id_target,key=k, status='on')
                            #print 'precolor'
                            if 'color' not in H.edge[id_source][id_target][k]:
                                H.add_edge(id_source,id_target,key=k, color='black')

                            if 'weight' not in H.edge[id_source][id_target][k]:
                                cap=H[id_source][id_target][k]['capacity']
                                H.add_edge(id_source,id_target,key=k, weight=0.1/cap)
                            if 'true_status' not in H.edge[id_source][id_target][k]:
                                H.add_edge(id_source,id_target,key=k, true_status='on')
                            #print 'ripeti'
                            #print keydict
                            #print len(keydict)

def merge_graphs(H,D):

    green_nodes = {}
    green_nodes = get_green_nodes(D)
    #print 'nodi verdi presi:' + str(green_nodes)

    #aggiorna attributi ai nodi green
    for i in H.nodes():
        for j in green_nodes:
            id_elem = H.node[i]['id']
            #print 'confronto ' +  str(id_elem) + str(j)
            if id_elem == j:
                H.node[i]['type'] = 'green'
                H.node[i]['color'] = 'green'
                #print 'modificato ' + str(j)

    #for i in H.nodes(data=True):
       # print i
        #if (str(H.node[i]['type']) == 'green'):
         #   print 'arco verde in H: ' + str(H.node[i]['id'])

    #for i in D.edges(data=True):
     #   print i

    #aggiunge gli archi green
    for i in H.nodes():
        if H.node[i]['type']=='green':
            id_source = H.node[i]['id']
            for j in H.nodes():
                if H.node[j]['type'] == 'green':
                    id_target = H.node[j]['id']
                    if D.has_edge(id_source,id_target):

                        demand = D[id_source][id_target][0]['demand']
                        if H.has_edge(id_source,id_target):
                            #print 'aggiunto arco verde:'+str(id_source)+str(id_target)
                            #H.add_edge(id_source, id_target, type='green', demand=demand)
                            number_edges=H.number_of_edges(id_source,id_target)
                            keydict =H[id_source][id_target]
                            count=0
                            #print 'Esiste gia arco: ' + str(id_source) + str(id_target)
                            #print H[id_source][id_target]

                            if number_edges==1 and (len(keydict)>1):
                                type_edge= H[id_source][id_target]['type']
                                #print str(type_edge)
                                if(str(type_edge) =='green'):
                                    count+=1
                            else:
                                key=len(keydict)
                                for k in keydict:
                                    #print k
                                    type_edge= H[id_source][id_target][k]['type']
                                    if(str(type_edge) =='green'):
                                        count+=1

                            if(count==0):
                                #aggiungo arco verde per la prima volta
                                #print 'aggiunto nuovo arco verde prima volta:'+str(id_source)+str(id_target)
                                #H.remove_edge(id_source,id_target)
                                #H.add_edge(id_source,id_target,key='0',attr_dict=keydict)
                                #print H[id_source][id_target]
                                #keydic_old=keydict
                                #keydic_new={'type':'green', 'demand':demand,'color':'green','style':'bold'}
                                #list=[(id_source,id_target,0,keydict),(id_source,id_target,1,keydic_new)]
                                #print list
                                root_edge=(id_source,id_target)
                                H.add_edge(id_source,id_target,type='green', demand=demand,color='green',style='bold',root_edge=root_edge,splitted_edge=False)
                                #H.add_edges_from([(id_source,id_target,keydic_old),(id_source,id_target,keydic_new)])
                                #H.add_edge(id_source,id_target,key=0)
                                # H.add_edge(id_source,id_target,key=1)
                                #print H[id_source][id_target]

                        else:
                            #print 'aggiunto nuovo arco verde:'+str(id_source)+str(id_target)
                            root_edge=(id_source,id_target)
                            H.add_edge(id_source, id_target, type='green', demand=demand, color='green',style='bold',root_edge=root_edge,splitted_edge=False)

def prepare_graph(H):

    # aggiungi attributi ai nodi e archi
    add_attribute_Nodes(H)
    add_attribute_Edges(H)
    #aggiungi grafo demand al grafo supply
    #merge_graphs(H,D)

    #for i in H.edges(data=True):
     #   print i

def get_green_nodes(H):

    list=[]

    for i in H.nodes():
        #if str(H.node[i]['type']) == "green":
        #   #print 'id' + str(  H.node[i]['id'] )
        list.append(H.node[i]['id'])


    #print 'lista ' + str(list)
    return list

def destroy_graph_manual(H,file_path):

    file=open(file_path,'r')
    flag_alt=0
    line=file.readline()
    while(line!=''):
        #print line
        if flag_alt==0:
            if line!='stop\n':
                id_node=int(line)
                #print id_node
                H.node[id_node]['status']='destroyed'
                H.node[id_node]['color']='red'
            else:
                flag_alt=1
        else:
            #if line !='stop\n':
                new_line = re.sub('[()]', '', line)
                #print 'ECCOMI:'
                #print new_line
                index_separator=new_line.index(',')
                id_source=int(new_line[:index_separator])
                id_target=int(new_line[index_separator+1:])
                #print id_source
                #print id_target
                keydict=H[id_source][id_target]
                for k in keydict:
                    if H[id_source][id_target][k]['type']=='normal':
                        H.add_edge(id_source,id_target,key=k, status='destroyed',labelfont='red',color='red',style='dashed')


        line=file.readline()


def destroy_graph(H,mu_x,mu_y,sigma):

    nodes_dest=destroy_nodes(H,mu_x,mu_y,sigma)
    edges_dest=destroy_edges(H,mu_x,mu_y,sigma)

    return nodes_dest,edges_dest

def destroy_graph_gray(H,mu_x,mu_y,sigma):

    nodes_dest,nodes_really_dest=destroy_nodes_gray(H,mu_x,mu_y,sigma)
    edges_dest,edges_really_dest=destroy_edges_gray(H,mu_x,mu_y,sigma)

    return nodes_dest,nodes_really_dest,edges_dest,edges_really_dest

def destroy_nodes(H,mu_x,mu_y,sigma):

    destroyed_nodes=[]
    #H.node[1]['status']='destroyed'
    #H.node[1]['color']='red'
    for i in H.nodes():
        x=H.node[i]['Latitude']
        y=H.node[i]['Longitude']
        id_node=H.node[i]['id']
        #print str(x)+str(y)
        pdf=bivariate_normal(x,y,sigma,sigma,mux=mu_x,muy=mu_y,sigmaxy=0)
        #print 'pdf calcolata: ' + str(pdf)
        prob=get_prob(pdf,x,y,sigma)
        #print str(prob)

        if flip_coin(prob):
            H.node[i]['status']='destroyed'
            H.node[i]['color']='red'
            if id_node not in destroyed_nodes:
                destroyed_nodes.append(id_node)
            #print 'nodo distrutto:' +str(i)

    return destroyed_nodes

def destroy_nodes_gray(H,mu_x,mu_y,sigma):

    destroyed_nodes=[]
    nodes_really_dest=[]
    #H.node[1]['status']='destroyed'
    #H.node[1]['color']='red'
    for i in H.nodes():
        if H.node[i]['color'] == 'green':
            continue
        x=H.node[i]['Latitude']
        y=H.node[i]['Longitude']
        id_node=H.node[i]['id']
        H.node[i]['status']='destroyed'
        H.node[i]['color']='gray'
        
        #print str(x)+str(y)
        pdf=bivariate_normal(x,y,sigma,sigma,mux=mu_x,muy=mu_y,sigmaxy=0)
        #print 'pdf calcolata: ' + str(pdf)
        prob=get_prob(pdf,x,y,sigma)
        #print str(prob)
        
        if flip_coin(prob):
            H.node[i]['true_status']='destroyed'
            if id_node not in nodes_really_dest:
                nodes_really_dest.append(id_node)			
        else:
            H.node[i]['true_status']='on'

		
        if id_node not in destroyed_nodes:
            destroyed_nodes.append(id_node)

            #print 'nodo distrutto:' +str(i)
    return destroyed_nodes,nodes_really_dest


def destroy_edges(H,mu_x,mu_y,sigma):

    destroyed_edges=[]
    for i in H.nodes():
        for j in H.nodes():
            id_source = H.node[i]['id']
            id_target = H.node[j]['id']
            if H.has_edge(id_source,id_target):
                x_1=H.node[i]['Latitude']
                x_2=H.node[j]['Latitude']
                y_1=H.node[i]['Longitude']
                y_2=H.node[j]['Longitude']
                #punto medio
                x_m=(x_1+x_2)/2
                y_m=(y_1+y_2)/2

                pdf_arc=bivariate_normal(x_m,y_m,sigma,sigma,mux=mu_x,muy=mu_y,sigmaxy=0)
                #print 'pdf calcolata: ' + str(pdf)
                prob_arc=get_prob(pdf_arc,x_m,y_m,sigma)
                #print 'prob_arco: ' + str(prob_arc)
                if(flip_coin(prob_arc)):
                    keydict =H[id_source][id_target]
                    #print str(keydict)
                    key=len(keydict)
                    for k in keydict:
                        if 'green'!= H.edge[id_source][id_target][k]['type']:
                            H.add_edge(id_source,id_target,key=k, status='destroyed',labelfont='red',color='red',style='dashed')
                            edge=(id_source,id_target)
                            edge_reverse=(id_target,id_source)
                            if edge not in destroyed_edges and edge_reverse not in destroyed_edges:
                                destroyed_edges.append(edge)
                            #print 'arco distrutto: '+str(id_source)+str(id_target)

    return destroyed_edges

def destroy_edges_gray(H,mu_x,mu_y,sigma):

    destroyed_edges=[]
    edges_dest_really_dest=[]
    for i in H.nodes():
        for j in H.nodes():
            id_source = H.node[i]['id']
            id_target = H.node[j]['id']
            if H.has_edge(id_source,id_target):
                x_1=H.node[i]['Latitude']
                x_2=H.node[j]['Latitude']
                y_1=H.node[i]['Longitude']
                y_2=H.node[j]['Longitude']
                #punto medio
                x_m=(x_1+x_2)/2
                y_m=(y_1+y_2)/2

                pdf_arc=bivariate_normal(x_m,y_m,sigma,sigma,mux=mu_x,muy=mu_y,sigmaxy=0)
                #print 'pdf calcolata: ' + str(pdf)
                prob_arc=get_prob(pdf_arc,x_m,y_m,sigma)
                #print 'prob_arco: ' + str(prob_arc)

                keydict =H[id_source][id_target]
                #print str(keydict)
                key=len(keydict)
                for k in keydict:
                    if 'normal' == H.edge[id_source][id_target][k]['type']:
                        edge=(id_source,id_target)		
                        edge_reverse=(id_target,id_source)
						
                        if(flip_coin(prob_arc)):
                            H.add_edge(id_source,id_target,key=k, status='destroyed',true_status="destroyed",labelfont='gray',color='gray',style='dashed')
                            if edge not in edges_dest_really_dest and edge_reverse not in edges_dest_really_dest:
                                edges_dest_really_dest.append(edge)							
                        else:
                            H.add_edge(id_source,id_target,key=k, status='destroyed',true_status="on",labelfont='gray',color='gray',style='dashed')

                        #edge=(id_source,id_target)
                        #edge_reverse=(id_target,id_source)
                        if edge not in destroyed_edges and edge_reverse not in destroyed_edges:
                            destroyed_edges.append(edge)


    return destroyed_edges,edges_dest_really_dest

def my_multivariate_pdf(vector, mean, cov):
    #vecotr= il punto x,y ; mean punto di epicentro, cov=matrice 2x2 delle covarienze
    #restituisce la pdf del punto x,y
    quadratic_form = np.dot(np.dot(vector-mean,np.linalg.inv(cov)),np.transpose(vector-mean))
    return np.exp(-.5 * quadratic_form)/ (2*np.pi * np.linalg.det(cov))

def test_multivariate(x,y):
    sigma=20
    #print str(x)+str(y)
    pdf=bivariate_normal(x,y,sigma,sigma,mux=0,muy=0,sigmaxy=0)
    #print 'pdf calcolata: ' + str(pdf)
    get_prob(pdf,x,y,sigma)

def compute_cov(H):

    x=[];
    y=[];

    for i in H.nodes():
        x_coord=H.node[i]['Latitude']
        y_coord=H.node[i]['Longitude']
        x.append(x_coord)
        y.append(y_coord)

    print x
    print y
    cov=np.cov(x,y)
    print cov

    return cov

def compute_mean(H):
    x_sum=0;
    y_sum=0;

    for i in H.nodes():
        x_coord=H.node[i]['Latitude']
        y_coord=H.node[i]['Longitude']
        x_sum=x_sum + x_coord
        y_sum= y_sum + y_coord

    print str(x_sum)
    print str(y_sum)
    mean_x=x_sum/len(H.nodes())
    mean_y=y_sum/len(H.nodes())
    mean=np.array([mean_x,mean_y])
    print str(mean_x)
    print str(mean_y)
    print mean

    return mean

def get_prob(pdf,x,y,sigma):

    pi=np.pi
    scale=2*pi*(sigma**2)
    #ans, err = dblquad(integrand, low_x, high_x,lambda x: low_y,lambda x: high_y)
    prob= pdf*(scale)

    #print 'prob: ' + str(prob)
    return prob


def disegnaPDF():

    points=np.arange(-5,5,0.1)
    #print points
    result=np.array([])
    for i in range(0,len(points),1):
        pdf=bivariate_normal(points[i],0,sigmax=20.0,sigmay=20.0,mux=0,muy=0,sigmaxy=0)
        result= np.append([result],pdf)

    #print result
    plt.plot(points,result)
    plt.show()


def disegna_3d():

    x = np.arange(-200.0,200.0,1)
    y = np.arange(-200.0,200.0,1)
    X,Y = np.meshgrid(x, y) # grid of point
    Z = z_func(X, Y) # evaluation of the function on the grid

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap=cm.RdBu,linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
    #print bivariate_normal(0,0,sigmax=20,sigmay=20,mux=0,muy=0,sigmaxy=0)

def z_func(x,y):
    sigma=10
    return (bivariate_normal(x,y,sigma,sigma,mux=0,muy=0,sigmaxy=0))



def compute_all_max_flows(H,green_couples):

    max_flows_dict={}
    nodes=[]
    edges=[]
    for i in H.nodes():
        nodes.append(Vertex(H.node[i]['id']))

    #for node in nodes:
            #print node.name

    for couple in green_couples:

        clean_edges(nodes)
        del edges
        edges=get_Edges_residual(H)

        #print edges
        buildGraph(nodes,edges)

        id_source=couple[0]
        id_target=couple[1]
        source_index=int(get_index_vertex(nodes,id_source))
        target_index=int(get_index_vertex(nodes,id_target))
        #print str(nodes[source_index].name) + '' + str(nodes[target_index].name)
        max_flow=maxFlow(nodes[source_index],nodes[target_index])
        edge=(id_source,id_target)
        if edge not in max_flows_dict:
            max_flows_dict.update({edge:max_flow})


    clean_edges(nodes)
    del edges
    del nodes
    return max_flows_dict



def generate_demand(H,prob,filename,alfa,seed,path_to_stats,distance_metric):

    residualGraph=nx.MultiGraph(H)
    green_edges_random=np.array([])
    green_edges_random=random_edges(H,prob)
    print green_edges_random
    green_selected=[]
    graph_dict={}
    global all_graph_paths
    global all_paths_feasible
    random.shuffle(green_edges_random)  #mescola casualmente gli elementi
    print green_edges_random
    nodes_R=[]
    edges_R=[]
    for i in H.nodes():
        nodes_R.append(Vertex(H.node[i]['id']))
    j=0

    path_to_file_flag_stat=path_to_stats+filename+'_Flags_statistics.txt'
    if not os.path.exists(path_to_file_flag_stat):
        file_flags=open(path_to_file_flag_stat,'w')
        file_flags.close()

    file_flags=open(path_to_file_flag_stat,'a')
    file_flags.write('\n\n\nTopologia: '+filename+'\nSeed: '+str(seed)+'\nAlfa: '+str(alfa)+'\n')
    file_flags.write('Coppie di nodi selezionati con probabilita = '+str(prob)+' : \n')
    string=''
    for edge in green_edges_random:
        string=string+str(edge)+' - '
    file_flags.write(string+'\n')

    #Calcola inizialmente il maxFlow sul grafo iniziale per ogni coppia di nodi verdi
    max_flows_dict={}
    max_flows_dict=compute_all_max_flows(H, green_edges_random)
    #print max_flows_dict

    file_flags.write('Max flows su grafo supply per ogni coppia: \n')
    string=''
    for key,value in max_flows_dict.items():
        string=string+str(key)+': '+str(value)+' - '

    file_flags.write(string+'\n')

    #print 'Max flows Calcolati:'
    #print max_flows_dict
    for couple in green_edges_random:
        clean_edges(nodes_R)
        del edges_R
        edges_R=get_Edges_residual(residualGraph)
        buildGraph(nodes_R,edges_R)
        id_source=couple[0]
        id_target=couple[1]
        source_index=int(get_index_vertex(nodes_R,id_source))
        target_index=int(get_index_vertex(nodes_R,id_target))

        print 'iterazione %d / %d --> %d-%d'%(j,len(green_edges_random)-1,source_index,target_index)
        max_flow_residual=maxFlow(nodes_R[source_index],nodes_R[target_index])
        print 'max flow residual: ' + str(max_flow_residual)
        if max_flow_residual != 0:
            del graph_dict
            #graph_dict=convert_graph_to_dict(residualGraph)
            #passo H perche devo calcolare tutti i path sul grafo originale
            graph_dict=convert_graph_to_dict(H)
            #print 'pre compute paths'
            edge=(id_source,id_target)
            edge_reverse=(id_target,id_source)
            #del paths
            global path_counter
            path_counter=0
            paths=find_all_paths(graph_dict,id_source,id_target,[])
            print
            #print 'paths calcolati tra %d-%d: '%(id_source,id_target)
            #print paths
            if not all_graph_paths.has_key(edge) and not all_graph_paths.has_key(edge_reverse):
                all_graph_paths.update({edge:paths})

            if(len(paths)>0 and max_flow_residual>0):

                #domanda casuale da asseganre
                if(alfa==0.0):
                    demand= random.randint(0,max_flow_residual)

                #domanda da assegnare in proporzione ad un valore alfa
                else:
                    if edge not in max_flows_dict:
                        print 'Errore in generate_demand: coppia senza maxflow'
                        sys.exit('Errore coppia senza maxflow')
                    else:
                        max_flow_edge=max_flows_dict[edge]
                        max_demand=int(math.ceil(alfa*max_flow_edge))
                        if max_demand > max_flow_residual:
                            #FLAG 1: Incapace di assegnare alfa*maxFlow, posso allocare al piu maxFlow_residuo
                            demand=max_flow_residual
                            file_flags.write('----------FLAG 1 per la coppia : ('+str(id_source)+','+str(id_target)+') : alfa*max_flow= '+str(max_demand)+' > '+str(max_flow_residual) + ' =max_flow_residuo -------\n')
                            string=''
                            for green in green_selected:
                                string=string+str(green)+' - '
                            file_flags.write('Domanda assegnata fino ad ora:\n'+string+'\n')
                        else:
                            demand=max_demand

                #print 'demand da assegnare: %d '%(demand)
                support_graph=nx.MultiGraph(residualGraph)
                temp_paths=deepcopy(paths)
                paths_feasible=feasible_path(support_graph,temp_paths)
                #print 'cammini disponibili'
                #print paths_feasible
                if not all_paths_feasible.has_key(edge) and not all_paths_feasible.has_key(edge_reverse):
                    all_paths_feasible.update({edge:paths_feasible})

                temp_feasible=deepcopy(paths_feasible)
                if (alfa==0.0):
                    demand_assigned=assign_demand(residualGraph,demand,temp_feasible)
                else:
                    flag_update_all_paths=False
                    demand_assigned=assign_demand_shortest(residualGraph,demand,id_source,id_target,file_flags,distance_metric,flag_update_all_paths,temp_feasible)
                """
                if demand_assigned!=0:
                    print 'NON E POSSIBILE DOMANDA ASSEGNATA MALE'
                """
                if(demand_assigned>0):
                    print 'domanda assegnata: %d/%d'%(demand_assigned,demand)
                    new_green_edge=(id_source,id_target,demand_assigned)
                    green_selected.append(new_green_edge)

                    my_draw(residualGraph,'residual'+str(j))
        j=j+1

    #print 'archi da aggiungere verdi:'
    #print green_selected
    file_gml=produce_gml_graph(green_selected,filename)

    file_flags.write('Domanda Finale assegnata al grafo: \n')
    string=''
    for edge in green_selected:
        string=string+ str(edge)+ ' - '
    file_flags.write(string+'\n')
    file_flags.close()
    return file_gml,green_selected




#OLD VERSION, USARE OTTIMIZZATA
def generate_demand_of_fixed_value_from_list_of_coupl(H,list_of_couple,flow_c_value,prob,filename,alfa,seed,path_to_stats,distance_metric):

    residualGraph=nx.MultiGraph(H)
    green_edges_random=np.array([])
    green_edges_random=list_of_couple
    print green_edges_random
    green_selected=[]
    graph_dict={}
    global all_graph_paths
    global all_paths_feasible
    #random.shuffle(green_edges_random)  #mescola casualmente gli elementi
    print green_edges_random
    nodes_R=[]
    edges_R=[]
    for i in H.nodes():
        nodes_R.append(Vertex(H.node[i]['id']))
    j=0

    path_to_file_flag_stat=path_to_stats+filename+'_Flags_statistics.txt'
    if not os.path.exists(path_to_file_flag_stat):
        file_flags=open(path_to_file_flag_stat,'w')
        file_flags.close()

    file_flags=open(path_to_file_flag_stat,'a')
    file_flags.write('\n\n\nTopologia: '+filename+'\nSeed: '+str(seed)+'\nAlfa: '+str(alfa)+'\n')
    file_flags.write('Coppie di nodi selezionati con probabilita = '+str(prob)+' : \n')
    string=''
    for edge in green_edges_random:
        string=string+str(edge)+' - '
    file_flags.write(string+'\n')

    #Calcola inizialmente il maxFlow sul grafo iniziale per ogni coppia di nodi verdi
    max_flows_dict={}
    max_flows_dict=compute_all_max_flows(H, green_edges_random)
    #print max_flows_dict

    file_flags.write('Max flows su grafo supply per ogni coppia: \n')
    string=''
    for key,value in max_flows_dict.items():
        string=string+str(key)+': '+str(value)+' - '

    file_flags.write(string+'\n')

    #print 'Max flows Calcolati:'
    #print max_flows_dict
    for couple in green_edges_random:
        clean_edges(nodes_R)
        del edges_R
        edges_R=get_Edges_residual(residualGraph)
        buildGraph(nodes_R,edges_R)
        id_source=couple[0]
        id_target=couple[1]
        source_index=int(get_index_vertex(nodes_R,id_source))
        target_index=int(get_index_vertex(nodes_R,id_target))

        print 'iterazione %d / %d --> %d-%d'%(j,len(green_edges_random)-1,source_index,target_index)
        max_flow_residual=maxFlow(nodes_R[source_index],nodes_R[target_index])
        print 'max flow residual: ' + str(max_flow_residual)
        if max_flow_residual >= flow_c_value:
            del graph_dict
            #graph_dict=convert_graph_to_dict(residualGraph)
            #passo H perche devo calcolare tutti i path sul grafo originale
            graph_dict=convert_graph_to_dict(H)
            #print 'pre compute paths'
            edge=(id_source,id_target)
            edge_reverse=(id_target,id_source)
            #del paths
            global path_counter
            path_counter=0
            paths=find_all_paths(graph_dict,id_source,id_target,[])
            #print
            #print 'paths calcolati tra %d-%d: '%(id_source,id_target)
            #print paths
            if not all_graph_paths.has_key(edge) and not all_graph_paths.has_key(edge_reverse):
                all_graph_paths.update({edge:paths})

            if(len(paths)>0 and max_flow_residual>0):

                #domanda casuale da asseganre
                if(alfa==0.0):
                    demand= random.randint(0,max_flow_residual)

                #domanda da assegnare in proporzione ad un valore alfa
                else:
                    if edge not in max_flows_dict:
                        print 'Errore in generate_demand: coppia senza maxflow'
                        sys.exit('Errore coppia senza maxflow')
                    else:
                        """
                        max_flow_edge=max_flows_dict[edge]
                        max_demand=int(math.ceil(alfa*max_flow_edge))
                        if max_demand > max_flow_residual:
                            #FLAG 1: Incapace di assegnare alfa*maxFlow, posso allocare al piu maxFlow_residuo
                            demand=max_flow_residual
                            file_flags.write('----------FLAG 1 per la coppia : ('+str(id_source)+','+str(id_target)+') : alfa*max_flow= '+str(max_demand)+' > '+str(max_flow_residual) + ' =max_flow_residuo -------\n')
                            string=''
                            for green in green_selected:
                                string=string+str(green)+' - '
                            file_flags.write('Domanda assegnata fino ad ora:\n'+string+'\n')
                        else:
                        """
                        demand=flow_c_value

                #print 'demand da assegnare: %d '%(demand)
                support_graph=nx.MultiGraph(residualGraph)
                temp_paths=deepcopy(paths)
                paths_feasible=feasible_path(support_graph,temp_paths)
                #print 'cammini disponibili'
                #print paths_feasible
                if not all_paths_feasible.has_key(edge) and not all_paths_feasible.has_key(edge_reverse):
                    all_paths_feasible.update({edge:paths_feasible})

                temp_feasible=deepcopy(paths_feasible)
                #if (alfa==0.0):
                #    demand_assigned=assign_demand(residualGraph,demand,temp_feasible)
                #else:
                #    flag_update_all_paths=False
                #   demand_assigned=assign_demand_shortest(residualGraph,demand,id_source,id_target,file_flags,distance_metric,flag_update_all_paths,temp_feasible)
                """
                if demand_assigned!=0:
                    print 'NON E POSSIBILE DOMANDA ASSEGNATA MALE'
                """
                #if(demand_assigned>0):
                print 'domanda assegnata: %d/%d'%(demand,demand)
                new_green_edge=(id_source,id_target,demand)
                green_selected.append(new_green_edge)

                #my_draw(residualGraph,'residual'+str(j))
        else:
            sys.exit("Errore in generate demand of fixed value: impossibile assegnare flusso Fixed ad una coppia")
        j=j+1

    #print 'archi da aggiungere verdi:'
    #print green_selected
    file_gml=produce_gml_graph(green_selected,filename)

    file_flags.write('Domanda Finale assegnata al grafo: \n')
    string=''
    for edge in green_selected:
        string=string+ str(edge)+ ' - '
    file_flags.write(string+'\n')
    file_flags.close()
    return file_gml,green_selected


#OTTIMIZZATA
def generate_demand_of_fixed_value_from_list_of_couple(H,list_of_couple,flow_c_value,prob,filename,alfa,seed,path_to_stats,distance_metric):

    residualGraph=nx.MultiGraph(H)
    green_edges_random=np.array([])
    green_edges_random=list_of_couple
    print green_edges_random
    green_selected=[]
    graph_dict={}

    nodes_R=[]
    edges_R=[]
    for i in H.nodes():
        nodes_R.append(Vertex(H.node[i]['id']))
    j=0

    path_to_file_flag_stat=path_to_stats+filename+'_Flags_statistics.txt'
    if not os.path.exists(path_to_file_flag_stat):
        file_flags=open(path_to_file_flag_stat,'w')
        file_flags.close()

    file_flags=open(path_to_file_flag_stat,'a')
    file_flags.write('\n\n\nTopologia: '+filename+'\nSeed: '+str(seed)+'\nAlfa: '+str(alfa)+'\n')
    file_flags.write('Coppie di nodi selezionati con probabilita = '+str(prob)+' : \n')
    string=''
    for edge in green_edges_random:
        string=string+str(edge)+' - '
    file_flags.write(string+'\n')

    #Calcola inizialmente il maxFlow sul grafo iniziale per ogni coppia di nodi verdi
    max_flows_dict={}
    max_flows_dict=compute_all_max_flows(H, green_edges_random)
    #print max_flows_dict

    file_flags.write('Max flows su grafo supply per ogni coppia: \n')
    string=''
    for key,value in max_flows_dict.items():
        string=string+str(key)+': '+str(value)+' - '

    file_flags.write(string+'\n')

    for couple in green_edges_random:
        clean_edges(nodes_R)
        del edges_R
        edges_R=get_Edges_residual(residualGraph)
        buildGraph(nodes_R,edges_R)
        id_source=couple[0]
        id_target=couple[1]
        source_index=int(get_index_vertex(nodes_R,id_source))
        target_index=int(get_index_vertex(nodes_R,id_target))

        print 'iterazione %d / %d --> %d-%d'%(j,len(green_edges_random)-1,source_index,target_index)
        max_flow_residual=maxFlow(nodes_R[source_index],nodes_R[target_index])
        print 'max flow residual: ' + str(max_flow_residual)
        if max_flow_residual >= flow_c_value:
            edge=(id_source,id_target)
            edge_reverse=(id_target,id_source)
            demand=flow_c_value
            print 'domanda assegnata: %d/%d'%(demand,demand)
            new_green_edge=(id_source,id_target,demand)
            green_selected.append(new_green_edge)

            #my_draw(residualGraph,'residual'+str(j))
        else:
            sys.exit("Errore in generate demand of fixed value: impossibile assegnare flusso Fixed ad una coppia")
        j=j+1

    #print 'archi da aggiungere verdi:'
    #print green_selected
    file_gml=produce_gml_graph(green_selected,filename)

    file_flags.write('Domanda Finale assegnata al grafo: \n')
    string=''
    for edge in green_selected:
        string=string+ str(edge)+ ' - '
    file_flags.write(string+'\n')
    file_flags.close()
    return file_gml,green_selected


def compute_max_value_of_fixed_flow_from_list_of_couple(H,list_of_couple,prob,alfa,filename,seed,path_to_stats,distance_metric):

    residualGraph=nx.MultiGraph(H)
    green_edges_random=np.array([])
    green_edges_random=list_of_couple
    print green_edges_random
    green_selected=[]
    graph_dict={}
    global all_graph_paths
    global all_paths_feasible
    #random.shuffle(green_edges_random)  #mescola casualmente gli elementi
    #print green_edges_random
    nodes_R=[]
    edges_R=[]
    for i in H.nodes():
        nodes_R.append(Vertex(H.node[i]['id']))
    j=0

    path_to_file_flag_stat=path_to_stats+filename+'_Flags_statistics.txt'
    if not os.path.exists(path_to_file_flag_stat):
        file_flags=open(path_to_file_flag_stat,'w')
        file_flags.close()

    file_flags=open(path_to_file_flag_stat,'a')
    file_flags.write('\n\n\nTopologia: '+filename+'\nSeed: '+str(seed)+'\nAlfa: '+str(alfa)+'\n')
    file_flags.write('Coppie di nodi selezionati con probabilita = '+str(prob)+' : \n')
    string=''
    for edge in green_edges_random:
        string=string+str(edge)+' - '
    file_flags.write(string+'\n')

    #Calcola inizialmente il maxFlow sul grafo iniziale per ogni coppia di nodi verdi
    max_flows_dict={}
    max_flows_dict=compute_all_max_flows(H, green_edges_random)
    #print max_flows_dict

    file_flags.write('Max flows su grafo supply per ogni coppia: \n')
    string=''
    for key,value in max_flows_dict.items():
        string=string+str(key)+': '+str(value)+' - '

    file_flags.write(string+'\n')

    #print 'Max flows Calcolati:'
    #print max_flows_dict

    exit_condition=False
    flow_c=0

    while(exit_condition==False):
        flow_c+=1
        residualGraph=nx.MultiGraph(H)
        j=0
        for couple in green_edges_random:
            clean_edges(nodes_R)
            del edges_R
            edges_R=get_Edges_residual(residualGraph)
            buildGraph(nodes_R,edges_R)
            id_source=couple[0]
            id_target=couple[1]
            source_index=int(get_index_vertex(nodes_R,id_source))
            target_index=int(get_index_vertex(nodes_R,id_target))

            #print 'iterazione %d / %d --> %d-%d'%(j,len(green_edges_random)-1,source_index,target_index)
            max_flow_residual=maxFlow(nodes_R[source_index],nodes_R[target_index])
            #print 'max flow residual: ' + str(max_flow_residual)
            if max_flow_residual >= flow_c:
                del graph_dict
                #graph_dict=convert_graph_to_dict(residualGraph)
                #passo H perche devo calcolare tutti i path sul grafo originale
                graph_dict=convert_graph_to_dict(H)
                #print 'pre compute paths'
                edge=(id_source,id_target)
                edge_reverse=(id_target,id_source)
                #del paths
                global path_counter
                path_counter=0
                paths=find_all_paths(graph_dict,id_source,id_target,[])
                print
                #print 'paths calcolati tra %d-%d: '%(id_source,id_target)
                #print paths
                if not all_graph_paths.has_key(edge) and not all_graph_paths.has_key(edge_reverse):
                    all_graph_paths.update({edge:paths})

                if(len(paths)>0 and max_flow_residual>0):

                    #domanda casuale da asseganre
                    if(alfa==0.0):
                        demand= random.randint(0,max_flow_residual)

                    #domanda da assegnare in proporzione ad un valore alfa
                    else:
                        if edge not in max_flows_dict:
                            print 'Errore in generate_demand: coppia senza maxflow'
                            sys.exit('Errore coppia senza maxflow')
                        else:
                            """
                            max_flow_edge=max_flows_dict[edge]
                            max_demand=int(math.ceil(alfa*max_flow_edge))
                            if max_demand > max_flow_residual:
                                #FLAG 1: Incapace di assegnare alfa*maxFlow, posso allocare al piu maxFlow_residuo
                                demand=max_flow_residual
                                file_flags.write('----------FLAG 1 per la coppia : ('+str(id_source)+','+str(id_target)+') : alfa*max_flow= '+str(max_demand)+' > '+str(max_flow_residual) + ' =max_flow_residuo -------\n')
                                string=''
                                for green in green_selected:
                                    string=string+str(green)+' - '
                                file_flags.write('Domanda assegnata fino ad ora:\n'+string+'\n')
                            else:
                                demand=max_demand
                            """
                            demand=flow_c

                    #print 'demand da assegnare: %d '%(demand)
                    support_graph=nx.MultiGraph(residualGraph)
                    temp_paths=deepcopy(paths)
                    paths_feasible=feasible_path(support_graph,temp_paths)
                    #print 'cammini disponibili'
                    #print paths_feasible
                    if not all_paths_feasible.has_key(edge) and not all_paths_feasible.has_key(edge_reverse):
                        all_paths_feasible.update({edge:paths_feasible})

                    temp_feasible=deepcopy(paths_feasible)
                    if (alfa==0.0):
                        demand_assigned=assign_demand(residualGraph,demand,temp_feasible)
                    else:
                        flag_update_all_paths=False
                        demand_assigned=assign_demand_shortest(residualGraph,demand,id_source,id_target,file_flags,distance_metric,flag_update_all_paths,temp_feasible)
                    """
                    if demand_assigned!=0:
                        print 'NON E POSSIBILE DOMANDA ASSEGNATA MALE'
                    """
                    if(demand_assigned>0):
                        print 'domanda assegnata: %d/%d'%(demand_assigned,demand)
                        new_green_edge=(id_source,id_target,demand_assigned)
                        green_selected.append(new_green_edge)

                        my_draw(residualGraph,'residual'+str(j))
            else:
                #non e' possibile assegnare la quantita di flusso c alla coppia corrente. Ritorno il valore precedente di c
                return (flow_c-1)

            j=j+1




def assign_demand(residualGraph,demand,paths_feasible):
    demand_assigned=0
    while(demand>0):
        #print 'Domanda ancora da assegnare: %d'%(demand)
        #print 'temp cammini disponibili'
        #print paths_feasible

        edges_satured=[]
        size=(len(paths_feasible))-1
        if size==0:
            index_random=0

        elif size<0:
            if len(paths_feasible)==0:
                print "Flusso inibente, domanda non completamente soddisfatta: %d/%d"%(demand_assigned,demand+demand_assigned)
                return demand_assigned
        else:
            index_random=random.randint(0,size)

        curr_path=paths_feasible[index_random]
        size_path=len(paths_feasible[index_random])-1
        #print 'seleziono il path:' + str(index_random)
        #print curr_path
        #check if path exist
        count=0
        for i in range(0,size_path,1):
            id_source=curr_path[i]
            id_target=curr_path[i+1]
            if residualGraph.has_edge(id_source,id_target,key=0):
                old_capacity=residualGraph[id_source][id_target][0]['capacity']
                new_capacity=old_capacity-1
                residualGraph[id_source][id_target][0]['capacity']=new_capacity
                if new_capacity<0:
                    print 'ERRORE IN ASSIGN_DEMAND: ARCO CON CAPACITA RESIDUA NEGATIVA '
                if new_capacity==0:
                    residualGraph.remove_edge(id_source,id_target,key=0)
                    #print 'rimosso arco: ' +str(id_source)+'-'+str(id_target)
                    edge=(id_source,id_target)
                    edge_reverse=(id_target,id_source)
                    edges_satured.append(edge)
                    edges_satured.append(edge_reverse)
                    #count+=1
        """
        if count>0:
            print 'Rimuovo path saturo'
            print curr_path
            paths_feasible.remove(curr_path)
            #print 'rimanenti path faesible:'
            #print paths_feasible
        """""
        path_to_remove=[]
        #calcola i path che non sono piu feasible perche gli archi sono saturi
        for edge in edges_satured:
            for path in paths_feasible:
                for i in range(0,len(path)-1,1):
                    source=path[i]
                    target=path[i+1]
                    if edge[0]==source and edge[1]==target:
                        if path not in path_to_remove:
                            path_to_remove.append(path)

        #rimuovo i path non piu feasible
        for path in path_to_remove:
            if path in paths_feasible:
                #print 'rimuovo path con arco saturo'
                #print path
                paths_feasible.remove(path)
            else:
                print 'Errore: path da rimuovere inesistente Assign demand'
                sys.exit('Assign demand errore path da rimuovere inesistente')

        demand_assigned=demand_assigned+1
        demand=demand-1

    return demand_assigned

def get_shortests_from_paths_weighted(weighted_paths):

    shortest_paths=[]
    minKey=sys.maxint
    for key_path in weighted_paths:
        if (key_path<minKey):
            minKey=key_path

    shortest_paths=weighted_paths[minKey]

    return shortest_paths


def assign_demand_shortest(residualGraph,demand,id_source,id_target,file_flags,distance_metric,flag_update_all_paths,path_feasible):

    demand_assigned=0
    shortests_array=[]
    #tutti i paths con relativi pesi
    #flag update=false, sto assegnando la domanda iniziale, non mi interessa fare i residui
    #weighted_paths=compute_lenght_paths_on_residual(residualGraph,id_source,id_target,distance_metric,flag_update_all_paths)

    weighted_paths=compute_lenght_paths_in_assign_demand(residualGraph,id_source,id_target,distance_metric,flag_update_all_paths,path_feasible)

    #print 'weighted paths tra %d-%d'%(id_source,id_target)
    #print weighted_paths
    while(demand>0):
        #print 'Domanda ancora da assegnare: %d'%(demand)
        #print 'weighted paths disponibili'
        #print weighted_paths
        capMin=0
        shortests_array=get_shortests_from_paths_weighted(weighted_paths)


        edges_satured=[]
        size=(len(shortests_array))-1
        if size==0:
            index_random=0

        elif size<0:
            if len(paths_feasible)==0:
                #FLAG 2: LA SCELTA DEI CAMMINI HA PORTATO A INIBIRE IL FLUSSO da ASSEGNARE
                print "Flusso inibente, domanda non completamente soddisfatta: %d/%d"%(demand_assigned,demand+demand_assigned)
                #sys.exit("Flusso inibente, domanda non completamente soddisfatta: ABORT !!!")
                file_flags.write('------FLAG 2: FLUSSO INIBENTE per la coppia: ( %d , %d ) --------\n',id_source,id_target)
                return demand_assigned
        else:
            index_random=random.randint(0,size)

        curr_path=shortests_array[index_random]
        size_path=len(shortests_array[index_random])-1
        #print 'seleziono il path:' + str(index_random)
        #print curr_path
        #check if path exist
        count=0
        capMin=sys.maxint
        for i in range(0,size_path,1):
            id_source=curr_path[i]
            id_target=curr_path[i+1]
            if residualGraph.has_edge(id_source,id_target,key=0):
                cap_edge=residualGraph[id_source][id_target][0]['capacity']
                if cap_edge <capMin:
                    capMin=cap_edge
        #print capMin
        increment_flow=min(capMin,demand)
        #print increment_flow
        for i in range(0,size_path,1):
            id_source=curr_path[i]
            id_target=curr_path[i+1]
            if residualGraph.has_edge(id_source,id_target,key=0):
                old_capacity=residualGraph[id_source][id_target][0]['capacity']
                new_capacity=old_capacity-increment_flow
                residualGraph[id_source][id_target][0]['capacity']=new_capacity
                if new_capacity<0:
                    print 'ERRORE IN ASSIGN_DEMAND SHORTEST: ARCO CON CAPACITA RESIDUA NEGATIVA '
                    sys.exit('ERRORE IN ASSIGN_DEMAND SHORTEST: ARCO CON CAPACITA RESIDUA NEGATIVA ')
                if new_capacity==0:
                    residualGraph.remove_edge(id_source,id_target,key=0)
                    #print 'rimosso arco: ' +str(id_source)+'-'+str(id_target)
                    edge=(id_source,id_target)
                    edge_reverse=(id_target,id_source)
                    edges_satured.append(edge)
                    edges_satured.append(edge_reverse)
                    #count+=1
        """
        if count>0:
            print 'Rimuovo path saturo'
            print curr_path
            paths_feasible.remove(curr_path)
            #print 'rimanenti path faesible:'
            #print paths_feasible
        """""
        path_to_remove=[]
        #calcola i path che non sono piu feasible perche gli archi sono saturi
        for edge in edges_satured:
            for key in weighted_paths:
                paths_array=weighted_paths[key]
                for path in paths_array:
                    for i in range(0,len(path)-1,1):
                        source=path[i]
                        target=path[i+1]
                        if edge[0]==source and edge[1]==target:
                            if path not in path_to_remove:
                                path_to_remove.append(path)

        #rimuovo i path non piu feasible
        for path in path_to_remove:
            for key in weighted_paths:
                if path in weighted_paths[key]:
                    (weighted_paths[key]).remove(path)
                    #print 'rimuovo path con arco saturo'
                    #print path
                #else:
                #    print 'Errore: path da rimuovere inesistente Assign demand'

        demand_assigned=demand_assigned+increment_flow
        demand=demand-increment_flow

        #update weightedPath rimuovendo le key che non hanno nessun path
        weighted_paths={key: value for key, value in weighted_paths.items() if len(value) >0}

    return demand_assigned

def compute_paths(H,green_selected):
    global all_graph_paths
    global all_paths_feasible
    graph_dict=convert_graph_to_dict(H)

    all_graph_paths={}
    all_paths_feasible={}
    for edge in green_selected:
        id_source=edge[0]
        id_target=edge[1]
        paths={}
        paths=find_all_paths(graph_dict,id_source,id_target,[])
        key=(id_source,id_target)
        #print 'pre'
        if not all_graph_paths.has_key(key):
                all_graph_paths.update({key:paths})
                #print paths
                #print 'aggiunto'
        temp_paths=deepcopy(paths)
        paths_feasible=feasible_path(H,temp_paths)
        if not all_paths_feasible.has_key(key):
            all_paths_feasible.update({key:paths_feasible})

def reduce_capacity_by_flow(R,paths):
    min=1
    max=count_paths(paths)
    #print 'numero path trovati: '+str(max)
    num_path_select= random.randint(min,max)
    to_remove=[]
    total_demand=0
    for key in paths:
            current_key=paths[key]  #itero sulle chiavi (le minCapacity)
            #print 'current key:'
            #print 'flusso: '+str(key)
            for path in current_key:  #itero sui path, possono essere piu di uno con la stesso flusso (minCapacity)
                if num_path_select>0:
                    #print 'current path'
                    #print 'prev demand: %d + flux %d = %d '%(total_demand,int(key),(total_demand+int(key)))
                    total_demand+=int(key)
                    #print "%d :"%int(key) + str(path)
                    for edge in path:
                        #print 'arco singolo'
                        #print edge
                        id_source=(edge.fromVertex.name)
                        id_target=(edge.toVertex.name)
                        #print str(id_source)+str(id_target)
                        keydict=R[id_source][id_target]
                        #print keydict
                        for k in keydict:
                            edge=R.edge[id_source][id_target][k]
                            #print 'ho preso questo'
                            #print edge
                            if 'type' not in edge:
                                R.remove_edge(id_source,id_target,key=k)
                                print 'rimosso: errore piu edge fra due nodi???'
                            else:
                                if (R.has_edge(id_source,id_target,key=k)):
                                        old_capacity=get_edge_attr(R,id_source,id_target,'capacity')
                                        #print old_capacity
                                        new_capacity=old_capacity-key
                                        #print new_capacity

                                        if(new_capacity>=0):
                                            R[id_source][id_target][k]['capacity']=new_capacity
                                            if(new_capacity==0): #aggiungo alla lista di archi da rimuovere
                                                #print 'aggiungo arco saturo: '+ str(id_source)+'-'+str(id_target)+'-'+str(new_capacity)
                                                arco_saturo=(id_source,id_target,k)
                                                to_remove.append(arco_saturo)
                                        else:
                                            print 'capacita insufficiente: '+ str(id_source)+'-'+str(id_target)+'-'+str(new_capacity)
                                            sys.exit('Reduce capacity by flow: Errore capacita dell arco insufficiente')

                remove_saturated_edge(R,to_remove)
                num_path_select-=1
                    #print to_remove
                to_remove[:]=[] #svuoto la lista degli archi rimossi
                    #print 'lista svuota'
                    #print to_remove
    return total_demand

def produce_gml_graph(green_selected,filename):
    graph=nx.MultiGraph()

    for node in green_selected:
        node_1=node[0]
        node_2=node[1]
        graph.add_node(node_1,id=node_1,label=node_1)
        graph.add_node(node_2,id=node_2,label=node_2)

    for edge in green_selected:

        id_node_source=edge[0]
        id_node_target=edge[1]
        demand_flow=edge[2]
        #print "%d-%d-%d: "%(id_node_source,id_node_target,demand_flow)
        graph.add_edge(id_node_source,id_node_target,type='green',demand=demand_flow)
    #print graph
    path_to_file='network topologies/'+filename+'.gml'
    #print 'da creare: '+path_to_file
    nx.write_gml(graph,path_to_file)
    #print 'creato'
    return path_to_file

def remove_saturated_edge(R,to_remove):
    for edge in to_remove: #rimuovo da R gli archi con capacity 0
        #print edge
        id_source=edge[0]
        id_target=edge[1]
        k=edge[2]
        #print 'valori :'+str(id_source)+'-'+str(id_target)+'-'+str(k)
        residual_cap=R[id_source][id_target][k]['capacity']
        if residual_cap==0:
            R.remove_edge(id_source,id_target,key=k)
            #print 'rimosso '+str(id_source)+'-'+str(id_target)
        else:
            print 'Errore arco con capacita maggiore'
            sys.exit('Remove saturated edge: Errore arco con capacita maggiore')

def count_paths(paths):
    #count=0
    #for key in paths:
     #   print len(key)
      #  for path in key:
       #     count+=1
    count=sum(len(val) for val in paths.itervalues())
    return count

def get_Edges_residual(R):

    edges_R=[]
    #for edge in R.edges(data=True):
    #   print edge

    for edge in R.edges():
        id_source=edge[0]
        id_target=edge[1]
        #print 'archi tra %d-%d'%(id_source,id_target)
        keydict=R[id_source][id_target]
        #print keydict
        for k in keydict:
            if R.has_edge(id_source,id_target,key=k):
                if R[id_source][id_target][k]['type']=='normal':
                    #capacity=get_edge_attr(R,id_source,id_target,'capacity')
                    capacity=R[id_source][id_target][k]['capacity']
                    elem = (id_source,id_target,capacity)
                    if elem not in edges_R:
                        edges_R.append(elem)
                    #else:
                        #print 'due volte stesso arco '
                        #print elem
                        #print edges_R
                        #sys.exit('due volte stesso arco')
    #print 'archi del grafo'
    #print edges_R
    return edges_R


def get_edge_attr(H,id_source,id_target,attr):
    #print H[id_source][id_target]
    keydict=H[id_source][id_target]

    for k in keydict:
        #print k
        type=H[id_source][id_target][k]['type']
        #print type
        if (type=='normal' and type!='green'):
            capacity=int(H[id_source][id_target][k][attr])
            #print str(capacity)
            return capacity



def random_edges(H,prob):
    edges=[]
    #print nodes
    for i in H.nodes():
        for j in H.nodes():
            id_source=H.node[i]['id']
            id_target=H.node[j]['id']
            if(id_source!=id_target):
                #print 'Coppia %d-%d :'%(id_source,id_target)
                if flip_coin(prob):
                    #print 'coppia presa'
                    elem=(id_source,id_target)
                    elem_reverse=(id_target,id_source)
                    if elem not in edges and elem_reverse not in edges:
                        edges.append(elem)
                #else:
                #   print 'coppia scartata'

    #print 'array delle coppie'
    #print nodes
    print 'Numero archi: %d'%(len(edges))
    #print edges
    return edges


def flip_coin(p):
    value=random.random()
    p=float(p)
    #print ' Confronto Valore generato: %f con %f'%(value,p)
    if value < p :
        return True
    elif value >= p:
        return False
    else:
        sys.exit('Errore in Flip Coin: valore ne <,>,=')



def get_num_simulation(path_to_file_simulation):
    file = open(path_to_file_simulation,'r')
    number = int(file.readline())
    file.close()

    return number

def set_num_next_simulation(path_to_file_simulation,set_num=None):

    file=open(path_to_file_simulation,'r')
    number = int(file.readline())
    file.close()
    if set_num!=None:
        number=set_num
    else:
        number+=1
    #print 'numero della simulazione: %d'%(number)
    file=open(path_to_file_simulation,'w')
    file.write(str(number))
    file.close()


def store_file(source,destination,number_simulation):
    name_directory=destination+'/'+'Simulation_'+str(number_simulation)
    path_to_images_dir=source

    #print name_directory
    for filename in os.listdir(source):
        #print filename

        if filename.endswith(".png"):
            if not os.path.exists(name_directory):
                os.makedirs(name_directory)
            path_to_image=path_to_images_dir+'/'+filename
            #print path_to_image
            shutil.copy(path_to_image,name_directory)


def remove_files_dot(path):
    for filename in os.listdir(path):
        lenght=len(str(filename))
        name=filename[:lenght-4]
        extension=filename[(lenght-4):]
        if (extension=='.dot'):
            path_to_dot_file=path+name
            #print path
            if os.path.exists(path_to_dot_file+'.dot'):
                os.remove(path_to_dot_file+'.dot')
            print 'cancello: '+name

def remove_files_image(path):

    for filename in os.listdir(path):
        lenght=len(str(filename))
        name=filename[:lenght-4]
        extension=filename[(lenght-4):]
        if (extension=='.png'):
            path_to_dot_file=path+name
            #print path
            if os.path.exists(path_to_dot_file+'.png'):
                os.remove(path_to_dot_file+'.png')
            print 'cancello: '+name

def convert_graph_to_dict(G):
        graph={}
        for node in G.nodes():
            if not graph.has_key(node):
                graph[node]=[]

        #print 'my_graph'
        #print graph

        for edge in G.edges():
            source=edge[0]
            target=edge[1]
            keydict=G[source][target]
            for k in keydict:
                if G[source][target][k]['type']=='normal':
                    #print str(source) +'-'+str(target)
                    if graph[source]==None:
                        graph.update({source:target})
                        #print graph
                    else:
                        graph[source].append(target)

                    if graph[target]==None:
                        graph.update({target:source})
                        #print graph
                    else:
                        #print graph[target]
                        graph[target].append(source)

        return graph

def find_all_paths(graph, start, end, path=[]):
        global path_counter
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    if newpath not in paths:
                        path_counter += 1
                        paths.append(newpath)
                        if path_counter % 1000==0:
                            sys.stdout.write("Path trovati: %d\r"%(path_counter))
                            sys.stdout.flush()

        return paths

def feasible_path(G,paths):
    #G is a graph
    #paths is a list of all path in G between two nodes
    paths_to_remove=[]
    #controllo se tutti i path tra sorgente e destinazione sono ancora validi, dato che sul grafo residuo potrebbero non esistere piu.
    lenght_paths=len(paths)

    for path in paths:
        minCap=sys.maxint
        #print 'selected:'
        #print path

        for i in range(0,(len(path)-1),1):
            id_source=path[i]
            id_target=path[(i+1)]

            if G.has_edge(id_source,id_target):
                keydict=G[id_source][id_target]
                count=0
                for k in keydict:
                    if G[id_source][id_target][k]['type']=='normal':
                        count=count+1

                if count==0:
                    paths_to_remove.append(path)

            else: # edge mising
                paths_to_remove.append(path)
                minCap=-1
                break   #i want stop the for index loop


    for path in paths_to_remove:
        if path in paths:
            paths.remove(path)

    return paths


def recover(H,nodes_repaired,edge_repaired):

    for node in nodes_repaired:
        H.node[node]['status']='repaired'
        H.node[node]['color']='blue'
        print 'nodo ripristinato %d : '%(node)

    for edge in edge_repaired:
        id_source=edge[0]
        id_target=edge[1]
        keydict =H[id_source][id_target]
        #print str(keydict)
        for k in keydict:
            if H.edge[id_source][id_target][k]['type']=='normal':
                H.add_edge(id_source,id_target,key=k, status='repaired',labelfont='blue',color='blue',style='solid')
                print 'arco ripristinato %d-%d: '%(id_source,id_target)

        if H.node[id_source]['status']=='destroyed':
            H.node[id_source]['status']='repaired'
            H.node[id_source]['color']='blue'
            print 'nodo ripristinato %d : '%(id_source)

        if H.node[id_target]['status']=='destroyed':
            H.node[id_target]['status']='repaired'
            H.node[id_target]['color']='blue'
            print 'nodo ripristinato %d : '%(id_target)



def generate_erdos_renyi_graph(num_nodes,prob_edge):

    graph=nx.MultiGraph(nx.erdos_renyi_graph(num_nodes,prob_edge,directed=False))
    #print compute_diameter_of_graph(graph)

    for i in range(0,graph.number_of_nodes(),1):
        latitude=random.randint(0,500)
        longitude=random.randint(0,500)
        graph.add_node(i,id=i,label=i,type='normal',Latitude=latitude,Longitude=longitude)


    for edge in graph.edges():
        id_source=int(edge[0])
        id_target=int(edge[1])
        #cap=random.randint(1,max_capacity)   #assign random capacity in range
        cap = 1000
        graph.add_edge(id_source,id_target,key=0,type='normal',capacity=cap)

    #for node in graph.nodes(data=True):
    #    print node

    #for edge in graph.edges(data=True):
    #    print edge

    #rimuovi nodi senza archi (isolati)
    for node in graph.nodes():
        id_node=graph.node[node]['id']
        #print id_node
        degree_node=get_degree_of_node(graph,id_node)
        if degree_node==0:
            graph.remove_node(id_node)

    count_node=0
    count_edge=0
    for node in graph.nodes():
        count_node+=1

    for edge in graph.edges():
        count_edge+=1

    print 'Nodi del grafo: %d'%(count_node)
    print 'Archi del grafo: %d'%(count_edge)

    filename='erdos_renyi_graph_%d_nodes_%d_edges'%(count_node,count_edge)
    path_to_file='network topologies/random_graphs_generated/'+filename+'.gml'
    nx.write_gml(graph,path_to_file)
    return path_to_file


def generate_random_graph(max_nodes,prob,max_x,max_y):
    #num_nodes=random.randint(0,max_nodes) #random nodes in range
    num_nodes=max_nodes
    graph=nx.MultiGraph()
    print 'prob of edge'
    print prob
    for i in range(0,num_nodes,1):
        latitude=random.randint(0,max_x)
        longitude=random.randint(0,max_y)
        graph.add_node(i,id=i,label=i,type='normal',Latitude=latitude,Longitude=longitude)

    edges=random_edges(graph,prob)

    for edge in edges:
        id_source=edge[0]
        id_target=edge[1]
        #cap=random.randint(1,max_capacity)   #assign random capacity in range
        cap = 1000
        graph.add_edge(id_source,id_target,type='normal',capacity=cap)

    #rimuovi nodi senza archi (isolati)
    for node in graph.nodes():
        id_node=graph.node[node]['id']
        degree_node=get_degree_of_node(graph,id_node)
        if degree_node==0:
            graph.remove_node(id_node)

    count_node=0
    count_edge=0
    for node in graph.nodes():
        count_node+=1

    for edge in graph.edges():
        count_edge+=1

    print 'Nodi del grafo: %d'%(count_node)
    print 'Archi del grafo: %d'%(count_edge)

    filename='random_graph_%d_nodes_%d_edges'%(count_node,count_edge)
    path_to_file='network topologies/random_graphs_generated/'+filename+'.gml'
    nx.write_gml(graph,path_to_file)
    return path_to_file


def distance_node(H,node_i,node_j,distance_metric):


    if distance_metric == "one-hop":
        return 1

    elif distance_metric == "capacity":
        #get capacity of link for 'capacity' metric
        keydict=H[node_i][node_j]
        for k in keydict:
            if H[node_i][node_j][k]['type']=='normal':
                cap=H[node_i][node_j][k]['capacity']

        return (1.0/cap)

    elif distance_metric == 'broken':
        #get status of the link for 'broken' metric
        keydict=H[node_i][node_j]
        for k in keydict:
            if H[node_i][node_j][k]['type']=='normal':
                status=H[node_i][node_j][k]['status']
        distanza_temp=0.0 #distanza con arco ok e nodi ok
        costo_vertici=0.5
        if H.node[node_i]['status']=='destroyed':
            distanza_temp+=costo_vertici
        if H.node[node_j]['status']=='destroyed':
            distanza_temp+=costo_vertici

        if status == 'destroyed':
            #return the lenght of a link broken
            costo_arco_rotto=1
            distanza_temp+=costo_arco_rotto

        else:
             distanza_temp+=0.1

        if distanza_temp==0.0:
            distanza_temp=0.1

        return distanza_temp

    elif distance_metric == 'broken_capacity':
        #get status of the link for 'broken' metric
        keydict=H[node_i][node_j]
        #print keydict
        #print node_i, node_j
        for k in keydict:
            if H[node_i][node_j][k]['type']=='normal':
                status=H[node_i][node_j][k]['status']
                capacity=H[node_i][node_j][k]['capacity']

        #print node_i,node_j
        distanza_temp=0.0 #distanza con arco ok e nodi ok
        costo_vertici=0.5
        if H.node[node_i]['status']=='destroyed':
            #print 'nodo rotto'
            distanza_temp+=costo_vertici
            #print 'aggiungo'
            #print distanza_temp
        #if H.node[node_j]['status']=='destroyed':
            #print 'nodo rotto'
            #distanza_temp+=costo_vertici
            #print 'aggiungo'
            #print 'Nodo rotto'
            #print distanza_temp

        #print distanza_temp
        if status == 'destroyed':
            #return the lenght of a link broken
            costo_arco_rotto=1.0
            ratio=0.0
            #print costo_arco_rotto,capacity
            #print costo_arco_rotto/capacity
            ratio=float("%.10f"%(costo_arco_rotto/capacity))
            #print 'arco rotto'
            #print ratio
            distanza_temp+=ratio
            #print 'arco rotto'
            #print distanza_temp

        else:
            distanza_temp+=0.1/(capacity)
            #print 'arco non rotto'
        #print distanza_temp
        if distanza_temp==0.0:
            sys.exit('Errore in distace node: distanza=0.0 !!!')
            distanza_temp=0.1

        return distanza_temp

    else:
        sys.exit('Errore distance_node: nessuna metrica di distanza riconosciuta')
        return None


def compute_lenght_paths(H,id_source,id_target,distance_metric,flag_update_all_paths):

    #graph_dict=convert_graph_to_dict(H)
    #paths=find_all_paths(graph_dict,id_source,id_target,[])

    global all_graph_paths
    #all_graph_paths={}

    #print all_graph_paths
    #AGGIORNA I PATH PRESENTI IN ALL_GRAPH_PATHS
    if flag_update_all_paths==True:
        update_all_graph_path(H)

    #print all_graph_paths

    edge=(id_source,id_target)
    edge_reverse=(id_target,id_source)
    #print edge
    #print edge_reverse
    #print all_graph_paths
    if edge in all_graph_paths:
        paths=all_graph_paths[edge]
    elif edge_reverse in all_graph_paths:
        paths=all_graph_paths[edge_reverse]
    else:
        #Nuova coppia verde, devo calcolare per la prima volta i suoi path
        print 'Calcolo paths per nuova coppia: %d-%d'%(id_source,id_target)
        #paths=compute_paths_for_split
        #sys.exit('Errore ho calcolato nuovi path per due nuove coppie !!!')
        graph_dict=convert_graph_to_dict(H)
        paths=find_all_paths(graph_dict,id_source,id_target,[])
        all_graph_paths.update({edge:paths})
        #print paths
        #print "non esiste l'arco verde tra i due nodi per calcolare la centralita"


    #print 'path trovati'
    #print paths
    weighted_paths={}
    #assegna ad ogni path un peso dato dalla somma delle distanze tra ogni coppia di nodi
    for path in paths:
        weight_of_path=0
        #print 'path prelevato'
        #print path
        for i in range(0,(len(path)-1),1):
            id_source=path[i]
            id_target=path[(i+1)]
            if H.has_edge(id_source,id_target):
                keydict=H[id_source][id_target]
                for k in keydict:
                        if H[id_source][id_target][k]['type']=='normal':
                            dist = distance_node(H,id_source,id_target,distance_metric)
                            weight_of_path+=dist
        #print weight_of_path
        trunk_weigh='%.2f'%(weight_of_path)
        #print trunk_weigh
        if not weighted_paths.has_key(trunk_weigh):
            weighted_paths.update({trunk_weigh:[]})
            weighted_paths[trunk_weigh].append(path)
        else:
            weighted_paths[trunk_weigh].append(path)

    #print weighted_paths

    return weighted_paths


def compute_lenght_paths_in_assign_demand(H,id_source,id_target,distance_metric,flag_update_all_paths,path_feasible):

    #graph_dict=convert_graph_to_dict(H)
    #paths=find_all_paths(graph_dict,id_source,id_target,[])
    #print paths

    #global all_graph_paths

    #Aggiorno all graph path solo se mi serve(es: nella generazione della domanda non mi serve), rimuovendo i path che non sono piu presenti
    #if flag_update_all_paths==True:
    #    print 'sto aggiornando'
    #    update_all_graph_path(H)

    edge=(id_source,id_target)
    edge_reverse=(id_target,id_source)
    """
    #print edge
    #print edge_reverse
    #print all_graph_paths
    if edge in all_graph_paths:
        paths=all_graph_paths[edge]
    elif edge_reverse in all_graph_paths:
        paths=all_graph_paths[edge_reverse]
    else:
        #Nuova coppia verde, devo calcolare per la prima volta i suoi path
        print 'calcolo path per nuova coppia'
        graph_dict=convert_graph_to_dict(H)
        paths=find_all_paths(graph_dict,id_source,id_target,[])
        all_graph_paths.update({edge:paths})
        #print paths
        #print "non esiste l'arco verde tra i due nodi per calcolare la centralita"
    """
    #print 'path trovati'
    #print paths
    weighted_paths={}
    #assegna ad ogni path un peso dato dalla somma delle distanze tra ogni coppia di nodi
    for path in path_feasible:
        weight_of_path=0
        #print 'path prelevato'
        #print path
        for i in range(0,(len(path)-1),1):
            id_source=path[i]
            id_target=path[(i+1)]
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':
                    dist = distance_node(H,id_source,id_target,distance_metric)
                    weight_of_path+=dist

        if not weighted_paths.has_key(weight_of_path):
            weighted_paths.update({weight_of_path:[]})
            weighted_paths[weight_of_path].append(path)
        else:
            weighted_paths[weight_of_path].append(path)

    #print weighted_paths

    return weighted_paths





#perche ho bisogno di ricalcolarli sul residual, dato che all paths graph tiene conto di cammini che potrebbero non esistere piu sul residuo
def compute_lenght_paths_on_residual(H,id_source,id_target,distance_metric,flag_update_all_paths):

    #graph_dict=convert_graph_to_dict(H)
    #paths=find_all_paths(graph_dict,id_source,id_target,[])
    #print paths

    global all_graph_paths

    #Aggiorno all graph path solo se mi serve(es: nella generazione della domanda non mi serve), rimuovendo i path che non sono piu presenti
    if flag_update_all_paths==True:
        print 'sto aggiornando'
        update_all_graph_path(H)

    edge=(id_source,id_target)
    edge_reverse=(id_target,id_source)

    #print edge
    #print edge_reverse
    #print all_graph_paths
    if edge in all_graph_paths:
        paths=all_graph_paths[edge]
    elif edge_reverse in all_graph_paths:
        paths=all_graph_paths[edge_reverse]
    else:
        #Nuova coppia verde, devo calcolare per la prima volta i suoi path
        print 'calcolo path per nuova coppia %d-%d:'%(id_source,id_target)
        graph_dict=convert_graph_to_dict(H)
        #sys.exit('Errore in compute lenghs on residual: ho calcolato i path per due nuove coppie!!!!')
        paths=find_all_paths(graph_dict,id_source,id_target,[])
        all_graph_paths.update({edge:paths})
        #print paths
        #print "non esiste l'arco verde tra i due nodi per calcolare la centralita"

    #print 'path trovati'
    #print paths
    weighted_paths={}
    #assegna ad ogni path un peso dato dalla somma delle distanze tra ogni coppia di nodi
    for path in paths:
        weight_of_path=0
        #print 'path prelevato'
        #print path
        for i in range(0,(len(path)-1),1):
            id_source=path[i]
            id_target=path[(i+1)]
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':
                    dist = distance_node(H,id_source,id_target,distance_metric)
                    weight_of_path+=dist

        if not weighted_paths.has_key(weight_of_path):
            weighted_paths.update({weight_of_path:[]})
            weighted_paths[weight_of_path].append(path)
        else:
            weighted_paths[weight_of_path].append(path)

    #print weighted_paths

    return weighted_paths


def compute_shortest_paths(H,id_source,id_target,distance_metric):

    shortest_paths=[]

    weighted_paths=compute_lenght_paths_on_residual(H,id_source,id_target,distance_metric,True)
    #print 'weighted_paths'
    #print weighted_paths

    minKey=float(sys.maxint)
    for key_path in weighted_paths:
        trunk_weigh=float('%.2f'%(float(key_path)))
        #print trunk_weigh
        if (trunk_weigh < minKey):
            minKey=trunk_weigh
            #print 'nuovo minkey'
            #print minKey

    minKey='%.2f'%(minKey)
    #print 'minkey selezionato e arrotondato'
    #print minKey
    shortest_paths=weighted_paths[minKey]

    #print 'shortest calcolati'
    #print shortest_paths
    return shortest_paths

def compute_my_betweeness_1(H,green_edges,distance_metric):

    global all_graph_paths

    epsilon_bet=0.1
    shortest_paths=[]
    betwenness_dict={}

    for node in H.nodes():
        betwenness_dict.update({node:0.0})


    #print 'Caloclo bet per nodo %d: '%(id_node)
    for edge in green_edges:
        id_source=edge[0]
        id_target=edge[1]
        arc=(id_source,id_target)
        arc_reverse=(id_target,id_source)
        shortest_paths=compute_shortest_paths_on_residual_for_betw_1(H,id_source,id_target,distance_metric)
        """
        if arc in all_graph_paths:
            paths= all_graph_paths[arc]
        elif arc_reverse in all_graph_paths:
            paths = all_graph_paths[arc_reverse]
        else:
            sys.exit('Errore in betwenees_1 non ce l arco verde in all_graph_paths')
        """
        #print 'path recuperati'
        #print paths
        #shortest_paths=compute_shortest_from_set(H,paths,distance_metric)
        #print shortest_paths
        #sys.exit(0)


        num_paths=len(shortest_paths)

        for path in shortest_paths:
            #print 'shortest calcolati tra %d-%d: '%(id_source,id_target)
            #print shortest_paths
            #print 'num path %d '%(num_paths)
            #print 'esamino path'
            #print path
            for id_node in path:
                node_betw_count=0
                if len(shortest_paths)==1:
                    if len(shortest_paths[0])==2:#one hop
                        #print 'valuto path one hop:'
                        #print shortest_paths
                        #if shortest_paths[0][0]==id_source and shortest_paths[0][1]==id_target:
                        if id_node in shortest_paths[0]:
                            node_betw_count+=epsilon_bet
                            #print 'aggiunto epsilon bet a %d'%id_node
                        #elif shortest_paths[0][1]==id_source and shortest_paths[0][0]==id_target:
                         #   node_betw_count+=epsilon_bet

                if (id_node!= id_source and id_node!=id_target):

                    #node=H.node[id_node]
                    count_occ=count_occurance(id_node,path)
                    #print '%d compare %d: '%(id_node,count_occ)
                    count_occ+=0.0
                    node_betw_count+=(count_occ/num_paths)

                if not betwenness_dict.has_key(id_node):
                    betwenness_dict.update({id_node:node_betw_count})
                else:
                    old_bet=betwenness_dict[id_node]
                    new_bet=old_bet+node_betw_count
                    betwenness_dict.update({id_node:new_bet})
                #print node_betw_count

    #print betwenness_dict


    for node in H.nodes():
        id_node=H.node[node]['id']
        H.node[node]['betweeness']=float('%.2f'%(betwenness_dict[id_node]))


    return betwenness_dict

def compute_my_betweeness_2(H,green_edges,code):

    shortest_paths=[]
    global betwenness_dict
    betwenness_dict={}
    global shortest_paths_for_bet
    shortest_paths_for_bet={}
    for node in H.nodes():
        id_node=H.node[node]['id']
        if id_node not in betwenness_dict:
            betwenness_dict.update({id_node:0.0})
    #print 'Dizionario inizializzato'
    #print betwenness_dict

    for edge in green_edges:
        residual_graph=nx.MultiGraph(H)
        #for edge in H.edges(data=True):
        #    print edge
        #print '-------------------------CONTROLLO SE SONO RESIDUI GLI ARCHI---'
        #for arco in residual_graph.edges(data=True):
        #    print arco
        #print 'esamino arco verde:'+str(edge)
        id_source=edge[0]
        id_target=edge[1]
        demand= edge[2]
        demand_flag=0
        arc=(id_source,id_target)
        #print '------------------------SHORTEST PATH CHE CONTRIBUISCONO ALLA BETW: coppia %d-%d = %d'%(id_source,id_target,demand)+' ---------------------------------'
        while (demand>0):
            #print 'grafo residuo'
            #for edge in residual_graph.edges(data=True):
            #    print edge
            total_capacity=0
            shortest_paths=compute_shortest_paths_on_residual(residual_graph,id_source,id_target,code)
            #print shortest_paths
            #salvo gli shortest path che contribuiscono alla betweenees del nodo per poterli usare nella funzione split
            if not shortest_paths_for_bet.has_key(arc):
                shortest_paths_for_bet.update({arc:[]})
            for path in shortest_paths:
                    shortest_paths_for_bet[arc].append(path)
            #-----------------------------------------------------------------------------------------------------------

            #print 'shortest tra %d-%d'%(id_source,id_target)
            #print shortest_paths
            paths_capacity=retrieve_capacity_paths(residual_graph,shortest_paths)
            #print 'capacita degli shortest selezionati'
            #print paths_capacity
            for key in paths_capacity:
                paths = paths_capacity[key]
                for single_path in paths:
                    #print 'previous total'
                    #print total_capacity
                    #print 'post increment'
                    total_capacity+= key+0.0
                    #print total_capacity


            #print "total capacity %d-%d"%(id_source,id_target)
            #print total_capacity

            for cap_key in paths_capacity:
                paths_key= paths_capacity[cap_key]
                for path in paths_key:
                    #print 'path esaminato:'
                    #print path
                    path_cap=cap_key + 0.0
                    alpha= cap_key/total_capacity
                    #print 'alpha per'
                    #print path
                    #print alpha
                    #print demand
                    if ( path_cap >= (alpha*demand) ):
                        #print 'sufficente'
                        demand_flag = 1
                        for id_node in path:
                            if id_node != id_source and id_node != id_target:
                                old_betw = betwenness_dict[id_node]
                                new_betw = old_betw + float(('%.2f'%(demand*alpha)))
                                betwenness_dict.update({id_node:new_betw})
                                #print 'betwenness aggiornata per %d'%(id_node)
                                #print betwenness_dict[id_node]
                    else:
                        #print 'non sufficiente'
                        for id_node in path:
                            #print id_node
                            if id_node != id_source and id_node != id_target:
                                old_betw = betwenness_dict[id_node]
                                new_betw = old_betw + path_cap
                                betwenness_dict.update({id_node:new_betw})
                                #print 'betwenness aggiornata per %d'%(id_node)
                                #print betwenness_dict[id_node]

                    for index in range(0,(len(path)-1),1):
                        source=path[index]
                        target=path[index+1]
                        key_dict=residual_graph[source][target]
                        #print 'prendo tutto gli archi tra %d-%d'%(source,target)
                        #print key_dict
                        for k in key_dict:
                            if residual_graph[source][target][k]['type']=='normal':
                                if residual_graph.has_edge(source,target,key=k):
                                    old_capacity=residual_graph[source][target][k]['capacity']
                                    #print 'old: %d'%(old_capacity)
                                    #print 'path cap: %d'%(path_cap)
                                    new_capacity=old_capacity-path_cap
                                    #print 'new cap: %d'%(new_capacity)
                                    residual_graph[source][target][k]['capacity'] = new_capacity
                                    if new_capacity<0:
                                        print 'CAPACITa RESIDUA NEGATIVAAAAA'
                                        sys.exit('CAPACITA NEGATIVA')

            if demand_flag == 1:
                demand=0
                #print 'domanda soddisfatta'
            else:
                demand -= total_capacity
                #print 'domanda ancora da soddisfare'

            residual_graph= nx.MultiGraph(get_residual_graph(residual_graph))

        residual_graph= nx.MultiGraph(get_residual_graph(residual_graph))

        #print '-------------DOPO DOMANDA SODDISFATTA ------------'
        #for arco2 in residual_graph.edges(data=True):
        #    print arco2
    for node in H.nodes():
        id_node=H.node[node]['id']
        H.node[node]['betweeness']=betwenness_dict[id_node]

    return betwenness_dict


def compute_my_betweeness_3(H,green_edges,distance_metric):

    sys.exit('Errore: bet aprox chiamata!!!')
    shortest_paths=[]
    global betwenness_dict
    betwenness_dict={}
    global shortest_paths_for_bet
    shortest_paths_for_bet={}
    global all_graph_paths
    for node in H.nodes():
        id_node=H.node[node]['id']
        if id_node not in betwenness_dict:
            betwenness_dict.update({id_node:0.0})
    #print 'Dizionario inizializzato'
    #print betwenness_dict

    for edge in green_edges:
        residual_graph=nx.MultiGraph(H)
        #print 'esamino arco verde:'+str(edge)
        id_source=edge[0]
        id_target=edge[1]
        demand= edge[2]
        arc=(id_source,id_target)
        #print '------------------------SHORTEST PATH CHE CONTRIBUISCONO ALLA BETW: coppia %d-%d = %d'%(id_source,id_target,demand)+' ---------------------------------'

        #lista di tutti i path tra source e target con relativi pesi
        weighted_paths=compute_lenght_paths(H,id_source,id_target,distance_metric,True)
        #print 'Path pesati'
        #print weighted_paths
        array_lenghts=[]
        for key in weighted_paths:
            if key not in array_lenghts:
                #print key
                array_lenghts.append(float(key))

        #ordina l'array per lunghezza
        array_lenghts.sort()
        #print 'array ordinato per lunghezza'
        #print array_lenghts

        if len(array_lenghts)==0:
            print 'Nessun Path disponibile per la domanda: %d-%d:'%(id_source,id_target)
            sys.exit('Errore in compute_my_betwenness_3: coppia di domanda non connessa !!!')

        flow_flag=False
        i=0
        total_capacity=0
        total_capacity_passing_node=0

        while(flow_flag == False):
            curr_length=array_lenghts[i]
            #insieme dei path minori di una certa lunghezza tra source e target
            paths_less_curr_lenght=compute_paths_less_of_lenght(weighted_paths,curr_length)
            #print paths_less_curr_lenght
            #denominatore della formula di centralita approssimata
            total_capacity=compute_total_flow_based_on_path_capacity(H,paths_less_curr_lenght)
            #print 'total_capacity e demand : %d-%d'%(total_capacity,demand)

            if total_capacity >= demand:
                #print 'trovato'
                flow_flag = True
            else:
                #print 'Continuo'
                i=i+1
        arc=(id_source,id_target)
        #aggiorno i paths che contribuiscono alla betweeness dell'arco verde
        if not shortest_paths_for_bet.has_key(arc):
            shortest_paths_for_bet.update({arc:[]})
        for path in paths_less_curr_lenght:
            shortest_paths_for_bet[arc].append(path)
        #print ' ????????????????????????????????????????????????????????????????????????????'
        #print shortest_paths_for_bet[arc]

        #aggiorna le betweeness dei nodi
        for node in H.nodes():
            id_node = H.node[node]['id']

            #paths che passano per il nodo e sono minori di una certa lunghezza tra source e sink
            paths_trough_node=paths_traverse_node(paths_less_curr_lenght,id_node)
            #numeratore della formula di centralita approssimata
            #print 'path attraversano %d '%(id_node)
            #print paths_trough_node
            total_capacity_passing_node=compute_total_flow_based_on_path_capacity(H,paths_trough_node)
            ratio=float(total_capacity_passing_node/total_capacity)
            #print 'ratio calcolato %f: '%(ratio*demand)
            old_betw = betwenness_dict[id_node]
            new_betw = old_betw + float(('%.2f'%(ratio*demand)))
            betwenness_dict.update({id_node:new_betw})
            #print 'betwenness aggiornata per %d'%(id_node)

    for node in H.nodes():
        id_node=H.node[node]['id']
        H.node[node]['betweeness']=betwenness_dict[id_node]

    print 'fine betwnees'
    return betwenness_dict


#old USARE OTTIMIZZATA (quesata calcola tutti i path)
def compute_my_betweeness_4(H,green_edges,distance_metric):

    shortest_paths=[]
    global betwenness_dict
    betwenness_dict={}
    global shortest_paths_for_bet
    shortest_paths_for_bet={}
    global all_graph_paths
    for node in H.nodes():
        id_node=H.node[node]['id']
        if id_node not in betwenness_dict:
            betwenness_dict.update({id_node:0.0})

    for edge in green_edges:
        residual_graph=nx.MultiGraph(H)
        id_source=edge[0]
        id_target=edge[1]
        demand= edge[2]
        arc=(id_source,id_target)
        #print '------------------------SHORTEST PATH CHE CONTRIBUISCONO ALLA BETW: coppia %d-%d = %f'%(id_source,id_target,demand)+' ---------------------------------'

        #lista di tutti i path tra source e target con relativi pesi
        weighted_paths=compute_lenght_paths(H,id_source,id_target,distance_metric,True)
        #print 'Path pesati'
        #print weighted_paths
        array_lenghts=[]
        for key in weighted_paths:
            if key not in array_lenghts:
                #print key
                array_lenghts.append(float(key))

        #ordina l'array per lunghezza
        array_lenghts.sort()
        #print 'array ordinato per lunghezza'
        #print array_lenghts

        if len(array_lenghts)==0:
            print 'Nessun Path disponibile per la domanda: %d-%d:'%(id_source,id_target)
            sys.exit('Errore in compute_my_betwenness_4: coppia di domanda non connessa !!!')

        flow_flag=False
        i=0
        total_flow=0
        total_flow_passing_node=0

        #trova l'insieme minimo (considernado le lunghezze) di path che fa passare almeno la domanda
        #print array_lenghts
        while(flow_flag == False):
            curr_length=array_lenghts[i]
            #insieme dei path minori di una certa lunghezza tra source e target
            #print 'Path della stessa lunghezza: %f'%(curr_length)
            paths_less_curr_lenght=compute_paths_less_of_lenght(weighted_paths,curr_length)
            #print paths_less_curr_lenght
            #denominatore della formula di centralita approssimata
            #total_capacity=compute_total_flow_based_on_path_capacity(H,paths_less_curr_lenght)
            total_flow=compute_total_flow_based_on_real_flow(H,paths_less_curr_lenght,id_source,id_target)
            #print 'total_flow e demand : %d-%f'%(total_flow,demand)

            if total_flow>= demand:
                #print 'trovato'
                flow_flag = True
            else:
                #print 'Continuo'
                i=i+1

        arc=(id_source,id_target)
        #aggiorno i paths che contribuiscono alla betweeness dell'arco verde
        if not shortest_paths_for_bet.has_key(arc):
            shortest_paths_for_bet.update({arc:[]})
        for path in paths_less_curr_lenght:
            shortest_paths_for_bet[arc].append(path)
        #print shortest_paths_for_bet[arc]

        #aggiorna le betweeness dei nodi
        for node in H.nodes():
            id_node = H.node[node]['id']

            #paths che passano per il nodo e sono minori di una certa lunghezza tra source e sink
            paths_trough_node=paths_traverse_node(paths_less_curr_lenght,id_node)
            #numeratore della formula di centralita approssimata
            #print 'path attraversano %d '%(id_node)
            #print paths_trough_node
            if len(paths_trough_node)>0:
                #total_flow_passing_node=compute_total_flow_based_on_real_flow(H,paths_trough_node,id_source,id_target)
                total_flow_passing_node=compute_total_flow_based_on_path_capacity(H,paths_trough_node)
                total_flow_capacity=0.0
                total_flow_capacity=compute_total_flow_based_on_path_capacity(H,paths_less_curr_lenght)
                ratio=float(total_flow_passing_node/total_flow_capacity)
                #print 'ratio calcolato %f: '%(ratio*demand)
                old_betw = betwenness_dict[id_node]
                new_betw = old_betw + float(('%.2f'%(ratio*demand)))
                betwenness_dict.update({id_node:new_betw})
                #print 'betwenness aggiornata per %d'%(id_node)

    for node in H.nodes():
        id_node=H.node[node]['id']
        H.node[node]['betweeness']=betwenness_dict[id_node]

    print 'fine betwnees'
    return betwenness_dict

#Ottimizzata
def compute_my_betweeness_4_opt(H,green_edges,distance_metric):

    shortest_paths=[]
    global betwenness_dict
    betwenness_dict={}
    global shortest_paths_for_bet
    #print shortest_paths_for_bet
    shortest_paths_for_bet={}
    #print shortest_paths_for_bet
    for node in H.nodes():
        id_node=H.node[node]['id']
        if id_node not in betwenness_dict:
            betwenness_dict.update({id_node:0.0})

    supply_graph=get_supply_graph(H,green_edges)
    star_time_bet=time.time()
    for edge in green_edges:
        residual_graph=nx.MultiGraph(supply_graph)
        id_source=edge[0]
        id_target=edge[1]
        demand= edge[2]
        arc=(id_source,id_target)
        #print '------------------------SHORTEST PATH CHE CONTRIBUISCONO ALLA BETW: coppia %d-%d = %f'%(id_source,id_target,demand)+' ---------------------------------'

        #lista di tutti i path tra source e target con relativi pesi
        #weighted_paths=compute_lenght_paths(H,id_source,id_target,distance_metric,True)
        paths_selected=[]
        demand_to_assign=demand
        flag_demand_satified=False
        while(flag_demand_satified==False):
            curr_shortest=my_dijkstra_shortest_path(residual_graph,id_source,id_target)
            if len(curr_shortest)==0:
                print 'Nessun Path disponibile per la domanda: %d-%d:'%(id_source,id_target)
                sys.exit('Errore in compute_my_betwenness_4_opt: coppia di domanda non connessa !!!')

            cap_path=get_capacity_of_path(residual_graph,curr_shortest)
            if cap_path>=demand_to_assign:
                flag_demand_satified=True

            else:
                reduce_capacity_path(residual_graph,curr_shortest,cap_path)

            demand_to_assign=demand_to_assign-cap_path
            paths_selected.append(curr_shortest)

        arc=(id_source,id_target)
        #aggiorno i paths che contribuiscono alla betweeness dell'arco verde
        if not shortest_paths_for_bet.has_key(arc):
            shortest_paths_for_bet.update({arc:[]})
        for path in paths_selected:
            #print 'aggiunto'
            shortest_paths_for_bet[arc].append(path)
        #print shortest_paths_for_bet[arc]

        #aggiorna le betweeness dei nodi
        nodes_to_update_bet=get_list_of_nodes_from_paths(paths_selected)
        #for node in H.nodes():
        for node in nodes_to_update_bet:
            id_node = H.node[node]['id']

            #paths che passano per il nodo e sono minori di una certa lunghezza tra source e sink
            paths_trough_node=paths_traverse_node(paths_selected,id_node)
            #numeratore della formula di centralita approssimata
            #print 'path attraversano %d '%(id_node)
            #print paths_trough_node
            if len(paths_trough_node)>0:
                #total_flow_passing_node=compute_total_flow_based_on_real_flow(H,paths_trough_node,id_source,id_target)
                total_flow_passing_node=compute_total_flow_based_on_path_capacity(H,paths_trough_node)
                total_flow_capacity=0.0
                total_flow_capacity=compute_total_flow_based_on_path_capacity(H,paths_selected)
                #print total_flow_passing_node
                #print total_flow_capacity
                ratio=float(total_flow_passing_node/total_flow_capacity)
                #print 'ratio calcolato %f: '%(ratio*demand)
                old_betw = betwenness_dict[id_node]
                new_betw = old_betw + float(('%.2f'%(ratio*demand)))
                betwenness_dict.update({id_node:new_betw})
                #print 'betwenness aggiornata per %d'%(id_node)

                #sys.exit(0)
    for node in H.nodes():
        id_node=H.node[node]['id']
        H.node[node]['betweeness']=betwenness_dict[id_node]

    #print 'fine betwnees_opt'
    #print shortest_paths_for_bet
    end_time_bet=round(time.time()-star_time_bet,3)
    return betwenness_dict,shortest_paths_for_bet,end_time_bet


def get_list_of_nodes_from_paths(list_paths):

    join=[]

    for curr_path in list_paths:
        join=list(set(join) | set(curr_path))

    #print 'Join'
    #print join
    return join


def compute_paths_less_of_lenght(weighted_paths,length):

    paths_selected=[]
    for key in weighted_paths:
        curr_key=float(key)

        if curr_key <= length:

            paths_of_curr_key=weighted_paths[key]
            for path in paths_of_curr_key:
                #print path
                if path not in paths_selected:
                    paths_selected.append(path)
                #else:
                #   sys.exit('IMPOSSIBILE DUE PATH UGUALI CON DIVERSA LUNGHEZZA')

    return paths_selected

def compute_total_flow_based_on_path_capacity(H,paths_less_curr_lenght):

    total_flow=0.0

    for path in paths_less_curr_lenght:

        minCap=compute_min_cap_of_path(H,path)
        total_flow=total_flow+minCap

    return total_flow



def compute_total_flow_based_on_real_flow(H,paths_less_curr_lenght,id_source,id_target):

    graph_of_paths=nx.MultiGraph()

    for path in paths_less_curr_lenght:

        add_path_to_graph(H,graph_of_paths,path)

    #compute max_flow on graph of paths
    max_flow=0.0
    max_flow=compute_max_flow(graph_of_paths,id_source,id_target)

    return max_flow


def add_path_to_graph(original_graph,graph_built,path):

    for node in path:
        if not graph_built.has_node(node):
            graph_built.add_node(node,id=node)



    for i in range(0,len(path)-1):
        source=path[i]
        target=path[i+1]
        if not graph_built.has_edge(source,target):
            if original_graph.has_edge(source,target):
                keydict=original_graph[source][target]
                for k in keydict:
                    if original_graph[source][target][k]['type']=='normal':
                        cap=original_graph[source][target][k]['capacity']
                        graph_built.add_edge(source,target,capacity=cap,type='normal')
            else:
                sys.exit('Errore in add_path_to_graph: arco del path inesistente')




def compute_min_cap_of_path(H,path):

    path_capacity=sys.maxint

    for i in range(0,(len(path)-1),1):
        id_source=path[i]
        id_target=path[(i+1)]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal':
                edge_capacity = H[id_source][id_target][k]['capacity']
                if edge_capacity < path_capacity:
                    path_capacity=edge_capacity
    return path_capacity

def paths_traverse_node(paths_less_curr_lenght,id_node):

    paths_selected=[]

    for path in paths_less_curr_lenght:
        source=path[0]
        sink=path[len(path)-1]
        if id_node in path:
            if id_node!=source and id_node!=sink:
                paths_selected.append(path)


    return paths_selected

def set_betwenness_from_dict(H,betwenness_dict):

    for node in H.nodes():
        id_node=H.node[node]['id']
        H.node[node]['betweeness']=betwenness_dict[id_node]


def compute_shortest_paths_on_residual(residual,id_source,id_target,distance_metric):

    shortest_paths=[]
    #print 'cammino tra %d- %d'%(id_source,id_target)
    #for edge in residual.edges(data=True):
    #    print edge
    weighted_paths=compute_lenght_paths_on_residual(residual,id_source,id_target,distance_metric,True)

    if (len(weighted_paths)>0):
        minKey=sys.maxint
        #print weighted_paths
        for key_path in weighted_paths:
            if (key_path<minKey):
                minKey=key_path

        #if minKey==sys.maxint:
        #    sys.exit('ERRORE COMPUTE SHORTEST PATH ON RESIDUAL')
        #else:
        shortest_paths=weighted_paths[minKey]

    #print 'shortest calcolati'
    #print shortest_paths
    return shortest_paths


def compute_shortest_paths_on_residual_for_betw_1(residual,id_source,id_target,distance_metric):

    shortest_paths=[]
    #print 'cammino tra %d- %d'%(id_source,id_target)
    #for edge in residual.edges(data=True):
    #    print edge
    weighted_paths=compute_lenght_paths_on_residual(residual,id_source,id_target,distance_metric,False)

    minKey=sys.maxint
    #print weighted_paths
    for key_path in weighted_paths:
        if (key_path<minKey):
            minKey=key_path

    #if minKey==sys.maxint:
    #    sys.exit('ERRORE COMPUTE SHORTEST PATH ON RESIDUAL')
    #else:
    shortest_paths=weighted_paths[minKey]

    #print 'shortest calcolati'
    #print shortest_paths
    return shortest_paths


def get_residual_graph(residual):
    edges_to_remove=[]
    #print 'archi pre saturazione:'
    #for edge in residual.edges(data=True):
    #    print edge

    for edge in residual.edges():
        #print 'esamino arco per vedere se  saturo'
        #print edge
        id_source=edge[0]
        id_target=edge[1]
        keydict=residual[id_source][id_target]
        #print 'keydict'
        #print keydict
        for k in keydict:
            #print 'k'
            #print k
            if residual.has_edge(id_source,id_target,key=k):
                if residual[id_source][id_target][k]['type']=='normal':
                    cap=residual[id_source][id_target][k]['capacity']
                    if cap==0:
                        #print 'arco da rimuovere %d-%d'%(id_source,id_target)
                        edge_sat = (id_source,id_target,k)
                        if not edge_sat in edges_to_remove:
                            edges_to_remove.append(edge_sat)

    for edge in edges_to_remove:
        source=edge[0]
        target=edge[1]
        k=edge[2]

        if residual.has_edge(source,target,key=k):
            residual.remove_edge(source,target,key=k)
            #print 'rimosso %d-%d'%(source,target)
        else:
            print 'arco saturo inesistente?'
            sys.exit('ERRORE ARCO SATURO INESISTENTE')

    #for edge in residual.edges(data=True):
     #   print edge

    return residual



def retrieve_capacity_paths(H,paths):
    dict_capacity={}

    for path in paths:
        path_capacity=sys.maxint
        for i in range(0,(len(path)-1),1):
            id_source=path[i]
            id_target=path[(i+1)]
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':
                    edge_capacity = H[id_source][id_target][k]['capacity']
                    if edge_capacity < path_capacity:
                        path_capacity=edge_capacity

        if not dict_capacity.has_key(path_capacity):
            dict_capacity.update({path_capacity:[]})
            dict_capacity[path_capacity].append(path)
        else:
            dict_capacity[path_capacity].append(path)

    return dict_capacity

def count_occurance(elem, path):


    count=0
    #for path in paths:

    count+=path.count(elem)

    return count

def write_stat_num_reparation(path_to_stats,filename_stat,prob_edge,seed_random,alfa,
                          num_rip_isp_nodes,num_rip_isp_edges,nodes_truely_recovered_isp,edges_truely_recovered_isp,        #ISP
                          num_rip_optimal_nodes,num_rip_optimal_edges,#OPTIMAL
                          num_rip_mult_nodes,num_rip_mult_edges,num_rip_truely_mult_nodes,num_rip_truely_mult_edges,       #Multicommodity generale
                          num_rip_mult_worst_nodes,num_rip_mult_worst_edges, #Multicommodity worst
                          num_rip_mult_best_nodes,num_rip_mult_best_edges,    #Multicommodity best
                          num_rip_shortest_nodes,num_rip_shortest_edges,num_rip_truely_shortest_nodes, num_rip_truely_shortest_edges,      #Shortest Based
                          num_rip_ranked_nodes,num_rip_ranked_edges,          #Ranked based
                          num_rip_all_nodes,num_rip_all_edges,                #All repairs algorithm
                          num_sim,
                          flag_solution_MCG,
                          total_demand_of_graph,
                          demand_not_satisfied_sb,
                          num_rip_ranked_comm_nodes,num_rip_ranked_comm_edges,
                          num_rip_ranked_no_comm_nodes,num_rip_ranked_no_comm_edges,
                          demand_not_satisfied_rb_comm,
                          flow_c_value,                                        #valore di flusso fixed assegnato a tutte le coppie
                          number_of_couple,                                     #numero di coppie di domanda della simulazione
                          var_distruption):                                     #varianza delle distruzione

        path_to_file_stat=path_to_stats+filename_stat
        print path_to_file_stat
        if not os.path.exists(path_to_file_stat):
            #print 'non esiste lo creo'
            file=open(path_to_file_stat,'w+')
            name_of_colunms="Prob_Edge\tSeed\t\tAlfa\tISP_Nodes\tISP_Edges\tTotal_ISP\tOPT_Nodes\tOPT_Edges\tTotal_OPT\tMCG_Nodes\tMCG_Edges\tTotal_MCG\tMCW_Nodes\tMCW_Edges\tTotal_MCW\tMCB_Nodes\tMCB_Edges\tTotal_MCB\tSRT_Nodes\tSRT_Edges\tTotal_SRT\tRNK_Nodes\tRNK_Edges\tTotal_RNK\tALL_Nodes\tALL_Edges\tTotal_ALL\tTotal_DEM\tSRT_SATIS\t%_DEM_SAT\tRNK_N_COM\tRNK_E_COM\tTot_RNK_C\tRNK_N_NC\tRNK_E_NC\tTot_RNK_NC\tRNK_SATIS\t%_DEM_RNK\tFLOW_FIXD\tNUM_COUPL\tVAR_DISTR\tERROR_FLG\tFlag_MCG\t\tDirImages\n"
            file.write(name_of_colunms)
            file.close

        tot_rip_isp=(num_rip_isp_nodes+num_rip_isp_edges)
        tot_truely_rip_isp=(nodes_truely_recovered_isp+edges_truely_recovered_isp)
		
        tot_rip_opt=(num_rip_optimal_nodes+num_rip_optimal_edges)
        tot_rip_mcg=(num_rip_mult_nodes+num_rip_mult_edges)
        tot_truely_rip_mcg=(num_rip_truely_mult_nodes+num_rip_truely_mult_edges)
		
        tot_rip_mcw=(num_rip_mult_worst_nodes+num_rip_mult_worst_edges)
        tot_rip_mcb=(num_rip_mult_best_nodes+num_rip_mult_best_edges)
        tot_rip_srt=(num_rip_shortest_nodes+num_rip_shortest_edges)
        tot_truely_rip_srt=(num_rip_truely_shortest_nodes+num_rip_truely_shortest_edges)
		
		
        tot_rip_rnk=(num_rip_ranked_nodes+num_rip_ranked_edges)
        tot_rip_all=(num_rip_all_nodes+num_rip_all_edges)
        tot_rip_rnk_com=(num_rip_ranked_comm_nodes+num_rip_ranked_comm_edges)
        tot_rip_rnk_no_com=(num_rip_ranked_no_comm_nodes+num_rip_ranked_no_comm_edges)

        print 'tot_isp %d = %d + %d'%(tot_rip_isp, num_rip_isp_nodes,num_rip_isp_edges)
        print 'tot_isp_truely %d = %d + %d'%(tot_truely_rip_isp, nodes_truely_recovered_isp,edges_truely_recovered_isp)
		
        print 'tot_opt %d = %d + %d'%(tot_rip_opt, num_rip_optimal_nodes,num_rip_optimal_edges)
        print 'tot_mcg %d = %d + %d'%(tot_rip_mcg, num_rip_mult_nodes,num_rip_mult_edges)
        print 'tot_mcg_truely %d = %d + %d'%(tot_truely_rip_mcg, num_rip_truely_mult_nodes,num_rip_truely_mult_edges)
		
        print 'tot_mcw %d = %d + %d'%(tot_rip_mcw, num_rip_mult_worst_nodes,num_rip_mult_worst_edges)
        print 'tot_mcb %d = %d + %d'%(tot_rip_mcb, num_rip_mult_best_nodes, num_rip_mult_best_edges)
        print 'tot_srt %d = %d + %d'%(tot_rip_srt, num_rip_shortest_nodes, num_rip_shortest_edges)
        print 'tot_srt_truely %d = %d + %d'%(tot_truely_rip_srt, num_rip_truely_shortest_nodes, num_rip_truely_shortest_edges)
		
		
        print 'tot_rnk %d = %d + %d'%(tot_rip_rnk, num_rip_ranked_nodes, num_rip_ranked_edges)
        print 'tot_rnk_com %d = %d + %d'%(tot_rip_rnk_com, num_rip_ranked_comm_nodes, num_rip_ranked_comm_edges)
        print 'tot_rnk_no_com %d = %d + %d'%(tot_rip_rnk_no_com, num_rip_ranked_no_comm_nodes, num_rip_ranked_no_comm_edges)
        print 'tot_all %d = %d + %d'%(tot_rip_all, num_rip_all_nodes, num_rip_all_edges)

        percent_of_demand=0.0
        demand_satisfied=0
        demand_satisfied=int(total_demand_of_graph-demand_not_satisfied_sb)
        percent_of_demand=int(((demand_satisfied/total_demand_of_graph)*100))
        print 'total demand: %f'%(total_demand_of_graph)
        print 'demand not satisfied shortest: %f'%(demand_not_satisfied_sb)
        print 'demand satisfied by shortest: %f'%(demand_satisfied)
        print 'Perc of demand satisfied by shortest: %d'%(percent_of_demand)

        percent_of_demand_rnk=0.0
        demand_satisfied_rnk=0
        demand_satisfied_rnk=int(total_demand_of_graph-demand_not_satisfied_rb_comm)
        percent_of_demand_rnk=int(((demand_satisfied_rnk/total_demand_of_graph)*100))
        print 'demand not satisfied ranked comm: %f'%(demand_not_satisfied_rb_comm)
        print 'demand satified by ranked comm: %f'%(demand_satisfied_rnk)
        print 'Perc of demand satisfied by rank comm: %d'%(percent_of_demand_rnk)

        total_demand_of_graph=int(total_demand_of_graph)



        if flag_solution_MCG==True:
            mcg_solution='SI'
        else:
            mcg_solution='-'



        error='-'
        #CONTROLLO SE QUALCHE ALGORITMO HA FATTO MEGLIO DELL'OTTIMO, IN CASO SEGNALO ERRORE
        if tot_rip_opt > tot_rip_isp or tot_rip_opt > tot_rip_mcg or tot_rip_opt > tot_rip_mcw or tot_rip_opt > tot_rip_mcb or tot_rip_opt > tot_rip_rnk or tot_rip_opt > tot_rip_all or tot_rip_opt > tot_rip_rnk_no_com:
            error='SI'
            print 'Errore: Num Riparazione Ottimo peggiore di qualche altro algoritmo!'
            sys.exit('Errore: Num Riparazione Ottimo peggiore di qualche altro algoritmo!')

        """
        #controllo con shortest, che puo fare meno, ma deve soddisfare meno domanda
        if tot_rip_opt > tot_rip_srt:
            #controlla la domanda soddisfatta
            if total_demand_of_graph==demand_satisfied:
                error='SI'
                print 'Errore: Num Riparazione Ottimo peggiore di shortest, che ha soddisfatto tutta la domanda!'
                sys.exit('Errore: Num Riparazione Ottimo peggiore di shortest, che ha soddisfatto tutta la domanda!')
        """

        #controllo con rank commitment, che puo fare meno, ma deve soddisfare meno domanda
        if tot_rip_opt > tot_rip_rnk_com:
            #controlla la domanda soddisfatta
            if total_demand_of_graph==demand_satisfied_rnk:
                error='SI'
                print 'Errore: Num Riparazione Ottimo peggiore di rank con commitment, che ha soddisfatto tutta la domanda!'
                sys.exit('Errore: Num Riparazione Ottimo peggiore di rank con commitment, che ha soddisfatto tutta la domanda!')

        #CONTROLLO SE QUALCHE ALGORITMO HA FATTO PEGGIO DI ALL REPAIRS, IN CASO SEGNALO ERRORE
        if tot_rip_all < tot_rip_isp  or tot_rip_all < tot_rip_opt or tot_rip_all < tot_rip_mcg or tot_rip_all < tot_rip_mcw or tot_rip_all < tot_rip_mcb or tot_rip_all < tot_rip_srt or tot_rip_all < tot_rip_rnk:
            error='SI'
            print 'Errore: Algoritmo ALL ha fatto meglio di qualche altro algoritmo!'
            sys.exit('Errore: Errore: Algoritmo ALL ha fatto meglio di qualche altro algoritmo!')

        #CONTROLLO SE BEST MULTY HA FATTO PEGGIO DI WORST MULTY, IN CASO SEGNALO ERRORE
        if tot_rip_mcb > tot_rip_mcw:
            error='SI'
            print 'Errore: Algoritmo Multicommodity Best ha fatto peggio del Multicommodity Worst!'
            sys.exit('Errore: Algoritmo Multicommodity Best ha fatto peggio del Multicommodity Worst!')

        file=open(path_to_file_stat,'a')
        raw_line=str(prob_edge)+'\t\t'+str(seed_random)+'\t\t'+str(alfa)+'\t\t'+str(num_rip_isp_nodes)+'\t\t'+str(num_rip_isp_edges)+'\t\t'+str(tot_rip_isp)+'\t\t'+str(num_rip_optimal_nodes)+'\t\t'+str(num_rip_optimal_edges)+'\t\t'+str(tot_rip_opt)+'\t\t'+str(num_rip_mult_nodes)+'\t\t'+str(num_rip_mult_edges)+'\t\t'+str(tot_rip_mcg)+'\t\t'+str(num_rip_mult_worst_nodes)+'\t\t'+str(num_rip_mult_worst_edges)+'\t\t'+str(tot_rip_mcw)+'\t\t'+str(num_rip_mult_best_nodes)+'\t\t'+str(num_rip_mult_best_edges)+'\t\t'+str(tot_rip_mcb)+'\t\t'+str(num_rip_shortest_nodes)+'\t\t'+str(num_rip_shortest_edges)+'\t\t'+str(tot_rip_srt)+'\t\t'+str(num_rip_ranked_nodes)+'\t\t'+str(num_rip_ranked_edges)+'\t\t'+str(tot_rip_rnk)+'\t\t'+str(num_rip_all_nodes)+'\t\t'+str(num_rip_all_edges)+'\t\t'+str(tot_rip_all)+'\t\t'+str(total_demand_of_graph)+'\t\t'+str(demand_satisfied)+'\t\t'+str(percent_of_demand)+'\t\t'+str(num_rip_ranked_comm_nodes)+'\t\t'+str(num_rip_ranked_comm_edges)+'\t\t'+str(tot_rip_rnk_com)+'\t\t'+str(num_rip_ranked_no_comm_nodes)+'\t\t'+str(num_rip_ranked_no_comm_edges)+'\t\t'+str(tot_rip_rnk_no_com)+'\t\t'+str(demand_satisfied_rnk)+'\t\t'+str(percent_of_demand_rnk)+'\t\t'+str(flow_c_value)+'\t\t'+str(number_of_couple)+'\t\t'+str(var_distruption)+'\t\t'+error+'\t\t'+str(mcg_solution)+'\t\t'+'Simulazione_'+str(num_sim)+'\n'
        file.write(raw_line)
        file.close()
		
def write_destroyed_graph(nodes_destroyed,edges_destroyed,filename_graph,path_to_stats):
    path_to_file=path_to_stats+filename_graph+'_Destroyed.txt'
    print path_to_file
    #if not os.path.exists(path_to_file):
    file=open(path_to_file,'w')

    for node in nodes_destroyed:
        file.write(str(node)+'\n')

    file.write('stop\n')

    for edge in edges_destroyed:
        edge_str='('+str(edge[0])+','+str(edge[1])+')'
        #print edge_str
        file.write(edge_str+'\n')

    file.close()

    return path_to_file

#Diman Added
def write_really_destroyed_graph(nodes_really_destroyed,edges_really_destroyed,filename_graph,path_to_stats):
    path_to_file=path_to_stats+filename_graph+'_Really_Destroyed.txt'
    print path_to_file
    #if not os.path.exists(path_to_file):
    file=open(path_to_file,'w')

    for node in nodes_really_destroyed:
        file.write(str(node)+'\n')

    file.write('stop\n')

    for edge in edges_really_destroyed:
        edge_str='('+str(edge[0])+','+str(edge[1])+')'
        #print edge_str
        file.write(edge_str+'\n')

    file.close()

    return path_to_file
#Diman Added
def check_if_path_exist(residualGraph,path):

    exist=True

    for i in range(0,len(path)-1,1):
        source=path[i]
        target=path[i+1]
        if residualGraph.has_edge(source,target):
            keydict=residualGraph[source][target]
            count=0
            for k in keydict:
                if residualGraph.has_edge(source,target,key=k):
                    if residualGraph[source][target][k]['type']=='normal' and residualGraph[source][target][k]['type']!='green':
                        count+=1
                else:
                    exist=False
                    return exist

            if count==0:
                exist=False
                return exist
        else:
            exist=False
            return exist

    return exist


def compute_shortest_passing_bc(residualGraph,id_bc,green_edges):

    #print 'used path'
    #print used_paths
    global shortest_paths_for_bet
    #print 'shortest paths for bet'
    #print shortest_paths_for_bet
    shortest_passing_bc={}
    for edge in green_edges:
        arc=(edge[0],edge[1])
        arc_reverse=(edge[1],edge[0])
        if shortest_paths_for_bet.has_key(arc):
            paths=shortest_paths_for_bet[arc]
        elif shortest_paths_for_bet.has_key(arc_reverse):
            paths=shortest_paths_for_bet[arc_reverse]
            #print paths
        else:
            sys.exit('ERRORE in compute shortest passing_bc: Non presente arco verde nel dizionario dei shortest path')
        for path in paths:
            if id_bc in path and path[0]!=id_bc and path[len(path)-1]!=id_bc:
                if check_if_path_exist(residualGraph,path):
                    if not shortest_passing_bc.has_key(edge):
                        shortest_passing_bc.update({edge:[]})
                        shortest_passing_bc[edge].append(path)
                    else:
                        shortest_passing_bc[edge].append(path)


    #print shortest_passing_bc
    return shortest_passing_bc


def retrieve_green_couple_passing_bc_from_dict(shortest_dict_bc):

    green_couple_bc=[]

    for key in shortest_dict_bc:
        if key not in green_couple_bc:
            green_couple_bc.append(key)
        else:
            sys.exit('ERRORE IN RETRIEVE GREEN COUPLE: piu volte stesso arco verde in dizionario')

    return green_couple_bc

def compute_shortest_from_set(residualGraph,paths,distance_metric):
    count=0
    min_lenght=sys.maxint
    curr_lenght=0.0
    path_selected=None
    dict_path_weighted={}
    #print len(paths)
    j=-1
    #print paths
    if len(paths)==0:
        path_selected=None
        return path_selected

    for path in paths:
        curr_lenght=0.0
        j=j+1
        #print 'iterazione %d'%(j)
        flag=False
        #print path
        for i in range(0,len(path)-1,1):
            source=path[i]
            target=path[i+1]
            #print 'esamino arco %d-%d'%(source,target)

            keydict=residualGraph[source][target]
            for k in keydict:
                if residualGraph.has_edge(source,target,key=k):
                    if residualGraph[source][target][k]['type']=='normal':
                        cap_edge=residualGraph[source][target][k]['capacity']
                        #lenght= (1.0/cap_edge)   #COMMMENTATO TEMPORANEMANETE
                        lenght=distance_node(residualGraph,source,target,distance_metric)
                        curr_lenght=curr_lenght +lenght
                        #print '1.0/%f = %f --total= %f'%(cap_edge,lenght,curr_lenght)
                    #else:
                     #   sys.exit('Compute shortest path from set: arco non normal')
                else:
                    flag=True

        if flag==False:
            if curr_lenght not in dict_path_weighted:
                dict_path_weighted.update({curr_lenght:[]})
                dict_path_weighted[curr_lenght].append(path)
            else:
                dict_path_weighted[curr_lenght].append(path)

            if curr_lenght<=min_lenght:
                #print 'trovato'
                path_selected=path
                min_lenght=curr_lenght
                #print path_selected

    #print 'Lunghezza paths'
    #print dict_path_weighted
    sorted_dict=collections.OrderedDict(sorted(dict_path_weighted.items()))
    #print sorted_dict
    #print 'shortest selected for implementing pruning'
    #print path_selected

    return path_selected

"""
def get_shortest_path_to_prune(residualGraph,couple_green,distance_metric):

    #print 'CONTROLLO GL SHORTEST PASS PER Bc per couple_green: %d-%d-%d'%(couple_green[0],couple_green[1],couple_green[2])
    #print shortest_pass_bc
    #paths_of_couple=shortest_pass_bc[couple_green]
    id_source=couple_green[0]
    id_target=couple_green[1]
    shortest_selected=None
    graph_dict=convert_graph_to_dict(residualGraph)
    #paths=find_all_paths(graph_dict,id_source,id_target,[])

    shortest_selected=compute_shortest_from_set(residualGraph,paths,distance_metric)
    #print 'path implementante: '
    #print shortest_selected
    return shortest_selected
"""



def get_graph_from_destroyed_graph(H):

    new_graph=nx.MultiGraph(H)
    edges_to_remove=[]
    nodes_to_remove=[]
    for edge in new_graph.edges():
        source=edge[0]
        target=edge[1]
        if new_graph.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type']!='green' and H[source][target][k]['status']=='destroyed':
                    arc=(source,target,k)
                    arc_reverse=(target,source,k)
                    if arc not in edges_to_remove and arc_reverse not in edges_to_remove:
                        edges_to_remove.append(arc)

    #BISOGNA RIMUOVERE ANCHE I NODI DISTRUTTI, E TUTTI GLI ARCHI INCIDENTI
    for node in H.nodes():
        if H.node[node]['status']=='destroyed':
            nodes_to_remove.append(node)
            """
            #recupera gli archi incidenti
            for edge in H.edges():
                if node==edge[0] or node==edge[1]:
                    keydict=H[edge[0]][edge[1]]
                    for k in keydict:
                        if H[edge[0]][edge[1]][k]['type']=='normal':
                            arco=(edge[0],edge[1],k)
                            arco_reverse=(edge[1],edge[0],k)
                            if arco not in edges_to_remove and arco_reverse not in edges_to_remove:
                                edges_to_remove.append(arc)
            """
    #print 'da rimuovere'
    #print edges_to_remove
    #print 'nodi da rimuovere'
    #print nodes_to_remove
    #rimuovi archi distrutti
    for arc in edges_to_remove:
        new_graph.remove_edge(u=arc[0],v=arc[1],key=arc[2])

    #rimuovi nodi
    for id_nodo in nodes_to_remove:
        new_graph.remove_node(id_nodo)

    #my_draw(new_graph,'1-Grafo_Distrutto')
    #sys.exit(0)
    """
    for node in new_graph.nodes():
        id_node=new_graph.node[node]['id']
        if (get_degree_of_node(new_graph,id_node))==0:
            new_graph.remove_node(id_node)
    """
    return new_graph

#Diman Added
def get_graph_from_truely_destroyed_graph(H):

    new_graph=nx.MultiGraph(H)
    edges_to_remove=[]
    nodes_to_remove=[]
    for edge in new_graph.edges():
        source=edge[0]
        target=edge[1]
        if new_graph.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type']!='green' and H[source][target][k]['true_status']=='destroyed':
                    arc=(source,target,k)
                    arc_reverse=(target,source,k)
                    if arc not in edges_to_remove and arc_reverse not in edges_to_remove:
                        edges_to_remove.append(arc)

    #BISOGNA RIMUOVERE ANCHE I NODI DISTRUTTI, E TUTTI GLI ARCHI INCIDENTI
    for node in H.nodes():
        if H.node[node]['true_status']=='destroyed':
            nodes_to_remove.append(node)
            """
            #recupera gli archi incidenti
            for edge in H.edges():
                if node==edge[0] or node==edge[1]:
                    keydict=H[edge[0]][edge[1]]
                    for k in keydict:
                        if H[edge[0]][edge[1]][k]['type']=='normal':
                            arco=(edge[0],edge[1],k)
                            arco_reverse=(edge[1],edge[0],k)
                            if arco not in edges_to_remove and arco_reverse not in edges_to_remove:
                                edges_to_remove.append(arc)
            """
    #print 'da rimuovere'
    #print edges_to_remove
    #print 'nodi da rimuovere'
    #print nodes_to_remove
    #rimuovi archi distrutti
    for arc in edges_to_remove:
        new_graph.remove_edge(u=arc[0],v=arc[1],key=arc[2])

    #rimuovi nodi
    for id_nodo in nodes_to_remove:
        new_graph.remove_node(id_nodo)

    #my_draw(new_graph,'1-Grafo_Distrutto')
    #sys.exit(0)
    """
    for node in new_graph.nodes():
        id_node=new_graph.node[node]['id']
        if (get_degree_of_node(new_graph,id_node))==0:
            new_graph.remove_node(id_node)
    """
    return new_graph
#Diman Added
def get_multiple_shortest_path_no_ramification_to_prune(H,distance_metric):

    green_edges=get_green_edges(H)
    paths_to_prune=[]
    edges_to_prune=[]
    global shortest_paths_for_bet
    #print shortest_paths_for_bet
    for couple in green_edges:
        id_source=couple[0]
        id_target=couple[1]
        edge=(id_source,id_target)
        if edge in shortest_paths_for_bet:
            shortest_paths=shortest_paths_for_bet[edge]
            #print shortest_paths
            shortest_path=compute_shortest_from_set(H,shortest_paths,distance_metric)
            #print shortest_path
            if len(shortest_path)==0:
                sys.exit('Errore in get_multiple_path_no_ramification: non esiste lo shortest path')

            if check_if_have_ramification(H,shortest_path)==False:
                if shortest_path not in paths_to_prune:
                    paths_to_prune.append(shortest_path)
                else:
                    sys.exit('Errore in get_multiple_path_no_ramification: due volte stesso path pruning')
                if couple not in edges_to_prune:
                    edges_to_prune.append(couple)
                else:
                    sys.exit('Errore in get_multiple_path_no_ramification: duev olte stessa coppia pruning')
        else:
            print 'coppia mancante'
            print couple
            sys.exit('Errore in get_multiple_path_no_ramification: coppia non presente nel dizionario degli shortest che contribuiscono alla bet')

    return paths_to_prune,edges_to_prune



def get_list_nodes_from_green_edges(green_edges):

    green_nodes=[]

    for couple in green_edges:
        id_source=couple[0]
        id_target=couple[1]
        if id_source not in green_nodes:
            green_nodes.append(id_source)
        if id_target not in green_nodes:
            green_nodes.append(id_target)

    return green_nodes

def get_multiple_path_no_ramification_to_prune(H,temp_graph_supply,destroyed_graph,distance_metric):

    #prendo i nodi verdi attuali (quindi considero quelli che sono stati gia risolti o spllitati
    green_edges=get_green_edges(temp_graph_supply)
    list_green_nodes=get_list_nodes_from_green_edges(green_edges)
    paths_to_prune=[]
    edges_to_prune=[]
    paths_available=[]
    #global shortest_paths_for_bet
    #print shortest_paths_for_bet

    #considero tutti i percorsi sul grafo originale, non quello solo distrutto e neanche quello su cui si fa split/pruning
    #graph_dict_original=convert_graph_to_dict(H)
    supply_graph=get_supply_graph(temp_graph_supply,green_edges)
    #my_draw(supply_graph,'last_supply_graph')
    for couple in green_edges:
        id_source=couple[0]
        id_target=couple[1]
        edge=(id_source,id_target)
        #paths=find_all_paths(graph_dict_original,id_source,id_target,[])

        #Modifica Ottimizzazione
        shortest_path=my_dijkstra_shortest_path(supply_graph,id_source,id_target)

        if check_if_path_exist(destroyed_graph,shortest_path)==True:
            #controllo se lo shortest path sul grafo inizialmente distrutto esiste anche sul grafo funzionante(cioe quello che sto ricostruendo)

            ramification_flag=False
            green_nodes_flag=False
            reach_a_green_node_flag=False
            #cerco se ha ramificazioni sul grafo originale e considerando i nodi verdi attuali sul su cui facciamo split and prune
            ramification_flag,green_nodes_flag=check_if_have_ramification(H,list_green_nodes,shortest_path)

            if green_nodes_flag==False:
                if ramification_flag==False:
                    if shortest_path not in paths_available:
                        #print 'path senza ramificazioni aggiunto per il pruning '
                        #print path
                        paths_available.append(shortest_path)
                else: # il path ha ramificazioni, bisogna controllare se raggiunge i nodi verdi
                    reach_a_green_node_flag=check_if_reach_a_green_node(H,list_green_nodes,shortest_path)
                    if reach_a_green_node_flag==False:
                        #ho trovato un cammino con ramificazione che non porta a nessun altro nodo verde
                            if shortest_path not in paths_available:
                                #print 'path con ramificazioni aggiunto per il pruning'
                                #print path
                                paths_available.append(shortest_path)

            if len(paths_available)>0:
                if len(paths_available)>=2:
                    print paths_available
                    #sys.exit('errore in get_path_no_ramification: due shortest impossibile')
                #shortest=compute_shortest_from_set(destroyed_graph,paths_available,distance_metric)
                shortest=paths_available[0]
                if shortest not in paths_to_prune:
                    paths_to_prune.append(shortest)
                #else:
                    #print shortest
                    #print paths_to_prune
                #    sys.exit('Errore in get_multiple_path_no_ramification: due volte stesso path pruning')

                    if couple not in edges_to_prune:
                        edges_to_prune.append(couple)
                    else:
                        sys.exit('Errore in get_multiple_path_no_ramification: duev olte stessa coppia pruning')


    return paths_to_prune,edges_to_prune


def get_multiple_path_no_ramification_to_prune_after_split(H,temp_graph_supply,destroyed_graph,distance_metric,couple_split):

    #prendo i nodi verdi attuali (quindi considero quelli che sono stati gia risolti o spllitati
    green_edges=get_green_edges(temp_graph_supply)
    list_green_nodes=get_list_nodes_from_green_edges(green_edges)
    paths_to_prune=[]
    edges_to_prune=[]
    #global shortest_paths_for_bet
    #print shortest_paths_for_bet
    #global all_graph_paths
    supply_graph=get_supply_graph(temp_graph_supply,green_edges)
    for couple in couple_split:
        paths_available=[]
        id_source=couple[0]
        id_target=couple[1]
        edge=(id_source,id_target)
        edge_reverse=(id_target,id_source)

        #Modifica Ottimizzazione
        shortest_path=my_dijkstra_shortest_path(supply_graph,id_source,id_target)

        if check_if_path_exist(destroyed_graph,shortest_path)==True:
            #controllo se lo shortest path sul grafo inizialmente distrutto esiste anche sul grafo funzionante(cioe quello che sto ricostruendo)

            ramification_flag=False
            green_nodes_flag=False
            reach_a_green_node_flag=False
            #cerco se ha ramificazioni sul grafo originale e considerando i nodi verdi attuali sul su cui facciamo split and prune
            ramification_flag,green_nodes_flag=check_if_have_ramification(H,list_green_nodes,shortest_path)

            if green_nodes_flag==False:
                if ramification_flag==False:
                    if shortest_path not in paths_available:
                        #print 'path senza ramificazioni aggiunto per il pruning '
                        #print path
                        paths_available.append(shortest_path)
                else: # il path ha ramificazioni, bisogna controllare se raggiunge i nodi verdi
                    reach_a_green_node_flag=check_if_reach_a_green_node(H,list_green_nodes,shortest_path)
                    if reach_a_green_node_flag==False:
                        #ho trovato un cammino con ramificazione che non porta a nessun altro nodo verde
                            if shortest_path not in paths_available:
                                #print 'path con ramificazioni aggiunto per il pruning'
                                #print path
                                paths_available.append(shortest_path)

            if len(paths_available)>0:
                if len(paths_available)>=2:
                    print paths_available
                    #sys.exit('errore in get_path_no_ramification: due shortest impossibile')
                #shortest=compute_shortest_from_set(destroyed_graph,paths_available,distance_metric)
                shortest=paths_available[0]
                if shortest not in paths_to_prune:
                    paths_to_prune.append(shortest)
                #else:
                    #print shortest
                    #print paths_to_prune
                #   sys.exit('Errore in get_multiple_path_no_ramification: due volte stesso path pruning')

                    if couple not in edges_to_prune:
                        edges_to_prune.append(couple)
                    else:
                        sys.exit('Errore in get_multiple_path_no_ramification: duev olte stessa coppia pruning')

    return paths_to_prune,edges_to_prune





#Commentata perche gia inglobata in quella senza ramificazioni
"""
def get_multiple_path_with_ramification_to_prune(destroyed_graph,distance_metric):

    green_edges=get_green_edges(destroyed_graph)
    paths_to_prune=[]
    edges_to_prune=[]

    global shortest_paths_for_bet
    #print shortest_paths_for_bet

    graph_dict=convert_graph_to_dict(destroyed_graph)

    for couple in green_edges:
        id_source=couple[0]
        id_target=couple[1]
        edge=(id_source,id_target)
        paths=find_all_paths(graph_dict,id_source,id_target,[])
        paths_available=[]
        print 'path da considerare per la coppia %d-%d:'%(id_source,id_target)
        print paths
        for path in paths:
            ramification_flag=False
            green_nodes_flag=False
            ramification_flag,green_nodes_flag=check_if_have_ramification(destroyed_graph,path)
            if ramification_flag==True and green_nodes_flag==False:
                print 'ramificazione trovata'
                reach_green_nodes_flag=check_if_reach_a_green_node(destroyed_graph,path)
                if reach_green_nodes_flag==False:
                    if path not in paths_available:
                        paths_available.append(path)

        if len(paths_available)>0:
            shortest=compute_shortest_from_set(destroyed_graph,paths_available,distance_metric)
            if shortest not in paths_to_prune:
                paths_to_prune.append(shortest)
            else:
                print shortest
                print paths_to_prune
                sys.exit('Errore in get_multiple_path_no_ramification: due volte stesso path pruning')

            if couple not in edges_to_prune:
                edges_to_prune.append(couple)
            else:
                sys.exit('Errore in get_multiple_path_no_ramification: duev olte stessa coppia pruning')

    return paths_to_prune,edges_to_prune


"""

def check_if_have_ramification(H,list_green_nodes,path):

    ramification_flag=False
    green_nodes_flag=False
    #print ' path da controllare se ha ramificazioni'
    #print path
    for i in range(1,len(path)-1,1):
        id_source=path[i]
        id_target=path[i+1]
        if H.has_edge(id_source,id_target):
            degree_node=0
            #print 'pre degree'
            degree_node=get_degree_of_node(H,id_source)
            #print 'grado del nodo %d = %d'%(id_source,degree_node)
            if degree_node==1:
                sys.exit('Errore check_if_have_ramification: nodo interno ad un path con degree 1')
            if degree_node>2:
                ramification_flag=True
            if id_source in list_green_nodes:
                green_nodes_flag=True
        else:
            sys.exit('Errore check_if_have_ramification: arco inesistente nello shortest path')

        if ramification_flag==True or green_nodes_flag==True:
            #print ramification_flag
            return ramification_flag,green_nodes_flag

    #print ramification_flag
    return ramification_flag,green_nodes_flag



def check_if_reach_a_green_node(H,list_green_nodes,path):

    green_nodes_flag=False

    #print 'path con ramificazione'
    #print path
    source_node=path[0]
    target_node=path[len(path)-1]
    #sono sicuro che esiste il nodo 1 perche questo path ha ramificazioni nei nodi intermedi
    middle_node=path[1]
    #print 'nodo verde raggiundo da %d  ??'%(middle_node)
    green_nodes_flag,node_green_reach=my_visit_of_graph(H,list_green_nodes,source_node,target_node,middle_node)

    """
    if green_nodes_flag==True:
        print node_green_reach
    else:
        print 'nessuno!'
    """

    return green_nodes_flag

def my_visit_of_graph(H,list_green_nodes,source_green,target_green,middle_node):

    node_green_found_flag=False
    graph_dict=convert_graph_to_dict(H)

    visited=set()
    stack=[middle_node]

    while stack:

        curr_node = stack.pop()
        if curr_node not in visited:
            if curr_node==source_green or curr_node==target_green:
                #ho raggiunto uno dei nodi estremi del path, non devo aggiungerli allo stack perche limito l'esplorazione ai soli nodi intermedi
                continue
            else:#nodo intermedio al path o raggiunto da uno intermedio
                if curr_node not in list_green_nodes:
                    #il nodo che sto esplorando non e verde quindi lo marco come visitato e aggiungo alla stack tutti i suoi adiacenti tranne quelli che ho gia espolrato prima
                    visited.add(curr_node)
                    stack.extend(set(graph_dict[curr_node])- visited)
                else: #ho raggiunto un nodo verde diverso dagli estremi del path. Mi fermo e restituisco TRUE
                    node_green_found_flag=True
                    #print 'nodo verde incontrato %d'%(curr_node)
                    return node_green_found_flag,curr_node


    #return visited
    return node_green_found_flag,None


def get_degree_of_node(H,id_node):

    degree=0

    list_adj=list(nx.all_neighbors(H,id_node))
    list_couple=[(id_node,target) for target in list_adj]
    edges_of_node=[]
    for edge in list_couple:
        id_source=edge[0]
        id_target=edge[1]
        if H.has_edge(id_source,id_target):
                keydict=H[id_source][id_target]
                for k in keydict:
                    if H[id_source][id_target][k]['type']=='normal' and H[id_source][id_target][k]['type']!='green':
                        edge_1=(id_source,id_target)
                        edge_2=(id_target,id_source)
                        if edge_1 not in edges_of_node and edge_2 not in edges_of_node:
                            edges_of_node.append(edge_1)
                            degree=degree+1

    return degree



def reduce_capacity_path(residualGraph,path,demand_to_assign,cap_of_path=None):
    #print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    #for edge in residualGraph.edges(data=True):
    #   print edge

    #print 'path da decrementare '
    #print path
    cap_path=sys.maxint
    edge_to_remove=[]

    if cap_of_path==None:
        for i in range(0,len(path)-1,1):
            source=path[i]
            target=path[i+1]
            if residualGraph.has_edge(source,target):
                keydict=residualGraph[source][target]
                for k in keydict:
                        if residualGraph[source][target][k]['type']=='normal':
                            cap_edge=residualGraph[source][target][k]['capacity']
                            if cap_edge<=cap_path:
                                cap_path=cap_edge
            else:
                sys.exit('path inesistente')
    else:
        cap_path=cap_of_path

    flow=min(demand_to_assign,cap_path)

    for i in range(0,len(path)-1,1):
        id_source=path[i]
        id_target=path[i+1]
        keydict=residualGraph[id_source][id_target]
        for k in keydict:
            if residualGraph.has_edge(id_source,id_target,key=k):
                if residualGraph[id_source][id_target][k]['type']=='normal':
                    old_capacity=residualGraph[id_source][id_target][k]['capacity']
                    #if old_capacity==1:
                    #   sys.exit('ARCO CON CAPACITA UNO')
                    new_capacity=old_capacity-flow
                    residualGraph[id_source][id_target][k]['capacity']=new_capacity
                    if new_capacity == 0:
                        #print 'Capacita arco pari a zero %d-%d'%(id_source,id_target)
                        #residualGraph.remove_edge(id_source,id_target,key=k)
                        arc=(id_source,id_target,k)
                        edge_to_remove.append(arc)
                        #sys.exit('Ho rimosso un arco saturo')
                        #print 'rimosso arco: ' +str(id_source)+'-'+str(id_target)
                    if new_capacity<0:
                        print 'ERRORE IN ASSIGN_DEMAND SHORTEST: ARCO CON CAPACITA RESIDUA NEGATIVA '
                        sys.exit('ERRORE IN ASSIGN_DEMAND SHORTEST: ARCO CON CAPACITA RESIDUA NEGATIVA ')

    #print 'dopo decremento'
    #for edge in residualGraph.edges(data=True):
    #    print edge
    remove_saturated_edge(residualGraph,edge_to_remove)

    return flow

def split_edge(H,id_source,id_target,demand):

    if H.has_edge(id_source,id_target):
        number_edges=H.number_of_edges(id_source,id_target)
        keydict =H[id_source][id_target]
        count=0

        if number_edges==1 and (len(keydict)>1):
            type_edge= H[id_source][id_target]['type']
            #print str(type_edge)
            if(str(type_edge) =='green'):
                count+=1
        else:
            key=len(keydict)
            for k in keydict:
                #print k
                type_edge= H[id_source][id_target][k]['type']
                if(str(type_edge) =='green'):
                    count+=1

        if(count==0):
            H.add_edge(id_source,id_target,type='green', demand=demand,color='green',style='bold')

        elif count>1:
            print 'Doppio Arco verde tra source e bc %d-%d'%(id_source,id_target)
            sys.exit('Non possono esserci due archi distinti fra stessa coppia di nodi')
        else:
            #ha piu di un arco verde giA source e bc, devo fare la somma delle demand
            key=len(keydict)
            for k in keydict:
                #print k
                type_edge= H[id_source][id_target][k]['type']
                if(str(type_edge) =='green'):
                    key_to_update=k

            old_demand=H[id_source][id_target][key_to_update]['demand']
            new_demand=old_demand+demand
            H.add_edge(id_source,id_target,key=key_to_update,type='green', demand=new_demand,color='green',style='bold')
            #sys.exit('SPLIT EDGE: Arco fuso')

    else:
        #print 'aggiunto nuovo arco verde:'+str(id_source)+str(id_target)
        H.add_edge(id_source, id_target, type='green', demand=demand, color='green',style='bold')

def choice_couple_to_split_over_bc_path_diversity(shortest_pass_bc):

    max_num_path=0
    demand_selected=0
    #print 'shortest passanti per bc'

    #print shortest_pass_bc
    for couple in shortest_pass_bc:

        #print couple
        source=couple[0]
        target=couple[1]
        demand=couple[2]
        list_paths=shortest_pass_bc[couple]
        #print list_paths
        num_paths=len(list_paths)
        #print num_paths

        if num_paths > max_num_path:
            demand_selected=demand
            couple_selected=couple
            max_num_path=num_paths
        elif num_paths==max_num_path:
            if demand_selected < demand:
                demand_selected=demand
                couple_selected=couple

    #print couple_selected
    return couple_selected

def choice_couple_to_split_over_bc_min_flow(residualGraph,shortest_pass_bc):


    max_ratio=-1 +0.0
    flag_no_couple=False
    nodes=[]
    edges=[]
    array_of_ratio=[]
    for i in residualGraph.nodes():
        nodes.append(Vertex(residualGraph.node[i]['id']))

    clean_edges(nodes)
    couple_selected=None
    #print 'path che hanno contribuito alla betweeness'
    #print shortest_pass_bc
    for couple in shortest_pass_bc:


        clean_edges(nodes)
        del edges
        edges=get_Edges_residual(residualGraph)
        buildGraph(nodes,edges)

        id_source=couple[0]
        id_target=couple[1]
        demand= couple[2]
        ratio=0.0
        source_index=int(get_index_vertex(nodes,id_source))
        target_index=int(get_index_vertex(nodes,id_target))

        max_flow=maxFlow(nodes[source_index],nodes[target_index])
        print '----------------------SCELTA MIN RATIO DEMAND/FLOW-----------------------'

        """ SCELTA DELLA COPPIA BASATA SU MIN FLOW RESIDUO
        #print 'confronto selected con flow esaminato: %d-%d'%(min_flow,max_flow)
        if max_flow<=min_flow:
            couple_selected=couple
            min_flow=max_flow
            print 'nuovo min flow: %d'%(min_flow)
        """

        """ SCELTA DELLA COPPIA BASATA SU MIN RATIO DEMAND/FLOW"""""
        demand+=0.0
        print 'ratio esaminato per %d-%d : ratio = %f/%f'%(id_source,id_target,demand,max_flow)
        ratio=demand/max_flow
        elem=(id_source,id_target,demand,ratio)
        array_of_ratio.append(elem)
        if ratio >= max_ratio:
            couple_selected=couple
            max_ratio=ratio
            #print 'nuovo min ratio: %f'%(min_ratio)


    print 'coppia selezionata con il min ratio'
    print couple_selected

    if couple_selected==None:
        flag_no_couple=True
        #sys.exit('NESSUNA COPPIA SELEZIONABILE PER LO SPLIT')
    #print couple_selected

    return array_of_ratio,flag_no_couple


def split(H,temp_graph_supply,id_bc,number_of_split):

    green_edges=get_green_edges(H)
    residualGraph=nx.MultiGraph(temp_graph_supply)
    #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
    shortest_pass_bc=compute_shortest_passing_bc(H,id_bc,green_edges)
    #print 'cammini che hanno contribuito alla betwneess di %d '%(id_bc)
    #print shortest_pass_bc
    list_green_bc=retrieve_green_couple_passing_bc_from_dict(shortest_pass_bc)
    #print 'coppie verdi che hanno almeno un cammino che passa per il bc %d'%(id_bc)
    #print list_green_bc

    nodes=[]
    edges=[]

    #select which couple of green node it'll be splitted
    #couple_selected=inizio split_couple_to_split_over_bc_path_diversity(shortest_pass_bc)
    couple_selected=choice_couple_to_split_over_bc_min_flow(residualGraph,shortest_pass_bc)

    ##for couple in list_green_bc:
    #print '-------INIZIO SPLIT COPPIA: %d-%d-%d ---------------------------'%(couple_selected[0],couple_selected[1],couple_selected[2])


    shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)

    for i in residualGraph.nodes():
        nodes.append(Vertex(residualGraph.node[i]['id']))
    clean_edges(nodes)

    clean_edges(nodes)
    del edges
    edges=get_Edges_residual(residualGraph)
    buildGraph(nodes,edges)

    id_source=couple_selected[0]
    id_target=couple_selected[1]
    demand=couple_selected[2]
    source_index=int(get_index_vertex(nodes,id_source))
    target_index=int(get_index_vertex(nodes,id_target))
    bc_index=int(get_index_vertex(nodes,id_bc))

    #print '----------------------INIZIO MAX FLOW BC--------------------'

    max_flow_to_bc=maxFlow(nodes[source_index],nodes[bc_index])
    #print 'max_flow tra %d-%d : %d '%(nodes[source_index].name,nodes[bc_index].name,max_flow_to_bc)

    clean_edges(nodes)
    del edges
    edges=get_Edges_residual(residualGraph)
    buildGraph(nodes,edges)

    #print 'costruisco nuovo grafo per flusso tra bc-target : %d-%d'%(nodes[bc_index].name,nodes[target_index].name)
    max_flow_from_bc=maxFlow(nodes[bc_index],nodes[target_index])
    #print 'max_flow tra %d-%d : %d '%(nodes[bc_index].name,nodes[target_index].name,max_flow_from_bc)
    min_cap=min(max_flow_to_bc,max_flow_from_bc)
    #print 'min cap %d - demand %d'%(min_cap,demand)

    demand_assigned=0
    demand_to_assign=0
    if demand <= min_cap:
        total_split=True
        demand_to_assign=demand
    else:
        total_split=False
        demand_to_assign=min_cap

    #print 'demand to assign %d'%(demand_to_assign)
    #while(demand_to_assign>0):

    path_selected=get_implementing_path(residualGraph,couple_selected,shortest_pass_bc)
    increment_flow=reduce_capacity_path(residualGraph,path_selected,demand_to_assign)
    #print 'increment flow %d'%(increment_flow)
    #demand_to_assign=demand_to_assign-increment_flow
    demand_assigned=demand_assigned+increment_flow
    #shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)
    #print 'shortest pass bc'
    #print shortest_pass_bc
    #if not shortest_pass_bc:
    if demand_assigned<demand:
        total_split=False
    #    demand_to_assign=0


    #if demand_to_assign==0:

    #modifica grafo originale con lo split degli archi.
    #aggiungi bc come nodo verde.

    # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

    H.node[id_bc]['type']='green'
    if H.node[id_bc]['status']=='destroyed':
        H.node[id_bc]['status']='repaired'
        H.node[id_bc]['color']='blue'
    else:
        H.node[id_bc]['color']='green'

    #remove green edge between original couple
    keydict=H[id_source][id_target]
    #print keydict
    for k in keydict:
        if H.edge[id_source][id_target][k]['type']=='green':
            key_to_remove=k

    if total_split==True:
        H.remove_edge(id_source,id_target,key=key_to_remove)
        #add two new green edge source,bc and bc,target
    else:
        H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

    #splitta l'arco in due sul bc
    split_edge(H,id_source,id_bc,demand_assigned)
    split_edge(H,id_bc,id_target,demand_assigned)

    #for edge in H.edges(data=True):
    #    print edge

    new_green_edges=get_green_edges(H)
    new_bet_dict=compute_my_betweeness_3(H,new_green_edges,assign_demand_shortest)
    #print new_bet_dict
    set_betwenness_from_dict(H,new_bet_dict)

    my_draw(H,'5-split-%d'%(number_of_split))



def split_by_one(H,number_of_split,distance_metric):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)
    array_of_ratio=[]
    #print 'ordine analisi dei candidati best candidate'
    #print array_sorted_bcs
    for i in range(0,len(array_sorted_bcs),1):
        flag_no_split=False
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            #print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)
            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)
            #list_green_bc=retrieve_green_couple_passing_bc_from_dict(shortest_pass_bc)
            array_of_ratio,flag_no_couple=choice_couple_to_split_over_bc_min_flow(residualGraph,shortest_pass_bc)
            if flag_no_couple == True:
                flag_no_split=True
            else:
                #print 'sono qui'
                flag_no_split=False
                sorted_array_of_ratio=[]
                sorted_array_of_ratio=sort_reverse_ratio(array_of_ratio)
                #print 'sorted array ratio of %d'%(id_bc)
                #print sorted_array_of_ratio
                for elem in range(0,len(sorted_array_of_ratio),1):
                    if (bc_found==False):
                        couple_selected=sorted_array_of_ratio[elem]

                        #print 'INIZIO SPLIT COPPIA: %d-%d-%d '%(couple_selected[0],couple_selected[1],couple_selected[2])

                        nodes=[]
                        edges=[]

                        for j in residualGraph.nodes():
                            nodes.append(Vertex(residualGraph.node[j]['id']))

                        clean_edges(nodes)
                        del edges
                        edges=get_Edges_residual(residualGraph)
                        buildGraph(nodes,edges)

                        id_source=couple_selected[0]
                        id_target=couple_selected[1]
                        demand=couple_selected[2]
                        source_index=int(get_index_vertex(nodes,id_source))
                        target_index=int(get_index_vertex(nodes,id_target))
                        bc_index=int(get_index_vertex(nodes,id_bc))

                        #print '----------------------INIZIO MAX FLOW BC--------------------'

                        max_flow_to_bc=maxFlow(nodes[source_index],nodes[bc_index])
                        #print 'max_flow tra %d-%d : %d '%(nodes[source_index].name,nodes[bc_index].name,max_flow_to_bc)

                        clean_edges(nodes)
                        del edges
                        edges=get_Edges_residual(residualGraph)
                        buildGraph(nodes,edges)

                        #print 'costruisco nuovo grafo per flusso tra bc-target : %d-%d'%(nodes[bc_index].name,nodes[target_index].name)
                        max_flow_from_bc=maxFlow(nodes[bc_index],nodes[target_index])
                        #print 'max_flow tra %d-%d : %d '%(nodes[bc_index].name,nodes[target_index].name,max_flow_from_bc)
                        #min_cap=min(max_flow_to_bc,max_flow_from_bc)
                        #print 'min cap %d - demand %d'%(min_cap,demand)

                        demand_assigned=0
                        demand_to_assign=0
                        #se la domanda da splittare e pari a 1 allora faccio lo split totale dell'arco
                        if demand == 1:
                            total_split=True
                            demand_to_assign=demand
                        else:
                            #altrimenti faccio lo split per una unita di flusso
                            total_split=False
                            demand_to_assign=1

                        #print 'demand to assign %d'%(demand_to_assign)
                        #while(demand_to_assign>0):

                        #increment_flow=reduce_capacity_path(residualGraph,path_selected,demand_to_assign)
                        #print 'increment flow %d'%(increment_flow)
                        #demand_to_assign=demand_to_assign-increment_flow
                        demand_assigned=1

                        graph_temp=nx.MultiGraph(H)
                        result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,number_of_split)
                        if result_check==True:
                            #print 'Split possible'
                            result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                        else:
                            #print 'Split impossible'
                            result_routability_check=False


                        #sys.exit('stop')

                        if result_routability_check==True:
                            #modifica grafo originale con lo split degli archi.
                            #aggiungi bc come nodo verde.

                            bc_found=True

                            # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                            H.node[id_bc]['type']='green'
                            if H.node[id_bc]['status']=='destroyed':
                                H.node[id_bc]['status']='repaired'
                                H.node[id_bc]['true_status']='on'
                                H.node[id_bc]['color']='blue'
                            else:
                                H.node[id_bc]['color']='green'

                            #remove green edge between original couple
                            keydict=H[id_source][id_target]
                            #print keydict
                            for k in keydict:
                                if H.edge[id_source][id_target][k]['type']=='green':
                                    key_to_remove=k

                            if total_split==True:
                                H.remove_edge(id_source,id_target,key=key_to_remove)
                                #add two new green edge source,bc and bc,target
                            else:
                                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                            #splitta l'arco in due sul bc
                            new_edges_added=[]
                            split_edge(H,id_source,id_bc,demand_assigned)
                            edge_1=(id_source,id_bc,demand_assigned)
                            new_edges_added.append(edge_1)
                            split_edge(H,id_bc,id_target,demand_assigned)
                            edge_2=(id_bc,id_target,demand_assigned)
                            new_edges_added.append(edge_2)

                            #for edge in H.edges(data=True):
                            #    print edge

                            new_green_edges=get_green_edges(H)
                            #print 'pre_compute_my_betw'
                            new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #print new_bet_dict
                            set_betwenness_from_dict(H,new_bet_dict)

                            my_draw(H,'5-split-%d-split'%(number_of_split))

    if flag_no_split==True:

        return None,None,flag_no_split
    else:

        return couple_selected,new_edges_added,flag_no_split

#variante che tiene conto delle prenotazioni precedenti per fare gli split
def split_by_capacity_path_reservation(H,counter_isp,distance_metric,nodes_recovered):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    global shortest_paths_for_bet
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)
    array_of_ratio=[]
    #print 'ordine analisi dei candidati best candidate'
    #print array_sorted_bcs

    for i in range(0,len(array_sorted_bcs),1):
        flag_no_split=False
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)

            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)

            array_of_ratio,flag_no_couple=choice_couple_to_split_over_bc_min_flow(residualGraph,shortest_pass_bc)
            if flag_no_couple == True:
                flag_no_split=True
                print 'Candidato %d: non ha arco feasible da splittare'%(id_bc)
            else:
                #print 'sono qui'
                flag_no_split=False
                sorted_array_of_ratio=[]
                sorted_array_of_ratio=sort_reverse_ratio(array_of_ratio)
                print 'sorted array ratio of %d'%(id_bc)
                print sorted_array_of_ratio
                for elem in range(0,len(sorted_array_of_ratio),1):
                    if (bc_found==False):
                        couple_selected=sorted_array_of_ratio[elem]
                        print 'INIZIO SPLIT COPPIA: %d-%d-%d '%(couple_selected[0],couple_selected[1],couple_selected[2])
                        id_source=couple_selected[0]
                        id_target=couple_selected[1]
                        demand=couple_selected[2]
                        #ci possono essere piu archi verdi tra la coppia selezionata. Ne scelgo uno.
                        key_dict_edge=residualGraph[id_source][id_target]
                        for key_edge in key_dict_edge:
                            split_check=False
                            if residualGraph[id_source][id_target][key_edge]['type']=='green':
                                if (bc_found==False):
                                    edge_split=(id_source,id_target,demand)

                                    #shortest che hanno contribuito alla centralita del bc
                                    shortests_contribute_to_bc=shortest_pass_bc[edge_split]

                                    #controllo se l'arco che voglio splittare e' una domanda originaria o e' gia splittata
                                    if residualGraph[id_source][id_target][key_edge]['splitted_edge']==True:
                                        #vedi chi e' la radice
                                        root_edge=None
                                        root_edge=residualGraph[id_source][id_target][key_edge]['root_edge']
                                        #shortest_path=compute_shortest_from_set(residualGraph,shortests_contribute_to_bc,distance_metric)
                                        #controlla se non e cambiato lo shortest rispetto alla root.True se e' cambiato
                                        if check_if_shortest_changed(residualGraph,edge_split):
                                            #si lo shortest e' cambiato
                                            graph_reservation=get_graph_reservations(residualGraph)
                                            shortest_path=compute_shortest_from_set(graph_reservation,shortests_contribute_to_bc,distance_metric)
                                            if shortest_path==None:
                                                #significa che levando i path prenotati, non ci sono piu path che passano per quel bc. Quindi va scartato
                                                split_condition=False
                                        else:
                                            #se no continua a fare lo split sullo shortest
                                            split_check=True


                                    elif residualGraph[id_source][id_target][key_edge]['splitted_edge']==False:
                                        #e' la prima volta che splitto questo arco.
                                        #Bisogna calcolare lo shortest considerando le domande gia' prenotate.
                                        #Quindi bisogna passargli un grafo residuo diverso

                                        #creo grafo su cui fare il residuo delle prenotazioni
                                        graph_reservation=get_graph_reservations(residualGraph)
                                        shortest_path=compute_shortest_from_set(graph_reservation,shortests_contribute_to_bc,distance_metric)
                                        if shortest_path==None:
                                            #significa che levando i path prenotati, non ci sono piu path che passano per quel bc. Quindi va scartato
                                            split_check=False
                                        else:
                                            split_check=True


                                    path_capacity=get_capacity_of_path(residualGraph,shortest_path)
                                    demand_assigned=0

                                    #calcola surplus del nodo
                                    surplus=0.0
                                    surplus=compute_surplus_of_node(residualGraph,id_bc)
                                    #fai la meta e prendi l'intero inferiore
                                    half_surplus=int(math.floor(surplus/2.0))

                                    if half_surplus>0:
                                        demand_to_assign=min(demand,path_capacity,half_surplus)
                                    else:
                                        demand_to_assign=min(demand,path_capacity)

                                    print demand_to_assign

                                    quantity_to_split_flag=False
                                    quantity_to_split=demand_to_assign

                                    while(quantity_to_split_flag==False):

                                            demand_to_assign=quantity_to_split
                                            print 'Provo Demand to assign %f'%(demand_to_assign)
                                            if demand_to_assign>0:
                                                #se la domanda da splittare e pari alla domanda totale allora faccio lo split totale dell'arco
                                                if demand == demand_to_assign:
                                                    total_split=True
                                                else:
                                                    #altrimenti faccio lo split pari alla path_capacity
                                                    total_split=False

                                                demand_assigned=demand_to_assign

                                                graph_temp=nx.MultiGraph(H)
                                                print 'Pre simulate split provando con %f di quantita di flusso'%(demand_assigned)
                                                result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,counter_isp)
                                                print 'post simulate split'
                                                if result_check==True:
                                                    print 'Cut condition ok'
                                                    result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                                                else:
                                                    print 'Cut condition non soddisfatta'
                                                    result_routability_check=False
                                                    quantity_to_split_flag=True

                                                if result_routability_check==True:
                                                    quantity_to_split_flag=True
                                                else:
                                                    print 'Routability False, devo cambiare quantita'
                                                    quantity_to_split=quantity_to_split-1
                                                    #else:
                                                    #   quantity_to_split=quantity_to_split/2.0
                                                    """
                                                    if quantity_to_split>0 and quantity_to_split<1:
                                                        print 'prox quantita = 0'
                                                        print 'flag half'
                                                        print flag_half_split
                                                        if flag_half_split==True:
                                                            quantity_to_split=0.5
                                                            print 'QUANTITY HALF'
                                                    """
                                                    if quantity_to_split<=0:
                                                        quantity_to_split_flag=False
                                                        quantity_to_split=0
                                                        print 'Non posso piu diminuire la quantita da splittare. Cambio Bc'

                                            elif demand_to_assign==0:
                                                    quantity_to_split_flag=True
                                                    result_routability_check=False
                                            else:
                                                sys.exit('Errore in splity by capacity: demand_to_assing <0')



                                    #sys.exit('stop')

                                    if result_routability_check==True:
                                        #modifica grafo originale con lo split degli archi.
                                        #aggiungi bc come nodo verde.

                                        bc_found=True
                                        quantity_to_split_flag=True
                                        if H.node[id_bc]['status']=='destroyed':
                                            if id_bc not in nodes_recovered:
                                                nodes_recovered.append(id_bc)


                                        # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                                        H.node[id_bc]['type']='green'
                                        if H.node[id_bc]['status']=='destroyed':
                                            H.node[id_bc]['status']='repaired'
                                            H.node[id_bc]['color']='blue'
                                            H.node[id_bc]['true_status']='on'
                                        else:
                                            H.node[id_bc]['color']='green'

                                        #remove green edge between original couple
                                        keydict=H[id_source][id_target]
                                        #print keydict
                                        for k in keydict:
                                            if H.edge[id_source][id_target][k]['type']=='green':
                                                key_to_remove=k
                                        """
                                        if flag_half_split==True:
                                            if demand==1:
                                                if demand_assigned==0.5:
                                                    if (demand_assigned*2)==demand:
                                                        total_split=True
                                        """

                                        if total_split==True:
                                            H.remove_edge(id_source,id_target,key=key_to_remove)
                                            #add two new green edge source,bc and bc,target
                                        else:
                                            H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                                        #splitta l'arco in due sul bc
                                        new_edges_added=[]
                                        split_edge(H,id_source,id_bc,demand_assigned)
                                        edge_1=(id_source,id_bc,demand_assigned)
                                        new_edges_added.append(edge_1)
                                        split_edge(H,id_bc,id_target,demand_assigned)
                                        edge_2=(id_bc,id_target,demand_assigned)
                                        new_edges_added.append(edge_2)

                                        #for edge in H.edges(data=True):
                                        #    print edge

                                        new_green_edges=get_green_edges(H)
                                        #print 'pre_compute_my_betw'
                                        new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                                        #print new_bet_dict
                                        set_betwenness_from_dict(H,new_bet_dict)

                                        my_draw(H,'5-isp-%d-split'%(counter_isp))

    if flag_no_split==True:

        return None,None,flag_no_split
    else:

        return couple_selected,new_edges_added,flag_no_split


def check_if_shortest_changed(residualGraph,edge_split):

    global reservation_dict

    id_source=edge_split[0]
    id_target=edge_split[1]
    edge=(id_source,id_target)
    shortest_reserved=None
    shortest_reserved=reservation_dict[edge]
    if shortest_reserved==None:
        sys.exit('Errore in check if shortest_changed: shortest prenotato inesistente')
    else:
        #calcola shortest path attuale
        curr_shortest=compute_shortest_paths_on_residual(residualGraph,id_source,id_target,distance_metric)
        if are_paths_equals(shortest_reserved,curr_shortest):
            return False
        else:
            return True

def are_paths_equals(path_1,path_2):

    result=True

    if len(path_1)==len(path_2):

        for i in range(0,len(path_1),1):
            if path_1[i]==path_2[i]:
                continue
            else:
                result=False
                return result

    else:
        result=False
        return result

    return result



def get_graph_reservations(residualGraph):

    global reservation_dict
    graph_reservation=nx.MultiGraph(residualGraph)

    for couple in reservation_dict:
        shortest_reserved=reservation_dict[couple]
        if check_if_path_exist(graph_reservation,shortest_reserved):
            demand=couple[2]
            reduce_capacity_path(graph_reservation,shortest_reserved,demand)
        else:
            sys.exit('Errore in get_graph_reservation: path prenotato non piu presente nel grafo')

    return graph_reservation











def split_by_capacity_path(H,counter_isp,distance_metric,nodes_recovered):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    global shortest_paths_for_bet
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)
    array_of_ratio=[]
    #print 'ordine analisi dei candidati best candidate'
    #print array_sorted_bcs

    for i in range(0,len(array_sorted_bcs),1):
        flag_no_split=False
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)
            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)
            #list_green_bc=retrieve_green_couple_passing_bc_from_dict(shortest_pass_bc)
            array_of_ratio,flag_no_couple=choice_couple_to_split_over_bc_min_flow(residualGraph,shortest_pass_bc)
            if flag_no_couple == True:
                flag_no_split=True
                print 'Candidato %d: non ha arco feasible da splittare'%(id_bc)
            else:
                #print 'sono qui'
                flag_no_split=False
                sorted_array_of_ratio=[]
                sorted_array_of_ratio=sort_reverse_ratio(array_of_ratio)
                print 'sorted array ratio of %d'%(id_bc)
                print sorted_array_of_ratio
                for elem in range(0,len(sorted_array_of_ratio),1):
                    if (bc_found==False):
                        couple_selected=sorted_array_of_ratio[elem]

                        print 'INIZIO SPLIT COPPIA: %d-%d-%d '%(couple_selected[0],couple_selected[1],couple_selected[2])
                        id_source=couple_selected[0]
                        id_target=couple_selected[1]
                        demand=couple_selected[2]
                        edge_split=(id_source,id_target,demand)

                        #shortest che hanno contribuito alla centralita del bc
                        print shortest_pass_bc
                        shortests_contribute_to_bc=shortest_pass_bc[edge_split]

                        shortest_path=compute_shortest_from_set(residualGraph,shortests_contribute_to_bc,distance_metric)

                        path_capacity=get_capacity_of_path(residualGraph,shortest_path)
                        demand_assigned=0

                        #calcola surplus del nodo
                        surplus=0.0
                        surplus=compute_surplus_of_node(residualGraph,id_bc)
                        #fai la meta e prendi l'intero inferiore
                        half_surplus=int(math.floor(surplus/2.0))

                        if half_surplus>0:
                            demand_to_assign=min(demand,path_capacity,half_surplus)
                        else:
                            demand_to_assign=min(demand,path_capacity)

                        print demand_to_assign

                        quantity_to_split_flag=False
                        quantity_to_split=demand_to_assign

                        while(quantity_to_split_flag==False):

                                demand_to_assign=quantity_to_split
                                print 'Provo Demand to assign %f'%(demand_to_assign)
                                if demand_to_assign>0:
                                    #se la domanda da splittare e pari alla domanda totale allora faccio lo split totale dell'arco
                                    if demand == demand_to_assign:
                                        total_split=True
                                    else:
                                        #altrimenti faccio lo split pari alla path_capacity
                                        total_split=False

                                    demand_assigned=demand_to_assign

                                    graph_temp=nx.MultiGraph(H)
                                    print 'Pre simulate split provando con %f di quantita di flusso'%(demand_assigned)
                                    result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,counter_isp)
                                    print 'post simulate split'
                                    if result_check==True:
                                        print 'Cut condition ok'
                                        result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                                    else:
                                        print 'Cut condition non soddisfatta'
                                        result_routability_check=False
                                        quantity_to_split_flag=True

                                    if result_routability_check==True:
                                        quantity_to_split_flag=True
                                    else:
                                        print 'Routability False, devo cambiare quantita'
                                        quantity_to_split=quantity_to_split-1
                                        #else:
                                        #   quantity_to_split=quantity_to_split/2.0
                                        """
                                        if quantity_to_split>0 and quantity_to_split<1:
                                            print 'prox quantita = 0'
                                            print 'flag half'
                                            print flag_half_split
                                            if flag_half_split==True:
                                                quantity_to_split=0.5
                                                print 'QUANTITY HALF'
                                        """
                                        if quantity_to_split<=0:
                                            quantity_to_split_flag=False
                                            quantity_to_split=0
                                            print 'Non posso piu diminuire la quantita da splittare. Cambio Bc'

                                elif demand_to_assign==0:
                                        quantity_to_split_flag=True
                                        result_routability_check=False
                                else:
                                    sys.exit('Errore in splity by capacity: demand_to_assing <0')



                        #sys.exit('stop')

                        if result_routability_check==True:
                            #modifica grafo originale con lo split degli archi.
                            #aggiungi bc come nodo verde.

                            bc_found=True
                            quantity_to_split_flag=True
                            if H.node[id_bc]['status']=='destroyed':
                                if id_bc not in nodes_recovered:
                                    nodes_recovered.append(id_bc)


                            # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                            H.node[id_bc]['type']='green'
                            if H.node[id_bc]['status']=='destroyed':
                                H.node[id_bc]['status']='repaired'
                                H.node[id_bc]['color']='blue'
                                H.node[id_bc]['true_status']='on'
                            else:
                                H.node[id_bc]['color']='green'

                            #remove green edge between original couple
                            keydict=H[id_source][id_target]
                            #print keydict
                            for k in keydict:
                                if H.edge[id_source][id_target][k]['type']=='green':
                                    key_to_remove=k
                            """
                            if flag_half_split==True:
                                if demand==1:
                                    if demand_assigned==0.5:
                                        if (demand_assigned*2)==demand:
                                            total_split=True
                            """

                            if total_split==True:
                                H.remove_edge(id_source,id_target,key=key_to_remove)
                                #add two new green edge source,bc and bc,target
                            else:
                                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                            #splitta l'arco in due sul bc
                            new_edges_added=[]
                            split_edge(H,id_source,id_bc,demand_assigned)
                            edge_1=(id_source,id_bc,demand_assigned)
                            new_edges_added.append(edge_1)
                            split_edge(H,id_bc,id_target,demand_assigned)
                            edge_2=(id_bc,id_target,demand_assigned)
                            new_edges_added.append(edge_2)

                            #for edge in H.edges(data=True):
                            #    print edge

                            new_green_edges=get_green_edges(H)
                            #print 'pre_compute_my_betw'
                            new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #print new_bet_dict
                            set_betwenness_from_dict(H,new_bet_dict)

                            my_draw(H,'5-isp-%d-split'%(counter_isp))

    if flag_no_split==True:

        return None,None,flag_no_split,None
    else:

        return couple_selected,new_edges_added,flag_no_split,id_bc


#variante 2: che fa lo split solo se il pruning dello shortest e' feasible
def split_by_capacity_path_and_pruning(H,counter_isp,distance_metric,nodes_recovered):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    global shortest_paths_for_bet
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)
    array_of_ratio=[]
    #print 'ordine analisi dei candidati best candidate'
    #print array_sorted_bcs

    for i in range(0,len(array_sorted_bcs),1):
        flag_no_split=False
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)
            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)
            #list_green_bc=retrieve_green_couple_passing_bc_from_dict(shortest_pass_bc)
            array_of_ratio,flag_no_couple=choice_couple_to_split_over_bc_min_flow(residualGraph,shortest_pass_bc)
            if flag_no_couple == True:
                flag_no_split=True
                print 'Candidato %d: non ha arco feasible da splittare'%(id_bc)
            else:
                #print 'sono qui'
                flag_no_split=False
                sorted_array_of_ratio=[]
                sorted_array_of_ratio=sort_reverse_ratio(array_of_ratio)
                print 'sorted array ratio of %d'%(id_bc)
                print sorted_array_of_ratio
                for elem in range(0,len(sorted_array_of_ratio),1):
                    if (bc_found==False):
                        couple_selected=sorted_array_of_ratio[elem]

                        print 'INIZIO SPLIT COPPIA: %d-%d-%d '%(couple_selected[0],couple_selected[1],couple_selected[2])
                        id_source=couple_selected[0]
                        id_target=couple_selected[1]
                        demand=couple_selected[2]
                        edge_split=(id_source,id_target,demand)

                        #shortest che hanno contribuito alla centralita del bc
                        shortests_contribute_to_bc=shortest_pass_bc[edge_split]

                        shortest_path=compute_shortest_from_set(residualGraph,shortests_contribute_to_bc,distance_metric)

                        path_capacity=get_capacity_of_path(residualGraph,shortest_path)
                        demand_assigned=0

                        #calcola surplus del nodo
                        surplus=0.0
                        surplus=compute_surplus_of_node(residualGraph,id_bc)
                        #fai la meta e prendi l'intero inferiore
                        half_surplus=int(math.floor(surplus/2.0))

                        if half_surplus>0:
                            demand_to_assign=min(demand,path_capacity,half_surplus)
                        else:
                            demand_to_assign=min(demand,path_capacity)

                        print demand_to_assign

                        quantity_to_split_flag=False
                        quantity_to_split=demand_to_assign

                        while(quantity_to_split_flag==False):

                                demand_to_assign=quantity_to_split
                                print 'Provo Demand to assign %f'%(demand_to_assign)
                                if demand_to_assign>0:
                                    #se la domanda da splittare e pari alla domanda totale allora faccio lo split totale dell'arco
                                    if demand == demand_to_assign:
                                        total_split=True
                                    else:
                                        #altrimenti faccio lo split pari alla path_capacity
                                        total_split=False

                                    demand_assigned=demand_to_assign

                                    graph_temp=nx.MultiGraph(H)
                                    print 'Pre simulate split provando con %f di quantita di flusso'%(demand_assigned)
                                    result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,counter_isp)
                                    print 'post simulate split'
                                    if result_check==True:
                                        print 'Cut condition ok'
                                        result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                                    else:
                                        print 'Cut condition non soddisfatta'
                                        result_routability_check=False
                                        quantity_to_split_flag=True

                                    if result_routability_check==True:
                                        quantity_to_split_flag=True
                                    else:
                                        print 'Routability False, devo cambiare quantita'
                                        quantity_to_split=quantity_to_split-1
                                        #else:
                                        #   quantity_to_split=quantity_to_split/2.0
                                        """
                                        if quantity_to_split>0 and quantity_to_split<1:
                                            print 'prox quantita = 0'
                                            print 'flag half'
                                            print flag_half_split
                                            if flag_half_split==True:
                                                quantity_to_split=0.5
                                                print 'QUANTITY HALF'
                                        """
                                        if quantity_to_split<=0:
                                            quantity_to_split_flag=False
                                            quantity_to_split=0
                                            print 'Non posso piu diminuire la quantita da splittare. Cambio Bc'

                                elif demand_to_assign==0:
                                        quantity_to_split_flag=True
                                        result_routability_check=False
                                else:
                                    sys.exit('Errore in splity by capacity: demand_to_assing <0')



                        #sys.exit('stop')

                        if result_routability_check==True:

                            #-----------------AGGIUNTA CONTROLLO SE IL PRUNING DELLO SHORTEST E' FEASIBLE------------
                            #shortest_path_selected_for_pruning=get_shortest_path_to_prune(temp_graph_supply,couple_selected,distance_metric)
                            shortest_path_selected_for_pruning=shortest_path
                            if shortest_path_selected_for_pruning!=None:
                                demand_to_prune=demand_to_assign
                                graph_temp_for_pruning=nx.MultiGraph(residualGraph)
                                graph_pruned,temp_green_edges_pruning=simulate_pruning(graph_temp_for_pruning,shortest_path_selected_for_pruning,demand_to_prune,distance_metric,counter_isp)
                                if check_routability(graph_pruned,temp_green_edges_pruning)==True:

                                # IL PRUNING NON COMPROMETTE LA SOLUZIONE, QUINDI FACCIO LO SPLIT UFFICILAE

                                    #modifica grafo originale con lo split degli archi.
                                    #aggiungi bc come nodo verde.

                                    bc_found=True
                                    quantity_to_split_flag=True
                                    if H.node[id_bc]['status']=='destroyed':
                                        if id_bc not in nodes_recovered:
                                            nodes_recovered.append(id_bc)


                                    # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                                    H.node[id_bc]['type']='green'
                                    if H.node[id_bc]['status']=='destroyed':
                                        H.node[id_bc]['status']='repaired'
                                        H.node[id_bc]['color']='blue'
                                        H.node[id_bc]['true_status']='on'
                                    else:
                                        H.node[id_bc]['color']='green'

                                    #remove green edge between original couple
                                    keydict=H[id_source][id_target]
                                    #print keydict
                                    for k in keydict:
                                        if H.edge[id_source][id_target][k]['type']=='green':
                                            key_to_remove=k
                                    """
                                    if flag_half_split==True:
                                        if demand==1:
                                            if demand_assigned==0.5:
                                                if (demand_assigned*2)==demand:
                                                    total_split=True
                                    """

                                    if total_split==True:
                                        H.remove_edge(id_source,id_target,key=key_to_remove)
                                        #add two new green edge source,bc and bc,target
                                    else:
                                        H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                                    #splitta l'arco in due sul bc
                                    new_edges_added=[]
                                    split_edge(H,id_source,id_bc,demand_assigned)
                                    edge_1=(id_source,id_bc,demand_assigned)
                                    new_edges_added.append(edge_1)
                                    split_edge(H,id_bc,id_target,demand_assigned)
                                    edge_2=(id_bc,id_target,demand_assigned)
                                    new_edges_added.append(edge_2)

                                    #for edge in H.edges(data=True):
                                    #    print edge

                                    new_green_edges=get_green_edges(H)
                                    #print 'pre_compute_my_betw'
                                    new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                                    #print new_bet_dict
                                    set_betwenness_from_dict(H,new_bet_dict)

                                    my_draw(H,'5-isp-%d-split'%(counter_isp))

    if flag_no_split==True:

        return None,None,flag_no_split
    else:

        return couple_selected,new_edges_added,flag_no_split



#variante 3: aggiunta del ranking per ogni path che ha contribuito alla centralita del bc (versione sempre usata prima di variante 5
def split_by_capacity_path_and_ranking(H,counter_isp,distance_metric,nodes_recovered,type_of_bet):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    global shortest_paths_for_bet
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)


    #lista di tutti i path in ordine di ranking dato dal min(cap_of_path,demand) /max_flow della coppia verde
    ranked_paths_of_bc=[]

    flag_no_split=True

    for i in range(0,len(array_sorted_bcs),1):
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)
            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)

            ranked_paths_of_bc,flag_no_couple=compute_ranking_paths_of_bc(residualGraph,shortest_pass_bc)

            if flag_no_couple == True:
                #flag_no_split=True
                print 'Candidato %d: non ha arco feasible da splittare'%(id_bc)
            else:
                #print 'sono qui'

                for elem in range(0,len(ranked_paths_of_bc),1):
                    if (bc_found==False):
                        #tupla = ratio, path, demand_to_split_, edge
                        tupla_selected=ranked_paths_of_bc[elem]

                        id_source=tupla_selected[3][0]      #id_source_green
                        id_target=tupla_selected[3][1]      #id_target_green
                        demand=tupla_selected[2]            #domanda dell'arco verde
                        ratio=tupla_selected[0]             #ratio
                        path=tupla_selected[1]              #path associato al ratio demand/maxflow
                        edge_split=(id_source,id_target,demand)

                        print 'INIZIO SPLIT COPPIA: %d-%d-%d: %.2f '%(id_source,id_target,demand,ratio)

                        ##shortest che hanno contribuito alla centralita del bc
                        #print 'Shortest che passno per BC:'
                        #print shortest_pass_bc

                        """
                        shortests_contribute_to_bc=shortest_pass_bc[edge_split]

                        shortest_path=compute_shortest_from_set(residualGraph,shortests_contribute_to_bc,distance_metric)
                        """

                        path_capacity=get_capacity_of_path(residualGraph,path)
                        demand_assigned=0


                        #calcola surplus del nodo
                        surplus=0.0
                        surplus=compute_surplus_of_node(residualGraph,id_bc)
                        #fai la meta e prendi l'intero inferiore
                        half_surplus=int(math.floor(surplus/2.0))

                        if half_surplus>0:
                            demand_to_assign=min(demand,path_capacity,half_surplus)
                        else:
                            demand_to_assign=min(demand,path_capacity)


                        print demand_to_assign

                        quantity_to_split_flag=False
                        quantity_to_split=demand_to_assign

                        while(quantity_to_split_flag==False):

                                demand_to_assign=quantity_to_split
                                print 'Provo Demand to assign %f'%(demand_to_assign)
                                if demand_to_assign>0:
                                    #se la domanda da splittare e pari alla domanda totale allora faccio lo split totale dell'arco
                                    if demand == demand_to_assign:
                                        total_split=True
                                    else:
                                        #altrimenti faccio lo split pari alla path_capacity
                                        total_split=False

                                    demand_assigned=demand_to_assign

                                    graph_temp=nx.MultiGraph(H)
                                    print 'Pre simulate split provando con %f di quantita di flusso'%(demand_assigned)
                                    result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,counter_isp)
                                    print 'post simulate split'
                                    if result_check==True:
                                        print 'Cut condition ok'
                                        result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                                    else:
                                        print 'Cut condition non soddisfatta'
                                        result_routability_check=False
                                        quantity_to_split_flag=True

                                    if result_routability_check==True:
                                        quantity_to_split_flag=True
                                    else:
                                        print 'Routability False, devo cambiare quantita'
                                        quantity_to_split=quantity_to_split-1
                                        #else:
                                        #   quantity_to_split=quantity_to_split/2.0
                                        """
                                        if quantity_to_split>0 and quantity_to_split<1:
                                            print 'prox quantita = 0'
                                            print 'flag half'
                                            print flag_half_split
                                            if flag_half_split==True:
                                                quantity_to_split=0.5
                                                print 'QUANTITY HALF'
                                        """
                                        if quantity_to_split<=0:
                                            quantity_to_split_flag=False
                                            quantity_to_split=0
                                            print 'Non posso piu diminuire la quantita da splittare. Cambio Bc'

                                elif demand_to_assign==0:
                                        quantity_to_split_flag=True
                                        result_routability_check=False
                                else:
                                    sys.exit('Errore in splity by capacity: demand_to_assing <0')



                        #sys.exit('stop')

                        if result_routability_check==True:
                            #modifica grafo originale con lo split degli archi.
                            #aggiungi bc come nodo verde.

                            bc_found=True
                            quantity_to_split_flag=True
                            if H.node[id_bc]['status']=='destroyed':
                                if id_bc not in nodes_recovered:
                                    nodes_recovered.append(id_bc)

                            couple_selected=(id_source,id_target,demand)

                            # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                            H.node[id_bc]['type']='green'
                            if H.node[id_bc]['status']=='destroyed':
                                H.node[id_bc]['status']='repaired'
                                H.node[id_bc]['color']='blue'
                                H.node[id_bc]['true_status']='on'
                            else:
                                H.node[id_bc]['color']='green'

                            #remove green edge between original couple
                            keydict=H[id_source][id_target]
                            #print keydict
                            for k in keydict:
                                if H.edge[id_source][id_target][k]['type']=='green':
                                    key_to_remove=k
                            """
                            if flag_half_split==True:
                                if demand==1:
                                    if demand_assigned==0.5:
                                        if (demand_assigned*2)==demand:
                                            total_split=True
                            """

                            if total_split==True:
                                H.remove_edge(id_source,id_target,key=key_to_remove)
                                #add two new green edge source,bc and bc,target

                            else:
                                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                            #splitta l'arco in due sul bc
                            new_edges_added=[]
                            split_edge(H,id_source,id_bc,demand_assigned)
                            edge_1=(id_source,id_bc,demand_assigned)
                            new_edges_added.append(edge_1)
                            split_edge(H,id_bc,id_target,demand_assigned)
                            edge_2=(id_bc,id_target,demand_assigned)
                            new_edges_added.append(edge_2)

                            #CALCOLA I PATH DELLE NUOVE COPPIE DI ARCHI PRENDENDOLI DALLA COPPIA ORIGINALE
                            #compute_paths_from_split(id_source,id_target,id_bc)
                            """
                            if total_split==True:
                                green_arc=(id_source,id_target)
                                green_arc_reverse=(id_target,id_source)
                                if green_arc in all_graph_paths:
                                    del all_graph_paths[green_arc]
                                elif green_arc_reverse in all_graph_paths:
                                    del all_graph_paths[green_arc_reverse]
                                else:
                                    sys.exit('Errore in spit path and ranking: domanda da rimuovere non presente in all_graph_paths')
                            """
                            #print 'Dopo lo split di %d-%d'%(id_source,id_target)
                            #print all_graph_paths
                            #for edge in H.edges(data=True):
                            #    print edge

                            new_green_edges=get_green_edges(H)
                            #print 'pre_compute_my_betw'
                            #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #print new_bet_dict
                            #set_betwenness_from_dict(H,new_bet_dict)
                            select_betweeness(H,new_green_edges,distance_metric,type_of_bet)
                            my_draw(H,'5-isp-%d-split'%(counter_isp))

                            #hai trovato il best candidate e sei riuscito a fare split.Finisci
                            bc_found=True
                            flag_no_split=False
                            return couple_selected,new_edges_added,flag_no_split,id_bc


    #ho ciclato su tutti i bc e su tutti i suoi archi per ogni quantita possibile. Non ho travato il bc su cui fare lo split
    if flag_no_split==True and bc_found==False:

        return None,None,flag_no_split,None
    else:
        print 'Flag no split %s'%(str(flag_no_split))
        print 'Bc Found %s'%(str(bc_found))

        sys.exit('Errore in split: ho trovato il bc ma flag_no_split= True o viceversa')



#variante 5: lo split si fa al massimo della feasibility sul bc
def split_by_capacity_path_and_ranking_max_split(H,counter_isp,distance_metric,nodes_recovered,nodes_truely_recovered,type_of_bet):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    global shortest_paths_for_bet
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)


    #lista di tutti i path in ordine di ranking dato dal min(cap_of_path,demand) /max_flow della coppia verde
    ranked_paths_of_bc=[]

    flag_no_split=True

    for i in range(0,len(array_sorted_bcs),1):
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)
            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)

            ranked_paths_of_bc,flag_no_couple=compute_ranking_paths_of_bc(residualGraph,shortest_pass_bc)

            if flag_no_couple == True:
                #flag_no_split=True
                print 'Candidato %d: non ha arco feasible da splittare'%(id_bc)
            else:

                for elem in range(0,len(ranked_paths_of_bc),1):
                    if (bc_found==False):
                        #tupla = ratio, path, demand_to_split_, edge
                        tupla_selected=ranked_paths_of_bc[elem]

                        id_source=tupla_selected[3][0]      #id_source_green
                        id_target=tupla_selected[3][1]      #id_target_green
                        demand=tupla_selected[2]            #domanda dell'arco verde
                        ratio=tupla_selected[0]             #ratio
                        path=tupla_selected[1]              #path associato al ratio demand/maxflow
                        edge_split=(id_source,id_target,demand)

                        print 'INIZIO SPLIT COPPIA: %d-%d-%d: %.2f '%(id_source,id_target,demand,ratio)

                        ##shortest che hanno contribuito alla centralita del bc
                        #print 'Shortest che passno per BC:'
                        #print shortest_pass_bc

                        """
                        shortests_contribute_to_bc=shortest_pass_bc[edge_split]

                        shortest_path=compute_shortest_from_set(residualGraph,shortests_contribute_to_bc,distance_metric)
                        """

                        temp_graph=nx.MultiGraph(residualGraph)
                        couples_to_split=[(id_source,id_bc,0),(id_bc,id_target,0)]
                        temp_green =deepcopy(green_edges)

                        #calcola surplus del nodo
                        surplus=0.0
                        surplus=compute_surplus_of_node(residualGraph,id_bc)+0.0
                        #fai la meta e prendi l'intero inferiore
                        half_surplus=(surplus/2.0)
                        #print 'upper buond surplus: %f'%half_surplus
                        cut_condition_value=min(demand,half_surplus)
                        #print 'al piu prendo :%f'%(cut_condition_value)

                        max_value_to_split=find_max_value_to_split(temp_graph,temp_green,couples_to_split,edge_split,cut_condition_value)
                        #sys.exit(0)
                        #if max_value_to_split<cut_condition_value:
                        #    print 'max value split - cut_condition value = %f -%f'%(max_value_to_split,cut_condition_value)
                        #    sys.exit('Valore massimo splittabile diverso da cut condition')

                        demand_to_assign=max_value_to_split

                        """
                        path_capacity=get_capacity_of_path(residualGraph,path)
                        demand_assigned=0


                        #calcola surplus del nodo
                        surplus=0.0
                        surplus=compute_surplus_of_node(residualGraph,id_bc)
                        #fai la meta e prendi l'intero inferiore
                        half_surplus=int(math.floor(surplus/2.0))

                        if half_surplus>0:
                            demand_to_assign=min(demand,path_capacity,half_surplus)
                        else:
                            demand_to_assign=min(demand,path_capacity)


                        print demand_to_assign
                        """

                        quantity_to_split_flag=False
                        quantity_to_split=demand_to_assign

                        if quantity_to_split>0:


                            #while(quantity_to_split_flag==False):

                                    quantity_to_split_flag=True
                                    demand_to_assign=quantity_to_split
                                    print 'Provo Demand to assign %f'%(demand_to_assign)
                                    if demand_to_assign>0:
                                        #se la domanda da splittare e pari alla domanda totale allora faccio lo split totale dell'arco
                                        if demand == demand_to_assign:
                                            total_split=True
                                        else:
                                            #altrimenti faccio lo split pari alla path_capacity
                                            total_split=False

                                        demand_assigned=demand_to_assign

                                        graph_temp=nx.MultiGraph(H)
                                        print 'Pre simulate split provando con %f di quantita di flusso'%(demand_assigned)
                                        result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,counter_isp)
                                        if result_check==True:
                                            print 'Cut condition ok'
                                            result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                                        else:
                                            print 'Cut condition non soddisfatta'
                                            sys.exit('Impossibile errore in split, cut condition non soddisfatta')
                                            result_routability_check=False
                                            quantity_to_split_flag=True

                                        if result_routability_check==True:
                                            quantity_to_split_flag=True
                                        else:
                                            print 'Routability False, devo cambiare quantita'
                                            sys.exit('Impossibile errore in split, routability check non soddisfatta')
                                            #quantity_to_split=quantity_to_split-1

                                            if quantity_to_split<=0:
                                                quantity_to_split_flag=False
                                                quantity_to_split=0
                                                print 'Non posso piu diminuire la quantita da splittare. Cambio Bc'

                                    elif demand_to_assign==0:
                                            quantity_to_split_flag=True
                                            result_routability_check=False
                                    else:
                                        sys.exit('Errore in splity by capacity: demand_to_assing <0')

                        else:
                            result_routability_check=False

                        #sys.exit('stop')

                        if result_routability_check==True:
                            #modifica grafo originale con lo split degli archi.
                            #aggiungi bc come nodo verde.

                            bc_found=True
                            quantity_to_split_flag=True
                            if H.node[id_bc]['status']=='destroyed':
                                if id_bc not in nodes_recovered:
                                    nodes_recovered.append(id_bc)
                            if H.node[id_bc]['true_status']=='destroyed':
                                if id_bc not in nodes_truely_recovered:
                                    nodes_truely_recovered.append(id_bc)
                            couple_selected=(id_source,id_target,demand)

                            # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                            H.node[id_bc]['type']='green'
                            if H.node[id_bc]['status']=='destroyed':
                                H.node[id_bc]['status']='repaired'
                                H.node[id_bc]['color']='blue'
                            else:
                                H.node[id_bc]['color']='green'

                            #remove green edge between original couple
                            keydict=H[id_source][id_target]
                            #print keydict
                            for k in keydict:
                                if H.edge[id_source][id_target][k]['type']=='green':
                                    key_to_remove=k
                            """
                            if flag_half_split==True:
                                if demand==1:
                                    if demand_assigned==0.5:
                                        if (demand_assigned*2)==demand:
                                            total_split=True
                            """

                            if total_split==True:
                                H.remove_edge(id_source,id_target,key=key_to_remove)
                                #add two new green edge source,bc and bc,target

                            else:
                                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                            #splitta l'arco in due sul bc
                            new_edges_added=[]
                            split_edge(H,id_source,id_bc,demand_assigned)
                            edge_1=(id_source,id_bc,demand_assigned)
                            new_edges_added.append(edge_1)
                            split_edge(H,id_bc,id_target,demand_assigned)
                            edge_2=(id_bc,id_target,demand_assigned)
                            new_edges_added.append(edge_2)

                            #CALCOLA I PATH DELLE NUOVE COPPIE DI ARCHI PRENDENDOLI DALLA COPPIA ORIGINALE
                            #compute_paths_from_split(id_source,id_target,id_bc)
                            """
                            if total_split==True:
                                green_arc=(id_source,id_target)
                                green_arc_reverse=(id_target,id_source)
                                if green_arc in all_graph_paths:
                                    del all_graph_paths[green_arc]
                                elif green_arc_reverse in all_graph_paths:
                                    del all_graph_paths[green_arc_reverse]
                                else:
                                    sys.exit('Errore in spit path and ranking: domanda da rimuovere non presente in all_graph_paths')
                            """
                            #print 'Dopo lo split di %d-%d'%(id_source,id_target)
                            #print all_graph_paths
                            #for edge in H.edges(data=True):
                            #    print edge

                            new_green_edges=get_green_edges(H)
                            #print 'pre_compute_my_betw'
                            #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #print new_bet_dict
                            #set_betwenness_from_dict(H,new_bet_dict)
                            select_betweeness(H,new_green_edges,distance_metric,type_of_bet)
                            my_draw(H,'5-isp-%d-split'%(counter_isp))

                            #hai trovato il best candidate e sei riuscito a fare split.Finisci
                            bc_found=True
                            flag_no_split=False
                            return couple_selected,new_edges_added,flag_no_split,id_bc


    #ho ciclato su tutti i bc e su tutti i suoi archi per ogni quantita possibile. Non ho travato il bc su cui fare lo split
    if flag_no_split==True and bc_found==False:

        return None,None,flag_no_split,None
    else:
        print 'Flag no split %s'%(str(flag_no_split))
        print 'Bc Found %s'%(str(bc_found))

        sys.exit('Errore in split: ho trovato il bc ma flag_no_split= True o viceversa')




#variante 4: si fa lo split prendendo l'arco con maggiore domanda (che ha contribuito al bc)
def split_by_capacity_path_and_demand(H,counter_isp,distance_metric,nodes_recovered,type_of_bet):

    green_edges=get_green_edges(H)
    #print 'archi verdi'
    #print green_edges
    global betwenness_dict
    global shortest_paths_for_bet
    bc_found=False
    array_sorted_bcs=[]
    array_sorted_bcs=get_bc(H)

    flag_no_split=True

    for i in range(0,len(array_sorted_bcs),1):
        if (bc_found==False):

            id_bc=array_sorted_bcs[i][0]
            print '----------------CANDIDATO BEST CANDIDATE: %d ----------------'%(id_bc)

            residualGraph=nx.MultiGraph(H)
            #calcola dizionario con chiavi i green edges e valori i path che hanno contribuito alla betweens del bc
            shortest_pass_bc=compute_shortest_passing_bc(residualGraph,id_bc,green_edges)

            if len(shortest_pass_bc)==0:
                flag_no_couple=True
            else:
                flag_no_couple=False


            if flag_no_couple == True:
                #flag_no_split=True
                print 'Candidato %d: non ha arco feasible da splittare'%(id_bc)
            else:
                #print 'sono qui'
                #sort edge by demand: descendent way
                list_green_bc=retrieve_green_couple_passing_bc_from_dict(shortest_pass_bc)
                list_green_bc=sort_array_demand(list_green_bc,'reverse')
                print 'Domande ordinate decrescente: '
                print list_green_bc
                #sys.exit(0)

                for elem in range(0,len(list_green_bc),1):
                    if (bc_found==False):
                        #tupla = source, target, demand
                        tupla_selected=list_green_bc[elem]

                        id_source=tupla_selected[0]      #id_source_green
                        id_target=tupla_selected[1]      #id_target_green
                        demand=tupla_selected[2]            #domanda dell'arco verde

                        edge_split=(id_source,id_target,demand)

                        print 'INIZIO SPLIT COPPIA: %d-%d-%d'%(id_source,id_target,demand)

                        ##shortest che hanno contribuito alla centralita del bc
                        #print 'Shortest che passno per BC:'
                        #print shortest_pass_bc


                        shortests_contribute_to_bc=shortest_pass_bc[edge_split]

                        shortest_path=compute_shortest_from_set(residualGraph,shortests_contribute_to_bc,distance_metric)


                        path_capacity=get_capacity_of_path(residualGraph,shortest_path)
                        demand_assigned=0


                        #calcola surplus del nodo
                        surplus=0.0
                        surplus=compute_surplus_of_node(residualGraph,id_bc)
                        #fai la meta e prendi l'intero inferiore
                        half_surplus=int(math.floor(surplus/2.0))

                        if half_surplus>0:
                            demand_to_assign=min(demand,path_capacity,half_surplus)
                        else:
                            demand_to_assign=min(demand,path_capacity)


                        print demand_to_assign

                        quantity_to_split_flag=False
                        quantity_to_split=demand_to_assign

                        while(quantity_to_split_flag==False):

                                demand_to_assign=quantity_to_split
                                print 'Provo Demand to assign %f'%(demand_to_assign)
                                if demand_to_assign>0:
                                    #se la domanda da splittare e pari alla domanda totale allora faccio lo split totale dell'arco
                                    if demand == demand_to_assign:
                                        total_split=True
                                    else:
                                        #altrimenti faccio lo split pari alla path_capacity
                                        total_split=False

                                    demand_assigned=demand_to_assign

                                    graph_temp=nx.MultiGraph(H)
                                    print 'Pre simulate split provando con %f di quantita di flusso'%(demand_assigned)
                                    result_check,graph_splitted,temp_green_edges_after_split=simulate_split(graph_temp,id_bc,id_source,id_target,total_split,demand,demand_assigned,counter_isp)
                                    print 'post simulate split'
                                    if result_check==True:
                                        print 'Cut condition ok'
                                        result_routability_check=check_routability(graph_splitted,temp_green_edges_after_split)
                                    else:
                                        print 'Cut condition non soddisfatta'
                                        result_routability_check=False
                                        quantity_to_split_flag=True

                                    if result_routability_check==True:
                                        quantity_to_split_flag=True
                                    else:
                                        print 'Routability False, devo cambiare quantita'
                                        quantity_to_split=quantity_to_split-1
                                        #else:
                                        #   quantity_to_split=quantity_to_split/2.0
                                        """
                                        if quantity_to_split>0 and quantity_to_split<1:
                                            print 'prox quantita = 0'
                                            print 'flag half'
                                            print flag_half_split
                                            if flag_half_split==True:
                                                quantity_to_split=0.5
                                                print 'QUANTITY HALF'
                                        """
                                        if quantity_to_split<=0:
                                            quantity_to_split_flag=False
                                            quantity_to_split=0
                                            print 'Non posso piu diminuire la quantita da splittare. Cambio Bc'

                                elif demand_to_assign==0:
                                        quantity_to_split_flag=True
                                        result_routability_check=False
                                else:
                                    sys.exit('Errore in splity by capacity: demand_to_assing <0')



                        #sys.exit('stop')

                        if result_routability_check==True:
                            #modifica grafo originale con lo split degli archi.
                            #aggiungi bc come nodo verde.

                            bc_found=True
                            quantity_to_split_flag=True
                            if H.node[id_bc]['status']=='destroyed':
                                if id_bc not in nodes_recovered:
                                    nodes_recovered.append(id_bc)

                            couple_selected=(id_source,id_target,demand)

                            # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

                            H.node[id_bc]['type']='green'
                            if H.node[id_bc]['status']=='destroyed':
                                H.node[id_bc]['status']='repaired'
                                H.node[id_bc]['color']='blue'
                                H.node[id_bc]['true_status']='on'
                            else:
                                H.node[id_bc]['color']='green'

                            #remove green edge between original couple
                            keydict=H[id_source][id_target]
                            #print keydict
                            for k in keydict:
                                if H.edge[id_source][id_target][k]['type']=='green':
                                    key_to_remove=k
                            """
                            if flag_half_split==True:
                                if demand==1:
                                    if demand_assigned==0.5:
                                        if (demand_assigned*2)==demand:
                                            total_split=True
                            """

                            if total_split==True:
                                H.remove_edge(id_source,id_target,key=key_to_remove)
                                #add two new green edge source,bc and bc,target
                            else:
                                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

                            #splitta l'arco in due sul bc
                            new_edges_added=[]
                            split_edge(H,id_source,id_bc,demand_assigned)
                            edge_1=(id_source,id_bc,demand_assigned)
                            new_edges_added.append(edge_1)
                            split_edge(H,id_bc,id_target,demand_assigned)
                            edge_2=(id_bc,id_target,demand_assigned)
                            new_edges_added.append(edge_2)

                            #for edge in H.edges(data=True):
                            #    print edge

                            new_green_edges=get_green_edges(H)
                            #print 'pre_compute_my_betw'
                            #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #print new_bet_dict
                            #set_betwenness_from_dict(H,new_bet_dict)
                            select_betweeness(H,new_green_edges,distance_metric,type_of_bet)
                            my_draw(H,'5-isp-%d-split'%(counter_isp))

                            #hai trovato il best candidate e sei riuscito a fare split.Finisci
                            bc_found=True
                            flag_no_split=False
                            return couple_selected,new_edges_added,flag_no_split,id_bc


    #ho ciclato su tutti i bc e su tutti i suoi archi per ogni quantita possibile. Non ho travato il bc su cui fare lo split
    if flag_no_split==True and bc_found==False:

        return None,None,flag_no_split,None
    else:
        print 'Flag no split %s'%(str(flag_no_split))
        print 'Bc Found %s'%(str(bc_found))

        sys.exit('Errore in split: ho trovato il bc ma flag_no_split= True o viceversa')





def compute_ranking_paths_of_bc(H,shortest_pass_bc):

    ranked_paths=[]

    for edge in shortest_pass_bc:

        #print 'Inizio ranking dei path per arco:'
        #print edge

        source=edge[0]
        target=edge[1]
        demand=edge[2]
        max_flow=0.0
        max_flow=compute_max_flow(H,source,target)

        paths_of_edge=shortest_pass_bc[edge]
        #print paths_of_edge

        for path in paths_of_edge:
            #calcola il rank per questo path
            #calcola capacita del path
            cap_path=get_capacity_of_path(H,path)
            demand_to_split=min(demand,cap_path)
            ratio=0.0
            ratio=float ('%.2f'%(demand_to_split/max_flow))
            #crea l'elemento tupla= ( ratio , path , demand, edge)
            tupla=( ratio, path,demand, edge)
            if tupla not in ranked_paths:
                ranked_paths.append(tupla)
            else:
                sys.exit('Errore in compute_ranking_paths_of_bc: aggiunta due volte la stessa tupla')


    #ordina in maniera decrescente di rank le coppie
    ranked_paths=sorted(ranked_paths,key=itemgetter(0), reverse=True)

    #print 'Path del Bc ordinanti decrescenti '
    #print ranked_paths
    #sys.exit(0)
    if len(ranked_paths)==0:
        flag_no_couple=True
    else:
        flag_no_couple=False

    return ranked_paths,flag_no_couple



def get_key_for_sorting_general(item,index):

    return item[index]


def sort_in_order_ratio(array_of_ratio):

    temp=0

    for i in range(0,len(array_of_ratio)):
        for j in range(0,len(array_of_ratio)):
            if array_of_ratio[i][2]<=array_of_ratio[j][2]:
                temp=array_of_ratio[i]
                array_of_ratio[i]=array_of_ratio[j]
                array_of_ratio[j]=temp

    return array_of_ratio

def sort_reverse_ratio(array_of_ratio):

    temp=0

    for i in range(0,len(array_of_ratio)):
        for j in range(0,len(array_of_ratio)):
            if array_of_ratio[i][3]>=array_of_ratio[j][3]:
                temp=array_of_ratio[i]
                array_of_ratio[i]=array_of_ratio[j]
                array_of_ratio[j]=temp

    return array_of_ratio

def simulate_split(H,id_bc,id_source,id_target,total_split,demand,demand_assigned,number_of_split):
        # INIZIO MODIFICA NODI E ARCHI DEL GRAFO

    H.node[id_bc]['type']='green'
    if H.node[id_bc]['status']=='destroyed':
        H.node[id_bc]['status']='repaired'
        H.node[id_bc]['color']='blue'
        H.node[id_bc]['true_status']='on'
    else:
        H.node[id_bc]['color']='green'

    #remove green edge between original couple
    keydict=H[id_source][id_target]
    #print keydict
    for k in keydict:
        if H.edge[id_source][id_target][k]['type']=='green':
            key_to_remove=k

    if total_split==True:
        H.remove_edge(id_source,id_target,key=key_to_remove)
        #add two new green edge source,bc and bc,target
    else:
        H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')

    #splitta l'arco in due sul bc
    new_edges_added=[]
    split_edge(H,id_source,id_bc,demand_assigned)
    edge_1=(id_source,id_bc,demand_assigned)
    new_edges_added.append(edge_1)
    split_edge(H,id_bc,id_target,demand_assigned)
    edge_2=(id_bc,id_target,demand_assigned)
    new_edges_added.append(edge_2)

    #for edge in H.edges(data=True):
    #    print edge

    new_green_edges=get_green_edges(H)
    """
    new_bet_dict=compute_my_betweeness_3(H,new_green_edges,assign_demand_shortest)
    print new_bet_dict
    set_betwenness_from_dict(H,new_bet_dict)
    """
    #my_draw(H,'5-Split_simulated-%d'%(number_of_split))

    if check_routability_split_over_bc(H,id_bc)== True:
        return True,H,new_green_edges
    else:
        return False,H,new_green_edges



def check_routability_split_over_bc(H,id_bc):

    total_demand=0
    total_capacity=0
    edge_green_of_bc=[]
    edge_normal_of_bc=[]

    list_adj=list(nx.all_neighbors(H,id_bc))
    list_couple=[(id_bc,target) for target in list_adj]

    for edge in list_couple:
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]

        for k in keydict:
            if H[id_source][id_target][k]['type']=='green':
                demand=H[id_source][id_target][k]['demand']
                edge_green=(id_source,id_target,demand)
                edge_green_reverse=(id_target,id_source,demand)
                if edge_green not in edge_green_of_bc and edge_green_reverse not in edge_green_of_bc:
                    edge_green_of_bc.append(edge_green)
            elif H[id_source][id_target][k]['type']=='normal':
                capacity=H[id_source][id_target][k]['capacity']
                edge_normal=(id_source,id_target,capacity)
                edge_normal_reverse=(id_target,id_source,capacity)
                if edge_normal not in edge_normal_of_bc and edge_normal_reverse not in edge_normal_of_bc:
                    edge_normal_of_bc.append(edge_normal)

            else:
                sys.exit('Errore in Check routability split: arco no verde, no normal')

    #print 'Controllo array per check demand/capacity'
    #print edge_green_of_bc
    #print edge_normal_of_bc

    for green_edge in edge_green_of_bc:
        demand=green_edge[2]
        total_demand=total_demand+demand

    for normal_edge in edge_normal_of_bc:
        capacity=normal_edge[2]
        total_capacity=total_capacity+capacity


    #print 'Confronto total demand e total capacity %d-%d '%(total_demand,total_capacity)
    if total_demand<= total_capacity:
        return True
    elif total_demand > total_capacity:
        return False
    else:
        sys.exit('Total demand ne <,=,> di total capacity ')


#calcola il surplus tra total capacity e total domand di un nodo

def compute_surplus_of_node(H,id_bc):
    total_demand=0
    total_capacity=0
    edge_green_of_bc=[]
    edge_normal_of_bc=[]

    list_adj=list(nx.all_neighbors(H,id_bc))
    list_couple=[(id_bc,target) for target in list_adj]


    for edge in list_couple:
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]

        for k in keydict:
            if H[id_source][id_target][k]['type']=='green':
                demand=H[id_source][id_target][k]['demand']
                edge_green=(id_source,id_target,demand)
                edge_green_reverse=(id_target,id_source,demand)
                if edge_green not in edge_green_of_bc and edge_green_reverse not in edge_green_of_bc:
                    edge_green_of_bc.append(edge_green)
            elif H[id_source][id_target][k]['type']=='normal':
                capacity=H[id_source][id_target][k]['capacity']
                edge_normal=(id_source,id_target,capacity)
                edge_normal_reverse=(id_target,id_source,capacity)
                if edge_normal not in edge_normal_of_bc and edge_normal_reverse not in edge_normal_of_bc:
                    edge_normal_of_bc.append(edge_normal)

            else:
                sys.exit('Errore in Check routability split: arco no verde, no normal')

    #print 'Controllo array per check demand/capacity'
    #print edge_green_of_bc
    #print edge_normal_of_bc

    for green_edge in edge_green_of_bc:
        demand=green_edge[2]
        total_demand=total_demand+demand

    for normal_edge in edge_normal_of_bc:
        capacity=normal_edge[2]
        total_capacity=total_capacity+capacity

    surplus=0.0
    #print total_capacity
    #print total_demand
    surplus=total_capacity-total_demand

    return surplus

def get_green_edges(H):

    green_edges=[]
    for i in H.nodes():
        source=H.node[i]['id']
        for j in H.nodes():
            target=H.node[j]['id']
            if H.has_edge(source,target):
                keydict=H[source][target]
                for k in keydict:
                    if H[source][target][k]['type']=='green' and H[source][target][k]['color']=='green':
                        demand=H[source][target][k]['demand']
                        #SE FACCIAMO MODIFICA AGGIUNGERE K
                        edge=(source,target,demand)
                        edge_reverse=(target,source,demand)
                        if edge not in green_edges and edge_reverse not in green_edges:
                            green_edges.append(edge)

    return green_edges


def get_bc(H):

    global betwenness_dict
    max_bc=-1
    array_of_bc=[]
    for key in betwenness_dict:
        id_node=int(key)
        value=betwenness_dict[key]
        couple=(id_node,value)
        if couple not in array_of_bc:
            array_of_bc.append(couple)
        if betwenness_dict[key] > max_bc:
            max_bc=betwenness_dict[key]
            id_bc=int(key)

    #print array_of_bc
    #array_sorted=sort_reverse_bc(array_of_bc)
    array_of_bc.sort(key=itemgetter(1),reverse=True)
    #print array_of_bc
    #sys.exit(0)
    return array_of_bc

def sort_reverse_bc(array_of_bc):
    temp=0

    for i in range(0,len(array_of_bc)):
        for j in range(0,len(array_of_bc)):
            if array_of_bc[i][1]>=array_of_bc[j][1]:
                temp=array_of_bc[i]
                array_of_bc[i]=array_of_bc[j]
                array_of_bc[j]=temp

    return array_of_bc

def pruning(H,path_for_pruning,flow_to_prune,couples_to_prune,number_of_prune,distance_metric):

    flow_reduced=reduce_capacity_path(H,path_for_pruning,flow_to_prune)

    if flow_reduced!=flow_to_prune:
        sys.exit("Non e stato fatto il pruning assegnato ")

    else:
        for couple in couples_to_prune:

            id_source=couple[0]
            id_target=couple[1]
            demand=couple[2]

            keydict=H[id_source][id_target]

            for k in keydict:
                if H.edge[id_source][id_target][k]['type']=='green':
                    key_to_prune=k
                    #current_demand=H.edge[id_source][id_target][k]['demand']

            if demand==flow_reduced:
                #total prune of the green edge and its demand
                H.remove_edge(id_source,id_target,key=key_to_prune)
                #add two new green edge source,bc and bc,target
            else:
                #partial prune of the green edge
                H.add_edge(id_source, id_target, key=key_to_prune, type='green', demand=(demand-flow_reduced), color='green',style='bold')

    id_bc=(couples_to_prune[0])[1]

    #remove_saturated_edge(H)
    check_if_are_green(H)



    new_green_edges=get_green_edges(H)
    new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
    #print new_bet_dict
    set_betwenness_from_dict(H,new_bet_dict)

    my_draw(H,'5-isp-%d-pruned'%(number_of_prune))


def get_capacity_of_path(H,path):

    path_capacity=sys.maxint

    for i in range(0,(len(path)-1),1):
        id_source=path[i]
        id_target=path[(i+1)]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':
                    edge_capacity = H[id_source][id_target][k]['capacity']
                    if edge_capacity < path_capacity:
                        path_capacity=edge_capacity
        else:
            print path
            print 'arco mancante: %d-%d'%(id_source,id_target)
            sys.exit('Errore get_capacity_of_path: arco inesistente')
    return path_capacity



def pruning_multiple(H,paths_for_pruning,counter_isp,counter_pruning,distance_metric,type_of_bet):
    #global all_graph_paths

    for path in paths_for_pruning:
        path_cap=get_capacity_of_path(H,path)
        #get_the_current_demand:
        id_source=path[0]
        id_target=path[len(path)-1]
        #print 'arco da fare il pruning %d-%d'%(id_source,id_target)
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green' and H[id_source][id_target][k]['type']!='normal':
                    demand=H[id_source][id_target][k]['demand']
                    key_to_prune=k

        flow_to_prune=min(path_cap,demand)
        flow_reduced=reduce_capacity_path(H,path,flow_to_prune,cap_of_path=path_cap)

        if flow_reduced!=flow_to_prune:
            sys.exit("Non e stato fatto il pruning assegnato ")

        else:
            if demand==flow_reduced:
                #total prune of the green edge and its demand
                H.remove_edge(id_source,id_target,key=key_to_prune)
                green_arc=(id_source,id_target)
                green_arc_reverse=(id_target,id_source)
                """
                if green_arc in all_graph_paths:
                    del all_graph_paths[green_arc]
                elif green_arc_reverse in all_graph_paths:
                    del all_graph_paths[green_arc_reverse]
                else:
                    sys.exit('Errore in Pruning multiple: domanda da rimuovere non presente in all_graph_paths')
                """
                update_status_node(H,id_source)
                update_status_node(H,id_target)

            else:
                #partial prune of the green edge
                H.add_edge(id_source, id_target, key=key_to_prune, type='green', demand=(demand-flow_reduced), color='green',style='bold')

        #remove_saturated_edge(H)
        #check_if_are_green(H)

    #Pruning finito procedere ad aggiornare tutte le centralita e disegnare il nuovo grafo pruned

    new_green_edges=get_green_edges(H)
    #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
    #print new_bet_dict
    #set_betwenness_from_dict(H,new_bet_dict)
    select_betweeness(H,new_green_edges,distance_metric,type_of_bet)
    #print 'pruning multiplo'
    my_draw(H,'5-isp-%d-prune_%d'%(counter_isp,counter_pruning))


def pruning_multiple_after_recover(H,paths_for_pruning,edges_to_prune,flow_to_prune,number_of_prune,distance_metric):

    for path in paths_for_pruning:
        path_cap=get_capacity_of_path(H,path)
        #get_the_current_demand:
        id_source=path[0]
        id_target=path[len(path)-1]
        #print 'arco da fare il pruning %d-%d'%(id_source,id_target)
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green' and H[id_source][id_target][k]['type']!='normal':
                    demand=H[id_source][id_target][k]['demand']
                    key_to_prune=k

        flow_to_prune=min(path_cap,demand)
        flow_reduced=reduce_capacity_path(H,path,flow_to_prune)

        if flow_reduced!=flow_to_prune:
            sys.exit("Non e stato fatto il pruning assegnato ")

        else:
            if demand==flow_reduced:
                #total prune of the green edge and its demand
                H.remove_edge(id_source,id_target,key=key_to_prune)
                #add two new green edge source,bc and bc,target
            else:
                #partial prune of the green edge
                H.add_edge(id_source, id_target, key=key_to_prune, type='green', demand=(demand-flow_reduced), color='green',style='bold')

        #remove_saturated_edge(H)
        check_if_are_green(H)

    #Pruning finito procedere ad aggiornare tutte le centralita e disegnare il nuovo grafo pruned

    new_green_edges=get_green_edges(H)
    new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
    #print new_bet_dict
    set_betwenness_from_dict(H,new_bet_dict)
    #print 'pruning multiplo'
    my_draw(H,'5-split-%d-recover-pruned'%(number_of_prune))

"""
def recover_one_hop_edge_green(H,edges_recovered,nodes_recovered):

    green_edges=get_green_edges(H)
    print green_edges
    destroyed_graph=nx.MultiGraph(get_graph_from_destroyed_graph(H))
    #vale true se ho riparato almeno un link ad 1 hop
    recovered_flag=False

    #lista delle coppie ad un hop
    recovered_edge_one_hop=[]

    #my_draw(destroyed_graph,'5-isp_grafo_distrutto_da_controllare')
    for couple in green_edges:
        supply_edge=False
        id_source=couple[0]
        id_target=couple[1]
        demand=couple[2]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']!='green' and H[id_source][id_target][k]['type']=='normal':
                    if supply_edge==False:
                        supply_edge=True
                        #print H[id_source][id_target][k]
                        arc=(id_source,id_target,k)
                    else:
                        sys.exit('Errore in recovery pruning one hop: piu di un arco normal tra stessa coppia!!')

        if supply_edge==True:

            #vedi se il flusso residuo soddisfa la domanda, altrimenti lo ripristini
            max_flow_on_residual=compute_max_flow(destroyed_graph,id_source,id_target)

            if max_flow_on_residual < demand :
                #need to repair the arc
                source=arc[0]
                target=arc[1]
                key_to_recover=arc[2]
                if H[source][target][key_to_recover]['status']=='destroyed':
                    #seamus add if for color true_status
                    if H[source][target][key_to_recover]['true_status'] == 'on':
                        H.add_edge(source,target,key=key_to_recover, type='normal',status='on',true_status='on',labelfont='black',color='black',style='solid')
                    else:
                        H.add_edge(source,target,key=key_to_recover, type='normal',status='repaired',true_status='on',labelfont='blue',color='blue',style='solid')
                    recovered_flag=True
                    print 'Arco Ricoverato one hop: %d - %d'%(source,target)
                    edge=(source,target)
                    if edge not in edges_recovered:
                        edges_recovered.append(edge)

                        #aggiungi l'arco tra quelli da controllare per fare il pruning
                        if edge not in recovered_edge_one_hop:
                            recovered_edge_one_hop.append(edge)

                        #controllo se i nodi sono da ripristinare
                        if H.node[source]['status']=='destroyed':
                            if source not in nodes_recovered:
                                nodes_recovered.append(source)
                                H.node[source]['status']='repaired'
                                H.node[source]['color']='blue'
                                H.node[source]['true_status']='on'

                        if H.node[target]['status']=='destroyed':
                            if target not in nodes_recovered:
                                nodes_recovered.append(target)
                                H.node[target]['status']='repaired'
                                H.node[target]['color']='blue'
                                H.node[target]['true_status']='on'
                    else:
                        sys.exit('Errore in recover_one_hop: arco gia riparato in precedenza!!')
                else:
                    print 'Arco non rotto da riparare'
                    print arc
                    sys.exit('Errore in recover_one_hop: arco non rotto selezionato per essere riparato!!')

    return recovered_edge_one_hop,recovered_flag
"""

def recover_one_hop_edge_green(H,edges_recovered,nodes_recovered,edges_truely_recovered,nodes_truely_recovered):

    green_edges=get_green_edges(H)
    print green_edges
    destroyed_graph=nx.MultiGraph(get_graph_from_destroyed_graph(H))
    really_destroyed_graph=nx.MultiGraph(get_graph_from_truely_destroyed_graph(H))
	
    #vale true se ho riparato almeno un link ad 1 hop
    recovered_flag=False

    #lista delle coppie ad un hop
    recovered_edge_one_hop=[]

    #my_draw(destroyed_graph,'5-isp_grafo_distrutto_da_controllare')
    for couple in green_edges:
        supply_edge=False
        id_source=couple[0]
        id_target=couple[1]
        demand=couple[2]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']!='green' and H[id_source][id_target][k]['type']=='normal':
                    if supply_edge==False:
                        supply_edge=True
                        #print H[id_source][id_target][k]
                        arc=(id_source,id_target,k)
                    else:
                        sys.exit('Errore in recovery pruning one hop: piu di un arco normal tra stessa coppia!!')

        if supply_edge==True:

            #vedi se il flusso residuo soddisfa la domanda, altrimenti lo ripristini
            #max_flow_on_residual=compute_max_flow(destroyed_graph,id_source,id_target)
            max_flow_on_residual=compute_max_flow(destroyed_graph,id_source,id_target)

            if max_flow_on_residual < demand :
                #need to repair the arc
                source=arc[0]
                target=arc[1]
                key_to_recover=arc[2]
#DIMAN Added
                if H[source][target][key_to_recover]['status']=='destroyed':
                    if H[source][target][key_to_recover]['true_status']=='destroyed':				
                        H.add_edge(source,target,key=key_to_recover, type='normal',status='repaired',labelfont='blue',color='blue',style='solid')
                        recovered_flag=True
                        print 'Arco Ricoverato one hop: %d - %d'%(source,target)
                        edge=(source,target)
                        if edge not in edges_truely_recovered:
                            edges_truely_recovered.append(edge)

                        #aggiungi l'arco tra quelli da controllare per fare il pruning
                            if edge not in recovered_edge_one_hop:
                                recovered_edge_one_hop.append(edge)

                        #controllo se i nodi sono da ripristinare
                            if H.node[source]['true_status']=='destroyed':
                                if source not in nodes_truely_recovered:
                                    nodes_truely_recovered.append(source)
                                    H.node[source]['status']='repaired'
                                    H.node[source]['color']='blue'

                            if H.node[target]['true_status']=='destroyed':
                                if target not in nodes_truely_recovered:
                                    nodes_truely_recovered.append(target)
                                    H.node[target]['status']='repaired'
                                    H.node[target]['color']='blue'
#DIMAN Added

                if H[source][target][key_to_recover]['status']=='destroyed':
                #if H[source][target][key_to_recover]['true_status']=='destroyed':
				
                    #H.add_edge(source,target,key=key_to_recover, type='normal',status='repaired',labelfont='blue',color='blue',style='solid')
                    #recovered_flag=True
                    print 'Arco Ricoverato one hop: %d - %d'%(source,target)
                    edge=(source,target)
                    if H[source][target][key_to_recover]['true_status']=='destroyed':						
                        if edge not in edges_truely_recovered:
                            edges_truely_recovered.append(edge)					
                    if edge not in edges_recovered:
                        edges_recovered.append(edge)
						
                        #aggiungi l'arco tra quelli da controllare per fare il pruning
                        if edge not in recovered_edge_one_hop:
                            recovered_edge_one_hop.append(edge)

                        #controllo se i nodi sono da ripristinare
                        if H.node[source]['status']=='destroyed':
                            if source not in nodes_recovered:
                                nodes_recovered.append(source)
                                H.node[source]['status']='repaired'
                                H.node[source]['color']='blue'
                        if H.node[source]['true_status']=='destroyed':
                            if source not in nodes_truely_recovered:
                                nodes_truely_recovered.append(source)
                                H.node[source]['status']='repaired'
                                H.node[source]['color']='blue'
								
                        if H.node[target]['status']=='destroyed':
                            if target not in nodes_recovered:
                                nodes_recovered.append(target)
                                H.node[target]['status']='repaired'
                                H.node[target]['color']='blue'
                        if H.node[target]['true_status']=='destroyed':
                            if target not in nodes_truely_recovered:
                                nodes_truely_recovered.append(target)
                                H.node[target]['status']='repaired'
                                H.node[target]['color']='blue'

                    else:
                        sys.exit('Errore in recover_one_hop: arco gia riparato in precedenza!!')
                else:
                    print 'Arco non rotto da riparare'
                    print arc
                    sys.exit('Errore in recover_one_hop: arco non rotto selezionato per essere riparato!!')								
			
#Diman Added

#                if H[source][target][key_to_recover]['status']=='destroyed':
#                    H.add_edge(source,target,key=key_to_recover, type='normal',status='repaired',labelfont='blue',color='blue',style='solid')
#                    recovered_flag=True
#                    print 'Arco Ricoverato one hop: %d - %d'%(source,target)
#                    edge=(source,target)
#                    if edge not in edges_recovered:
#                        edges_recovered.append(edge)
#
#                        #aggiungi l'arco tra quelli da controllare per fare il pruning
#                        if edge not in recovered_edge_one_hop:
#                            recovered_edge_one_hop.append(edge)
#
#                        #controllo se i nodi sono da ripristinare
#                        if H.node[source]['status']=='destroyed':
#                            if source not in nodes_recovered:
#                                nodes_recovered.append(source)
#                                H.node[source]['status']='repaired'
#                                H.node[source]['color']='blue'
#
#                        if H.node[target]['status']=='destroyed':
#                            if target not in nodes_recovered:
#                                nodes_recovered.append(target)
#                                H.node[target]['status']='repaired'
#                                H.node[target]['color']='blue'
#								

    return recovered_edge_one_hop,recovered_flag


def pruning_one_hop(H,recovered_edges_one_hop,distance_metric,counter_isp,type_of_bet):

    couple_pruned_one_hop=[]
    #global all_graph_paths

    #my_draw(H,'5-isp_grafo_distrutto_da_controllare')
    for couple in recovered_edges_one_hop:
        supply_edge=False
        pruning_flag=False
        id_source=couple[0]
        id_target=couple[1]
        demand=get_demand_of_couple(H,id_source,id_target)
        #print couple
        #print demand
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green' :
                    arc_green=(id_source,id_target,k)

                elif H[id_source][id_target][k]['type']=='normal':
                    if H[id_source][id_target][k]['status']!='destroyed':
                        if supply_edge==False:
                            supply_edge=True
                            #print H[id_source][id_target][k]
                            arc=(id_source,id_target,k)
                            pruning_flag=True
                        else:
                            sys.exit('Errore in recovery pruning one hop: piu di un arco normal tra stessa coppia!!')

        if pruning_flag==True:
            edge_pruned=(arc[0],arc[1])
            if edge_pruned not in couple_pruned_one_hop:
                #print 'da fare pruning'
                couple_pruned_one_hop.append(edge_pruned)

            cap_path=H[arc[0]][arc[1]][arc[2]]['capacity']
            #print cap_path
            flow_to_prune=min(demand,cap_path)
            #print flow_to_prune
            if flow_to_prune==cap_path:
                #edges_to_remove.append(arc)
                H.remove_edge(arc[0],arc[1],arc[2])
                #print 'rimosso'
            else:
                H.add_edge(arc[0],arc[1],arc[2],capacity=cap_path-flow_to_prune)
                #print 'nuova capacita arco %f'%H[arc[0]][arc[1]][arc[2]]['capacity']
                #print 'aggiornato'

            if flow_to_prune==demand:
                H.remove_edge(arc_green[0],arc_green[1],arc_green[2])
                update_status_node(H,arc_green[0])
                update_status_node(H,arc_green[1])
            else:
                H.add_edge(arc_green[0],arc_green[1],arc_green[2], type='green', demand=demand-flow_to_prune, color='green',style='bold')
                #print'aggiornato verde'

    #check_if_are_green(H)

    print 'fine pruning one hop'

    new_green_edges=get_green_edges(H)
    #print new_green_edges
    #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
    #print new_bet_dict
    #set_betwenness_from_dict(H,new_bet_dict)

    #print_edge_graph(H)

    #select_betweeness(H,new_green_edges,distance_metric,type_of_bet)

    #print 'pruning multiplo'
    my_draw(H,'5-isp-%d-prune_one_hop'%(counter_isp))

    return couple_pruned_one_hop

def update_couple_to_prune(couples_to_prune,couple_pruned):

    couple_to_remove=[]

    #print 'couple pruned ad un hop'
    #print couple_pruned

    if couples_to_prune!=None:
        #print 'couples to prune'
        #print couples_to_prune
        for couple in couples_to_prune:
            arc=(couple[0],couple[1])
            arc_reverse=(couple[1],couple[0])
            #print 'analisi couple'
            #print couple

            if arc in couple_pruned  or arc_reverse in couple_pruned:
                #print 'rimuovo'
                #print couple
                couple_to_remove.append(couple)

    for elem in couple_to_remove:
        if elem in couples_to_prune:
            couples_to_prune.remove(elem)
        else:
            sys.exit('Errore in update couples to prune: coppia da rimuovere inesistente')


def add_edges_recovered_to_graph(H,graph_built,edges_recovered):

    for edge in edges_recovered:
        source=edge[0]
        target=edge[1]
        if H.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type']=='normal':
                    cap=H[source][target][k]['capacity']
                    graph_built.add_edge(source,target, type='normal',status='repaired',labelfont='blue',color='blue',style='solid',capacity=cap)
        else:

            sys.exit('Errore in add_edges_recovered_to_graph: larco da aggiungere non esiste nel grafo supply')

def add_node_to_graph_recovered(H,graph_built,id_nodo):

        for node in H.nodes():
            if H.node[node]['id']==id_nodo:

                if id_nodo not in graph_built.nodes():
                    long=H.node[node]['Longitude']
                    lat=H.node[node]['Latitude']
                    graph_built.add_node(H.node[node]['id'],id=id_nodo,Longitude=long,Latitude=lat)


def recovery_supply_graph(H,temp_graph_supply,nodes_recovered,edges_recovered):

    #ripara i nodi
    print 'ciao'





def compute_max_flow(graph,id_source,id_target):

    nodes=[]
    edges=[]

    clean_edges(nodes)

    for j in graph.nodes():
        nodes.append(Vertex(graph.node[j]['id']))

    clean_edges(nodes)
    del edges
    edges=get_Edges_residual(graph)
    buildGraph(nodes,edges)
    #for node in nodes:
    #    print node.name
    #print id_source
    #print id_target
    source_index=int(get_index_vertex(nodes,id_source))
    target_index=int(get_index_vertex(nodes,id_target))

    max_flow=maxFlow(nodes[source_index],nodes[target_index])
    #print 'max_flow tra %d-%d : %d '%(nodes[source_index].name,nodes[bc_index].name,max_flow_to_bc)

    return max_flow

#DIMAN ADDED
def Find_truely_recovered_nodes(H,nodes_recovered_isp):

    nodes_truely_recovered=[]

    for node in nodes_recovered_isp:
        if H.node[node]['true_status']=='destroyed':
            nodes_truely_recovered.append(node)

    return nodes_truely_recovered

def Find_truely_recovered_edges(H,edges_recovered_isp):

    edges_truely_recovered=[]

#    for edge in edges_recovered_isp:
#        source=edge[0]
#        target=edge[1]
#        #if H.has_edge(source,target):
#        keydict=H[source][target]
#        for k in keydict:
#            if H[source][target][k]['true_status']=='destroyed':
#                if edge not in edges_truely_recovered:
#				    edges_truely_recovered.append(edge)

    for edge in edges_recovered_isp:
                keydict=H[edge[0]][edge[1]]
                for k in keydict:
                    arc=(edge[0],edge[1])
                    arc_reverse=(edge[1],edge[0])
                    if arc not in edges_truely_recovered and arc_reverse not in edges_truely_recovered:
                        edges_truely_recovered.append(arc)
				
    return edges_truely_recovered	
#DIMAN ADDED	
def recover_all_green_nodes_really_destroyed(H):

    nodes_recovered=[]
    for node in H.nodes():
        if H.node[node]['type']=='green' and H.node[node]['type']!='normal':
            if H.node[node]['true_status']=='destroyed':
                #ripristina nodo verde distrutto
                H.node[node]['status']='repaired'
                H.node[node]['color']='blue'
                id_node=H.node[node]['id']
                nodes_recovered.append(id_node)
            #if H.node[node]['true_status']=='destroyed':
            #    if H.node[node]['true_status']=='on':
            #    H.node[node]['status']='repaired'
            #    H.node[node]['color']='blue'
            #    id_node=H.node[node]['id']
            #    nodes_recovered.append(id_node)
    return nodes_recovered
	
#DIMAN ADDED	
	
def recover_all_green_nodes_destroyed(H):

    nodes_recovered=[]
    for node in H.nodes():
        if H.node[node]['type']=='green' and H.node[node]['type']!='normal':
            if H.node[node]['status']=='destroyed':
                #ripristina nodo verde distrutto
                H.node[node]['status']='repaired'
                H.node[node]['color']='blue'
                H.node[node]['true_status']='on'
                id_node=H.node[node]['id']
                nodes_recovered.append(id_node)

    return nodes_recovered

def check_if_are_green(H):
    count=0
    number_of_green_nodes=0

    get_green_edges()

    for node_source in H.nodes():
        count=0
        id_source= H.node[node_source]['id']
        for node_target in H.nodes():
            id_target=H.node[node_target]['id']
            if H.has_edge(id_source,id_target):
                keydict=H[id_source][id_target]
                for key in keydict:
                    if H[id_source][id_target][key]['type']=='green':
                        count=count+1
                        number_of_green_nodes=number_of_green_nodes+1

        if count==0:
            #non ha piu archi verdi.
            H.node[node_source]['type']='normal'
            if H.node[node_source]['status']=='destroyed':
                H.node[node_source]['color']='red'
            elif  H.node[node_source]['status']=='repaired':
                H.node[node_source]['color']='blue'
            elif H.node[node_source]['status']=='on':
                H.node[node_source]['color']='None'
            else:
                sys.exit('Errore check if all green: nodo ne on,ne repaired,ne destroyed')

    if number_of_green_nodes>0:
        return True
        print 'ci sono ancora nodi verdi'
    else:
        print 'Non ci sono piu archi verdi'
        return False


def recovery_algorithm_based_on_shortest(H,distance_metric):

    nodes_recovered=[]
    edges_recovered=[]
    policy_sorting='reverse'
    iteration=0


    while(check_if_are_green(H)):

        green_edges=get_green_edges(H)

        #array delle domande ordinato
        green_edges_sorted=sort_array_demand(green_edges,policy_sorting)
        #print green_edges_sorted

        for couple in green_edges_sorted:
            #print 'coppia da soddisfare'
            #print couple
            graph_dict=convert_graph_to_dict(H)
            id_source=couple[0]
            id_target=couple[1]
            #all_paths=find_all_paths(graph_dict,id_source,id_target,[])
            demand=couple[2]

            key_to_remove=-1
            #find key of the edge to remove
            if H.has_edge(id_source,id_target):
                keydict=H[id_source][id_target]
                for k in keydict:
                    if H[id_source][id_target][k]['type']=='green' and H[id_source][id_target][k]['type']!='normal':
                        key_to_remove=k
            else:
                print 'Arco mancante %d-%d: '%(id_source,id_target)
                sys.exit('Errore in recovery algorithm based on shortest: non esiste l arco verde da rimuovere')


            while(demand>0):
                shortest_paths=compute_shortest_paths_on_residual(H,id_source,id_target,distance_metric)

                if len(shortest_paths)==0:
                    sys.exit('Errore in recovery_algorithm_based_on_shortest: non ci sono piu path per soddisfare la domanda corrente')
                else: #esiste almeno un path che si puo usare
                    size=(len(shortest_paths))-1
                    if size==0:
                        index_random=0
                    else:
                        index_random=random.randint(0,size)

                    curr_shortest=shortest_paths[index_random]

                    #----------------------MODIFICA SUL TEST DELLA ROUTABILITY
                    graph_temp=nx.MultiGraph(H)
                    graph_pruned,temp_green_edges_pruning=simulate_pruning(graph_temp,curr_shortest,demand,distance_metric,iteration)

                    if check_routability(graph_pruned,temp_green_edges_pruning)==True:
                        print 'Shortest prunable'

                        if check_if_path_exist(H,curr_shortest):
                            #ripristina tutti i nodi e i link del path utilizzato per soddisfare la domanda
                            recover_entire_path(H,curr_shortest,nodes_recovered,edges_recovered,)

                            iteration=iteration+1
                            new_green_edges=get_green_edges(H)
                            #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #set_betwenness_from_dict(H,new_bet_dict)
                            my_draw(H,'13-recovered_shortest_iteration_%d'%(iteration))

                            cap_of_path=get_capacity_of_path(H,curr_shortest)
                            demand_to_assign=min(cap_of_path,demand)
                            demand_assigned=reduce_capacity_path(H,curr_shortest,demand_to_assign)
                            demand=demand-demand_assigned

                            if demand==0:
                                H.remove_edge(id_source,id_target,key=key_to_remove)
                                #add two new green edge source,bc and bc,target
                            elif demand > 0:
                                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
                            else:
                                sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

                            iteration=iteration+1
                            new_green_edges=get_green_edges(H)
                            #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                            #set_betwenness_from_dict(H,new_bet_dict)
                            check_if_are_green(H)
                            my_draw(H,'13-recovered_shortest_iteration_%d'%(iteration))

                    else:
                        #non posso selezionare questo shortest altrimenti comprometto la soluzione finale.
                        # Forzo la condizione di uscita come se avessi soddisfatto la domanda
                        demand=0

    return nodes_recovered,edges_recovered




def recovery_algorithm_based_on_shortest_no_routability(H,distance_metric):

    nodes_recovered=[]
    edges_recovered=[]
    policy_sorting='reverse'
    iteration=0

    demand_inibited=[]
    #while(check_if_are_green(H)):

    green_edges=get_green_edges(H)

    #array delle domande ordinato
    #green_edges_sorted=sort_array_demand(green_edges,policy_sorting)
    #print green_edges_sorted

    for couple in green_edges:
        #print 'coppia da soddisfare'
        #print couple
        graph_dict=convert_graph_to_dict(H)
        id_source=couple[0]
        id_target=couple[1]
        #all_paths=find_all_paths(graph_dict,id_source,id_target,[])
        demand=couple[2]

        key_to_remove=-1
        #find key of the edge to remove
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green' and H[id_source][id_target][k]['type']!='normal':
                    key_to_remove=k
        else:
            print 'Arco mancante %d-%d: '%(id_source,id_target)
            sys.exit('Errore in recovery algorithm based on shortest: non esiste l arco verde da rimuovere')


        while(demand>0):
            shortest_paths=compute_shortest_paths_on_residual(H,id_source,id_target,distance_metric)

            if len(shortest_paths)==0:
                #sys.exit('Errore in recovery_algorithm_based_on_shortest: non ci sono piu path per soddisfare la domanda corrente')
                # non ci sono piu path per questa coppia di domanda.
                #va aggiunta alle domanda non soddisfatte e si prosegue con la prossima.
                #demand_inibited.append(couple)
                demand=0
            else: #esiste almeno un path che si puo usare
                size=(len(shortest_paths))-1
                if size==0:
                    index_random=0
                else:
                    index_random=random.randint(0,size)

                curr_shortest=shortest_paths[index_random]


                if check_if_path_exist(H,curr_shortest):
                    print 'Shortest prunable'

                    #ripristina tutti i nodi e i link del path utilizzato per soddisfare la domanda
                    recover_entire_path(H,curr_shortest,nodes_recovered,edges_recovered,)

                    iteration=iteration+1
                    new_green_edges=get_green_edges(H)
                    #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                    #set_betwenness_from_dict(H,new_bet_dict)
                    my_draw(H,'13-recovered_shortest_iteration_%d'%(iteration))

                    cap_of_path=get_capacity_of_path(H,curr_shortest)
                    demand_to_assign=min(cap_of_path,demand)
                    demand_assigned=reduce_capacity_path(H,curr_shortest,demand_to_assign)
                    demand=demand-demand_assigned

                    if demand==0:
                        H.remove_edge(id_source,id_target,key=key_to_remove)
                        #add two new green edge source,bc and bc,target
                    elif demand > 0:
                        H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
                    else:
                        sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

                    iteration=iteration+1
                    new_green_edges=get_green_edges(H)
                    #new_bet_dict=compute_my_betweeness_3(H,new_green_edges,distance_metric)
                    #set_betwenness_from_dict(H,new_bet_dict)
                    check_if_are_green(H)
                    my_draw(H,'13-recovered_shortest_iteration_%d'%(iteration))


    green_residual=get_green_edges(H)
    demand_residual=0.0
    for edge in green_residual:
        elem=edge[2]
        demand_residual+=elem
    """
    #calcola quanta domanda non e stata soddisfatta
    demand_not_assigned=0.0
    for demand in demand_inibited:
        curr_demand=demand[2]
        demand_not_assigned+=curr_demand

    if demand_not_assigned!=demand_residual:
        print 'Domanda green_edges %f'%(demand_residual)
        print 'Domanda not satisfied %f'%(demand_not_assigned)
        sys.exit('Errore in shortest algorithm: domanda residue non corrispondono')
    """

    return nodes_recovered,edges_recovered, demand_residual


#Per ogni coppia viene calcolato l'insieme minimo di shortest path che servono per soddisfare quella coppia
#Tutte le coppie calcolano i loro insiemi in modo indipendente. Calcolano gli shortest sul grafo distrutto inizialmente
#senza considerare le altre coppie. NON FA COMMITMENT
#OLD WITH ALL_PATHS
def recovery_algorithm_based_on_shortest_set(H,distance_metric):

    nodes_recovered=[]
    edges_recovered=[]
    policy_sorting='reverse'
    iteration=0

    green_edges=get_green_edges(H)

    #array delle domande ordinato
    #green_edges_sorted=sort_array_demand(green_edges,policy_sorting)
    #print green_edges_sorted

    original_graph_destroyed=nx.MultiGraph(H)
    paths_total_to_recover=[]

    #global all_graph_paths

    for couple in green_edges:
        #print 'coppia da soddisfare'
        #print couple
        id_source=couple[0]
        id_target=couple[1]
        demand=couple[2]

        couple_1=(id_source,id_target)
        couple_reverse=(id_target,id_source)

        if couple_1 in all_graph_paths:
            paths_of_couple=all_graph_paths[couple_1]
        elif couple_reverse in all_graph_paths:
            paths_of_couple=all_graph_paths[couple_reverse]
        else:
            sys.exit('Errore in compute shortest set: la coppia non esiste in all_graph_paths')

        #ordina i path in base al costo totale
        paths_of_couple=sort_path_by_cost(original_graph_destroyed,paths_of_couple)
        set_of_shortest_path=[]
        set_of_shortest_path=compute_set_of_shortest_demand_based(original_graph_destroyed,paths_of_couple,id_source,id_target,demand)

        for elem in set_of_shortest_path:
            if elem not in paths_total_to_recover:
                paths_total_to_recover.append(elem)


    for path in paths_total_to_recover:
        recover_entire_path(H,path,nodes_recovered,edges_recovered)

    #green_residual=get_green_edges(H)
    #demand_residual=0.0
    #for edge in green_residual:
    #    elem=edge[2]
    #    demand_residual+=elem


    return nodes_recovered,edges_recovered


#NEW OPTIMIZED VERSION
def recovery_algorithm_based_on_shortest_set_opt(H,shortest_set_algo,distance_metric):

    nodes_recovered=[]
    edges_recovered=[]
    policy_sorting='reverse'
    iteration=0

    green_edges=get_green_edges(H)

    #array delle domande ordinato
    #green_edges_sorted=sort_array_demand(green_edges,policy_sorting)
    #print green_edges_sorted

    original_graph_destroyed=nx.MultiGraph(H)
    paths_total_to_recover=[]

    print shortest_set_algo

    for couple in green_edges:
        #print 'coppia da soddisfare'
        #print couple
        id_source=couple[0]
        id_target=couple[1]
        demand=couple[2]

        couple_1=(id_source,id_target)
        couple_reverse=(id_target,id_source)

        if couple_1 in shortest_set_algo:
            paths_of_couple=shortest_set_algo[couple_1]
        elif couple_reverse in shortest_set_algo:
            paths_of_couple=shortest_set_algo[couple_reverse]
        else:
            print couple
            sys.exit('Errore in compute shortest set: la coppia non esiste in shortest_set_algo')

        #ordina i path in base al costo totale
        paths_of_couple=sort_path_by_cost(original_graph_destroyed,paths_of_couple)
        set_of_shortest_path=[]
        set_of_shortest_path=paths_of_couple
        #set_of_shortest_path=compute_set_of_shortest_demand_based(original_graph_destroyed,paths_of_couple,id_source,id_target,demand)

        for elem in set_of_shortest_path:
            if elem not in paths_total_to_recover:
                paths_total_to_recover.append(elem)


    for path in paths_total_to_recover:
        recover_entire_path(H,path,nodes_recovered,edges_recovered)

    #green_residual=get_green_edges(H)
    #demand_residual=0.0
    #for edge in green_residual:
    #    elem=edge[2]
    #    demand_residual+=elem


    return nodes_recovered,edges_recovered


def sort_path_by_cost(H,paths_of_couple):

    paths_ranked=[]

    for path in paths_of_couple:
        cost_of_path=0.0
        cost_of_path=compute_cost_of_path(H,path)
        tupla=(cost_of_path,path)
        if tupla not in paths_ranked:
            paths_ranked.append(tupla)


    paths_ranked=sorted(paths_ranked,key=itemgetter(0),reverse=False)
    path_to_return=[]
    #print paths_ranked
    for path in paths_ranked:
        if path[1] not in path_to_return:
            path_to_return.append(path[1])

    #print path_to_return
    #sys.exit(0)
    return path_to_return

def compute_set_of_shortest_demand_based(original_graph_destroyed,paths_of_couple,id_source,id_target,demand):

    paths_selected=[]

    demand_flag=False
    number_of_path=1
    paths_selected=[]

    while(demand_flag==False):
        paths_selected=get_first_n_element_of_list(paths_of_couple,number_of_path)
        current_flow=compute_total_flow_based_on_real_flow(original_graph_destroyed,paths_selected,id_source,id_target)

        if current_flow>=demand:
            demand_flag=True
        else:
            number_of_path+=1

    return paths_selected

def get_first_n_element_of_list(paths_of_couple,number_of_path):

    paths_selected=[]
    if len(paths_of_couple)<number_of_path:
        sys.exit('Errore in get_first_n_element: richiesti piu elementi di quanti ce ne sono')

    for i in range(0,number_of_path,1):
        curr_path=paths_of_couple[i]
        if curr_path not in paths_selected:
            paths_selected.append(curr_path)

    return paths_selected

def compute_total_demand_of_graph(H):

    total=0.0
    green_edges=get_green_edges(H)
    for couple in green_edges:
        curr_demand=couple[2]
        total+=curr_demand

    return total


def recover_entire_path(H,path,nodes_recovered,edges_recovered):

    for i in range(0,len(path)-1,1):
        id_source=path[i]
        id_target=path[i+1]

        if H.has_edge(id_source,id_target):

            if H.node[id_source]['status']=='destroyed':
                H.node[id_source]['status']='repaired'
                H.node[id_source]['color']='blue'
                if id_source not in nodes_recovered:
                    nodes_recovered.append(id_source)
                print 'nodo ripristinato %d : '%(id_source)

            if H.node[id_target]['status']=='destroyed':
                H.node[id_target]['status']='repaired'
                H.node[id_target]['color']='blue'
                if id_target not in nodes_recovered:
                    nodes_recovered.append(id_target)
                print 'nodo ripristinato %d : '%(id_target)

            keydict =H[id_source][id_target]
            for k in keydict:
                if H.edge[id_source][id_target][k]['type']=='normal' and H.edge[id_source][id_target][k]['type']!='green':
                    if H.edge[id_source][id_target][k]['status']=='destroyed':
                        H.add_edge(id_source,id_target,key=k, status='repaired',labelfont='blue',color='blue',style='solid')
                        edge=(id_source,id_target)
                        edge_reverse=(id_target,id_source)
                        if edge not in edges_recovered and edge_reverse not in edges_recovered:
                            edges_recovered.append(edge)
                        #else:
                        #    sys.exit('Errore in recover entire path: arco gia ripristinato in precedenza')

                        print 'arco ripristinato %d-%d: '%(id_source,id_target)

        else:
            sys.exit('Errore in recover entire path: non esiste l arco del cammino da ripristinare')


def simulate_pruning(graph_temp,path_to_prune,demand,distance_metric,number_of_iteration):

        id_source=path_to_prune[0]
        id_target=path_to_prune[len(path_to_prune)-1]
        cap_of_path=get_capacity_of_path(graph_temp,path_to_prune)
        demand_to_assign=min(cap_of_path,demand)
        demand_assigned=reduce_capacity_path(graph_temp,path_to_prune,demand_to_assign)

        keydict=graph_temp[id_source][id_target]
        for k in keydict:
            if graph_temp.edge[id_source][id_target][k]['type']=='green':
                key_to_remove=k

        if demand_assigned==demand:
            graph_temp.remove_edge(id_source,id_target,key=key_to_remove)
            #add two new green edge source,bc and bc,target
        else:
            graph_temp.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=(demand-demand_assigned), color='green',style='bold')


        new_green_edges=get_green_edges(graph_temp)
        """
        new_bet_dict=compute_my_betweeness_3(graph_temp,new_green_edges,distance_metric)
        set_betwenness_from_dict(graph_temp,new_bet_dict)
        my_draw(graph_temp,'13-recovered_shortest_iteration_%d_pruning_simulation'%(number_of_iteration))
        """

        #sys.exit(0)

        return graph_temp,new_green_edges

def sort_array_demand(green_edges,policy_sorting):

    for i in range(0,len(green_edges),1):
        for j in range(0,len(green_edges),1):
            couple_i=green_edges[i]
            couple_j=green_edges[j]
            temp_elem=None

            if policy_sorting=='reverse': #ordine decrescente delle domande
                #print 'confronto %s con %s'%(str(couple_i),str(couple_j))
                if couple_i[2] >= couple_j[2]:
                    temp_elem=couple_i
                    green_edges[i]=couple_j
                    green_edges[j]=temp_elem
                    #print green_edges
            elif policy_sorting=='order': #ordine crescente delle domande
                if couple_i[2] <= couple_j[2]:
                    temp_elem=couple_i
                    green_edges[i]=couple_j
                    green_edges[j]=temp_elem
            else:
                sys.exit('Errore in sort array demand: politica non riconosciuta')

    #print 'fine ordinamento'
    #print green_edges


    return green_edges



def recovery_algorithm_ranking_path(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]

    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)


    #print 'ranked path sorted'
    #print paths_ranked


    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')

    path_used=[]

    iteration=0
    print 'Inizio algoritmo di riparazione'
    while check_routability(only_graph_destroyed,green_edges)==False:

        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked
        #assegna un punteggio ad ogni path.
        print 'Compute Ranking of paths iteration %d: '%(iteration)
        paths_ranked=compute_ranking_of_paths(H,all_graph_paths,distance_metric,path_used)


        print 'Sorting ranked paths'
        #ordina i path in ordine decresente di ranking
        sort_ranked_path(paths_ranked,policy_sort)

        if len(paths_ranked)==0:
            sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        print 'shortest preso'
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
        else:
            print 'Arco verde non trovato %d-%d: '%(id_source,id_target)
            sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')

        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        print 'pre bet'
        new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
        set_betwenness_from_dict(H,new_bet_dict)
        print 'fine bet'
        my_draw(H,'14-ranking_%d'%iteration)
        iteration+=1
        only_graph_destroyed=get_graph_from_destroyed_graph(H)

        """
        max_flow_on_destroyed=compute_max_flow(only_graph_destroyed,id_source,id_target)
        if max_flow_on_destroyed>=demand:
            remove_all_path_source_target(paths_ranked,id_source,id_target)
        """

    #sys.exit('stop')

    return nodes_recovered,edges_recovered


def compute_number_of_total_path():

    global all_graph_paths

    counter=0
    path_visited=[]
    for couple in all_graph_paths:
        paths_of_couple=all_graph_paths[couple]
        for path in paths_of_couple:
            if path not in path_visited:
                path_visited.append(path)
                counter+=1

    return counter


#nuovo ranking che assegna ad ogni path il valore costo_riparazione/capacita del path. Inoltre fa il pruning del path ripristinato
def recovery_algorithm_ranking_path_commitment(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]

    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)

    number_of_total_path=compute_number_of_total_path()
    print number_of_total_path

    #print 'ranked path sorted'
    #print paths_ranked


    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')

    path_used=[]

    iteration=0

    print 'Inizio algoritmo di riparazione'
    #while check_routability(only_graph_destroyed,green_edges)==False:
    while check_if_are_green(H):
        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked
        #assegna un punteggio ad ogni path.
        print 'Compute Ranking of paths iteration %d: '%(iteration)
        #paths_ranked=compute_ranking_of_paths(H,all_graph_paths,distance_metric,path_used)
        update_all_graph_path(H)
        paths_ranked=compute_ranking_of_paths_cost_and_capacity(H,all_graph_paths,path_used)

        print 'Sorting ranked paths'
        #ordina i path in ordine decresente di ranking
        sort_ranked_path(paths_ranked,policy_sort)
        print 'Sorted path '
        #print paths_ranked

        if len(paths_ranked)==0:
            #sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')
            print 'Non ci sono piu path disponibili'
            break


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        #shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        shortest_path=select_random_path_from_set(paths_same_value)
        print 'shortest preso'

        if shortest_path in path_used:
            sys.exit('Errore in ranking commitment: stesso path gia preso')
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        key_to_remove=-1
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
                    key_to_remove=k
        else:
            #print 'Arco non trovato %d-%d: '%(id_source,id_target)
            #sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')
            key_to_remove=-1


        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        #se e' uguale a -1 vuol dire che l'arco verde delle coppia associata al path e' stata gia soddisfatta in precedenza
        if key_to_remove!=-1:

            my_draw(H,'14-ranking_comm_%d_repaired'%iteration)
            cap_of_path=get_capacity_of_path(H,shortest_path)
            demand_to_assign=min(cap_of_path,demand)
            demand_assigned=reduce_capacity_path(H,shortest_path,demand_to_assign)
            demand=demand-demand_assigned


            if demand==0:
                H.remove_edge(id_source,id_target,key=key_to_remove)
                #add two new green edge source,bc and bc,target
            elif demand > 0:
                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
            else:
                sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

            my_draw(H,'14-ranking_comm_%d_residual'%iteration)

        iteration+=1
        #only_graph_destroyed=get_graph_from_destroyed_graph(H)
        check_if_are_green(H)

    #sys.exit('stop')
    green_residual=get_green_edges(H)

    demand_residual=0.0
    for edge in green_residual:
        elem=edge[2]
        demand_residual+=elem

    return nodes_recovered,edges_recovered,demand_residual


#nuovo ranking che assegna ad ogni path il valore costo_riparazione/capacita del path. Inoltre fa il pruning del path ripristinato
#VARIANTE: QUANDO UNA DOMANDA VIENE SODDISFATTA: VENGONO RIMOSSI TUTTI I PATH RELATIVI ALLA DOMANDA, CHE NON FANNO PIU PARTE DEL RANK
def recovery_algorithm_ranking_path_commitment_2(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]


    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)

    number_of_total_path=compute_number_of_total_path()
    print number_of_total_path

    #print 'ranked path sorted'
    #print paths_ranked


    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')

    path_used=[]

    iteration=0

    print 'Inizio algoritmo di riparazione'
    #while check_routability(only_graph_destroyed,green_edges)==False:
    while check_if_are_green(H):
        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked
        #assegna un punteggio ad ogni path.
        print 'Compute Ranking of paths iteration %d: '%(iteration)
        #paths_ranked=compute_ranking_of_paths(H,all_graph_paths,distance_metric,path_used)
        update_all_graph_path(H)
        #print 'Path da classificare:'
        #print all_graph_paths
        paths_ranked=compute_ranking_of_paths_cost_and_capacity(H,all_graph_paths,path_used)

        print 'Sorting ranked paths'
        #ordina i path in ordine decresente di ranking
        sort_ranked_path(paths_ranked,policy_sort)
        print 'Sorted path '
        #print paths_ranked

        if len(paths_ranked)==0:
            #sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')
            print 'Non ci sono piu path disponibili'
            break


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        #shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        shortest_path=select_random_path_from_set(paths_same_value)
        print 'shortest preso'

        if shortest_path in path_used:
            sys.exit('Errore in ranking commitment: stesso path gia preso')
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        key_to_remove=-1
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
                    key_to_remove=k
        else:
            #print 'Arco non trovato %d-%d: '%(id_source,id_target)
            #sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')
            key_to_remove=-1


        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        #se e' uguale a -1 vuol dire che l'arco verde delle coppia associata al path e' stata gia soddisfatta in precedenza
        if key_to_remove!=-1:

            my_draw(H,'14-ranking_comm_%d_repaired'%iteration)
            cap_of_path=get_capacity_of_path(H,shortest_path)
            demand_to_assign=min(cap_of_path,demand)
            demand_assigned=reduce_capacity_path(H,shortest_path,demand_to_assign)
            demand=demand-demand_assigned


            if demand==0:
                H.remove_edge(id_source,id_target,key=key_to_remove)
                #add two new green edge source,bc and bc,target

                #----------VARIANTE: RIMUOVO I PATH DELLA COPPIA---------#
                arc=(id_source,id_target)
                arc_reverse=(id_target,id_source)

                if all_graph_paths.has_key(arc):
                    del all_graph_paths[arc]

                elif all_graph_paths.has_key(arc_reverse):
                    del all_graph_paths[arc_reverse]

                else:
                    sys.exit('Errore in ranking path commitment 2: edge da rimuovere non presente in all_graph_paths')


            elif demand > 0:
                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
            else:
                sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

            my_draw(H,'14-ranking_comm_%d_residual'%iteration)

        iteration+=1
        #only_graph_destroyed=get_graph_from_destroyed_graph(H)
        check_if_are_green(H)

    #sys.exit('stop')
    green_residual=get_green_edges(H)

    demand_residual=0.0
    for edge in green_residual:
        elem=edge[2]
        demand_residual+=elem

    return nodes_recovered,edges_recovered,demand_residual



#nuovo ranking che assegna ad ogni path il valore costo_riparazione/capacita del path. Inoltre fa il pruning del path ripristinato
#VARIANTE: Dopo aver usato il path per soddisfare la domanda (se non gia soddisfatta) si controlla se altre domande possono usare questi path
def recovery_algorithm_ranking_path_commitment_3(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]


    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)

    number_of_total_path=compute_number_of_total_path()
    print number_of_total_path

    #print 'ranked path sorted'
    #print paths_ranked


    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')

    path_used=[]

    iteration=0

    print 'Inizio algoritmo di riparazione'
    #while check_routability(only_graph_destroyed,green_edges)==False:
    while check_if_are_green(H):
        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked
        #assegna un punteggio ad ogni path.
        print 'Compute Ranking of paths iteration %d: '%(iteration)
        #paths_ranked=compute_ranking_of_paths(H,all_graph_paths,distance_metric,path_used)
        update_all_graph_path(H)
        #print 'Path da classificare:'
        #print all_graph_paths

        #remove_path_works(H)

        paths_ranked=compute_ranking_of_paths_cost_and_capacity(H,all_graph_paths,path_used)

        print 'Sorting ranked paths'
        #ordina i path in ordine decresente di ranking
        sort_ranked_path(paths_ranked,policy_sort)
        print 'Sorted path '
        #print paths_ranked

        if len(paths_ranked)==0:
            #sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')
            print 'Non ci sono piu path disponibili'
            break


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        #shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        shortest_path=select_random_path_from_set(paths_same_value)
        print 'shortest preso'

        if shortest_path in path_used:
            sys.exit('Errore in ranking commitment: stesso path gia preso')
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        key_to_remove=-1
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
                    key_to_remove=k
        else:
            #print 'Arco non trovato %d-%d: '%(id_source,id_target)
            #sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')
            key_to_remove=-1


        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        #se e' uguale a -1 vuol dire che l'arco verde delle coppia associata al path e' stata gia soddisfatta in precedenza
        if key_to_remove!=-1:

            my_draw(H,'14-ranking_comm_%d_repaired'%iteration)
            cap_of_path=get_capacity_of_path(H,shortest_path)
            demand_to_assign=min(cap_of_path,demand)
            demand_assigned=reduce_capacity_path(H,shortest_path,demand_to_assign)
            demand=demand-demand_assigned


            if demand==0:
                H.remove_edge(id_source,id_target,key=key_to_remove)
                #add two new green edge source,bc and bc,target

            elif demand > 0:
                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
            else:
                sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

            my_draw(H,'14-ranking_comm_%d_residual'%iteration)

        #ORA CONTROLLO SE SI PUO SODDISFARE QUALCHE ALTRA DOMANDA
        #non esiste piu l'arco associato a quel path. Controllo se posso usare il grafo attuale per soddisfare qualche altra
        #domanda.
        flag_satisfy_demands=True

        while(flag_satisfy_demands):
            graph_repaired=get_graph_from_destroyed_graph(H)
            couples_to_satisfy=get_couples_to_satisfy(graph_repaired)
            if len(couples_to_satisfy)>0:
                #esiste almeno un arco verde che puo essere soddisfatta.
                #seleziona una casualmente.
                #ogni elemento e' (source,target,paths)
                couple_selected=couples_to_satisfy[random.randint(0,len(couples_to_satisfy)-1)]
                source=couple_selected[0]
                target=couple_selected[1]
                paths_of_couple=couple_selected[2]
                shortest_path_of_couple=select_random_path_from_set(paths_of_couple)
                if check_if_path_exist(graph_repaired,shortest_path_of_couple):
                    if H.has_edge(source,target):
                        key_to_remove=-1
                        keydict=H[source][target]
                        for k in keydict:
                            if H[source][target][k]['type']=='green':
                                demand=H[source][target][k]['demand']
                                key_to_remove=k

                        if key_to_remove==-1:
                            sys.exit('Errore in ranking committment 3: domanda non trovare')

                        cap_of_path=get_capacity_of_path(H,shortest_path_of_couple)
                        demand_to_assign=min(cap_of_path,demand)
                        demand_assigned=reduce_capacity_path(H,shortest_path_of_couple,demand_to_assign)
                        demand=demand-demand_assigned

                        if demand==0:
                            H.remove_edge(source,target,key=key_to_remove)
                            #add two new green edge source,bc and bc,target

                        elif demand > 0:
                            H.add_edge(source, target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
                        else:
                            sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

                        iteration+=1
                        my_draw(H,'14-ranking_comm_%d_residual'%iteration)

                    else:
                        sys.exit('Errore in rank commitment 3: coppia da soddisfare non esiste')
                else:
                    sys.exit('Errore in ranking commitment 3: path da utilizzare non presente nel grafo riparato')
            else:
                #non ci sono piu domande smetto di controllare
                flag_satisfy_demands=False

        iteration+=1
        #only_graph_destroyed=get_graph_from_destroyed_graph(H)
        check_if_are_green(H)

    #sys.exit('stop')
    green_residual=get_green_edges(H)

    demand_residual=0.0
    for edge in green_residual:
        elem=edge[2]
        demand_residual+=elem

    return nodes_recovered,edges_recovered,demand_residual


#IMPLEMENTAZIONE DEL KNAPSACK CON COMMITMENT:
#AD OGNI ITERAZIONE CAMBIANO LE CAPACITA' DEI LINK, MA NON CAMBIANO IL COSTO DEL PATH, CHE QUINDI SI BASA SUL GRAFO DISTRUTTO INIZIALE
def knapsack_commitment(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]


    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)

    number_of_total_path=compute_number_of_total_path()
    print number_of_total_path

    #print 'ranked path sorted'
    #print paths_ranked

    original_graph_destroyed=nx.MultiGraph(H)

    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')
    path_used=[]

    iteration=0

    print 'Inizio algoritmo di riparazione'
    #while check_routability(only_graph_destroyed,green_edges)==False:
    while check_if_are_green(H):
        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked
        #assegna un punteggio ad ogni path.
        print 'Compute Ranking of paths iteration %d: '%(iteration)
        #paths_ranked=compute_ranking_of_paths(H,all_graph_paths,distance_metric,path_used)
        update_all_graph_path(H)
        #print 'Path da classificare:'
        #print all_graph_paths

        remove_path_works(H)

        paths_ranked=compute_ranking_of_paths_cost_and_capacity_on_original_destroyed(H,original_graph_destroyed,all_graph_paths,path_used)

        print 'Sorting ranked paths'
        #ordina i path in ordine decresente di ranking
        sort_ranked_path(paths_ranked,policy_sort)
        print 'Sorted path '
        #print paths_ranked
        #sys.exit(0)
        if len(paths_ranked)==0:
            #sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')
            print 'Non ci sono piu path disponibili'
            break


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        #shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        shortest_path=select_random_path_from_set(paths_same_value)
        print 'shortest preso'

        if shortest_path in path_used:
            sys.exit('Errore in ranking commitment: stesso path gia preso')
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        key_to_remove=-1
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
                    key_to_remove=k
        else:
            #print 'Arco non trovato %d-%d: '%(id_source,id_target)
            #sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')
            key_to_remove=-1


        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        #se e' uguale a -1 vuol dire che l'arco verde delle coppia associata al path e' stata gia soddisfatta in precedenza
        if key_to_remove!=-1:

            my_draw(H,'14-ranking_comm_%d_repaired'%iteration)
            cap_of_path=get_capacity_of_path(H,shortest_path)
            demand_to_assign=min(cap_of_path,demand)
            demand_assigned=reduce_capacity_path(H,shortest_path,demand_to_assign)
            demand=demand-demand_assigned


            if demand==0:
                H.remove_edge(id_source,id_target,key=key_to_remove)
                #add two new green edge source,bc and bc,target

            elif demand > 0:
                H.add_edge(id_source, id_target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
            else:
                sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

            my_draw(H,'14-ranking_comm_%d_residual'%iteration)

        #ORA CONTROLLO SE SI PUO SODDISFARE QUALCHE ALTRA DOMANDA
        #non esiste piu l'arco associato a quel path. Controllo se posso usare il grafo attuale per soddisfare qualche altra
        #domanda.

        else:
            #disegna l'iterazione in cui ce solo la riparazione
            my_draw(H,'14-ranking_comm_%d_repaired'%iteration)
        flag_satisfy_demands=True

        while(flag_satisfy_demands):
            graph_repaired=get_graph_from_destroyed_graph(H)
            couples_to_satisfy=get_couples_to_satisfy(graph_repaired)
            if len(couples_to_satisfy)>0:
                #esiste almeno un arco verde che puo essere soddisfatta.
                #seleziona una casualmente.
                #ogni elemento e' (source,target,paths)
                couple_selected=couples_to_satisfy[random.randint(0,len(couples_to_satisfy)-1)]
                source=couple_selected[0]
                target=couple_selected[1]
                paths_of_couple=couple_selected[2]
                shortest_path_of_couple=select_random_path_from_set(paths_of_couple)
                if check_if_path_exist(graph_repaired,shortest_path_of_couple):
                    if H.has_edge(source,target):
                        key_to_remove=-1
                        keydict=H[source][target]
                        for k in keydict:
                            if H[source][target][k]['type']=='green':
                                demand=H[source][target][k]['demand']
                                key_to_remove=k

                        if key_to_remove==-1:
                            sys.exit('Errore in knapsack: domanda non trovare')

                        cap_of_path=get_capacity_of_path(H,shortest_path_of_couple)
                        demand_to_assign=min(cap_of_path,demand)
                        demand_assigned=reduce_capacity_path(H,shortest_path_of_couple,demand_to_assign)
                        demand=demand-demand_assigned

                        if demand==0:
                            H.remove_edge(source,target,key=key_to_remove)
                            #add two new green edge source,bc and bc,target

                        elif demand > 0:
                            H.add_edge(source, target, key=key_to_remove, type='green', demand=demand, color='green',style='bold')
                        else:
                            sys.exit('Errore in recovery_algorithm_based_on_shortest: demand negativa!!!')

                        iteration+=1
                        my_draw(H,'14-ranking_comm_%d_residual'%iteration)

                    else:
                        sys.exit('Errore in rank commitment 3: coppia da soddisfare non esiste')
                else:
                    sys.exit('Errore in ranking commitment 3: path da utilizzare non presente nel grafo riparato')
            else:
                #non ci sono piu domande smetto di controllare
                flag_satisfy_demands=False


        iteration+=1
        #only_graph_destroyed=get_graph_from_destroyed_graph(H)
        check_if_are_green(H)

    #sys.exit('stop')
    green_residual=get_green_edges(H)

    demand_residual=0.0
    for edge in green_residual:
        elem=edge[2]
        demand_residual+=elem

    return nodes_recovered,edges_recovered,demand_residual


def get_couples_to_satisfy(H):

    green_edges_remaining=get_green_edges(H)

    couples_selected=[]
    if len(green_edges_remaining)==0:
        return []
    else:
        graph_dict=convert_graph_to_dict(H)
        #esiste almeno una coppia verde nel grafo
        for couple in green_edges_remaining:
            #vedi se ha path nel grafo riparato
            source=couple[0]
            target=couple[1]
            paths=find_all_paths(graph_dict,source,target)
            if len(paths)>0:
                #esiste almeno un path
                tupla=(source,target,paths)
                couples_selected.append(tupla)

    return couples_selected




def select_random_path_from_set(paths_same_value):

    if len(paths_same_value)<=0:
        sys.exit('Errore select_random_path_from_set: non ci sono path da scegliere')

    if len(paths_same_value)==1:
        return paths_same_value[0]
    else:
        random_index=random.randint(0,len(paths_same_value)-1)
        return paths_same_value[random_index]



#nuovo ranking che non fa il commitment ma assegna ad ogni path il valore costo_riparazioni/capacita
def recovery_algorithm_ranking_path_no_commitment(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]

    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)


    #print 'ranked path sorted'
    #print paths_ranked


    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')

    path_used=[]

    iteration=0
    print 'Inizio algoritmo di riparazione'
    while check_routability(only_graph_destroyed,green_edges)==False:

        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked
        #assegna un punteggio ad ogni path.
        print 'Compute Ranking of paths iteration %d: '%(iteration)
        #rimuovi i path gia sani tra quelli da computare
        remove_path_works(H)
        paths_ranked=compute_ranking_of_paths_cost_and_capacity(H,all_graph_paths,path_used)


        print 'Sorting ranked paths'
        #ordina i path in ordine decresente di ranking
        sort_ranked_path(paths_ranked,policy_sort)
        print paths_ranked

        if len(paths_ranked)==0:
            sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        #shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        shortest_path=select_random_path_from_set(paths_same_value)
        print 'shortest preso'
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
        else:
            print 'Arco verde non trovato %d-%d: '%(id_source,id_target)
            sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')

        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        """
        print 'pre bet'
        new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
        set_betwenness_from_dict(H,new_bet_dict)
        print 'fine bet'
        """
        my_draw(H,'15-ranking_recover_path_%d'%iteration)
        iteration+=1
        only_graph_destroyed=get_graph_from_destroyed_graph(H)

        """
        max_flow_on_destroyed=compute_max_flow(only_graph_destroyed,id_source,id_target)
        if max_flow_on_destroyed>=demand:
            remove_all_path_source_target(paths_ranked,id_source,id_target)
        """

    #sys.exit('stop')

    return nodes_recovered,edges_recovered

#recovery basato su knapsack SENZA MAI Aggiornare i costi e neanche le capacita. costo_path/cap_path.
#Si usa il grafo iniziale della distruzione per calcolare il costo dei path
def knapsack_no_commitment(H,distance_metric,policy_sort):

    global all_graph_paths
    nodes_recovered=[]
    edges_recovered=[]

    green_edges=get_green_edges(H)
    #print 'green'
    #print green_edges
    #compute all path between couple green. Usare la variabile globale all_paths
    compute_paths(H,green_edges)


    #print 'ranked path sorted'
    #print paths_ranked

    original_graph_destroyed=nx.MultiGraph(H)

    #prendi in considerazione il grafo distrutto
    only_graph_destroyed=get_graph_from_destroyed_graph(H)

    #my_draw(only_graph_destroyed,'14-only_destroyed')

    path_used=[]

    #non bisogna aggiornare i path, ne i costi, ne le capacita' quindi il rank e' uguale per tutti.
    iteration=0
    print 'Compute Ranking of paths iteration %d: '%(iteration)
    paths_ranked=compute_ranking_of_paths_cost_and_capacity_on_original_destroyed(H,original_graph_destroyed,all_graph_paths,path_used)


    print 'Sorting ranked paths'
    #ordina i path in ordine decresente di ranking
    sort_ranked_path(paths_ranked,policy_sort)
    #print paths_ranked
    #sys.exit(0)
    print 'Inizio algoritmo di riparazione'
    while check_routability(only_graph_destroyed,green_edges)==False:

        #print 'devo ripristinare un path'

        #print 'ranked path sorted'
        #print paths_ranked

        #rimuovi i path gia sani tra quelli da computare
        remove_path_works(H)



        if len(paths_ranked)==0:
            sys.exit('Errore in recovery ranking based: non ci sono piu path da utilizzare')


        best_value=paths_ranked[0][0]
        paths_same_value=[]
        #print 'best value'
        #print best_value
        for i in range(0,len(paths_ranked),1):
            curr_value=paths_ranked[i][0]
            #print 'confronto con'
            #print paths_ranked[i][1]
            #print curr_value
            if curr_value== best_value:
                paths_same_value.append(paths_ranked[i][1])

        print 'paths stessa lunghezza'
        #print paths_same_value

        #shortest_path=compute_shortest_from_set(H,paths_same_value,distance_metric)
        shortest_path=select_random_path_from_set(paths_same_value)
        print 'shortest preso'
        id_source=shortest_path[0]
        id_target=shortest_path[len(shortest_path)-1]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='green':
                    demand=H[id_source][id_target][k]['demand']
        else:
            print 'Arco verde non trovato %d-%d: '%(id_source,id_target)
            sys.exit('Errore in algorithm ranking based: arco di domanda non trovato')

        #print 'shortest selezionato'
        #print shortest_path
        best_tuple=(best_value,shortest_path)
        paths_ranked.remove(best_tuple)
        #print 'dopo rimozione'
        #print paths_ranked
        recover_entire_path(H,shortest_path,nodes_recovered,edges_recovered)

        path_used.append(shortest_path)

        """
        print 'pre bet'
        new_bet_dict=compute_my_betweeness_1(H, green_edges,distance_metric)
        set_betwenness_from_dict(H,new_bet_dict)
        print 'fine bet'
        """
        my_draw(H,'15-ranking_recover_path_%d'%iteration)
        iteration+=1
        only_graph_destroyed=get_graph_from_destroyed_graph(H)

        """
        max_flow_on_destroyed=compute_max_flow(only_graph_destroyed,id_source,id_target)
        if max_flow_on_destroyed>=demand:
            remove_all_path_source_target(paths_ranked,id_source,id_target)
        """

    #sys.exit('stop')

    return nodes_recovered,edges_recovered




def remove_path_works(H):

    global all_graph_paths

    for key in all_graph_paths:
        path_to_remove=[]
        paths=all_graph_paths[key]

        for path in paths:

            if check_if_destroyed(H,path)==False:
                #e' un path gia sano o riparato, lo levo dalle computazioni
                path_to_remove.append(path)

        for elem in path_to_remove:
            if elem in all_graph_paths[key]:
                all_graph_paths[key].remove(elem)
            else:
                sys.exit('Errore in remove_path_works: path da rimuovere non presente')

def check_if_destroyed(H,path):

    element_destroyed=False

    for i in range(0,len(path)-1,1):
        source=path[i]
        target=path[i+1]

        if H.node[source]['status']=='destroyed':
            element_destroyed=True
            return element_destroyed
        if H.node[target]['status']=='destroyed':
            element_destroyed=True
            return element_destroyed

        if H.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type']=='normal':
                    if H[source][target][k]['status']=='destroyed':
                        element_destroyed=True
                        return element_destroyed
        else:
            sys.exit('Errore in check_if_destroyed: arco del path non trovato')


    return element_destroyed




def compute_ranking_of_paths_cost_and_capacity(H,all_paths,path_used):
    ranked_path=[]

    for key in all_paths:
        paths=all_paths[key]

        for path in paths:
            if path not in path_used:
                cap_path=get_capacity_of_path(H,path)
                total_cost=0.0
                total_cost = compute_cost_of_path(H,path)

                #compute rank of path rank=total_cost/cap_path
                rank=0.0
                rank=float('%.2f'%(total_cost/cap_path))
                #crea tupla=(rank,path)
                tupla=(rank,path)
                if tupla not in ranked_path:
                    ranked_path.append(tupla)


    return ranked_path



def compute_ranking_of_paths_cost_and_capacity_on_original_destroyed(H,original_destroyed,all_paths,path_used):

    ranked_path=[]

    for key in all_paths:
        paths=all_paths[key]

        for path in paths:
            if path not in path_used:
                #la capacita si aggiorna e viene calcolata sul path che si sta ricostruendo (quindi sul commitment vengono aggiornata)
                cap_path=get_capacity_of_path(H,path)
                total_cost=0.0
                #il costo dei path non cambia quindi gli viene passato il grafo con la distruzione inizale, indipendemente dalle riparazioni gia fatte
                total_cost = compute_cost_of_path(original_destroyed,path)

                #compute rank of path rank=total_cost/cap_path
                rank=0.0
                rank=float('%.2f'%(total_cost/cap_path))
                #crea tupla=(rank,path)
                tupla=(rank,path)
                if tupla not in ranked_path:
                    ranked_path.append(tupla)


    return ranked_path




def compute_cost_of_path(H,path):
    costo_arco=1
    costo_vertice=0.50
    total_cost=0.0

    for node in path:
        if H.node[node]['status']=='destroyed':
            total_cost+=costo_vertice


    for i in range(0,len(path)-1,1):
        source=path[i]
        target=path[i+1]
        if H.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type']=='normal':
                    if H[source][target][k]['status']=='destroyed':
                        total_cost+=costo_arco
        else:
            sys.exit('Errore compute_cost_of_path: arco del path inesistente')

    if total_cost==0.0:
        total_cost=0.1

    return total_cost



def remove_all_path_source_target(paths_ranked,id_source,id_target):

    path_to_remove=[]
    for tuple in paths_ranked:
        value=tuple[0]
        path=tuple[1]
        if path[0]==id_source and path[len(path)-1]==id_target:
            if path not in path_to_remove:
                path_to_remove.append(tuple)
            else:
                sys.exit('Remove all path_source_target: rimosso due volte stesso path')
        elif path[len(path)-1]==id_source and path[0]==id_target:
            if path not in path_to_remove:
                path_to_remove.append(tuple)
            else:
                sys.exit('Remove all path_source_target: rimosso due volte stesso path')
        else:
            continue

    for tuple in path_to_remove:
        if tuple in paths_ranked:
            paths_ranked.remove(tuple)
        else:
            sys.exit('Remove all path_source_target: tupla da rimuovere inesistente')



def compute_ranking_of_paths(H,all_paths,distance_metric,path_used):

    #lista dei path con ranking. Saranno nella forma ( rank, path )
    ranked_path=[]

    for key in all_paths:
        paths=all_paths[key]

        for path in paths:
            if path not in path_used:
                total_bet=0.0
                total_bet= compute_sum_bet_path(H,path)
                #print 'lenght interm'
                lenght_path_inter=len(path)-2
                #print lenght_path_inter
                ratio=0.0
                if lenght_path_inter==0:
                    lenght_path_inter=0.01

                ratio=total_bet/lenght_path_inter
                #print 'ratio'
                #print ratio
                #sys.exit(0)
                tuple=None
                #tupla= rank/lenght_path, path
                tuple=(ratio,path)
                if tuple not in ranked_path:
                    ranked_path.append(tuple)

    return ranked_path

def compute_sum_bet_path(H,path):

    #MODIFICA FATTA: CONTIAMO ANCHEGLI ESTREMI (NODI VERDI) PER INCLUDERE UN PESO NON NULLO AI PATH ONE HOP
    #print path
    id_source=path[0]
    id_target=path[len(path)-1]
    #print 'sorgente e destinazione'
    #print id_source
    #print id_target
    sum_bet=0.0

    #print 'nodi del path esaminati'
    for i in range(0,len(path),1):
        curr_node=path[i]
        #print curr_node
        node_bet=H.node[curr_node]['betweeness']
        sum_bet+=node_bet

    #print sum_bet
    return sum_bet

def sort_ranked_path(paths_ranked,policy_sort):

    if policy_sort=='reverse':
        reverse=True
    else:
        reverse=False

    temp_tuple=None

    paths_ranked.sort(key=lambda tupla: tupla[0],reverse=reverse)

    #print 'Path ordinati per punteggio'
    #print paths_ranked





def recovery_all_graph_algorithm(H):

    nodes_recovered=[]
    edges_recovered=[]

    for node in H.nodes():
        if H.node[node]['status']=='destroyed':
            nodes_recovered.append(node)

    for edge in H.edges():
        id_source=edge[0]
        id_target=edge[1]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':
                    if H[id_source][id_target][k]['status']=='destroyed':
                        if edge not in edges_recovered:
                            edges_recovered.append(edge)

    return nodes_recovered,edges_recovered

def update_all_graph_path(H):

    global all_graph_paths
    #new_all_graph_paths={}

    for couple in all_graph_paths:
        #print 'esamino couple %d-%d'%(couple[0],couple[1])
        path_to_remove=[]
        paths_of_couple=all_graph_paths[couple]
        #print 'path attuali per la coppia'
        #print paths_of_couple
        for path in paths_of_couple:
            if check_if_path_exist(H,path)==False:
                if path not in path_to_remove:
                    #print 'non esiste piu'
                    #print path
                    path_to_remove.append(path)

        for elem in path_to_remove:
            if elem in all_graph_paths[couple]:
                all_graph_paths[couple].remove(elem)
            else:
                sys.exit('Errore update all graph path: path da rimuovere non presente')

def compute_lenght_of_path(H,path):

    edge=(id_source,id_target)
    edge_reverse=(id_target,id_source)

    weight_of_path=0
    #print 'path prelevato'
    #print path
    for i in range(0,(len(path)-1),1):
        id_source=path[i]
        id_target=path[(i+1)]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal':
                dist = distance_node(H,id_source,id_target,distance_metric)
                weight_of_path+=dist

    return weight_of_path

def assign_random_capacity_to_edges(H,filename):

    for edge in H.edges():
        random_cap=random.randint(20,50)
        #random_cap=1000
        H[edge[0]][edge[1]][0]['capacity']=random_cap

    path_to_file='network topologies/'+filename+'_Random_Capacity.gml'
    #print 'da creare: '+path_to_file
    nx.write_gml(H,path_to_file)

def destroy_all_graph(H):

    nodes=[]
    edges=[]
    for node in H.nodes():
        H.node[node]['status']='destroyed'
        H.node[node]['color']='red'
        id_nodo = H.node[node]['id']
        nodes.append(id_nodo)

    for edge in H.edges():
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal':
                H.add_edge(id_source,id_target,key=k, status='destroyed',labelfont='red',color='red',style='dashed')
                arc=(id_source,id_target)
                edges.append(arc)
    return nodes,edges

#Destroyes random nodes and edges
def destroy_graph_random(H, node_chance, edge_chance):
    nodes=[]
    edges=[]
    for node in H.nodes():
        if (random.randint(1,100) <= node_chance):
            H.node[node]['status']='destroyed'
            H.node[node]['color']='red'
            id_nodo = H.node[node]['id']
            nodes.append(id_nodo)

    for edge in H.edges():
        if (random.randint(1,100) <= edge_chance):
            id_source=edge[0]
            id_target=edge[1]
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']=='normal':
                    H.add_edge(id_source,id_target,key=k, status='destroyed',labelfont='red',color='red',style='dashed')
                    arc=(id_source,id_target)
                    edges.append(arc)
    return nodes,edges
    

def check_if_have_multiple_edges(H):

    edges_to_remove=[]

    for edge in H.edges():
        count_edge=0
        keydict=H[edge[0]][edge[1]]
        for k in keydict:
            count_edge+=1

        if count_edge>1:
            edge_reverse=(edge[1],edge[0])
            if edge not in edges_to_remove and edge_reverse not in edges_to_remove:
                edges_to_remove.append(edge)
        elif count_edge<=0:
            sys.exit('Errore check if have multiple edges: numero di archi <=0')

    print 'Archi che hanno piu di un arco '
    print edges_to_remove

    if len(edges_to_remove)>0:
        sys.exit('Graph with multiple edges')

def build_graph_repaired(H,list_nodes,list_edges):

    graph_repaired=nx.MultiGraph()
    nodes_added=[]
    edges_added=[]
    for id_nodo in list_nodes:
            node=id_nodo

            if id_nodo not in nodes_added:
                long=H.node[node]['Longitude']
                lat=H.node[node]['Latitude']
                graph_repaired.add_node(H.node[node]['id'],id=id_nodo,Longitude=long,Latitude=lat)
                nodes_added.append(id_nodo)


    for edge in list_edges:
                keydict=H[edge[0]][edge[1]]
                for k in keydict:
                    if H[edge[0]][edge[1]][k]['type']=='normal':
                        if not graph_repaired.has_edge(edge[0],edge[1]) or not graph_repaired.has_edge(edge[1],edge[0]):
                            arc=(edge[0],edge[1])
                            arc_reverse=(edge[1],edge[0])
                            if arc not in edges_added and arc_reverse not in edges_added:
                                edges_added.append(arc)
                                cap=H[edge[0]][edge[1]][k]['capacity']
                                status='repaired'
                                color='blue'
                                graph_repaired.add_edge(edge[0],edge[1],capacity=cap,status=status,color=color)

    #aggiungi anche gli archi e i nodi mai rotti
    for node in H.nodes():
        if H.node[node]['id'] not in nodes_added:
            id_nodo=H.node[node]['id']
            long=H.node[node]['Longitude']
            lat=H.node[node]['Latitude']
            graph_repaired.add_node(H.node[node]['id'],id=id_nodo,Longitude=long,Latitude=lat)

    for edge in H.edges():
        keydict=H[edge[0]][edge[1]]
        for k in keydict:
            if H[edge[0]][edge[1]][k]['type']=='normal':
                if H[edge[0]][edge[1]][k]['status']=='on':
                    if not graph_repaired.has_edge(edge[0],edge[1]) or not graph_repaired.has_edge(edge[1],edge[0]):
                        arc=(edge[0],edge[1])
                        arc_reverse=(edge[1],edge[0])
                        if arc not in edges_added and arc_reverse not in edges_added:
                            edges_added.append(arc)
                            cap=H[edge[0]][edge[1]][k]['capacity']
                            status='on'
                            color='black'
                            graph_repaired.add_edge(edge[0],edge[1],capacity=cap,status=status,color=color)

    return graph_repaired

def get_demand_of_couple(H,source,target):

    green_edges=get_green_edges(H)
    demand=-1
    #print green_edges
    #print 'Domanda da trovare %d-%d:'%(source,target)
    for edge in green_edges:
        id_source=edge[0]
        id_target=edge[1]
        if id_source==source and id_target==target:
            demand=edge[2]
        elif id_source==target and id_target==source:
            demand=edge[2]

    if demand==-1:
        sys.exit('Errore in get demand: domanda non trovata')
    else:
        return demand


def select_betweeness(H,green_edges,distance_metric,type_of_bet):
    #seamus add to information gain
    if type_of_bet=='classic':
        compute_my_betweeness_1(H,green_edges,distance_metric)

    elif type_of_bet=='aproximate':
        compute_my_betweeness_3(H,green_edges,distance_metric)
    elif type_of_bet=='exact':
        return compute_my_betweeness_4_opt(H,green_edges,distance_metric)
    else:
        sys.exit('Errore select betweeness: tipologia non riconosciuta')




def generate_graph_barabasi(number_of_nodes,m,seed):

    #number_of_nodes :numero di nodi del grafo
    #m : variabile del preferential attachment
    # seed : seed per generare stesso grafo o diversi
    graph= nx.MultiGraph ( nx.barabasi_albert_graph(number_of_nodes,m,seed) )

    #add node's attribute: latidute, longitude, type and id
    for node in graph.nodes():
        latitude=random.randint(0,300)
        longitude=random.randint(0,300)
        graph.add_node(node,id=node,label=node,type='normal',Latitude=latitude,Longitude=longitude)

    #for node in graph.nodes(data=True):
    #    print node

    for edge in graph.edges():
        id_source=edge[0]
        id_target=edge[1]
        #cap=random.randint(1,max_capacity)   #assign random capacity in range
        keydict=graph[id_source][id_target]
        for k in keydict:
            #cap = 1
            cap=random.randint(10,30)
            graph.add_edge(id_source,id_target,key=k,type='normal',capacity=cap)

    num_nodes=graph.number_of_nodes()
    num_edges=graph.number_of_edges()
    print 'Grafo Albert-Barabasi creato:'
    print 'Nodi: %d'%(num_nodes)
    print 'Edges: %d'%(num_edges)

    filename='Barabasi_graph_%d_nodes_%d_edges'%(num_nodes,num_edges)
    path_to_file='network topologies/random_graphs_generated/'+filename+'.gml'
    nx.write_gml(graph,path_to_file)

    return path_to_file

def compute_paths_from_split(id_source,id_target,id_bc):

    global all_graph_paths

    edge=(id_source,id_target)
    edge_reverse=(id_target,id_source)
    paths=[]
    if edge in all_graph_paths:
        paths=all_graph_paths[edge]
    elif edge_reverse in all_graph_paths:
        paths=all_graph_paths[edge_reverse]
    else:
        sys.exit('Errore in compute_paths_from_split: arco della coppia inesistente in all_graph_paths')

    couple_to_bc=(id_source,id_bc)
    couple_from_bc=(id_bc,id_target)

    """
    if couple_to_bc in all_graph_paths or couple_from_bc in all_graph_paths:
        print edge
        print couple_to_bc
        print couple_from_bc
        print all_graph_paths
        sys.exit('Coppia splitta gia presente in all_graph_path')
    """
    for path in paths:
        if id_bc in path:
            path_to_bc,path_from_bc=split_path_in_bc(id_source,id_target,path,id_bc)

            if couple_to_bc not in all_graph_paths:
                all_graph_paths.update({couple_to_bc:[]})
            if path_to_bc not in all_graph_paths[couple_to_bc]:
                all_graph_paths[couple_to_bc].append(path_to_bc)

            if couple_from_bc not in all_graph_paths:
                all_graph_paths.update({couple_from_bc:[]})
            if path_from_bc not in all_graph_paths[couple_from_bc]:
                all_graph_paths[couple_from_bc].append(path_from_bc)




def split_path_in_bc(id_source,id_target,path,id_bc):

    path_source_to_bc=[]
    path_target_to_bc=[]

    if id_bc not in path:
        sys.exit('Errore in split_path_in_bc: id_bc non presente nel path')

    #controllo come e orientato il path.
    if path[0]==id_source and path[len(path)-1]==id_target:
        path_source_to_bc = path[ : path.index(id_bc)+1]
        path_target_to_bc = path[path.index(id_bc) : ]
    elif path[0]==id_target and path[len(path)-1]==id_source:
        path_target_to_bc = path[ : path.index(id_bc)+1]
        path_source_to_bc = path[path.index(id_bc) : ]

    #print 'Best Candidate: %d'%(id_bc)
    #print 'Path da dividere:'
    #print path
    #print path_source_to_bc
    #print path_target_to_bc

    return path_source_to_bc,path_target_to_bc



def compute_diameter_of_graph(H):
    diameter=-1

    diameter=nx.diameter(H)


    return diameter

def compute_all_shortest_distance(H):

    dict_of_lenghts={}

    dict_of_lenghts=nx.shortest_path_length(H,source=None,target=None,weight=None)

    print 'Dictionary of lenghts: '
    print dict_of_lenghts

    list_of_couple=[]
    for node in dict_of_lenghts:

        dict_of_distance=dict_of_lenghts[node]
        furthest_node=get_furthest_node_from_list(dict_of_distance)
        new_couple=[]
        new_couple=(node,furthest_node[0],furthest_node[1])
        new_couple_reverse=(furthest_node[0],node,furthest_node[1])
        if new_couple not in list_of_couple and new_couple_reverse not in list_of_couple:
            list_of_couple.append(new_couple)

    print list_of_couple
    list_of_couple=sorted(list_of_couple,key=itemgetter(2),reverse=True)
    print list_of_couple
    return list_of_couple


def compute_all_shortest_distance_disjoint(H):

    dict_of_lenghts={}

    dict_of_lenghts=nx.shortest_path_length(H,source=None,target=None,weight=None)

    #print 'Dictionary of lenghts: '
    #print dict_of_lenghts

    nodes_used=[]
    list_of_couple=[]
    for node in dict_of_lenghts:

        if node not in nodes_used:
            dict_of_distance=dict_of_lenghts[node]
            target_found=False
            while(target_found==False):
                furthest_node=get_furthest_node_from_list(dict_of_distance)
                if furthest_node[0] not in nodes_used:
                    if furthest_node[0]!=node:
                        target_found=True
                        nodes_used.append(furthest_node[0])
                        nodes_used.append(node)
                    else:
                        target_found=True
                else:
                    target_found=False
                    del dict_of_distance[furthest_node[0]]

            if furthest_node[1]>0:
                #almeno a distanza 1
                new_couple=[]
                new_couple=(node,furthest_node[0],furthest_node[1])
                new_couple_reverse=(furthest_node[0],node,furthest_node[1])
                if new_couple not in list_of_couple and new_couple_reverse not in list_of_couple:
                    list_of_couple.append(new_couple)

    print list_of_couple
    list_of_couple=sorted(list_of_couple,key=itemgetter(2),reverse=True)
    print list_of_couple
    return list_of_couple


def check_if_are_disjoint(list_of_couples):

    all_nodes=[]
    for couple in list_of_couples:
        source=couple[0]
        target=couple[1]
        if source not in all_nodes:
            all_nodes.append(source)
        else:
            sys.exit('Errore check if are disjoint: stesso nodo piu volte')

        if target not in all_nodes:
            all_nodes.append(target)
        else:
            sys.exit('Errore check if are disjoint: stesso nodo piu volte')

    all_nodes=sorted(all_nodes,key=int)

    print 'Tutti i nodi delle coppie:'
    print all_nodes

def get_furthest_node_from_list(dict):

    couple=None
    highest_value=-1
    for node in dict:
        value=dict[node]
        if value>highest_value:
            highest_value=value
            couple=(node,highest_value)

    return couple


def subset_of_list(list_of_couples,num_of_couple):

    if len(list_of_couples)<num_of_couple:
        num_of_couple=len(list_of_couples)

    subset_list=[]
    for i in range(0,num_of_couple,1):
        if list_of_couples[i] not in subset_list:
            subset_list.append(list_of_couples[i])


    return subset_list



def get_first_n_couple(list_of_couples,num_couple):

    couples_selected=[]
    for i in range(0,num_couple,1):
        couples_selected.append(list_of_couples[i])

    return couples_selected

def select_random_couples_from_list(list_of_couples,num_couple):

    couples_selected=[]
    for i in range(0,num_couple,1):

        couple=list_of_couples[random.randint(0,len(list_of_couples)-1)]
        couples_selected.append(couple)
        list_of_couples.remove(couple)


    print 'Coppie selezionate Random:'
    #print couples_selected

    return couples_selected


def check_if_istance_is_feasible(H,list_of_couples,flow_c_value):

    graph=nx.MultiGraph(H)

    green_edges=[]
    for couple in list_of_couples:
        edge=(couple[0],couple[1],flow_c_value)
        if edge not in green_edges:
            green_edges.append(edge)
        else:
            sys.exit('Errore in check if istance is feasible: coppia di domanda gia presente')


    prepare_graph(graph)

    add_green_edges_to_graph(graph,green_edges)

    #print 'Archi verdi :'
    #print green_edges

    #my_draw(graph,'domanda_generata_fissa')

    if check_routability(graph,green_edges):
        return True
    else:
        return False


def add_green_edges_to_graph(graph,green_edges):



    for couple in green_edges:
        node_1=couple[0]
        node_2=couple[1]
        graph.add_node(node_1,id=node_1,label=node_1,type='green',color='green')
        graph.add_node(node_2,id=node_2,label=node_2)

    for couple in green_edges:

        id_node_source=couple[0]
        id_node_target=couple[1]
        demand_flow=couple[2]
        #print "%d-%d-%d: "%(id_node_source,id_node_target,demand_flow)
        graph.add_edge(id_node_source,id_node_target,type='green',demand=demand_flow,color='green',style='bold')



def find_max_radius_destruction_of_graph(H,coor_x,coor_y):

    graph=nx.MultiGraph(H)
    nodes_destroyed=[]
    edges_destroyed=[]
    total_nodes=nx.number_of_nodes(graph)
    total_edges=nx.number_of_edges(graph)

    radius_find=False

    var_distruption=0

    while(radius_find==False):
        var_distruption+=5
        sys.stdout.write("Varianza distruzione: %d\r"%(var_distruption))
        sys.stdout.flush()
        del graph
        graph=nx.MultiGraph(H)
        nodes_destroyed,edges_destroyed=destroy_graph(graph,coor_x,coor_y,var_distruption)
        my_draw(graph,'distruzione_var_%d'%var_distruption)
        """
        if var_distruption>390:
            print nodes_destroyed
            print edges_destroyed
            print len(nodes_destroyed)
            print len(edges_destroyed)
            print 'Total nodes: %d'%(total_nodes)
            print 'Total edges: %d'%(total_edges)
        """
        if (len(nodes_destroyed)==total_nodes) and (len(edges_destroyed)==total_edges):
            print 'Max radius trovato %d:'%(var_distruption)
            radius_find=True
            return var_distruption
        else:
            radius_find=False





def print_edge_graph(H):

    for edge in H.edges(data=True):
        print edge



def compute_and_save_distance_couples(H,path_to_folder_couple,filename_graph):

    list_of_couples=compute_all_shortest_distance_disjoint(H)
    check_if_are_disjoint(list_of_couples)

    #salva su file le coppie calcolate
    file_couple=open(path_to_folder_couple+filename_graph+'_couples.txt','w')
    file_couple.write('\n'.join('%d %d %d' % x for x in list_of_couples))
    file_couple.close()


def get_list_distance_couples(path_to_folder_couple,filename_graph):

    path_to_couple=path_to_folder_couple+filename_graph+'_couples.txt'
    if not os.path.exists(path_to_couple):
        print 'entro'
        os.system("python calcolo_coppie_distanti.py "+str(filename_graph))

    file_to_couple=open(path_to_couple,'r')
    mylist = [tuple(map(int, i.split(' '))) for i in file_to_couple]

    return mylist




def my_dijkstra_shortest_path(H,source,target):

    (length, path) = my_single_source_dijkstra(H, source=source, target=target)
    #print length

    #print path
    try:
        return path[target]
    except KeyError:
        raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))




def my_single_source_dijkstra(G, source, target=None, cutoff=None, weight='weight'):

    #weight_e='capacity'
    if source == target:
        return ({source: 0}, {source: [source]})

    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    paths = {source: [source]}  # dictionary of paths
    seen = {source: 0}
    c = count()
    fringe = []  # use heapq with (distance,label) tuples
    push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break
        # for ignore,w,edgedata in G.edges_iter(v,data=True):
        # is about 30% slower than the following
        """
        if G.is_multigraph():
            edata = []
            for w, keydata in G[v].items():
                list_vertex=[]
                #print list(dd.get(weight, 1) for k, dd in keydata.items())
                for k,dd in keydata.items():
                    #sys.exit(0)

                    if dd.get('status')=='destroyed':
                        edge_cost=1.0
                    else:
                        edge_cost=0.1

                        #list_vertex.append(edge_cost/dd.get('capacity'))
                    value="%.2f"%(1.0/dd.get('capacity'))
                    list_vertex.append(value)

                minweight=min(list_vertex)
                edata.append((w, {'capacity': minweight}))
        else:
        """
        edata = iter(G[v].items())

        for w, edgedata in edata:
            #print v,edgedata,w
            #vw_dist = dist[v] + float(edgedata.get('capacity', 1))+G.node[w][weight]
            vw_dist = dist[v] + distance_node(G,v,w,'broken_capacity') #+G.node[w][weight]

            if cutoff is not None:
                if vw_dist > cutoff:
                    continue
            if w in dist:
                if vw_dist < dist[w]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif w not in seen or vw_dist < seen[w]:
                seen[w] = vw_dist
                push(fringe, (vw_dist, next(c), w))
                paths[w] = paths[v] + [w]

    return (dist, paths)


def get_supply_graph(H,green_edges):

    my_draw(H,'grafo_da_cui_prendere')
    green_edge_to_remove=[]
    supply_graph=nx.MultiGraph(H)
    for edge in green_edges:
        source=edge[0]
        target=edge[1]
        if supply_graph.has_edge(source,target):
            keydict=H[source][target]
            if len(keydict)>1:
                for k in keydict:
                    if H[source][target][k]['type']=='green':
                        #print 'Trovato'
                        green_edge_to_remove.append((source,target,k))
            else:
                green_edge_to_remove.append((source,target,-1))
        else:
            sys.exit('Errore in get_supply graph: arco verde non presente!!')

    #print green_edge_to_remove
    for edge in green_edge_to_remove:
        source=edge[0]
        target=edge[1]
        key_to_remove=edge[2]
        if key_to_remove==-1:
            supply_graph.remove_edge(source,target)
        else:
            supply_graph.remove_edge(source,target,key=key_to_remove)
        #print 'RIMOSSO'

    #for edge in supply_graph.edges(data=True):
    #    print edge
    #sys.exit(0)

    return supply_graph


def update_status_node(H,node):

    H.node[node]['type']='normal'
    if H.node[node]['status']=='destroyed':
        H.node[node]['color']='red'
    elif  H.node[node]['status']=='repaired':
        H.node[node]['color']='blue'
    elif H.node[node]['status']=='on':
        H.node[node]['color']='None'
    else:
        sys.exit('Errore check if all green: nodo ne on,ne repaired,ne destroyed')



def write_progress_algorithm_on_file(path_stat_prog,name_graph,name_algo,num_couple,curr_sim,num_tot_simu,curr_seed,num_nodes_repaired,num_edges_repaired,num_max_nodes_repaired,num_max_edges_repaired):

    #path_to_stat='C:\Users'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\statistiche\stats\\'
    if not os.path.exists(path_stat_prog):
        os.makedirs(path_stat_prog)

    #crea file di progresso degli algoritmi
    file_prog=open(path_stat_prog+name_graph+'_'+str(num_couple)+'_couples_progress.txt','w+')
    string='Sim: %d/%d Seed: %d --- %s --- %d/%d --- %d/%d \n'%(curr_sim,num_tot_simu,curr_seed,name_algo,num_nodes_repaired,num_max_nodes_repaired,num_edges_repaired,num_max_edges_repaired)
    file_prog.write(string)



def write_stat_time_simulation(path_to_stat_times,name_algo,name_graph,curr_sim,num_tot_simu,curr_seed,num_couple,time_in_seconds):


    if not os.path.exists(path_to_stat_times):
        os.makedirs(path_to_stat_times)

    #crea file di progresso degli algoritmi
    file_prog=open(path_to_stat_times+name_graph+'_times_'+str(name_algo)+'_'+str(num_couple)+'_couple.txt','a')
    string='Sim: %d/%d Seed: %d --- Time: %s seconds \n'%(curr_sim,num_tot_simu,int(curr_seed),str(time_in_seconds))
    file_prog.write(string)

def get_node_edges(H,id_node):

    list_adj=list(nx.all_neighbors(H,id_node))
    list_couple=[(id_node,target) for target in list_adj]
    edges_of_node=[]
    for edge in list_couple:
        id_source=edge[0]
        id_target=edge[1]
        if H.has_edge(id_source,id_target):
                keydict=H[id_source][id_target]
                for k in keydict:
                    edge_1=(id_source,id_target)
                    edge_2=(id_target,id_source)
                    if edge_1 not in edges_of_node and edge_2 not in edges_of_node:
                        edges_of_node.append(edge_1)
    return edges_of_node

def get_node_status(H,id_node):
    return H.node[id_node]['status']


def init_owned_nodes(green_edges):
    owned_nodes = []
    for tup in green_edges:
        if tup[0] not in owned_nodes:
            owned_nodes.append(tup[0])
        if tup[1] not in owned_nodes:
            owned_nodes.append(tup[1])

    return owned_nodes

def resolve_onwed_node_edges(H,G,owned_nodes):
    for node in owned_nodes:
        edges = get_node_edges(H, node)
        for edge in edges:
            id_source=edge[0]
            id_target=edge[1]
            add_node_to_graph_info_gather(H,G,id_target)
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type'] != 'normal':
                    continue
                if G.has_edge(id_source,id_target) and G[id_source][id_target][k]['type'] == 'normal' and (G[id_source][id_target][k]['status'] == 'repaired' or G[id_source][id_target][k]['status'] == 'on'):
                    continue
                #if H[id_source][id_target][k]['status']=='destroyed':
                cap = H[id_source][id_target][k]['capacity']
                if H[id_source][id_target][k]['true_status'] == 'on':
                    if G.has_edge(id_source,id_target):
                        if G[id_source][id_target][k]['status'] == 'repaired':
                           continue
                        G[id_source][id_target][k]['color'] = 'black'
                        G[id_source][id_target][k]['style'] = 'solid'
                        G[id_source][id_target][k]['status'] = 'on'
                        G[id_source][id_target][k]['true_status'] = 'on'
                    else:
                        G.add_edge(id_source,id_target,type='normal',status='on',true_status='on', capacity=cap,color='black',style='solid')
                if H[id_source][id_target][k]['true_status'] == 'destroyed':
                    if G.has_edge(id_source,id_target):
                        G[id_source][id_target][k]['color'] = 'red'
                        G[id_source][id_target][k]['style'] = 'dashed'
                        G[id_source][id_target][k]['status'] = 'destroyed'
                        G[id_source][id_target][k]['true_status'] = 'destroyed'
                    else:
                        G.add_edge(id_source,id_target,type='normal',status='destroyed',true_status='destroyed',capacity=cap,color='red',style='dashed')

                   #status='on',labelfont='gray',color='gray',style='dashed'



def resolve_one_hop_nodes(H, G, owned_nodes):
    on_nodes = []
    destroyed_nodes = []
    for node in owned_nodes:
        edges = get_node_edges(G, node)
        for edge in edges:
            id_source=edge[0]
            id_target=edge[1]
            keydict=G[id_source][id_target]
            for k in keydict:
                if G[id_source][id_target][k]['type'] == 'green':
                    continue
                if G[id_source][id_target][k]['status'] == 'on' or G[id_source][id_target][k]['status'] == 'repaired':
                    if G.node[id_target]['status']=='on':
                        if (G.node[id_target]['color'] == 'gray' or G.node[id_target]['color'] == 'red'):
                            G.node[id_target]['color'] = '""'
                        if (id_target not in owned_nodes) and (id_target not in on_nodes):
                            on_nodes.append(id_target)
                    elif G.node[id_target]['status'] == 'repaired':
                        G.node[id_target]['color'] = 'blue'
                        if (id_target not in owned_nodes) and (id_target not in on_nodes):
                            on_nodes.append(id_target)
                    else:
                        if H.node[id_target]['true_status'] == 'on':
                            G.node[id_target]['status'] = 'on'
                            G.node[id_target]['color'] = '""'
                            if (id_target not in owned_nodes) and (id_target not in on_nodes):
                                on_nodes.append(id_target)
                        else:
                            G.node[id_target]['status'] = 'destroyed'
                            G.node[id_target]['color'] = 'red'
                            if (id_target not in owned_nodes) and (id_target not in destroyed_nodes):
                                destroyed_nodes.append(id_target)
    return on_nodes,destroyed_nodes
                            
def add_edges_recovered_to_graph_gray(H,graph_built,edges_recovered):
    print edges_recovered
    for edge in edges_recovered:     
        source=edge[0]
        target=edge[1]
        print source
        print target
        if H.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type']=='normal':
                    cap=H[source][target][k]['capacity']
                    #graph_built.add_edge(source,target, type='normal',status='repaired',labelfont='blue',color='blue',style='solid',capacity=cap)
                    if graph_built.has_edge(source,target):
                        true_status = graph_built[source][target][k]['true_status']
                        if true_status == 'destroyed':
                            graph_built[source][target][k]['color'] = 'blue'
                            graph_built[source][target][k]['status'] = 'repaired'
                        else:
                            graph_built[source][target][k]['color'] = 'black'
                            graph_built[source][target][k]['status'] = 'on'
                        graph_built[source][target][k]['style'] = 'solid'
                        graph_built[source][target][k]['true_status'] = 'on'
                    else:
                        true_status = 'on'
                        graph_built.add_edge(source,target, type='normal',status='repaired',true_status='on',labelfont='blue',color='blue',style='solid',capacity=cap)
            
        else:
            sys.exit('Errore in add_edges_recovered_to_graph: larco da aggiungere non esiste nel grafo supply')
    return (true_status == 'on')

def add_node_to_graph_info_gather(H,graph_built,id_nodo):
        for node in H.nodes():
            if H.node[node]['id']==id_nodo:
                if id_nodo not in graph_built.nodes():
                    long=H.node[node]['Longitude']
                    lat=H.node[node]['Latitude']
                    graph_built.add_node(H.node[node]['id'],id=id_nodo,Longitude=long,Latitude=lat,status=H.node[node]['status'],true_status=H.node[node]['true_status'], color=H.node[node]['color'], type=H.node[node]['type'], betweeness=H.node[node]['betweeness'])

def add_node_to_graph_recovered_gray(H,graph_built,id_nodo):
        for node in H.nodes():
            if H.node[node]['id']==id_nodo:
                if id_nodo not in graph_built.nodes():
                    long=H.node[node]['Longitude']
                    lat=H.node[node]['Latitude']
                    true_status = 'on'
                    graph_built.add_node(H.node[node]['id'],id=id_nodo,Longitude=long,Latitude=lat,status='repaired',true_status='on', color='blue', type=H.node[node]['type'], betweeness=H.node[node]['betweeness'])
                else:
                    true_status = graph_built.node[node]['true_status']
                    if true_status == 'destroyed':
                        graph_built.node[node]['color'] = 'blue'
                        graph_built.node[node]['status'] = 'repaired'
                    else:
                        graph_built.node[node]['color'] = 'blue'
                        graph_built.node[node]['shape'] = 'square'
                        graph_built.node[node]['status'] = 'on'
                    graph_built.node[node]['true_status'] = 'on'
        return (true_status == 'on')

def recover_gray(H,nodes_repaired,edge_repaired, owned_nodes, hops):
    
    for node in nodes_repaired:
        H.node[node]['status']='repaired'
        H.node[node]['true_status']='on'
        H.node[node]['color']='blue'
        print 'nodo ripristinato %d : '%(node)

    for edge in edge_repaired:
        id_source=edge[0]
        id_target=edge[1]
        keydict =H[id_source][id_target]
        #print str(keydict)
        for k in keydict:
            if H.edge[id_source][id_target][k]['type']=='normal':
                if H.has_edge(id_source,id_target):
                    H.edge[id_source][id_target][k]['status']='repaired'
                    H.edge[id_source][id_target][k]['true_status']='on'
                    H.edge[id_source][id_target][k]['color']='blue'
                    H.edge[id_source][id_target][k]['style']='solid'
                else:
                    H.add_edge(id_source,id_target,key=k, status='repaired',labelfont='blue',color='blue',style='solid')
                print 'arco ripristinato %d-%d: '%(id_source,id_target)

        if H.node[id_source]['status']=='destroyed':
            H.node[id_source]['status']='repaired'
            H.node[id_source]['true_status']='on'
            H.node[id_source]['color']='blue'
            print 'nodo ripristinato %d : '%(id_source)

        if H.node[id_target]['status']=='destroyed':
            H.node[id_target]['status']='repaired'
            H.node[id_target]['true_status']='on'
            H.node[id_target]['color']='blue'
            print 'nodo ripristinato %d : '%(id_target)

    for node in nodes_repaired:
        if node not in owned_nodes:
            owned_nodes.append(node)
    #if couples_to_prune:      
    #    for couple in couples_to_prune:
    #        keydict = H[couple[0]][couple[1]]
    #        for k in keydict:
    #            if H.has_edge(couple[0],couple[1]):
    #                H[couple[0]][couple[1]][k]['status'] = 'repaired'
    #                H[couple[0]][couple[1]][k]['true_status'] = 'on'
    #                H[couple[0]][couple[1]][k]['style'] = 'solid'
    #                H[couple[0]][couple[1]][k]['color'] = 'blue'
    #                #H[couple[0]][couple[1]][k]['capacity'] = H[couple[0]][couple[1]][k]['capacity'] - couple[2]
                    
    information_gain(H, H, owned_nodes, hops)


def get_k_hop_nodes(H, node_list, hops):
    if not node_list:
        return []
    if hops == 0:
        return node_list
    k_hop_nodes = list(node_list)
    infinity_flag = False
    if hops <= -1:
        infinity_flag = True
    x = 0
    tmp = []
    while ((x < hops and not infinity_flag) or (tmp != k_hop_nodes and infinity_flag)):
        tmp = list(k_hop_nodes)
        for node in tmp:
            edges = get_node_edges(H, node)
            for edge in edges:
                id_source=edge[0]
                id_target=edge[1]
                keydict=H[id_source][id_target]
                for k in keydict:
                    if H[id_source][id_target][k]['type'] == 'green':
                        continue
                    if H[id_source][id_target][k]['status'] == 'on' or H[id_source][id_target][k]['status'] == 'repaired':
                        if id_target not in k_hop_nodes:
                            k_hop_nodes.append(id_target)
        x = x + 1
    return k_hop_nodes

def probe_network(H, G, nodes):
    if not nodes:
        return []
    discovered_nodes = []
    for node in nodes:
        edges = get_node_edges(H, node)
        for edge in edges:
            id_source=edge[0]
            id_target=edge[1]
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['color'] == 'gray' and H[id_source][id_target][k]['true_status'] == 'on' and H.node[id_target]['color'] == 'gray' and H.node[id_target]['true_status'] == 'on':
                    H[id_source][id_target][k]['color'] = 'black'
                    H[id_source][id_target][k]['style'] = 'solid'
                    H[id_source][id_target][k]['status'] = 'on'
                    H.node[id_target]['color'] = '""'
                    H.node[id_target]['status'] = 'on'
                    if id_target not in discovered_nodes:
                        discovered_nodes.append(id_target)
    return discovered_nodes
    

def information_gain(H, G, owned_nodes, k):
    if k == 0:
        return
    resolve_onwed_node_edges(H,G,owned_nodes)
    on_nodes,destroyed_nodes = resolve_one_hop_nodes(H, G,owned_nodes)

    if k > 0:
        for x in range(k-1):
            on_nodes = probe_network(H, G, on_nodes)
    else:
        on_nodes_last = []
        while (on_nodes != on_nodes_last):
            on_nodes_last = list(on_nodes)
            on_nodes = probe_network(H, G, on_nodes)

def find_green_edges(H):
    green_edges = []
    for edge in H.edges():     
        source=edge[0]
        target=edge[1]
        if H.has_edge(source,target):
            keydict=H[source][target]
            for k in keydict:
                if H[source][target][k]['type'] == 'green':
                    if (source,target,H[source][target][k]['demand']) not in green_edges:
                        green_edges.append((source,target,H[source][target][k]['demand']))
    return green_edges
    
def write_really_destroyed_graph(nodes_really_destroyed,edges_really_destroyed,filename_graph,path_to_stats):
    path_to_file=path_to_stats+filename_graph+'_Really_Destroyed.txt'
    print path_to_file
    #if not os.path.exists(path_to_file):
    file=open(path_to_file,'w')

    for node in nodes_really_destroyed:
        file.write(str(node)+'\n')

    file.write('stop\n')

    for edge in edges_really_destroyed:
        edge_str='('+str(edge[0])+','+str(edge[1])+')'
        #print edge_str
        file.write(edge_str+'\n')

    file.close()

    return path_to_file

def create_real_destroyed_graph(H,nodes_really_destroyed,edges_really_destroyed):
    destroyed = nx.MultiGraph(H)

    




    
