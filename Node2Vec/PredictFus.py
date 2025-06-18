import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD

# === Load embeddings ===
embedding_df = pd.read_csv("../data/DummyData/node_embedding.csv")
embedding_df.set_index(embedding_df.columns[0], inplace=True)

# === Load labels ===
labels_df = pd.read_csv("../data/DummyData/labels.csv")

# === Siapkan fitur dan label ===
X, y = [], []

for _, row in labels_df.iterrows():
    applicant = str(row['applicant'])
    job = str(row['job'])
    label = row['accepted']

    if applicant in embedding_df.index and job in embedding_df.index:
        applicant_vec = embedding_df.loc[applicant].values
        job_vec = embedding_df.loc[job].values

        concat = np.concatenate([applicant_vec, job_vec])
        mul = applicant_vec * job_vec
        abs_diff = np.abs(applicant_vec - job_vec)

        combined_vec = np.concatenate([concat, mul, abs_diff])
        X.append(combined_vec)
        y.append(label)

X = np.array(X)
y = np.array(y)

# === SVD untuk reduksi dimensi ===
svd = TruncatedSVD(n_components=64, random_state=42)
X_svd = svd.fit_transform(X)

# === Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(
    X_svd, y, test_size=0.2, random_state=42, stratify=y
)

# === Linear Regression ===
model = LinearRegression()
model.fit(X_train, y_train)

# === Prediksi dan threshold ===
y_pred_continuous = model.predict(X_test)
y_pred = (y_pred_continuous >= 0.5).astype(int)

# === Evaluasi ===
report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()
report_df.to_csv("classification_report_linreg.csv", index=True)

print("✅ Classification report disimpan ke classification_report_linreg.csv")
