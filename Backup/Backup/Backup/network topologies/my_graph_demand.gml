graph [
  
  label "my_graph_demand"
 
  node [
    id 0
    label "New York"
    Country "United States"
    Longitude 50
    Internal 1
    Latitude 150
	
  ]

  node [
    id 2
    label "Washington DC"
    Country "United States"
    Longitude 100
    Internal 1
    Latitude 200
  ]
  node [
    id 3
    label "Seattle"
    Country "United States"
    Longitude 100
    Internal 1
    Latitude 150
  ]
  


    edge [
	
    source 0
    target 2
    LinkLabel "NY-DC"
	demand 6
    LinkNote "c"
  ]
  
  
    edge [
	
    source 0
    target 3
    LinkLabel "NY-SE"
	demand 1
    LinkNote "c"
  ]

 ]