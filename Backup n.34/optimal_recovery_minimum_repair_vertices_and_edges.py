#ROUTABILITY AND REPAIRABILITY


from gurobipy import *

# Model data


dmax=100
demand_flows = ['F1','F2']
nodes = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11']

arcs, capacity = multidict({
  ('x1', 'x2'):   2,
  ('x2', 'x3'):  1,
  ('x3', 'x4'):  1,
  ('x4',  'x5'):   2,
  ('x2',  'x8'): 2,
  ('x8', 'x9'):   3,
  ('x9', 'x4'):  2,
  ('x6', 'x7'):   2,
  ('x7', 'x8'):  2,
  ('x9', 'x10'):  2,
  ('x10',  'x11'):   2 })
arcs = tuplelist(arcs)

print 'arcs:'
print arcs
print 'capacity:'
print capacity

vertex_cost={
  ('x1'): 0,
  ('x2'): 0,
  ('x3'): 0,
  ('x4'): 0,
  ('x5'): 0,
  ('x6'): 0,
  ('x7'): 0,
  ('x8'): 0,
  ('x9'): 0,
  ('x10'): 0,
  ('x11'): 0 }

print vertex_cost

arc_cost = {
  ('x1', 'x2'): 0,
  ('x2', 'x3'): 0,
  ('x3', 'x4'): 1, #1 if broken
  ('x4',  'x5'): 0,
  ('x2',  'x8'): 0,
  ('x8',  'x9'): 0,
  ('x9', 'x4'):  0,
  ('x9', 'x10'): 0,
  ('x10', 'x11'): 0,
  ('x6', 'x7'): 0,
  ('x7', 'x8'): 0 }

inflow = {
  ('F1', 'x1'):   2,
  ('F1', 'x5'):  -2,
  ('F2', 'x6'):   2,
  ('F2', 'x11'): -2,
  ('F1', 'x2'):   0,
  ('F1', 'x3'):   0,
  ('F1', 'x4'):   0,
  ('F1', 'x6'):   0,
  ('F1', 'x7'):   0,
  ('F1', 'x8'):   0,
  ('F1', 'x9'):   0,
  ('F1', 'x10'):  0,
  ('F1', 'x11'):  0,
  ('F2', 'x1'):   0,
  ('F2', 'x2'):   0,
  ('F2', 'x3'):   0,
  ('F2', 'x4'):   0,
  ('F2', 'x5'):   0,
  ('F2', 'x7'):   0,
  ('F2', 'x8'):   0,
  ('F2', 'x9'):   0,
  ('F2', 'x10'):   0 }

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

# Flow conservation constraints
for h in demand_flows:
    for j in nodes:
        m.addConstr(
          quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) +
              inflow[h,j] ==
          quicksum(flow[h,j,k] for j,k in arcs.select(j,'*')),
                   'node_%s_%s' % (h, j))

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

