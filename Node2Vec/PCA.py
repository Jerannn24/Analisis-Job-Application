import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load embeddings
embedding_df = pd.read_csv("../data/DummyData/node_embedding.csv")

# Load node type untuk pewarnaan
nodes_info = pd.read_csv("../data/DummyData/nodes.csv")  # kolom: node, type

# Merge agar tahu tipe tiap node
embedding_df = embedding_df.merge(nodes_info, on="node")

# Ambil nama node dan fitur embedding
nodes = embedding_df['node']
features = embedding_df.drop(columns=['node', 'type'])

# Lakukan PCA ke 2 dimensi
pca = PCA(n_components=2, random_state=42)
reduced = pca.fit_transform(features)

# Buat DataFrame hasil
pca_df = pd.DataFrame({
    'node': nodes,
    'type': embedding_df['type'],
    'pca_x': reduced[:, 0],
    'pca_y': reduced[:, 1]
})

# Simpan hasil ke CSV
pca_df.to_csv("node_embedding_pca.csv", index=False)

# Warna berbeda untuk tiap tipe node
type_colors = {
    'applicant': 'skyblue',
    'job': 'orange',
    'skill': 'green',
    'company': 'red',
    'school': 'brown',
    'city': 'purple',
    'experience_level': 'cyan',
    'certification': 'gold',
    'job_role': 'gray',
    'GPA_level': 'olive'
}

# Visualisasi dengan warna per tipe
plt.figure(figsize=(12, 10))
for node_type, group in pca_df.groupby('type'):
    plt.scatter(group['pca_x'], group['pca_y'],
                label=node_type,
                color=type_colors.get(node_type, 'black'),
                alpha=0.7, s=60)

plt.title("2D PCA Visualization of Node2Vec Embeddings by Node Type", fontsize=14)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.grid(True)
plt.legend(title="Node Type")
plt.tight_layout()
plt.show()
