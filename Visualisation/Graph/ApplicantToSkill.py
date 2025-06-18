import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
nodes_df = pd.read_csv("../data/DummyData/nodes.csv")
edges_df = pd.read_csv("../data/DummyData/edges.csv")

# Ambil node sesuai jenis
applicants = nodes_df[nodes_df['type'] == 'applicant']['node'].tolist()
skills = nodes_df[nodes_df['type'] == 'skill']['node'].tolist()
jobs = nodes_df[nodes_df['type'] == 'job']['node'].tolist()

# Filter edges untuk 3 jenis hubungan:
edges_app_skill = edges_df[
    (edges_df['source'].isin(applicants)) &
    (edges_df['target'].isin(skills)) &
    (edges_df['relation'] == 'has_skill')
]

edges_job_skill = edges_df[
    (edges_df['source'].isin(jobs)) &
    (edges_df['target'].isin(skills)) &
    (edges_df['relation'] == 'requires')
]

# (Optional) batasi applicant untuk kejelasan grafik
selected_applicants = edges_app_skill['source'].unique()[:15]
edges_app_skill = edges_app_skill[edges_app_skill['source'].isin(selected_applicants)]

# Ambil semua skill dari applicant terpilih
selected_skills = edges_app_skill['target'].unique()

# Ambil edges job-skill yang relevan saja
edges_job_skill = edges_job_skill[edges_job_skill['target'].isin(selected_skills)]

# Ambil semua job yang relevan
selected_jobs = edges_job_skill['source'].unique()

# Bangun graf
G = nx.Graph()

# Tambahkan node dengan atribut type
for n in selected_applicants:
    G.add_node(n, type='applicant')
for n in selected_skills:
    G.add_node(n, type='skill')
for n in selected_jobs:
    G.add_node(n, type='job')

# Tambahkan edges applicant-skill
for _, row in edges_app_skill.iterrows():
    G.add_edge(row['source'], row['target'], relation=row['relation'])

# Tambahkan edges job-skill
for _, row in edges_job_skill.iterrows():
    G.add_edge(row['source'], row['target'], relation=row['relation'])

# Mapping warna berdasarkan tipe node
type_to_color = {
    'applicant': 'skyblue',
    'skill': 'lightgreen',
    'job': 'orange'
}
node_colors = [type_to_color.get(G.nodes[n]['type'], 'gray') for n in G.nodes()]

# Layout dan visualisasi
pos = nx.spring_layout(G, seed=42, k=0.5)
plt.figure(figsize=(14, 10))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, alpha=0.9)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=9)

# Label relasi (opsional)
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("Graph: Applicant → Skill → Job")
plt.axis('off')
plt.tight_layout()
plt.show()
