graph [
  label "Demi"
  
  node [
    id 0
    label "Cold Lake"
    Country "Canada"
    Longitude -110.2017
    Internal 1
    Latitude 54.45018
    
  ]
  node [
    id 1
    label "Grande Prairie"
    Country "Canada"
    Longitude -118.80271
    Internal 1
    Latitude 55.16667
    
  ]
  node [
    id 2
    label "Edmonton"
    Country "Canada"
    Longitude -113.46871
    Internal 1
    Latitude 53.55014
    
  ]
  node [
    id 3
    label "Fort McMurray"
    Country "Canada"
    Longitude -111.38519
    Internal 1
    Latitude 56.7335
    
  ]
  node [
    id 4
    label "Kamloops"
    Country "Canada"
    Longitude -120.3192
    Internal 1
    Latitude 50.66648
    
  ]
  node [
    id 5
    label "Vernon"
    Country "United States"
    Longitude -73.83708
    Internal 1
    Latitude 40.9126
    
  ]
  edge [
    source 0
    target 1
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 10
  ]
  edge [
    source 1
    target 2
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 5
  ]
  edge [
    source 1
    target 3
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 5
  ]
  edge [
    source 3
    target 4
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 5
  ]
  edge [
    source 2
    target 4
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 5
  ]
  edge [
    source 4
    target 5
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 10
  ]

  
]
