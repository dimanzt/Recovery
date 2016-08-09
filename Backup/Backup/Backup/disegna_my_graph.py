__author__='Stefano'

import networkx as nx
import matplotlib.pyplot as plt

H=nx.read_gml('network topologies/my_graph.gml')  #grafo supply
D=nx.read_gml('network topologies/my_graph_demand.gml') #grafo demand

#num_nodes = H.number_of_nodes()
#print 'number of nodes: ' + str(num_nodes)


#pos = nx.random_layout(H)

#for i in D.nodes():
   # print 'id_Node: ' + str( H.node[i]['id'])
    #print 'label: ' + str( D.node[i]['label'])
   # print 'Longitude: ' + str( H.node[i]['Longitude'])
   # print 'Latitude: ' + str( H.node[i]['Latitude'])

pos_supply={}
for i in H.nodes():
    pos_supply[i]= (H.node[i]['Longitude'],H.node[i]['Latitude'])

pos_demand={}
for i in D.nodes():
    pos_demand[i]= (D.node[i]['Longitude'], D.node[i]['Latitude'])

labelsNodes_supply={}

for i in H.nodes():
    labelsNodes_supply[i] = H.node[i]['label']
    
labelsNodes_demand={}

for i in D.nodes():
    labelsNodes_demand[i] = D.node[i]['label']
    #print 'label: ' + str( D.node[i]['label'])



#labelsEdges={}
#color=nx.get_edge_attributes(H,'LinkLabel')
#i=0
#for j in color: 
#    labelsEdges[i] = color[j]
    #print 'source: ' + str( color[i]['source'])
    #print 'target: ' + str( H.edge[i]['target'])
    #print 'LinkLable: ' + str( H.edge[i]['LinkLable'])
 #   print 'Linklabel: ' + str(labelsEdges[i])
#    i=i+1

#posEdges={}
#for i in H.nodes():
#    posEdges[i]= (H.node[i]['Longitude']+3,H.node[i]['Latitude']+3)

edge_capacity=dict( [ ( (u,v), d['capacity'] ) for u,v,d in H.edges(data=True)])
edge_demand=dict( [ ( (u,v), d['demand'] ) for u,v,d in D.edges(data=True)])

#disegna i grafi
nx.draw_networkx(H, pos_supply,labels=labelsNodes_supply)
nx.draw_networkx(D, pos_demand,labels=labelsNodes_demand,node_color='#21F51E',edge_color='#21F51E')

#disegna capacita sugli archi
nx.draw_networkx_edge_labels(H,pos_supply,edge_labels=edge_capacity,font_size=12)
nx.draw_networkx_edge_labels(D,pos_demand,edge_labels=edge_demand,font_size=12)

#nx.draw_networkx_labels(H,posEdges,labelsEdges,font_size=16)
#nx.draw_networkx_labels(H,pos_supply,labelsNodes_supply,font_size=16)
#nx.draw_networkx_labels(D,pos_demand,labelsNodes_demand,font_size=16)


plt.show()