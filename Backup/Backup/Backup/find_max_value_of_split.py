
from gurobipy import *
import networkx as nx
# Model data

def get_degree_node(H,id_node):

    degree=0

    list_adj=list(nx.all_neighbors(H,id_node))
    list_couple=[(id_node,target) for target in list_adj]
    edges_of_node=[]
    for edge in list_couple:
        id_source=edge[0]
        id_target=edge[1]
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

def find_max_value_to_split(H,green_edges,couple_to_split,original_edge,cut_condition_value):

    nodes=[]
    #construct the array nodes:
    for node in H.nodes():
        #print 'id nodo %d'%(node)
        if get_degree_node(H,node)>0:
            nodes.append(node)

    #controllo se tutti i nodi di domanda non sono nodi isolati. Altrimenti la soluzione e sicuramente infeasible

    for edge in green_edges:
        source=edge[0]
        target=edge[1]
        if source not in nodes or target not in nodes: #nodo verde isolato. Soluzione sicuramente infeasible
            print 'Nodi di domanda sconnessi: soluzione infeasible'
            return False

    demand_flows=[]
    #construct demand_flows array:
    i=0
    #se non ci sono archi verdi sicuramente e instradabile
    #print green_edges
    #print len(green_edges)

    #print green_edges

    green_edges.append(couple_to_split[0])
    green_edges.append(couple_to_split[1])
    #aggiungo gli altri due archi da splittare
    edge_demand_to_split=[]

    if len(green_edges)==0:
        #print 'entro'
        print 'Nessuna domanda da soddisfare: soluzione sicuramente feasible'
        return True

    for edge in green_edges:
        name_flow='F%d'%(i)
        if edge in couple_to_split or edge in [original_edge]:
            edge_demand_to_split.append((name_flow,edge))
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

    #max_demand_edge=cut_condition_value

    #print edge_demand_to_split
    #print original_edge
    #print couple_to_split[0]
    #print couple_to_split[1]
    total_demand=original_edge[2]
    #print 'max_demand_edge %f'%total_demand

    result = find_max_value_solution(nodes,demand_flows,arcs,capacity,inflow,total_demand,cut_condition_value,edge_demand_to_split,original_edge,couple_to_split[0],couple_to_split[1])

    return result



def find_max_value_solution(nodes,demand_flows,arcs,capacity,inflow,total_demand,cut_condition_value,edge_demand_to_split,original_edge,edge_1,edge_2):

    if len(arcs)==0:
        print 'Routability Check False: nessun arco, impossibile soddisfare la domanda'
        return False

    # Create optimization model
    m = Model('netflow')

    #print demand_flows

    # Create variables
    flow = {}
    #print demand_flows
    for h in demand_flows:
        for i,j in arcs:
            flow[h,i,j] = m.addVar(ub=capacity[i,j],vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, i, j))
            flow[h,j,i] = m.addVar(ub=capacity[i,j],vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, j, i))
            #continuous
    m.update()

    max_split=m.addVar(ub=cut_condition_value,vtype=GRB.CONTINUOUS,name='max_split')

    m.update()
    #print max_split

    #print 'edge demand to split'
    #print edge_demand_to_split
    #cambio il valore di inflow per i tre archi dello split
    h=edge_demand_to_split[0][0]
    inflow[h,original_edge[0]]=total_demand+(-max_split)
    inflow[h,original_edge[1]]=-total_demand+max_split
    #print h
    #print original_edge[0]
    #print original_edge[1]

    #print  inflow[h,original_edge[0]]
    #print inflow[h,original_edge[1]]


    #primo arco da splittare
    #print edge_1
    h=edge_demand_to_split[1][0]
    #print h
    inflow[h,edge_1[0]]=max_split
    inflow[h,edge_1[1]]=-max_split
    #print edge_1[0]
    #print edge_1[1]
    #print inflow[h,edge_1[0]]
    #print inflow[h,edge_1[1]]

    #primo arco da splittare
    h=edge_demand_to_split[2][0]
    #print h
    inflow[h,edge_2[0]]=max_split
    inflow[h,edge_2[1]]=-max_split
    #print edge_2[0]
    #print edge_2[1]
    #print inflow[h,edge_2[0]]
    #print inflow[h,edge_2[1]]


    m.setObjective(max_split, GRB.MAXIMIZE)

    m.update()

    m.addConstr(max_split>=0)

    m.addConstr(max_split<=cut_condition_value)

    #print inflow

    #list_edges_split=[]
    #list_edges_split.append(original_edge[0],original_edge[1])
    #for couple in couple_to_split:
    #    edge=(couple[0],couple[1])
    #   list_edges_split.append(edge)


    # Arc capacity constraints
    for i,j in arcs:
        m.addConstr(quicksum(flow[h,i,j]+flow[h,j,i] for h in demand_flows) <= capacity[i,j],'cap_%s_%s' % (i, j))


    demand_to_split=[]
    for edge in edge_demand_to_split:
       demand_to_split.append(edge[0])


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

            flow_in_j=(quicksum(flow[h,i,j] for i,j in to_j))
            flow_generated_j=inflow[h,j]
            total_sum_out_of_j=flow_in_j+flow_generated_j
            #print '-----------------------------------------------------------------'
            #print 'Flusso in %d'%(j)
            #print flow_in_j
            #print 'Flusso prodotto da %d'%(j)
            #print flow_generated_j
            #print 'Somma del flusso che entra-generato da %d'%(j)
            #print total_sum_out_of_j
            #print 'flusso entrante in %d = %f + flusso prodotto da %d = %f, flusso totale = %f '%(j,flow_in_j,j,flow_generated_j,total_sum_out_of_j)
            flow_out_j=(quicksum(flow[h,j,k] for j,k in from_j))
            #print 'Confrotare con flusso totale che esce da %d'%(j)
            #print flow_out_j

            #if h in demand_to_split:
            #    #print 'flusso uscente da %d = %f  deve essere uguale a %f'%(j,flow_out_j,total_sum_out_of_j)
            #   m.addConstr( (quicksum(flow[h,i,j] for i,j in to_j) + inflow[h,]) == (quicksum(flow[h,j,k] for j,k in from_j)),'node_%s_%s' % (h, j))

            #else:
            m.addConstr( (quicksum(flow[h,i,j] for i,j in to_j) + inflow[h,j]) == (quicksum(flow[h,j,k] for j,k in from_j)),'node_%s_%s' % (h, j))

    m.update()

    #positiveness
    for h in demand_flows:
        for i,j in arcs:
            m.addConstr(flow[h,i,j]>=0)

    m.update()

    #for v in m.getVars():
    #    print v.varName

    # Compute optimal solution
    m.optimize()

    flag_solution=False
    # Print solution
    if m.status == GRB.status.OPTIMAL:
        flag_solution=True

        #for v in m.getVars():
        #     print v.varName, v.x

        solution = m.getAttr('x', flow)
        #print solution
        #print 'Check Routability True'

        print 'Valore massimo splittabile %f'% m.objVal
        return m.objVal
    else:
        flag_solution=False
        """
        for h in demand_flows:
            print('\nOptimal flows for %s:' % h)
            for i,j in arcs:
                #print 'arco : %d-%d flow: %.2f '%(i,j,solution[h,i,j])
                if solution[h,i,j] > 0:
                    print('%s -> %s: %g' % (i, j, solution[h,i,j]))
                    edge=(i,j)
                    if(edge not in my_used_arc):
                        my_used_arc.append(edge)
                    if (i not in my_used_vertex):
                        my_used_vertex.append(i)
                    if (j not in my_used_vertex):
                        my_used_vertex.append(j)
                if solution[h,j,i]>0:
                    print('%s -> %s: %g' % (j, i, solution[h,j,i]))
                    edge_reverse=(j,i)
                    if(edge_reverse not in my_used_arc):
                        my_used_arc.append(edge_reverse)
                    if (i not in my_used_vertex):
                        my_used_vertex.append(i)
                    if (j not in my_used_vertex):
                        my_used_vertex.append(j)
        """
        #print 'Check Routability False'

        return 0