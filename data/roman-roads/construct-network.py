# %%
""" This script processes and constructs a network representation of Roman roads.
 It performs the following main tasks:
 1. Imports necessary libraries for geospatial data processing and analysis.
 2. Loads and preprocesses road data from a GeoDataFrame.
 3. Creates edge and node tables from the road data.
 4. Simplifies the graph by removing nodes with degree 2.
 5. Outputs the processed data for further analysis or visualization.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

# Load and preprocess data
# Read the GeoDataFrame from file and convert to EPSG:4326 coordinate system
gdf = gpd.read_file("dataverse_files").to_crs(4326)

# Create edge table
edges = gdf.copy()
# Create unique identifiers for start and end points of each edge
edges["u"] = [
    f"{round(g.coords[0][0], 3)}_{round(g.coords[0][1], 3)}" for g in edges.geometry
]
edges["v"] = [
    f"{round(g.coords[-1][0], 3)}_{round(g.coords[-1][1], 3)}" for g in edges.geometry
]
edges["key"] = range(len(edges))
edges = edges.set_index(["key"])


# Create node table
# Combine start and end points to create a list of all nodes
nodes = pd.DataFrame(edges["u"].tolist() + edges["v"].tolist(), columns=["osmid"])
# Create Point geometries for each node
nodes["geometry"] = [
    Point(float(n.split("_")[0]), float(n.split("_")[1])) for n in nodes.osmid
]
nodes.geometry.map(lambda x: x.coords[0][0])
# %%
nodes["x"] = nodes.geometry.map(lambda x: x.coords[0][0])
nodes["y"] = nodes.geometry.map(lambda x: x.coords[0][1])
nodes = gpd.GeoDataFrame(nodes).set_index("osmid")

# Create node and edge tables
node_table = pd.DataFrame({"node_id": range(len(nodes)), "osmid": nodes.index})
osmid2node_id = dict(zip(nodes.index, node_table["node_id"]))

# Create edge table with source and target node IDs
edge_table = pd.DataFrame(
    {
        "src": np.maximum(edges["u"].map(osmid2node_id), edges["v"].map(osmid2node_id)),
        "trg": np.minimum(edges["u"].map(osmid2node_id), edges["v"].map(osmid2node_id)),
    }
)
# Remove self-loops and duplicate edges
edge_table = edge_table[edge_table["src"] != edge_table["trg"]].drop_duplicates()


def simplify_graph(node_table, edge_table):
    while True:
        # Count the degree of each node
        node_degrees = np.bincount(
            edge_table[["src", "trg"]].values.flatten().astype(int)
        )
        # Find nodes with degree 2 (candidates for removal)
        nodes_to_remove = np.where(node_degrees == 2)[0]

        if len(nodes_to_remove) == 0:
            break

        for node in nodes_to_remove:
            # Find edges connected to the current node
            edges = edge_table.query("src == @node | trg == @node")
            if len(edges) != 2:
                continue

            # Get the two edges connected to the node
            edge1, edge2 = edges.iloc[0], edges.iloc[1]
            # Determine the new source and target for the merged edge
            new_src = (
                edge2["src"]
                if edge2["src"] != node
                else edge2["trg"] if edge1["src"] == node else edge1["src"]
            )
            new_trg = (
                edge1["trg"]
                if edge1["src"] == node
                else edge2["src"] if edge2["src"] != node else edge2["trg"]
            )

            # Create the new edge
            new_edge = edge1.copy()
            new_edge["src"], new_edge["trg"] = new_src, new_trg

            # Remove old edges and add the new edge
            edge_table = edge_table[~edge_table.index.isin(edges.index)]
            edge_table = pd.concat(
                [edge_table, pd.DataFrame([new_edge])], ignore_index=True
            )
            edge_table = edge_table[edge_table["src"] != edge_table["trg"]]

        # Remove the simplified nodes from the node table
        node_table = node_table[~node_table["node_id"].isin(nodes_to_remove)]

    # Remove isolated nodes (nodes with degree 0)
    node_degrees = np.bincount(edge_table[["src", "trg"]].values.flatten().astype(int))
    nodes_to_remove = np.where(node_degrees == 0)[0]
    node_table = node_table[~node_table["node_id"].isin(nodes_to_remove)]

    return node_table, edge_table


# Simplify and reindex the graph
simplified_node_table, simplified_edge_table = simplify_graph(node_table, edge_table)
# Create a mapping from old node IDs to new node IDs
nodeid2newid = dict(
    zip(simplified_node_table["node_id"], range(len(simplified_node_table)))
)
# Update node IDs in both node and edge tables
simplified_node_table["node_id"] = simplified_node_table["node_id"].map(nodeid2newid)
simplified_edge_table["src"] = simplified_edge_table["src"].map(nodeid2newid)
simplified_edge_table["trg"] = simplified_edge_table["trg"].map(nodeid2newid)

# Add coordinates to node table
simplified_node_table["lon"] = simplified_node_table["osmid"].map(
    dict(zip(nodes.index, nodes["x"]))
)
simplified_node_table["lat"] = simplified_node_table["osmid"].map(
    dict(zip(nodes.index, nodes["y"]))
)

# Save the simplified node and edge tables to CSV files
simplified_node_table.drop(columns=["osmid"]).to_csv("node_table.csv", index=False)
simplified_edge_table.to_csv("edge_table.csv", index=False)
