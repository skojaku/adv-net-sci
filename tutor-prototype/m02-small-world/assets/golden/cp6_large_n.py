# 1. Set a LARGE network size — much bigger than the N=200 you played with.
N = 2000  # try 2000
k = 4
p_values = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]

L0 = C0 = None
rows = []
for p in p_values:
    G = nx.connected_watts_strogatz_graph(N, k, p, seed=1) if p > 0 else nx.watts_strogatz_graph(N, k, 0)
    # 2. Measure the average distance of G — nx.average_shortest_path_length
    L = nx.average_shortest_path_length(G)
    # 3. Measure the average clustering of G — nx.average_clustering
    C = nx.average_clustering(G)
    if p == 0.0:
        L0, C0 = L, C
    rows.append({"p": str(p), "L/L0": L / L0, "C/C0": C / C0})

df = pd.DataFrame(rows).melt("p", var_name="measure", value_name="ratio")
alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("p:O", title="rewiring probability p"),
    y=alt.Y("ratio:Q", title="ratio to p=0 baseline"),
    color=alt.Color("measure:N", scale=alt.Scale(range=["#B4552D", "#35577F"])),
).properties(title=f"N={N}, k={k}")
