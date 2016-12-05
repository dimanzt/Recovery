__author__ = 'Utente'
#python_path='c:\\Python27\\python '
#python_path='C:\Python27\python '

import os
from my_lib import *

#path_to_dot='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\DotFile\\'
#path_to_image='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\immagini_generate\\'
#path_to_image_store='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\store_images\\'
#path_to_file_simulation='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\current_simulation.txt'
#path_to_image_store='c:\\Users\\'+user_name+'\\Documents\Lab Work\\image_graph_dot\\store_images'
path_to_image_store='..\..\..\image_graph_dot\store_images'
#path_to_image_store='C:\Users\user\Novella\image_graph_dot\store_images'

#Diman Added
#import runpy, sys
#Diman Added



if len(sys.argv)>1:
    num_couple_passed=int(sys.argv[1])
    filename_graph=str(sys.argv[2])
    print num_couple_passed
else:
    num_couple_passed=-1
if len(sys.argv)>2:
    K_HOPS=int(sys.argv[3])
else: 
    K_HOPS=1
if len(sys.argv)>3:
    distance_metric=str(sys.argv[4])
else:
    distance_metric='broken_capacity'
if len(sys.argv)>4:
    type_of_bet=str(sys.argv[5])
else:
    type_of_bet='exact'
if len(sys.argv)>5:
    always_split=int(sys.argv[6])
else:
    always_split=0
if len(sys.argv)>6:
   random_disruption=int(sys.argv[7])
else:
   random_disruption=0
if len(sys.argv)>7:
   Monitors=int(sys.argv[8])
else:
   Monitors=5
if len(sys.argv)>8:
   var_distruption=float(sys.argv[9])
else:
   var_disruption=100

if len(sys.argv)>9:
   error=float(sys.argv[10])
else:
   error=0.0
if len(sys.argv)>10:
   ProbeCost=int(sys.argv[11])
else:
   ProbeCost=100

#parametri delle simulazioni

#flag per scegliere sempre lo stesso seed oppure no
seed_fixed=False
#seed della simulazione
seed=0
#alpha: proporzione di max_flow da usare come domanda
alpha=0.0
alpha_fixed=False
#flow_fixed=True
flow_fixed=False
error_fixed=False
Probe_fixed = False
flow_c=1
if num_couple_passed!=-1:
    num_couple_fix=True
    number_of_couple=num_couple_passed

else:
    num_couple_fix=False
    number_of_couple=5

fixed_distruption=True
fixed_dist_value=False
fixed_hop=False

#probabilita di selezionare un arco come green edges
#prob_edge=0.05
prob_edge=0.002
prob_edge_fixed=True

#numero di simulazioni da eseguire (per far variare alpha oppure far variare la prob edge)
num_simulations= 30
#metrica di distanza per calcolare lunghezza dei path : 'one-hop' , 'capacity', 'broken'
#distance_metric='broken'
#distance_metric='broken_capacity'
#distance_metric='unknown_capacity'

#type of betw 'classic', 'aprox', 'exact'
#type_of_bet='exact'
#type_of_bet='diman'

#specificare il nome del programma per la simulazione
name_of_program_simulation='Tomography_v2.py'

#specificare il nome del programma per generare le immagini
name_of_program_images='genera_immagini.py'

if alpha_fixed==False:
    if len(sys.argv)>1:
        for i in range(number_of_couple-1):
            alpha+=0.2
    else:
        alpha=0.0

if prob_edge_fixed==False:
    prob_edge=0.05

####if fixed_distruption==False:
###    var_distruption=0
###else:
###    var_distruption=0


#per 1 solo seed mettere size_array_seed ad 1
size_array_seed=10
seed_array=[]

if seed_fixed==False:
    for i in range(120,120+10,1):
        seed_array.append(i)
else:
    seed_array.append(seed)

if flow_fixed==True:
    flow_c=1

if num_couple_fix==False:
    number_of_couple=5


#number_of_couple=2



for i in range(0,num_simulations,1):


    if alpha_fixed==False:
        alpha+=0.2

    if num_couple_fix==False:
        number_of_couple+=0

    if flow_fixed==False:
        flow_c+=0

    if fixed_distruption==False:
        var_distruption+=0

    if fixed_dist_value==False:
        Monitors+=0

    if fixed_hop==False:
        K_HOPS+=0

    if error_fixed==False:
        error+=0.0

    if Probe_fixed==False:
        ProbeCost+=10

    for seed_elem in seed_array:
        #esegui una simulazione
        #os.system("python "+name_of_program_simulation +" "+str(seed_elem)+" "+str(alpha)+" "+str(prob_edge)+" "+str(num_simulations)+" "+str(i+1)+" "+distance_metric+" "+type_of_bet+" "+str(flow_fixed)+" "+str(flow_c)+" "+str(number_of_couple)+" "+str(fixed_distruption)+" "+filename_graph+" "+str(K_HOPS)+" "+str(always_split)+" "+str(random_disruption)+" "+str(disruption_value)+" "+str(error)+" "+str(Gap))
        os.system("python "+name_of_program_simulation +" "+str(seed_elem)+" "+str(alpha)+" "+str(prob_edge)+" "+str(num_simulations)+" "+str(i+1)+" "+distance_metric+" "+type_of_bet+" "+str(flow_fixed)+" "+str(flow_c)+" "+str(number_of_couple)+" "+str(fixed_distruption)+" "+str(var_distruption)+" "+filename_graph+" "+str(K_HOPS)+" "+str(always_split)+" "+str(random_disruption)+" "+str(Monitors)+" "+str(error)+" "+str(ProbeCost))
#Always split is 1 if we always put a monitor, 0 is we don't always put a monitor

        #genera le immagini della simulazione corrente
        #os.system("python "+name_of_program_images +" "+str(seed_elem)+" "+str(alpha)+" "+str(prob_edge)+" "+str(num_simulations)+" "+str(i+1)+" "+distance_metric)
        #sys.exit(0)
    if prob_edge_fixed==False:
        prob_edge+=0.01

    #sys.exit(0)
print 'SIMULAZIONI TERMINATE'
print 'Immagini generate nella cartella: '+path_to_image_store


