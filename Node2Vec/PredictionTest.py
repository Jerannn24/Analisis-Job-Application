import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# === Load embedding yang telah dibuat ===
embedding_df = pd.read_csv("../data/DummyData/node_embedding.csv")
embedding_df.set_index(embedding_df.columns[0], inplace=True)

# === Contoh Applicant dan Job yang ingin diuji ===
applicant_id = "Nina aditya"   # Ganti dengan ID yang sesuai
job_id = "job_8"              # Ganti dengan ID yang sesuai

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

    # Latih model langsung tanpa reduksi dimensi
    model = LinearRegression()
    model.fit(X_train_full, y_train_full)

    # Prediksi
    prediction_prob = model.predict(combined_vec)[0]
    prediction_class = 1 if prediction_prob >= 0.5 else 0

    print(f"📌 Prediction Probability: {prediction_prob:.4f}")
    print(f"✅ Predicted Class (Accepted?): {prediction_class} (1=Accepted, 0=Rejected)")

else:
    print("❌ ID applicant atau job tidak ditemukan di embedding.")
