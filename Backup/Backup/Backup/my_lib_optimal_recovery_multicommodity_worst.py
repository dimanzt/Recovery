__author__ = 'Novella'

from gurobipy import *

# Model data

def optimal_recovery_multicommodity_worst(H,green_edges):

    nodes=[]
    #construct the array nodes:
    for node in H.nodes():
        nodes.append(node)

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
            print 'ERRORE COSTRUZIONE VERTEX_COST: AGGIUNTO DUE VOLTE IL COSTO DELLO STESSO NODO'




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

    nodes_used, edges_used=multicommodity_solution_worst(nodes,demand_flows,arcs,capacity,vertex_cost,arc_cost,inflow)

    print 'node usati'
    print nodes_used
    print 'archi_usati'
    print edges_used

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


###








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


def multicommodity_solution_worst(nodes,demand_flows,arcs,capacity,vertex_cost,arc_cost,inflow):

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



# Print solution and fill my_used_arc and my_used_vertex
    if m.status == GRB.status.OPTIMAL:
        print 'La funzione obiettivo del multicommodity vale:'
        pippo=m.objVal
        print pippo


    #### DA QUI COME L'OTTIMO MA CON IL VINCOLO DI PIPPO IN PIU e la funzione obiettivo invertita

    dmax=100
    # Create optimization model
    m1 = Model('worstflow')
    #----------------INIZIO CREAZIONE VARIABILI F^h(i,j) SIGMA(i,j) e SIGMA(i)
    # Create variables
    flow = {}
    for h in demand_flows:
        for i,j in arcs:
            #CREO LE VARIABILI CHE MI DICONO QUANTO FLUSSO H PASSA TRA I E J
            flow[h,i,j] = m1.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                                   name='flow_%s_%s_%s' % (h, i, j))
            flow[h,j,i] = m1.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                                   name='flow_%s_%s_%s' % (h, j, i))
    m1.update()

    #print 'flow'
    #print flow


    usedArc = {}
    #print 'arc_cost'
    #print arc_cost
    for i,j in arcs:
        #print 'prendo i e j:'+ str(i) + str(j)
        #print 'arc cost i j:' + str(arc_cost[i,j])
        #CREO LA VARIABILE SIGMA I-J CHE MI DICE SE PRENDERE O MENO L'ARCO I-J e aggiungo anche LA VARIABILE PER L'ARCO J-I
        usedArc[i,j] = m1.addVar(ub=1, obj=-arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (i,j))
        usedArc[j,i] = m1.addVar(ub=1, obj=-arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (j,i))


    m1.update()

    usedVertex = {}
    for i in nodes:
        usedVertex[i] = m1.addVar(ub=1, obj=0.0, vtype=GRB.BINARY, name='usedVertex_%s' % (i))
    m1.update()


    #-----------------INIZIO VINCOLI ------------------------------------------

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

            m1.addConstr( (quicksum(flow[h,k,i] for k,i in to_i) + inflow[h,i]) == (quicksum(flow[h,i,j] for i,j in from_i)),'node_%s_%s' % (h, i))


    m1.update()

        # Arc capacity constraints    #VINCOLO B del paper
    for i,j in arcs:
        m1.addConstr(quicksum(flow[h,i,j]+flow[h,j,i] for h in demand_flows) <= capacity[i,j]*usedArc[i,j],
                    'cap_%s_%s' % (i, j))

    #COST CONSTRAINT FROM PREVIOUS MULTICOMMODITY
    # Flow conservation constraints


    m1.addConstr( quicksum(arc_cost[i,j]*(flow[h,i,j]+flow[h,j,i]) for h in demand_flows  for i,j in arcs) == pippo,'vincolocosto')







    # node recovery constraint   #VINCOLO C del paper

    #for i in nodes:
    #        usedVertex[i]*dmax >=
    #        quicksum(usedArc[i,j] for j in nodes),
    #               'nodeRec_%s' % (i))

    for i in nodes:

        arcs_inc_i=[]
        arcs_inc_i.extend(arcs.select(i,'*'))
        arcs_inc_i.extend(arcs.select('*',i))
        """
        from_i=[]
        to_i=[]
        for index in range(0,len(arcs_inc_i)):
                id_source=(arcs_inc_i[index])[0]
                id_target=(arcs_inc_i[index])[1]
                edge=(id_source,id_target)
                reverse_edge=(id_target,id_source)
                if edge[0]==i:
                    if edge not in from_i:
                        from_i.append(edge)
                    if reverse_edge not in to_i:
                        to_i.append(edge)
                elif edge[1]==i:
                    if reverse_edge not in from_i:
                        from_i.append(reverse_edge)
                    if edge not in to_i:
                        to_i.append(edge)
                else:
                    print 'ERRORE VINCOLO DEL NODO: NODO NE FROM NE TO'
                    print i,edge
        """
        #invece della variabile i gia usata nel for esterno sui nodi, metto k
        m1.addConstr(quicksum(usedArc[i,j] for i,j in arcs_inc_i) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))
        #m.addConstr(quicksum(usedArc[j,i] for j,i in to_i) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))
        #come era prima
        #m.addConstr(quicksum(usedArc[i,j] for i,j in arcs.select(i,'*')) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))

    m1.update()

    #positiveness
    for h in demand_flows:
        for i,j in arcs:
            m1.addConstr(flow[h,i,j]>=0)

    m1.update()

    #print 'modello costruito'
    #for v in m1.getVars():
    #    print v.varName

    # Compute optimal solution
    m1.optimize()



    ####VEDERE BENE!!!!!
    # Print solution


    if m1.status == GRB.status.OPTIMAL:

        #for v in m1.getVars():
        #      print v.varName, v.x

        #print("\n\nUsage of broken links\n")
        #for i,j in arcs:
         #  var_reference = m1.getVarByName('usedArc_%s_%s' % (i,j))
         #  if arc_cost[i,j]!=0:
         #        print var_reference.varName, var_reference.x


        """
        for i,j in arcs:
            var_reference = m.getVarByName('usedArc_%s_%s' % (i,j))
            if arc_cost[i,j]!=0 and var_reference.x>0:
            #if var_reference.x>0:
                edge=(i,j)
                edges_repaired.append(edge)


        for i in nodes:
            var_reference = m.getVarByName('usedVertex_%s' % (i))
            if vertex_cost[i]!=0 and var_reference.x>0:
                node=i
                nodes_repaired.append(node)
        """

        my_used_arc=[]
        my_used_vertex=[]
        #IN ARCS CI SONO SOLO GLI ARCHI DEL GRAFO QUINDI (I,J) , MA NON (J,I) 0 VICEVERSA
        for i,j in arcs:
           var_reference = m1.getVarByName('usedArc_%s_%s' % (i,j))    #arco ij
           var_reference_reverse=m1.getVarByName('usedArc_%s_%s'%(j,i)) #arco ji
           #SE L'ARCO E' STATO USATO NELLA SOLUZIONE OTTIMA
           if var_reference.x>0 or var_reference_reverse.x>0:
               #SE IL SUO COSTO ERA NON NULLO, QUINDI ERA ROTTO !!!
                if arc_cost[i,j]!=0:
                    edge=(i,j)
                    my_used_arc.append(edge)

        for i in nodes:
            var_reference=m1.getVarByName('usedVertex_%s'%(i))
            #SE IL NODO E' STATO USATO (ATTRAVERSATO DA UN FLUSSO NON NULLO
            #print 'ESAMINO VERTICE'
            #print var_reference, var_reference.x
            if var_reference.x>0:
                #SE IL SUO COSTO ERA NON NULLO, QUINDI ERA ROTTO !!!
                if vertex_cost[i] !=0:
                    my_used_vertex.append(i)


        """ VECCHIA RIPARAZIONE SBAGLIATA
        for h in demand_flows:
            for i,j in arcs:
                flow_edge=m.getVarByName('flow_%s_%s_%s'%(h,i,j))
                #print 'esamino flusso %s tra %s %s '%(h,i,j)
                #print flow_edge.varName, flow_edge.x
                if flow_edge.x>0: #passa del flusso non nullo sull'arco i-j
                    edge=(i,j)
                    if(edge not in my_used_arc):
                        my_used_arc.append(edge)

                    if (i not in my_used_vertex):
                        my_used_vertex.append(i)
                    if (j not in my_used_vertex):
                        my_used_vertex.append(j)
                flow_edge_reverse=m.getVarByName('flow_%s_%s_%s'%(h,j,i))
                if flow_edge_reverse.x>0:
                    edge_reverse=(j,i)
                    if(edge_reverse not in my_used_arc):
                        my_used_arc.append(edge_reverse)
                    if (i not in my_used_vertex):
                        my_used_vertex.append(i)
                    if (j not in my_used_vertex):
                        my_used_vertex.append(j)
        """

        return my_used_vertex,my_used_arc