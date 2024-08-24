# Roman Road Network

This data is taken from Roman Road Network dataset (version 2008) from Harvard's Dataverse, which provides historical road networks of the Roman Empire in GIS format. The dataset can be found at: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi%3A10.7910%2FDVN%2FTI0KAU

- The data describes the roads by points and polygons, and we consider each point as a node and each road polygon as an edge.
- A node with two edges is removed and the two edges are merged, resulting a network of 4529 nodes and 6495 edges.
- Each point is assigned a latitude and longitude.
