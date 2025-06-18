import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt

# === 1. Load Data ===
nodes_df = pd.read_csv("../data/DummyData/nodes.csv")
edges_df = pd.read_csv("../data/DummyData/edges.csv")
labels_df = pd.read_csv("../data/DummyData/labels.csv")

# === 2. Build Graph ===
G = nx.DiGraph()
for _, row in nodes_df.iterrows():
    G.add_node(row['node'], type=row['type'])

for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], relation=row['relation'])

# === 3. Node2Vec Embedding ===
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=2)
model = node2vec.fit(window=10, min_count=1)

# === 4. Build Feature Vectors from (applicant, job) pairs ===
X = []
y = []

for _, row in labels_df.iterrows():
    applicant = row['applicant']
    job = row['job']
    label = row['accepted']
    
    if applicant in model.wv and job in model.wv:
        vec_app = model.wv[applicant]
        vec_job = model.wv[job]
        
        # Combine embeddings (you can experiment: concat, diff, product, etc)
        feature = list(vec_app) + list(vec_job)
        X.append(feature)
        y.append(label)

# === 5. Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 6. Train Model ===
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# === 7. Evaluate ===
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))
