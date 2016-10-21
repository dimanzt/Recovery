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
        Yv[m] = m.addVar(ub=1, obj=0, vtype=GRB.BINARY, name='Selected_Monitor%s'% (m))  #m_cost[m],  
    m.update()
    m.addConstr(quicksum(Yv[m] for m in My_monitors) <= Max_monitors, 'Max_Monitors')
        
    for obj in my_objects:
        for m in obj.m
            m.addConstr(quicksum() <= )


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
        for i,j in arcs:
           var_reference = m1.getVarByName('usedArc_%s_%s' % (i,j))    #arco ij
           var_reference_reverse=m1.getVarByName('usedArc_%s_%s'%(j,i)) #arco ji
           if var_reference.x>0 or var_reference_reverse.x>0:
               #SE IL SUO COSTO ERA NON NULLO, QUINDI ERA ROTTO !!!
                if arc_cost[i,j]!=0:
                    edge=(i,j)
                    my_used_arc.append(edge)

        for i in nodes:
            var_reference=m1.getVarByName('usedVertex_%s'%(i))
            if var_reference.x>0:
                if vertex_cost[i] !=0:


    return Best_ILP_monitors, ILP_identifiable_links

