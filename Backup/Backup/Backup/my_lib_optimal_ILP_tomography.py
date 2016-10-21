__author__ = 'Diman'

from gurobipy import *

# Model data

def optimal_ILP_tomography(my_monitor_comb,my_objects, Max_monitors):
    Best_ILP_monitors=[]
    ILP_identifiable_links=[]
    #########################GREEEDY BASED APPROACH###############################
    Best_greedy=0
    Best_greedy_monitors=[]
    Identified_links=[]
    for obj in my_objects:
        print obj.e
        print obj.m
        print obj.n
    print '########################START MONITOR LISTS###################'
    for mon in my_monitor_comb:
        print 'Identifiable_Links:'
        print mon.ident
        print 'Number:'
        print mon.num
        print 'Monitor Combination:'
        print mon.monitors

    Best_ILP_monitors, ILP_identifiable_links = ILP_solution_best(my_monitor_comb, my_objects, Max_monitors)

    return Best_ILP_monitors, ILP_identifiable_links
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def ILP_solution_best(my_monitor_comb, my_objects, Max_monitors, My_monitors):
    Best_ILP_monitors=[]
    ILP_identifiable_links=[]
    #########################GREEEDY BASED APPROACH###############################
    Best_greedy=0
    Best_greedy_monitors=[]
    Identified_links=[]
    Edges={}

    #All Edges and set of moniotrs that can identify them
    for obj in my_objects:
        print obj.e
        print obj.m
        print obj.n
        if obj.n not in Edges:
            Edges.append(obj.n)
    print '########################START MONITOR LISTS###################'
    #All monitors and set of edges that can be identified by them
    for mon in my_monitor_comb:
        print 'Identifiable_Links:'
        print mon.ident
        print 'Number:'
        print mon.num
        print 'Monitor Combination:'
        print mon.monitors
    

    # Create optimization model
    # Xl = Identifiable links,
    # Zs = Selected Sets
    # Yv = Selected Monitors 
    m = Model('maxCoverage')
    Yv = {}
    Xl = {}
    Zs = {}
    for m in My_moonitors:
        Yv[m] = m.addVar(ub=1, vtype=GRB.BINARY, name='Selected_Monitor%s'% (m))  #m_cost[m], 
    for e in Edges:
        Xl[e] = m.addVar(ub =1, vtype=GRB.BINARY, name='Identified_Links%s'% (e)) 
    for mon in my_monitor_comb:
        Zs[mon.num] = maddVar(ub=1, vtype=GRB.BINARY, name='Selected_Set%s'% (mon.num) )
    m.update()
    m.addConstr(quicksum(Yv[m] for m in My_monitors) <= Max_monitors, 'Max_Monitors')
    #This part is not completely correct:
    for obj in my_objects:
        m.addConstr(Xl[my_objects.n] <= quicksum(Zs[i] for i in obj.m ), 'Identifiable_links' )
 
    for obj in my_objects:
        for m in obj.m
            m.addConstr(quicksum() <= )

    m.update()
    # Set objective
    m.setObjective(quicksum(Xl[i] for l in edges), GRB.MAXIMIZE)

    m.update()
    m.optimize()

    "
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError:
    print('Encountered a Gurobi error')

except AttributeError:
    print('Encountered an attribute error')
    "

    if m.status == GRB.status.OPTIMAL:

        my_used_arc=[]
        my_used_vertex=[]
        for m in My_monitors:
           var_reference = m.getVarByName('Selected_Monitors%s' % (m))    #selected monitor
           if var_reference.x>0:
                ILP_identifiable_links.append(m)

        for e in Edges:
            var_reference=m.getVarByName('Identified_Links%s'% (e))
            if var_reference.x>0:
                ILP_identifiable_links.append(e)


    return Best_ILP_monitors, ILP_identifiable_links

