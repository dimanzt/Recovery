__author__ = 'Utente'

import sys

def getKey(item):
    return item[0]

list=[(0,1),(3,1),(8,4),(3,1)]
new_list=[]
#order element of couple
print list
"""
for couple in list:
    if(couple[0]>couple[1]):
        new_edge=(couple[1],couple[0])
        if new_edge not in new_list:
            new_list.append(new_edge)
        else:
            sys.exit('Due volte stessa coppia riordinata')
    else:
        new_list.append(couple)

print new_list
"""
a= sorted(list,key=getKey, reverse=False)

print a
sys.exit(0)
#check if duplicate
seen = set()
uniq = []
for couple in new_list:
    edge=(couple[0],couple[1])
    edge_reverse=(couple[1],couple[0])

    if edge not in seen and edge_reverse not in seen:
        uniq.append(edge)
        seen.add(edge)
    else:
        print edge
        sys.exit('Errore esiste duplicato')