__author__ = 'Utente'

__author__ = 'Utente'
__author__ = 'Utente'

from gurobipy import *
from my_lib import *
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

# ATTENZIONE MANCONO DEI VINCOLI CHE NON GESTISCONO GLI EVENTUALI CICLI.
#BISOGNEREBE :
#SE SONO LA SORGENTE IL FLUSSO H (IL MIO) NON PUO ENTRARE IN ME
#SE SONO IL POZZO IL FLUSSO H (IL MIO) NON PUO USCIRE DA ME
#SE SONO INTERMEDIO IL FLUSSO ENTRANTE E USCENTE DEVE ESSERE UGUALE E PARI A QUELLO DELLA SORGENTE.



def compute_max_demand_in_the_graph(H):

    green_edges=get_green_edges(H)

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
            #return False

    demand_flows=[]
    #construct demand_flows array:
    i=0
    #se non ci sono archi verdi sicuramente e instradabile
    #print green_edges
    #print len(green_edges)
    if len(green_edges)==0:
        #print 'entro'
        print 'Nessun arco di domanda: flusso massimo 0'
        return 0

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

    result = compute_max_demand_solution(nodes,demand_flows,arcs,capacity,inflow,green_edges)

    return result



def compute_max_demand_solution(nodes,demand_flows,arcs,capacity,inflow,green_edges):


    if len(arcs)==0:
        print 'Compute Max Demand: nessun arco, max flow nel grafo = 0'
        return 0

    # Create optimization model
    m = Model('netflow')

    # Create variables
    flow = {}
    for h in demand_flows:
        for i,j in arcs:
            flow[h,i,j] = m.addVar(ub=capacity[i,j],vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, i, j))
            flow[h,j,i] = m.addVar(ub=capacity[i,j],vtype=GRB.CONTINUOUS,name='flow_%s_%s_%s' % (h, j, i))
            #continuous
    m.update()

    #VARIABILE AGGIUNTA PER LA QUANTITA DI FLUSSO
    var_demand={}
    for i in range(0,len(demand_flows),1):
        h=demand_flows[i]
        demand_i=green_edges[i][2]
        var_demand[h] = m.addVar(ub=demand_i,vtype=GRB.CONTINUOUS,name='var_demand_%s'%(h))

    m.update()
    #print var_demand

    # Arc capacity constraints
    for i,j in arcs:
        m.addConstr(quicksum(flow[h,i,j]+flow[h,j,i] for h in demand_flows) <= capacity[i,j],'cap_%s_%s' % (i, j))

    m.update()

    # Flow conservation constraints
    for h in demand_flows:
        #print 'Domanda :'
        #print h
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


            if (inflow[h,j]>0):
                #print 'Il nodo %d e sorgente'%(j)
                m.addConstr( ((quicksum(flow[h,j,k] for j,k in from_j)) - (quicksum(flow[h,i,j] for i,j in to_j)) ) == var_demand[h] ,'node_%s_%s' % (h, j))

            elif (inflow[h,j]<0):
                #print 'Il nodo %d e pozzo'%(j)
                m.addConstr( ( (quicksum(flow[h,i,j] for i,j in to_j)) - (quicksum(flow[h,j,k] for j,k in from_j)) ) == var_demand[h],'node_%s_%s' % (h, j))

            else:
                #print 'Il nodo %d e intermedio'%(j)
                m.addConstr( (quicksum(flow[h,j,k] for j,k in from_j) == (quicksum(flow[h,i,j] for i,j in to_j))) ,'node_%s_%s' % (h, j))

    m.update()

    #VINCOLO AGGIUNTO SULLA MAX QUANTITA DI DOMANDA PER LA VARIABILE VAR_DEMAND
    for i in range(0,len(demand_flows),1):
        h=demand_flows[i]
        demand_i=green_edges[i][2]

        m.addConstr(var_demand[h] <= demand_i)

    m.update()

    #VINCOLO DI POSITIVITA' DELLE VARIABILI VAR_DEMAND
    for i in range(0,len(demand_flows),1):
        h=demand_flows[i]
        m.addConstr(var_demand[h] >=0)

    m.update()

    #positiveness
    for h in demand_flows:
        for i,j in arcs:
            m.addConstr(flow[h,i,j]>=0)

    m.update()

    #---------------------------------------------------------------------FUNZIONE DA MASSIMIZZARE DEL PROBLEMA

    obj=LinExpr()
    obj=0.0
    for h in demand_flows:
        obj+=var_demand[h]

    #m.setObjective( (quicksum(var_demand[h]) for h in demand_flows), GRB.MAXIMIZE)
    m.setObjective( obj, GRB.MAXIMIZE)

    m.update()

    # Compute optimal solution
    m.optimize()

    flag_solution=False
    # Print solution
    max_flow_on_graph=0.0

    if m.status == GRB.status.OPTIMAL:


        #for v in m.getVars():
        #    print v.varName, v.x

        solution = m.getAttr('x', flow)
        #print solution
        #print 'Soluzione Trovata'
        #print m.objVal

        max_flow_on_graph=m.objVal


    return max_flow_on_graph


def get_all_incident_edge_of_node(node,arcs,option):

        list=[]
        list.extend(arcs.select('*',node))
        list.extend(arcs.select(node,'*'))
        #print 'lista archi incidenti a %d :'%(j)
        #print list


        from_source=[]
        to_target=[]
        for i in range(0,len(list)):
            id_source=(list[i])[0]
            id_target=(list[i])[1]
            edge=(id_source,id_target)
            reverse_edge=(id_target,id_source)
            if edge[0]==node:
                from_source.append(edge)
                to_target.append(reverse_edge)
            else:
                from_source.append(reverse_edge)
                to_target.append(edge)

        if option=='source':
            return from_source
        elif option=='target':
            return to_target
        else:
            sys.exit('Errore get_al_incident: ne source ne target')
