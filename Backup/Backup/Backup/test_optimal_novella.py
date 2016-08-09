__author__ = 'Utente'
#ROUTABILITY AND REPAIRABILITY


from gurobipy import *

# Model data


dmax=100
demand_flows = ['F0']
nodes = [0, 1, 2, 3, 4,5,6,7,8,9,10]

arcs, capacity = multidict({
  (0, 1):   5,
  (0, 2):  3,
  (1, 10):  4,
  (2,  9):   6,
  (3,  4): 5,
  (3, 6):   2,
  (4, 5):  7,
  (4, 6):   8,
  (5, 8):  7,
  (6, 7):  8,
  (7,  8):   3 ,
    (7,  10):   7 ,
    (8,  9):   5,
    (9,  10):   4 })
arcs = tuplelist(arcs)

print 'arcs:'
print arcs
print 'capacity:'
print capacity

vertex_cost={
  (0): 0,
  (1): 0,
  (2): 0,
  (3): 0,
  (4): 0,
  (5): 1,
  (6): 1,
  (7): 1,
  (8): 1,
  (9): 1,
  (10): 1 }

print vertex_cost

arc_cost = {
  (0, 1):   1,
  (0, 2):  0,
  (1, 10):  1,
  (2,  9):   1,
  (3,  4): 0,
  (3, 6):   0,
  (4, 5):  0,
  (4, 6):   1,
  (5, 8):  0,
  (6, 7):  0,
  (7,  8):   0 ,
    (7,  10):   1 ,
    (8,  9):   1,
    (9,  10):   1  }

inflow = {
  ('F0', 0):   -5,
  ('F0', 4):  5,
  ('F0', 1):   0,
  ('F0', 2): 0,
  ('F0', 3):   0,
  ('F0', 5):   0,
  ('F0', 6):   0,
  ('F0', 7):   0,
  ('F0', 8):   0,
  ('F0', 9):   0,
  ('F0', 10):   0,
   }

# Create optimization model
m = Model('netflow')

# Create variables
flow = {}
for h in demand_flows:
    for i,j in arcs:
        flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                               name='flow_%s_%s_%s' % (h, i, j))
        flow[h,j,i] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                               name='flow_%s_%s_%s' % (h, j, i))
m.update()

print 'flow'
print flow


usedArc = {}
for i,j in arcs:
    usedArc[i,j] = m.addVar(ub=1, obj=arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (i,j))
m.update()

usedVertex = {}
for i in nodes:
    usedVertex[i] = m.addVar(ub=1, obj=vertex_cost[i], vtype=GRB.BINARY, name='usedVertex_%s' % (i))
m.update()

# Arc capacity constraints
for i,j in arcs:
    m.addConstr(quicksum(flow[h,i,j] + flow[h,j,i] for h in demand_flows) <= capacity[i,j]*usedArc[i,j],
                'cap_%s_%s' % (i, j))

"""ORGINAL
# Flow conservation constraints
for h in demand_flows:
    for j in nodes:
        m.addConstr(
          quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) +
              inflow[h,j] ==
          quicksum(flow[h,j,k] for j,k in arcs.select(j,'*')),
                   'node_%s_%s' % (h, j))
"""
# Flow conservation constraints  #VINCOLO D del paper
for h in demand_flows:
    for i in nodes:
        list=[]
        list.extend(arcs.select('*',i))
        list.extend(arcs.select(i,'*'))
        #print 'lista archi incidenti a %d :'%(j)
        #print list
        to_i=[]
        from_i=[]
        for index in range(0,len(list)):
            id_source=(list[index])[0]
            id_target=(list[index])[1]
            edge=(id_source,id_target)
            reverse_edge=(id_target,id_source)
            if edge[0]==i:
                if edge not in from_i:
                    from_i.append(edge)
                if reverse_edge not in to_i:
                    to_i.append(reverse_edge)
            elif edge[1]==i:
                if reverse_edge not in from_i:
                    from_i.append(reverse_edge)
                if edge not in to_i:
                    to_i.append(edge)
            else:
                print 'ERRORE VINCOLO DI FLUSSO: ARCO NE FROM NE TO'
                print i,edge
        #siccome ce gia un for con indice i, chiamo i j nel for seguente ma si intende sempre la coppia (k,i) e (i,k), ma scrivo (k,j) e (j,k)
        m.addConstr( (quicksum(flow[h,k,i] for k,i in to_i) + inflow[h,i]) == (quicksum(flow[h,i,j] for i,j in from_i)),'node_%s_%s' % (h, i))


m.update()

# node recovery constraint

#for i in nodes:
#        usedVertex[i]*dmax >=
#        quicksum(usedArc[i,j] for j in nodes),
#               'nodeRec_%s' % (i))

for i in nodes:
       m.addConstr(
          quicksum(usedArc[i,j] for i,j in arcs.select(i,'*'))
            <=
          usedVertex[i]*dmax,
                'nodeRec_%s' % (i))

m.update()

#positiveness
for h in demand_flows:
    for i,j in arcs:
        m.addConstr(flow[h,i,j]>=0)

m.update()



# Compute optimal solution
m.optimize()



####VEDERE BENE!!!!!
# Print solution


if m.status == GRB.status.OPTIMAL:

    for v in m.getVars():
          print v.varName, v.x

    print("\n\nUsage of broken links\n")
    for i,j in arcs:
       var_reference = m.getVarByName('usedArc_%s_%s' % (i,j))
       if arc_cost[i,j]!=0:
             print var_reference.varName, var_reference.x

