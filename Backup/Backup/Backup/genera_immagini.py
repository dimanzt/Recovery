__author__ = 'Utente'


import os
from my_lib import *

path_to_dot='../../../image_graph_dot/DotFile/'
#..\..\..\immagini_generate\image_graph_dot\DotFile/'
#'/usr/local/home/'+user_name+'/Desktop/image_graph_dot/DotFile/'
path_to_image='../../../image_graph_dot/immagini_generate/'
#'/usr/local/home/'+user_name+'/Desktop/image_graph_dot/immagini_generate/'
path_to_image_store='../../../image_graph_dot/store_images/'
#'/usr/local/home/'+user_name+'/Desktop/image_graph_dot/store_images/'
path_to_file_simulation='../../../image_graph_dot/current_simulation.txt'
#'/usr/local/home/'+user_name+'/Desktop/image_graph_dot/current_simulation.txt'

#print path_to_dot
#sys.exit()

for filename in os.listdir(path_to_dot):

    print 'file '+ str(filename)
    lenght=len(str(filename))
    extension=filename[(lenght-4):]
    name=filename[:lenght-4]
    #print str(extension)
    if(extension=='.dot'):
        path_to_file_dot=path_to_dot+filename
        #print 'dot_path: '+path_to_file_dot
        #print str(path_to_image)
        os.system("fdp -n2 -Tpng "+ path_to_file_dot + " > " + path_to_image+name+".png")
        #os.system("dot -Tpng "+ path_to_file_dot+ " > " + path_to_image+name+".png")

        print 'immagine generata: ' + path_to_image

number_sim=get_num_simulation(path_to_file_simulation)
store_file(path_to_image, path_to_image_store,number_sim)
set_num_next_simulation(path_to_file_simulation)

#cancello file .dot e le vecchie immagini
remove_files_dot(path_to_dot)
#remove_files_image(path_to_image)
