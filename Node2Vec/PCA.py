import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load data
nodes_df = pd.read_csv("../data/DummyData/nodes.csv")
edges_df = pd.read_csv("../data/DummyData/edges.csv")

# Build undirected graph
G = nx.Graph()
for _, row in nodes_df.iterrows():
    G.add_node(row['node'], type=row['type'])

for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], relation=row['relation'])

# Generate Node2Vec embeddings
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=5)
model = node2vec.fit(window=10, min_count=1)

# Extract embeddings
node_ids = list(G.nodes())
embeddings = [model.wv[node] for node in node_ids]

# Convert to DataFrame and save
embedding_df = pd.DataFrame(embeddings, index=node_ids)
embedding_df['type'] = embedding_df.index.map(lambda n: G.nodes[n]['type'])
embedding_df.to_csv("node_embeddings.csv")
print("✅ Embeddings saved to 'node_embeddings.csv'")

# Apply PCA for visualization
pca = PCA(n_components=2)
emb_2d = pca.fit_transform(embeddings)

# Define color mapping for multiple node types
type_to_color = {
    'applicant': 'skyblue',
    'job': 'orange',
    'skill': 'green',
    'company': 'red',
    'language': 'purple',
    'school': 'brown',
    'city': 'pink',
    'experience_level': 'cyan',
    'certification': 'yellow',
    'job_role': 'gray',
    'GPA_level': 'olive'
}

# Assign colors based on node type
colors = [type_to_color.get(G.nodes[n]['type'], 'gray') for n in node_ids]

# Visualize
plt.figure(figsize=(10, 8))
plt.scatter(emb_2d[:, 0], emb_2d[:, 1], c=colors, alpha=0.7)

# (Optional) add node labels
for i, node in enumerate(node_ids):
    plt.text(emb_2d[i, 0], emb_2d[i, 1], node, fontsize=7)

plt.title("2D Visualization of Node Embeddings (Node2Vec + PCA)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.tight_layout()
plt.show()
