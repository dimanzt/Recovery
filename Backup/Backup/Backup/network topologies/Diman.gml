graph [
  label "Abilene"
  node [
    id 1
    label "New York"
    Country "United States"
    Longitude -74.00597

    Latitude 40.71427
  ]
  node [
    id 2
    label "Chicago"
    Country "United States"
    Longitude -87.65005

    Latitude 41.85003
  ]
  node [
    id 3
    label "Washington DC"
    Country "United States"
    Longitude -77.03637
    Internal 1
    Latitude 38.89511
  ]
  node [
    id 4
    label "Seattle"
    Country "United States"
    Longitude -122.33207
    Internal 1
    Latitude 47.60621
  ]
  node [
    id 5
    label "Sunnyvale"
    Country "United States"
    Longitude -122.03635
    Internal 1
    Latitude 37.36883
  ]
  node [
    id 6
    label "Los Angeles"
    Country "United States"
    Longitude -118.24368
    Internal 1
    Latitude 34.05223
  ]
  edge [
    source 1
    target 2
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 10
  ]
  edge [
    source 2
    target 3
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
    source 3
    target 5
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
	capacity 5
  ]
  edge [
    source 5
    target 6
    LinkType "OC-192"
    LinkLabel "OC-192c"
    LinkNote "c"
	capacity 10
  ]

  
]
