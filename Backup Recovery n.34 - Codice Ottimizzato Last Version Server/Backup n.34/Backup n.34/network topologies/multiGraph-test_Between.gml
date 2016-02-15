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
    Longitude 100
    Internal 1
    Latitude 50
  ]
  
  node [
    id 2
    label "Washington DC"
    Country "United States"
    Longitude 150
    Internal 1
    Latitude 100
  ]
  
  node [
    id 3
    label "Seattle"
    Country "United States"
    Longitude 150
    Internal 1
    Latitude 0

  ]
  node [
    id 4
    label "Seattle"
    Country "United States"
    Longitude 200
    Internal 1
    Latitude 70

  ]
  
  edge [
	
    source 0
    target 1
    LinkLabel "NY-CH"
	capacity 2
    LinkNote "c"
  ]
  
    edge [
	
    source 1
    target 2
    LinkLabel "CH-DC"
	capacity 2
    LinkNote "c"
  ]

  
    edge [
	
    source 2
    target 4
    LinkLabel "DC-SE"
	capacity 1 
    LinkNote "c"
  ]
  

    edge [
	
    source 1
    target 3
    LinkLabel "CH-DC"
	capacity 2 
    LinkNote "c"
  ]
   edge [
	
    source 3
    target 4
    LinkLabel "CH-DC"
	capacity 1 
    LinkNote "c"
  ]


 ]