To do:

1- recover gray

def recover_gray(H,nodes_repaired,edge_repaired, owned_nodes):

    for node in nodes_repaired:
        if H.node[node]['true_status']=='destroyed':
            H.node[node]['status']='repaired'
            H.node[node]['color']='blue'
        elif H.node[node]['true_status']=='on':
            H.node[node]['status']='on'
            H.node[node]['color']='""'			
        print 'nodo ripristinato %d : '%(node)

    for edge in edge_repaired:
        id_source=edge[0]
        id_target=edge[1]
        keydict =H[id_source][id_target]
        #print str(keydict)
        for k in keydict:
            if H.edge[id_source][id_target][k]['type']=='normal':
                if H.edge[id_source][id_target][k]['true_status']=='destroyed':
                    H.add_edge(id_source,id_target,key=k, status='repaired',labelfont='blue',color='blue',style='solid')
                    print 'arco ripristinato %d-%d: '%(id_source,id_target)
                elif H.edge[id_source][id_target][k]['true_status']=='on':
                    H.add_edge(id_source,id_target,key=k, status='on',labelfont='black',color='black',style='solid')
                    print 'arco ripristinato %d-%d: '%(id_source,id_target)
        if H.node[id_source]['true_status']=='destroyed':
            H.node[id_source]['status']='repaired'
            H.node[id_source]['color']='blue'
            print 'nodo ripristinato %d : '%(id_source)
        elif H.node[id_source]['true_status']=='on':
            H.node[id_source]['status']='on'
            H.node[id_source]['color']='""'
            print 'nodo ripristinato %d : '%(id_source)
			
        if H.node[id_target]['true_status']=='destroyed':
            H.node[id_target]['status']='repaired'
            H.node[id_target]['color']='blue'
            print 'nodo ripristinato %d : '%(id_target)
        if H.node[id_target]['true_status']=='on':
            H.node[id_target]['status']='on'
            H.node[id_target]['color']='""'
            print 'nodo ripristinato %d : '%(id_target)            
    resolve_onwed_node_edges(H,H,owned_nodes)
    resolve_one_hop_nodes(H,H,owned_nodes)
    resolve_onwed_node_edges(H,H,nodes_repaired)
    resolve_one_hop_nodes(H,H,nodes_repaired)

	
2- recover_one_hop_edge_green


def recover_one_hop_edge_green(H,edges_recovered,nodes_recovered,edges_truely_recovered_isp,nodes_truely_recovered_isp):

    green_edges=get_green_edges(H)
    print green_edges
    destroyed_graph=nx.MultiGraph(get_graph_from_destroyed_graph(H))
    really_destroyed_graph=nx.MultiGraph(get_graph_from_truely_destroyed_graph(H))
	
    #vale true se ho riparato almeno un link ad 1 hop
    recovered_flag=False

    #lista delle coppie ad un hop
    recovered_edge_one_hop=[]

    #my_draw(destroyed_graph,'5-isp_grafo_distrutto_da_controllare')
    for couple in green_edges:
        supply_edge=False
        id_source=couple[0]
        id_target=couple[1]
        demand=couple[2]
        if H.has_edge(id_source,id_target):
            keydict=H[id_source][id_target]
            for k in keydict:
                if H[id_source][id_target][k]['type']!='green' and H[id_source][id_target][k]['type']=='normal':
                    if supply_edge==False:
                        supply_edge=True
                        #print H[id_source][id_target][k]
                        arc=(id_source,id_target,k)
                    else:
                        sys.exit('Errore in recovery pruning one hop: piu di un arco normal tra stessa coppia!!')

        if supply_edge==True:

            #vedi se il flusso residuo soddisfa la domanda, altrimenti lo ripristini
            #max_flow_on_residual=compute_max_flow(destroyed_graph,id_source,id_target)
            max_flow_on_residual=compute_max_flow(really_destroyed_graph,id_source,id_target)

            if max_flow_on_residual < demand :
                #need to repair the arc
                source=arc[0]
                target=arc[1]
                key_to_recover=arc[2]
                if H[source][target][key_to_recover]['status']=='destroyed':
                    #seamus add if for color true_status
                    if H[source][target][key_to_recover]['true_status'] == 'on':
                        H.add_edge(source,target,key=key_to_recover, type='normal',status='on',true_status='on',labelfont='black',color='black',style='solid')
                    elif H[source][target][key_to_recover]['true_status'] == 'destroyed':
                        H.add_edge(source,target,key=key_to_recover, type='normal',status='repaired',true_status='on',labelfont='blue',color='blue',style='solid')
                        if edge not in edges_truely_recovered:
                            edges_truely_recovered.append(edge)
                    recovered_flag=True
                    print 'Arco Ricoverato one hop: %d - %d'%(source,target)
                    edge=(source,target)
                    if edge not in edges_recovered:
                        edges_recovered.append(edge)

                        #aggiungi l'arco tra quelli da controllare per fare il pruning
                        if edge not in recovered_edge_one_hop:
                            recovered_edge_one_hop.append(edge)

                        #controllo se i nodi sono da ripristinare
                        if H.node[source]['status']=='destroyed':
                            if source not in nodes_recovered:
                                nodes_recovered.append(source)
                                if H.node[source]['true_status']=='destroyed':								
                                    H.node[source]['status']='repaired'
                                    H.node[source]['color']='blue'
                                    if source not in nodes_truely_recovered:
                                        nodes_truely_recovered.append(source)
                                else:							
                                    H.node[source]['status']='on'
                                    H.node[source]['color']='black'	
									
                        if H.node[target]['status']=='destroyed':
                            if target not in nodes_recovered:
                                nodes_recovered.append(target)
                                if H.node[target]['true_status']=='destroyed':								
                                    H.node[target]['status']='repaired'
                                    H.node[target]['color']='blue'
                                    if target not in nodes_truely_recovered:
                                        nodes_truely_recovered.append(target)
                                else:							
                                    H.node[target]['status']='on'
                                    H.node[target]['color']='black'	
                    else:
                        sys.exit('Errore in recover_one_hop: arco gia riparato in precedenza!!')
                else:
                    print 'Arco non rotto da riparare'
                    print arc
                    sys.exit('Errore in recover_one_hop: arco non rotto selezionato per essere riparato!!')

    return recovered_edge_one_hop,recovered_flag
	