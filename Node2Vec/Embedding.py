import pandas as pd
import networkx as nx
from node2vec import Node2Vec

# Load data dari file CSV
nodes_df = pd.read_csv("../data/DummyData/nodes.csv")
edges_df = pd.read_csv("../data/DummyData/edges.csv")

# Bangun graph dari data
G = nx.DiGraph()
for _, row in nodes_df.iterrows():
    G.add_node(row['node'], type=row['type'])

for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], relation=row['relation'])

# Lakukan node2vec
node2vec = Node2Vec(
    G,
    dimensions=64,        # Ukuran vektor embedding
    walk_length=30,       # Panjang random walk
    num_walks=200,        # Jumlah walk per node
    workers=4,            # Jumlah thread
    seed=42
)

model = node2vec.fit(window=10, min_count=1, batch_words=4)

# Simpan embedding ke file CSV
embedding_vectors = []
for node in G.nodes():
    vector = model.wv[node]
    embedding_vectors.append([node] + vector.tolist())

embedding_df = pd.DataFrame(embedding_vectors)
embedding_df.columns = ['node'] + [f'dim_{i+1}' for i in range(64)]

embedding_df.to_csv("../data/DummyData/node_embedding.csv", index=False)
print("Node2Vec embeddings saved to node_embedding.csv")
