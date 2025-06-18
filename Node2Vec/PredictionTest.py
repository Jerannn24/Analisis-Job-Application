import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import TruncatedSVD

# === Load embedding yang telah dibuat ===
embedding_df = pd.read_csv("../data/DummyData/node_embedding.csv")
embedding_df.set_index(embedding_df.columns[0], inplace=True)

# === Contoh Applicant dan Job yang ingin diuji ===
applicant_id = "Puti Nugroho"   # Ganti dengan ID yang sesuai
job_id = "job_0"        # Ganti dengan ID yang sesuai

# === Pastikan keduanya ada di embedding ===
if applicant_id in embedding_df.index and job_id in embedding_df.index:
    applicant_vec = embedding_df.loc[applicant_id].values
    job_vec = embedding_df.loc[job_id].values

    # Gabungkan embedding: concat + multiply + abs diff
    concat = np.concatenate([applicant_vec, job_vec])
    mul = applicant_vec * job_vec
    abs_diff = np.abs(applicant_vec - job_vec)
    combined_vec = np.concatenate([concat, mul, abs_diff]).reshape(1, -1)

    # === Buat training set ===
    labels_df = pd.read_csv("../data/DummyData/labels.csv")
    X_train_list = []
    y_train_list = []

    for _, row in labels_df.iterrows():
        a, j, l = str(row['applicant']), str(row['job']), row['accepted']
        if a in embedding_df.index and j in embedding_df.index:
            av = embedding_df.loc[a].values
            jv = embedding_df.loc[j].values
            c = np.concatenate([av, jv])
            m = av * jv
            d = np.abs(av - jv)
            X_train_list.append(np.concatenate([c, m, d]))
            y_train_list.append(l)

    X_train_full = np.array(X_train_list)
    y_train_full = np.array(y_train_list)

    # Fit SVD di training set
    svd = TruncatedSVD(n_components=64, random_state=42)
    X_train_reduced = svd.fit_transform(X_train_full)

    # Transform test vector
    combined_vec_reduced = svd.transform(combined_vec)

    # Latih model
    model = LinearRegression()
    model.fit(X_train_reduced, y_train_full)

    # Prediksi
    prediction_prob = model.predict(combined_vec_reduced)[0]
    prediction_class = 1 if prediction_prob >= 0.5 else 0

    print(f"📌 Prediction Probability: {prediction_prob:.4f}")
    print(f"✅ Predicted Class (Accepted?): {prediction_class} (1=Accepted, 0=Rejected)")
else:
    print("❌ ID applicant atau job tidak ditemukan di embedding.")
