__author__ = 'Utente'


import os
from my_lib import *

#path_to_dot='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\DotFile\\'
#path_to_image='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\immagini_generate\\'
path_to_image_store='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\store_images\\'
#path_to_file_simulation='/usr/local/home/'+'\\'+user_name+'\\'+'Desktop\image_graph_dot\current_simulation.txt'

if len(sys.argv)>1:
    num_couple_passed=int(sys.argv[1])
    filename_graph=str(sys.argv[2])
    print num_couple_passed
else:
    num_couple_passed=-1


#parametri delle simulazioni

#flag per scegliere sempre lo stesso seed oppure no
seed_fixed=False
#seed della simulazione
seed=0
#alpha: proporzione di max_flow da usare come domanda
alpha=0.0
alpha_fixed=False
flow_fixed=True
flow_c=2
if num_couple_passed!=-1:
    num_couple_fix=True
    number_of_couple=num_couple_passed

else:
    num_couple_fix=False
    number_of_couple=3

fixed_distruption=True


#probabilita di selezionare un arco come green edges
#prob_edge=0.05
prob_edge=0.002
prob_edge_fixed=True

#numero di simulazioni da eseguire (per far variare alpha oppure far variare la prob edge)
num_simulations=1
#metrica di distanza per calcolare lunghezza dei path : 'one-hop' , 'capacity', 'broken'
#distance_metric='broken'
distance_metric='broken_capacity'

#type of betw 'classic', 'aprox', 'exact'
type_of_bet='exact'

#specificare il nome del programma per la simulazione
name_of_program_simulation='recovery_opt_only.py'

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

if fixed_distruption==False:
    var_distruption=0
else:
    var_distruption=0


#per 1 solo seed mettere size_array_seed ad 1
size_array_seed=20
seed_array=[]

if seed_fixed==False:
    for i in range(79,79+3,1):
        seed_array.append(i)
else:
    seed_array.append(seed)

if flow_fixed==True:
    flow_c=22

if num_couple_fix==False:
    number_of_couple=0

#number_of_couple=5
for i in range(0,num_simulations,1):


    if alpha_fixed==False:
        alpha+=0.2

    if num_couple_fix==False:
        number_of_couple+=1

    if flow_fixed==False:
        flow_c+=3

    if fixed_distruption==False:
        var_distruption+=15

    for seed_elem in seed_array:
        #esegui una simulazione
        os.system("python "+name_of_program_simulation +" "+str(seed_elem)+" "+str(alpha)+" "+str(prob_edge)+" "+str(num_simulations)+" "+str(i+1)+" "+distance_metric+" "+type_of_bet+" "+str(flow_fixed)+" "+str(flow_c)+" "+str(number_of_couple)+" "+str(fixed_distruption)+" "+str(var_distruption)+" "+filename_graph)

        #genera le immagini della simulazione corrente
        #os.system("python "+name_of_program_images +" "+str(seed_elem)+" "+str(alpha)+" "+str(prob_edge)+" "+str(num_simulations)+" "+str(i+1)+" "+distance_metric)
        #sys.exit(0)
    if prob_edge_fixed==False:
        prob_edge+=0.01

    #sys.exit(0)
print 'SIMULAZIONI TERMINATE'
print 'Immagini generate nella cartella: '+path_to_image_store
