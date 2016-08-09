graph [
  
  label "my_graph"
 
  node [
    id 0
    label "New York"
    Country "United States"
    Longitude 50
    Internal 1
    Latitude 50
	
  ]
  node [
    id 1
    label "Chicago"
    Country "United States"
    Longitude 50
    Internal 1
    Latitude 300
  ]
  
  node [
    id 2
    label "Washington DC"
    Country "United States"
    Longitude 300
    Internal 1
    Latitude 300
  ]
  
  node [
    id 3
    label "Seattle"
    Country "United States"
    Longitude 300
    Internal 1
    Latitude 50

  ]
  
  edge [
	
    source 0
    target 1
    LinkLabel "NY-CH"
	capacity 10
    LinkNote "c"
  ]
  
    edge [
	
    source 1
    target 2
    LinkLabel "CH-DC"
	capacity 5
    LinkNote "c"
  ]

  
    edge [
	
    source 2
    target 3
    LinkLabel "DC-SE"
	capacity 4
    LinkNote "c"
  ]
  

  edge[
	
	source 0
	target 3
	capacity 7
	LinkLabel "NY-SE"
	LinkNote "c"
  ]
 ]