__author__ = 'Utente'

from gurobipy import *

# Model data

def get_degree_node(H,id_node):

    degree=0
    edges_of_node=[]
    for edge in H.edges():
        id_source=edge[0]
        id_target=edge[1]

        if(id_source==id_node or id_target==id_node):
            if H.has_edge(id_source,id_target):
                keydict=H[id_source][id_target]
                for k in keydict:
                    if H[id_source][id_target][k]['type']=='normal' and H[id_source][id_target][k]['type']!='green':
                        edge_1=(id_source,id_target)
                        edge_2=(id_target,id_source)
                        if edge_1 not in edges_of_node and edge_2 not in edges_of_node:
                            edges_of_node.append(edge_1)
                            degree=degree+1

    return degree



def optimal_recovery_multicommodity_max_flow(H,green_edges):

    nodes=[]
    #construct the array nodes:
    for node in H.nodes():
        if get_degree_node(H,node)>0:
            nodes.append(node)

    for edge in green_edges:
        source=edge[0]
        target=edge[1]
        if source not in nodes or target not in nodes: #nodo verde isolato. Soluzione sicuramente infeasible
            print 'ERRORE: Nodi di domanda sconnessi: modello infeasible'
            return False




    demand_flows=[]
    #construct demand_flows array:
    i=0
    for edge in green_edges:
        name_flow='F%d'%(i)
        demand_flows.append(name_flow)
        i+=1

    arcs=[]
    capacity={}
    #construct arcs array and capacity:
    for edge in H.edges():
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal'and H[id_source][id_target][k]['type']!='green':
                arc=(id_source,id_target)
                if arc not in arcs:
                    arcs.append(arc)
                #else:
                #    print 'ERRORE: A STESSO ARCO'
                cap=H[id_source][id_target][k]['capacity']
                if not capacity.has_key(arc):
                    capacity.update({arc:cap})
                # else:
                   # print 'ERRORE: NON POSSONO ESSERCI DUE VOLTE LO STESSO ARCO'

    arcs = tuplelist(arcs)

    """Non abbiamo costo per il flusso attraverso i nodi
    vertex_cost={}
    #construct vertex costs array:
    for i in H.nodes():
        node_cost=0
        if H.node[i]['status']=='destroyed':
            node_cost=1

        id_node=H.node[i]['id']
        if not vertex_cost.has_key(id_node):
            vertex_cost.update({id_node:node_cost})
        else:
            print 'ERRORE: AGGIUNTO DUE VOLTE IL COST DI UN NODO'
    """

    arc_cost={}
    #construct arc costs array:
    #for edge in H.edges():
    for edge in arcs:
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal' and H[id_source][id_target][k]['type']!='green':
                edge_cost=0
                if H[id_source][id_target][k]['status']=='destroyed':
                    edge_cost=1

                edge_tupla_1=(id_source,id_target)
                #edge_tupla_2=(id_target,id_source)
                if not arc_cost.has_key(edge_tupla_1):
                    arc_cost.update({edge_tupla_1:edge_cost})
                    #arc_cost.update({edge_tupla_2:edge_cost})
                else:
                    print 'ERRORE: AGGIUNTO DUE VOLTE IL COSTO DELLO STESSO ARCO'

    inflow={}
    #construct inflow array:
    i=0
    for edge in green_edges:
        id_source=edge[0]
        id_target=edge[1]
        demand=edge[2]
        flow_label=demand_flows[i]
        for node in nodes:
            flow_value=0
            if str(node)==str(id_source):
                flow_value=demand
            if str(node)==str(id_target):
                flow_value=-demand

            tupla_key=(flow_label,node)
            if not inflow.has_key(tupla_key):
                inflow.update({tupla_key:flow_value})
            else:
                print 'ERRORE: HO AGGIUNTO DUE VOLTE  LA COPPIA FLUSSO/NODO'
        i+=1

    #print nodes
    #print demand_flows
    #print arcs
    #print capacity
    #print vertex_cost
    #print arc_cost
    #print inflow

    nodes_used=[]
    edges_used=[]
    nodes_repaired=[]
    edges_repaired=[]

    nodes_used, edges_used=multicommodity_solution(H,nodes,demand_flows,arcs,capacity,arc_cost,inflow)

    for node in nodes_used:
        if H.node[node]['status']=='destroyed':
            nodes_repaired.append(node)

    for edge in edges_used:
        id_source=edge[0]
        id_target=edge[1]
        keydict=H[id_source][id_target]
        for k in keydict:
            if H[id_source][id_target][k]['type']=='normal' and H[id_source][id_target][k]['type']!='green':
                if H[id_source][id_target][k]['status']=='destroyed':
                    edges_repaired.append(edge)

    return nodes_repaired,edges_repaired

#ROUTABILITY AND REPAIRABILITY

# Solve a multi-commodity flow problem with weights that are all zeros to
# only determine the feasibility of a flow.
# Very high cost edges could be added to every non existing edge,
# low cost edges could be added to every broken edge.
# If the objective function is non zero, the flow is infeasible with the existing network and
# is using either a broken edge (low non null cost) or a non existing edge (high cost).
# Two demand flows ('F1' and 'F2')
# are produced in 2 nodes ('x1' and 'x6') and must be sent to
# two other destination nodes ('x5' and 'x11') to
# satisfy demand ('inflow[h,i]').
#
# Flows  must respect arc capacity constraints
# ('capacity[i,j]'). The objective is to minimize the sum of the arc
# transportation costs ('cost[i,j]').


def multicommodity_solution(H,nodes,demand_flows,arcs,capacity,arc_cost,inflow):

    """
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

    cost = {
      ('F1', 'x1', 'x2'):   0,
      ('F1', 'x2', 'x3'): 0,
      ('F1', 'x3', 'x4'):  100,
      ('F1', 'x4',  'x5'):   0,
      ('F1', 'x2',  'x8'): 0,
      ('F1', 'x8',  'x9'):  0,
      ('F1', 'x9', 'x4'):   0,
      ('F1', 'x9', 'x10'): 0,
      ('F1', 'x10', 'x11'):  0,
      ('F1', 'x6', 'x7'):  0,
      ('F1', 'x7', 'x8'):  0,
      ('F2', 'x1', 'x2'):   0,
      ('F2', 'x2', 'x3'): 0,
      ('F2', 'x3', 'x4'):  100,
      ('F2', 'x4',  'x5'):   0,
      ('F2', 'x2',  'x8'): 0,
      ('F2', 'x8',  'x9'):  0,
      ('F2', 'x9', 'x4'):   0,
      ('F2', 'x9', 'x10'): 0,
      ('F2', 'x10', 'x11'):  0,
      ('F2', 'x6', 'x7'):  0,
      ('F2', 'x7', 'x8'):  0 }

    inflow = {
      ('F1', 'x1'):   2,
      ('F1', 'x5'):    -2,
      ('F2', 'x6'):   2,
      ('F2', 'x11'):    -2,
      ('F1', 'x2'):   0,
      ('F1', 'x3'):   0,
      ('F1', 'x4'):   0,
      ('F1', 'x6'):   0,
      ('F1', 'x7'):   0,
      ('F1', 'x8'):   0,
      ('F1', 'x9'):   0,
      ('F1', 'x10'):  0,
      ('F1', 'x11'):   0,
      ('F2', 'x1'):    0,
      ('F2', 'x2'):   0,
      ('F2', 'x3'):    0,
      ('F2', 'x4'): 0 ,
      ('F2', 'x5'):   0,
      ('F2', 'x7'):   0,
      ('F2', 'x8'):   0,
      ('F2', 'x9'):   0,
      ('F2', 'x10'):   0 }


    """
    # Create optimization model
    m = Model('netflow')

    # Create variables
    flow = {}
    for h in demand_flows:
        for i,j in arcs:
            flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=arc_cost[i,j],vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, i, j))
            flow[h,j,i] = m.addVar(ub=capacity[i,j], obj=arc_cost[i,j],vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, j, i))
    m.update()

    # Arc capacity constraints
    for i,j in arcs:
        m.addConstr(quicksum(flow[h,i,j]+flow[h,j,i] for h in demand_flows) <= capacity[i,j],'cap_%s_%s' % (i, j))

    # Flow conservation constraints

    """ #old version
    for h in demand_flows:
        for j in nodes:
            m.addConstr(
              quicksum(flow[h,i,j] for i,j in arcs.select('*',j)) +inflow[h,j] == quicksum(flow[h,j,k] for j,k in arcs.select(j,'*')),'node_%s_%s' % (h, j))
    """
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

            m.addConstr( (quicksum(flow[h,i,j] for i,j in to_j) + inflow[h,j]) == (quicksum(flow[h,j,k] for j,k in from_j)),'node_%s_%s' % (h, j))

    m.update()

    #positiveness
    for h in demand_flows:
        for i,j in arcs:
            m.addConstr(flow[h,i,j]>=0)

    m.update()

    # Compute optimal solution
    m.optimize()

    my_used_arc=[]
    my_used_vertex=[]
    # Print solution and fill my_used_arc and my_used_vertex
    if m.status == GRB.status.OPTIMAL:

        print 'La funzione obiettivo del multicommodity vale:'
        pippo=m.objVal
        print pippo




        tem_used_vertex=0
        temp_max_flow=0
        total_flow=0
        for i in nodes:
          #var_reference=m.getVarByName('usedVertex_%s'%(i))
          var_reference=m.getAttr('x', usedVertex)
          if var_reference[i]>0:
            if vertex_cost[i] !=0:
              for j in nodes:
                if (i,j) in arcs:
                  for h in demand_flows:
                    temp_max_flow=temp_max_flow+flow[h,i,j]
              if temp_max_flow >= max_flow:
                max_flow=temp_max_flow
                tem_used_vertex = i
                print 'INJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                print i
                print max_flow
          temp_max_flow=0

        """
        solution = m.getAttr('x', flow)
        #print solution
        max_flow=0
        for h in demand_flows:
            #print('\nOptimal flows for %s:' % h)
            for i,j in arcs:
                #print 'arco : %d-%d flow: %.2f '%(i,j,solution[h,i,j])
                if solution[h,i,j] >= max_flow and H.node[i]['prob']>0 :
                    max_flow=solution[h,i,j]
                    print 'INJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    print('%s -> %s: %g' % (i, j, solution[h,i,j]))
                    edge=(i,j)
                    edge_reverse=(j,i)
                    if(edge not in my_used_arc) and (edge_reverse not in my_used_arc):
                        my_used_arc.append(edge)
                    if (i not in my_used_vertex):
                        my_used_vertex.append(i)
                    if (j not in my_used_vertex):
                        my_used_vertex.append(j)
                if solution[h,j,i]>= max_flow and H.node[j]['prob']>0:
                    max_flow=solution[h,j,i]
                    print 'INJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                    print('%s -> %s: %g' % (j, i, solution[h,j,i]))
                    edge_reverse=(j,i)
                    edge=(i,j)
                    if(edge_reverse not in my_used_arc) and (edge not in my_used_arc):
                        my_used_arc.append(edge)
                    if (i not in my_used_vertex):
                        my_used_vertex.append(i)
                    if (j not in my_used_vertex):
                        my_used_vertex.append(j)
        """
    my_used_vertex.append(temp_used_vertex)
    return my_used_vertex,my_used_arc
