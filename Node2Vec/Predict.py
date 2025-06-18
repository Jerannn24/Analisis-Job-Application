import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load data
nodes_df = pd.read_csv("../data/DummyData/nodes.csv")
edges_df = pd.read_csv("../data/DummyData/edges.csv")
labels_df = pd.read_csv("../data/DummyData/labels.csv").set_index("node")

# Build directed graph
G = nx.DiGraph()
for _, row in nodes_df.iterrows():
    G.add_node(row["node"], type=row["type"])

for _, row in edges_df.iterrows():
    G.add_edge(row["source"], row["target"], relation=row["relation"])

# Generate Node2Vec embeddings
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=2)
model = node2vec.fit(window=10, min_count=1)

# Save embeddings to DataFrame
embeddings = {node: model.wv[node] for node in G.nodes if node in model.wv}
emb_df = pd.DataFrame.from_dict(embeddings, orient="index")
emb_df.index.name = "node"

# Join with labels
data = emb_df.join(labels_df).dropna()

# Train/test split
X = data.drop(columns="accepted")
y = data["accepted"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Reduce dimensions for PCA visualization
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

# Plot PCA
plt.figure(figsize=(10, 8))
colors = ['skyblue' if label == 0 else 'orange' for label in y]
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=colors, alpha=0.7)
plt.title("2D PCA of Node2Vec Embeddings")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.tight_layout()
plt.show()

accuracy
