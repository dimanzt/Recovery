graph [
  label "Abilene"
  node [
    id 0
    label "New York"
    Country "United States"
    Longitude -74.00597

    Latitude 40.71427
  ]
  node [
    id 1
    label "Chicago"
    Country "United States"
    Longitude -87.65005

    Latitude 41.85003
  ]
  node [
    id 2
    label "Washington DC"
    Country "United States"
    Longitude -77.03637
    Internal 1
    Latitude 38.89511
  ]
  node [
    id 3
    label "Seattle"
    Country "United States"
    Longitude -122.33207
    Internal 1
    Latitude 47.60621
  ]
  node [
    id 4
    label "Sunnyvale"
    Country "United States"
    Longitude -122.03635
    Internal 1
    Latitude 37.36883
  ]
  node [
    id 5
    label "Los Angeles"
    Country "United States"
    Longitude -118.24368
    Internal 1
    Latitude 34.05223
  ]
  node [
    id 6
    label "Denver"
    Country "United States"
    Longitude -104.9847
    Internal 1
    Latitude 39.73915
  ]
  node [
    id 7
    label "Kansas City"
    Country "United States"
    Longitude -94.62746
    Internal 1
    Latitude 39.11417
  ]
  node [
    id 8
    label "Houston"
    Country "United States"
    Longitude -95.36327
    Internal 1
    Latitude 29.76328
  ]
  node [
    id 9
    label "Atlanta"
    Country "United States"
    Longitude -84.38798
    Internal 1
    Latitude 33.749
  ]
  node [
    id 10
    label "Indianapolis"
    Country "United States"
    Longitude -86.15804
    Internal 1
    Latitude 39.76838
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
    source 0
    target 2
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 8
  ]
  edge [
    source 1
    target 10
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 9
  ]
  edge [
    source 2
    target 9
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 11
  ]
  edge [
    source 3
    target 4
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 10
  ]
  edge [
    source 3
    target 6
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 12
  ]
  edge [
    source 4
    target 5
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 13
  ]
  edge [
    source 4
    target 6
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 13
  ]
  edge [
    source 5
    target 8
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 12
  ]
  edge [
    source 6
    target 7
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 13
  ]
  edge [
    source 7
    target 8
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 8
  ]
  edge [
    source 7
    target 10
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 12	
  ]
  edge [
    source 8
    target 9
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 10
  ]
  edge [
    source 9
    target 10
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 9
  ]
  
  
]
