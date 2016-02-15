graph [
  
  label "my_graph"
 
  node [
    id 0
    Longitude 1
    Latitude -15
  ]
  node [
    id 1
    Longitude 50
    Latitude 0
  ]
  node [
    id 2
    Longitude 100
    Latitude 0
  ]
  
   node [
    id 3

    Longitude 130
    Latitude 0
  ]
  
  node [
    id 4

    Longitude 150
    Latitude -15
  ]
  
    node [
    id 5

    Longitude 100
    Latitude -20
  ]
    node [
    id 6

    Longitude 130
    Latitude -20
  ]
    
	node [
    id 7

    Longitude 115
    Latitude -30
  ] 
  	node [
    id 8

    Longitude 115
    Latitude -40
  ] 
  edge [

    source 0
    target 1
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
  
    edge [
    source 3
    target 4
    LinkLabel "SE-NY"
	capacity 4
    LinkNote "c"
  ]
  
    edge [

    source 2
    target 5
    LinkLabel "SE-NY"
	capacity 4
    LinkNote "c"
  ]
    edge [

    source 5
    target 7
    LinkLabel "SE-NY"
	capacity 4
    LinkNote "c"
  ]
    edge [

    source 7
    target 6
    LinkLabel "SE-NY"
	capacity 4
    LinkNote "c"
  ]
  edge[
    source 6
    target 3
    LinkLabel "SE-NY"
	capacity 4
    LinkNote "c"
  ]
    edge[
    source 7
    target 8
    LinkLabel "SE-NY"
	capacity 4
    LinkNote "c"
  ]
 ]