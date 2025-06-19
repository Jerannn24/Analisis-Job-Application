import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
nodes_df = pd.read_csv("../data/DummyData/nodes.csv")
edges_df = pd.read_csv("../data/DummyData/edges.csv")

# Filter only applicants and jobs
applicants = nodes_df[nodes_df['type'] == 'applicant']['node'].tolist()
jobs = nodes_df[nodes_df['type'] == 'job']['node'].tolist()

# Ambil edges yang merepresentasikan applicant melamar job
applied_edges = edges_df[
    (edges_df['source'].isin(applicants)) &
    (edges_df['target'].isin(jobs)) &
    (edges_df['relation'] == 'applied')
]

# (Optional) Batasi jumlah applicant agar visual tidak terlalu padat
selected_applicants = applied_edges['source'].unique()[:20]
filtered_edges = applied_edges[applied_edges['source'].isin(selected_applicants)]

# Bangun graf kosong
G = nx.DiGraph()

# Tambahkan node dan atributnya
for app in selected_applicants:
    G.add_node(app, type='applicant')
for job in filtered_edges['target'].unique():
    G.add_node(job, type='job')

# Tambahkan edges
for _, row in filtered_edges.iterrows():
    G.add_edge(row['source'], row['target'], relation=row['relation'])

# Warna node berdasarkan type
type_to_color = {
    'applicant': 'skyblue',
    'job': 'orange',
}
node_colors = [type_to_color.get(G.nodes[n]['type'], 'gray') for n in G.nodes()]

# Layout dan visualisasi
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, alpha=0.9)
nx.draw_networkx_edges(G, pos, alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=9)

# Optional: tampilkan label relasi pada edge
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("Graph: Applicants Applied to Jobs")
plt.axis('off')
plt.tight_layout()
plt.show()
