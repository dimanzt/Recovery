__author__ = 'Utente'

import os
import time
import shutil
import math

path_to_stats=path_to_stats='../../../image_graph_dot/stats/statistiche/' #'../../../image_graph_dot/stats/statistiche'
#'C:\Users\Utente\Desktop\image_graph_dot\stats\statistiche\\'

def avarage(name_of_file,filename,path_to_stats):

    path_to_file=path_to_stats+"\\"+filename
    print path_to_file
    file=open(path_to_file,'r')
    array_mean=[]
    flag=True
    for line in file:
        if flag==True:
            flag=False
            columns=line.split('\t')
            #print 'columns'
            #print columns
            for i in range(0,len(columns)-4,1):
                temp=[]
                array_mean.append(temp)
            #print 'stampo array_mean inizializzato con liste vuote'
            #print array_mean
        else:
            raw=line.split('\t\t')
            for i in range(0,len(raw)-2,1):
                #print raw[i]
                array_mean[i].append(raw[i])

    #print array_mean
    line_to_write=""
    # CALCOLA AVG E DEV STAND
    for array in array_mean:
        size=len(array)
        sum=0.0
        for elem in array:
            sum=sum+(float(elem))

        avg=0.0
        avg=sum/size
        line_to_write+=str(avg)+'\t'

        #ORA calcola dev std
        sum_dev=0.0
        print 'avg :%f'%(float(avg))
        epsilon=0.0001
        for elem in array:
            diff=0.0
            diff=float(elem)- float(avg)
            if (diff<epsilon):
                diff=0.0
            print pow (diff, 2 )
            sum_dev= sum_dev + ( pow (diff, 2 ) )

        print sum_dev

        sum_dev_nor=0.0
        sum_dev_nor=sum_dev/(len(array))
        print sum_dev_nor
        dev_std=0.0

        dev_std=math.sqrt(sum_dev_nor)
        print dev_std

        line_to_write+=str(dev_std)+'\t'


    file.close()

    #scrivi statistiche aggregate su file
    datestamp=(time.strftime("%d-%m-%Y"))
    timestamp=(time.strftime("%H-%M-%S"))
    print timestamp
    name_directory=path_to_stats+'\\'+'Statistiche aggregate_'
    if not os.path.exists(name_directory):
        os.makedirs(name_directory)

    filename=filename[:-4]
    filename='stat_prob_edge_based'
    path_to_file_to_write=name_directory+'\\'+filename+"_Dati_Aggregati"
    if not os.path.exists(path_to_file_to_write+'.txt'):
        file_to_write=open(path_to_file_to_write+'.txt','w+')
    else:
        file_to_write=open(path_to_file_to_write+'.txt','a')

    file_to_write.write(line_to_write+'\n')
    file_to_write.close()

    move_to_dir(name_directory,path_to_file)


def move_to_dir(name_directory,path_to_file):

    shutil.copy(path_to_file,name_directory)
    if os.path.exists(path_to_file):
        os.remove(path_to_file)

for filename in os.listdir(path_to_stats):
    prefix='stat_simulations'
    prefix_lenght=len(prefix)
    temp=filename[:prefix_lenght]
    if temp==prefix:
        print 'file '+ str(filename)
        lenght=len(str(filename))
        extension=filename[(lenght-4):]
        name=filename[len(prefix)+1:lenght-4]
        print name
        #print str(extension)
        if(extension=='.txt'):
            filename
            print filename
            avarage(name,filename,path_to_stats)
