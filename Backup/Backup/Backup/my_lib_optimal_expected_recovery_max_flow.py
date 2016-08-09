__author__ = 'Utente'
#ROUTABILITY AND REPAIRABILITY


from gurobipy import *

# Model data


def optimal_expected_recovery_max_flow(H,green_edges,Gap):
    print "INIZIO Optimal Recovery model"
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
    #print 'archi da usare'
    #for edge in H.edges(data=True):
    #    print edge

    for edge in H.edges():
        id_source=edge[0]
        id_target=edge[1]

        keydict=H[id_source][id_target]
        #print 'esamino arco'
        arc=(id_source,id_target)
        #print arc
        #print keydict
        for k in keydict:
            #print 'iterazione %d:'%(int(k))
            #print H[id_source][id_target][k]
            #print 'tipo arco: %s'%(H[id_source][id_target][k]['type'])
            if H[id_source][id_target][k]['type']=='normal' and H[id_source][id_target][k]['type']!='green':
                if arc not in arcs:
                    arcs.append(arc)
                else:
                    print 'ERRORE: COSTRUZIONE VETTORE ARCS: AGGIUNTO DUE VOLTE STESSO ARCO ?'
                    print arc
                cap=H[id_source][id_target][k]['capacity']
                if not capacity.has_key(arc):
                    capacity.update({arc:cap})
                else:
                    print 'ERRORE: COSTRUZIONE VETTORE CAPACITY: AGGIUNTO DUE VOLTE LO STESSO ARCO'
                    print arc

    arcs = tuplelist(arcs)

    vertex_cost={}
    #construct vertex costs array:
    for i in H.nodes():
        node_cost= 0 #H.node[i]['prob'] #0
        print 'HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEYYYYYYYYYYYYYYYYYYYYYYYYYY'
        print node_cost
        if H.node[i]['color']=='red':
            node_cost= 1 #H.node[i]['prob'] #1
        if H.node[i]['color']=='gray':
            node_cost=H.node[i]['prob']
        else:
            node_cost=H.node[i]['prob']

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
                edge_cost= 0#H[id_source][id_target][k]['prob'] #0
                if H[id_source][id_target][k]['color']=='red':
                    edge_cost=1 #H[id_source][id_target][k]['prob']#1
                if H[id_source][id_target][k]['color']=='gray':
                    edge_cost=H[id_source][id_target][k]['prob']
                else:
                    edge_cost=H[id_source][id_target][k]['prob']
                edge_tupla_1=(id_source,id_target)
                #edge_tupla_2=(id_target,id_source)
                if not arc_cost.has_key(edge_tupla_1):
                    arc_cost.update({edge_tupla_1:edge_cost})
                    #arc_cost.update({edge_tupla_2:edge_cost})
                else:
                    print 'ERRORE COSTRUZIONE VETTORE COSTO ARCHI: AGGIUNTO DUE VOLTE IL COSTO DELLO STESSO ARCO'

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
                print 'ERRORE COSTRUZIONE INFLOW: HO AGGIUNTO DUE VOLTE  LA COPPIA STESSO FLUSSO/NODO'
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
    Gaps = Gap
    nodes_used, edges_used=optimize(nodes,demand_flows,arcs,capacity,vertex_cost,arc_cost,inflow,Gaps)

    print 'node usati'
    print nodes_used
    print 'archi_usati'
    print edges_used

    for node in nodes_used:
        #if H.node[node]['status']=='destroyed':
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



def optimize(nodes,demand_flows,arcs,capacity,vertex_cost,arc_cost,inflow,Gaps):

    dmax=100
    # Create optimization model
    m = Model('netflow')
    #----------------INIZIO CREAZIONE VARIABILI F^h(i,j) SIGMA(i,j) e SIGMA(i)
    # Create variables
    flow = {}
    for h in demand_flows:
        for i,j in arcs:
            #CREO LE VARIABILI CHE MI DICONO QUANTO FLUSSO H PASSA TRA I E J
            flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                                   name='flow_%s_%s_%s' % (h, i, j))
            flow[h,j,i] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                                   name='flow_%s_%s_%s' % (h, j, i))
    m.update()

    #print 'flow'
    #print flow


    usedArc = {}
    #print 'arc_cost'
    #print arc_cost
    for i,j in arcs:
        #print 'prendo i e j:'+ str(i) + str(j)
        #print 'arc cost i j:' + str(arc_cost[i,j])
        #CREO LA VARIABILE SIGMA I-J CHE MI DICE SE PRENDERE O MENO L'ARCO I-J e aggiungo anche LA VARIABILE PER L'ARCO J-I
        #usedArc[i,j] = m.addVar(ub=1, obj=arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (i,j))
        usedArc[i,j] = m.addVar(lb=0,ub=1, obj=arc_cost[i,j], vtype=GRB.CONTINUOUS, name='usedArc_%s_%s' % (i,j))

        #usedArc[j,i] = m.addVar(ub=1, obj=arc_cost[i,j], vtype=GRB.BINARY, name='usedArc_%s_%s' % (j,i))
        usedArc[j,i] = m.addVar(lb=0,ub=1, obj=arc_cost[i,j], vtype=GRB.CONTINUOUS, name='usedArc_%s_%s' % (j,i))


    m.update()

    usedVertex = {}
    for i in nodes:
        #usedVertex[i] = m.addVar(ub=1, obj=vertex_cost[i], vtype=GRB.BINARY, name='usedVertex_%s' % (i))
        usedVertex[i] = m.addVar(lb=0,ub=1, obj=vertex_cost[i], vtype=GRB.CONTINUOUS, name='usedVertex_%s' % (i))

    m.update()


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

            m.addConstr( (quicksum(flow[h,k,i] for k,i in to_i) + inflow[h,i]) == (quicksum(flow[h,i,j] for i,j in from_i)),'node_%s_%s' % (h, i))


    m.update()

        # Arc capacity constraints    #VINCOLO B del paper
    for i,j in arcs:
        m.addConstr(quicksum(flow[h,i,j]+flow[h,j,i] for h in demand_flows) <= capacity[i,j]*usedArc[i,j],
                    'cap_%s_%s' % (i, j))


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
        m.addConstr(quicksum(usedArc[i,j] for i,j in arcs_inc_i) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))
        #m.addConstr(quicksum(usedArc[j,i] for j,i in to_i) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))
        #come era prima
        #m.addConstr(quicksum(usedArc[i,j] for i,j in arcs.select(i,'*')) <=usedVertex[i]*dmax,'nodeRec_%s' % (i))

    m.update()

    #positiveness
    for h in demand_flows:
        for i,j in arcs:
            m.addConstr(flow[h,i,j]>=0)

    m.update()
    #m.update()
    m.setParam('MIPGap',Gaps)
    #m.setParam('ITERATION_LIMIT',Gaps)
    #m.setParam('IterationLimit',100)
    #m.params.timeLimit = Gaps
    #m.setParam('TimeLimit', Gaps)
    m.update()

    #print 'modello costruito'
    #for v in m.getVars():
    #    print v.varName

    #m.setParam("Method",2)
    #m.setParam("Crossover",2)
    # Compute optimal solution
    m.optimize()



    ####VEDERE BENE!!!!!
    # Print solution


    if m.status == GRB.status.OPTIMAL:

        #for v in m.getVars():
        #      print v.varName, v.x

        #print("\n\nUsage of broken links\n")
        #for i,j in arcs:
        #   var_reference = m.getVarByName('usedArc_%s_%s' % (i,j))
        #   if arc_cost[i,j]!=0:
        #         print var_reference.varName, var_reference.x


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
        """
        #IN ARCS CI SONO SOLO GLI ARCHI DEL GRAFO QUINDI (I,J) , MA NON (J,I) 0 VICEVERSA
        for i,j in arcs:
           var_reference = m.getVarByName('usedArc_%s_%s' % (i,j))    #arco ij
           var_reference_reverse=m.getVarByName('usedArc_%s_%s'%(j,i)) #arco ji
           #SE L'ARCO E' STATO USATO NELLA SOLUZIONE OTTIMA
           if var_reference.x>0 or var_reference_reverse.x>0:
               #SE IL SUO COSTO ERA NON NULLO, QUINDI ERA ROTTO !!!
                if arc_cost[i,j]!=0:
                    edge=(i,j)
                    my_used_arc.append(edge)

        for i in nodes:
            var_reference=m.getVarByName('usedVertex_%s'%(i))
            #SE IL NODO E' STATO USATO (ATTRAVERSATO DA UN FLUSSO NON NULLO
            #print 'ESAMINO VERTICE'
            #print var_reference, var_reference.x
            if var_reference.x>0:
                #SE IL SUO COSTO ERA NON NULLO, QUINDI ERA ROTTO !!!
                if vertex_cost[i] !=0:
                    my_used_vertex.append(i)
        """

        temp_used_vertex=[]
        temp_max_flow=0
        total_flow=0
        max_flow=0
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
                if temp_max_flow == max_flow:
                  temp_used_vertex.append(i)
                  print 'INJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                  print i
                  print max_flow
                else: 
                  max_flow=temp_max_flow
                  temp_used_vertex = []
                  temp_used_vertex.append(i)
                  print 'INJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                  print i
                  print max_flow
          temp_max_flow=0


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
        my_used_vertex=temp_used_vertex
        return my_used_vertex,my_used_arc
