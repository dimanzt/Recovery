__author__ = 'Utente'

array=[]
for i in range(0,4,1):
    edge=(i,i*10)
    array.append(edge)

print array

for edge in array:

    for i in range(0,2,1):
        print edge

print 'nuova iterazione'

i=0
for i in array:
    print 'elemento'
    print i
    for i in range(0,2,1):
        print i