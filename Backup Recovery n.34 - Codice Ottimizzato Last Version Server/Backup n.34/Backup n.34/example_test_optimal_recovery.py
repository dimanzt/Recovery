__author__ = 'Utente'
#from my_lib_optimal_recovery import optimal_recovery
import networkx as nx

from gurobipy import *
dmax=100
demand_flows = ['F1','F2']
nodes = [0,1, 2, 3]

arcs, capacity = multidict({
  (0, 1):  3,
  (1, 2):  4,
  (1,  3):   5,
   })
arcs = tuplelist(arcs)

print 'arcs:'
print arcs
print 'capacity:'
print capacity

vertex_cost={
  (0): 0,
  (1): 1,
  (2): 0,
  (3): 0,
 }


arc_cost = {
  (0, 1): 0,
  (1, 2): 0,#1 if broken
  (1, 3): 1,
   }

inflow = {
  ('F1', 0):   -2,
  ('F1', 1):   0,
   ('F1', 2):   0,
  ('F1', 3):  2,
    ('F2',1): 4,
    ('F2',2):-4,
    ('F2',0): 0,
    ('F2',3): 0

   }

dmax=100
# Create optimization model
m = Model('netflow')

# Create variables
flow = {}
for h in demand_flows:
    for i,j in arcs:
        flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, i, j))
        flow[h,j,i] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, j, i))

m.update()

#print 'flow'
#print flow


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
    m.addConstr(quicksum((flow[h,i,j]+flow[h,j,i]) for h in demand_flows) <= capacity[i,j]*usedArc[i,j],
                'cap_%s_%s' % (i, j))

# Flow conservation constraints

for h in demand_flows:
    for j in nodes:
        list=[]
        list.extend(arcs.select('*',j))
        list.extend(arcs.select(j,'*'))
        #print 'lista archi incidenti a %d :'%(j)
        #print list
        to_j=[]
        from_j=[]
        for i in range(0,len(list)):
            id_source=(list[i])[0]
            id_target=(list[i])[1]
            edge=(id_source,id_target)
            reverse_edge=(id_target,id_source)
            if edge[0]==j:
                from_j.append(edge)
                to_j.append(reverse_edge)
            else:
                from_j.append(reverse_edge)
                to_j.append(edge)

        #print 'to %d'%j
        #print to_j
        #print 'from %d'%j
        #print from_j
        #sum_exit=quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) + inflow[h,j]
        #sum_in=quicksum(flow[h,j,k] for j,k in arcs.select(j,'*'))
        #print 'exit e in:' + str(sum_exit.)+str(sum_in)
        #list=arcs.select('*',j)
        #list2=arcs.select(j,'*')
        m.addConstr( (quicksum(flow[h,i,j] for i,j in to_j) + inflow[h,j]) == (quicksum(flow[h,j,k] for j,k in from_j)),'node_%s_%s' % (h, j))
"""
for h in demand_flows:
    for j in nodes:
        m.addConstr(
          quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) +
              inflow[h,j] ==
          quicksum(flow[h,j,k] for j,k in arcs.select(j,'*')),
                   'node_%s_%s' % (h, j))

"""

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
        m.addConstr(flow[h,j,i]>=0)

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

