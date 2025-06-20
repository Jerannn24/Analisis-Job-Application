Berikut adalah contoh isi `README.md` yang rapi dan informatif untuk repositori proyek prediksi penerimaan kerja berbasis **Node2Vec** dan **Logistic Regression**:

---

```markdown
# 🧠 Job Application Success Prediction using Node2Vec and Logistic Regression

This project aims to predict the success of job applications in an online recruitment setting by modeling the relationships between applicants, job posts, skills, and supporting attributes using a graph-based approach. Node2Vec is used to embed graph nodes into vector representations, which are then fed into a logistic regression classifier for prediction.

---

## 📁 Project Structure

```

.
├── data/
│   ├── nodes.csv
│   ├── edges.csv
│   └── labels.csv
├── Node2Vec/
│   ├── node2vec\_embedding.py
│   └── PredictionTest.py
├── classification\_report\_logreg\_nosmote.csv
├── README.md

````

---

## 📊 Dataset Description

- `nodes.csv` : Contains graph nodes (e.g., applicants, jobs, skills).
- `edges.csv` : Contains edges (e.g., applicant-has-skill, job-requires-skill).
- `labels.csv`: Pairs of (applicant, job) with labels `1` (accepted) or `0` (rejected).

---

## 🔧 How It Works

1. **Graph Construction**  
   A graph is created from the dataset connecting applicants, jobs, and skills.

2. **Node Embedding with Node2Vec**  
   Node2Vec is applied to convert graph nodes into dense vector representations.

3. **Feature Combination**  
   For each applicant-job pair, their embeddings are combined (concat + multiply + absolute difference).

4. **Dimensionality Reduction (Optional)**  
   Truncated SVD can be used to reduce feature dimensions.

5. **Prediction with Logistic Regression**  
   A logistic regression model is trained using labeled data and used for prediction.

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
````

Minimal packages used:

* `pandas`
* `numpy`
* `scikit-learn`
* `networkx`
* `node2vec`

---

## ▶️ Run the Project

### Step 1: Generate Embeddings

```bash
python Node2Vec/node2vec_embedding.py
```

### Step 2: Run Prediction Test

Edit `PredictionTest.py` to set the applicant/job ID you want to test, then run:

```bash
python Node2Vec/PredictionTest.py
```

---

## 📈 Example Output

```txt
📌 Prediction Probability: 0.6447
✅ Predicted Class (Accepted?): 1 (Accepted)
```

---

## 📹 Demonstration Video & Source Code

* 🔗 [GitHub Repository](https://github.com/Jerannn24/Analisis-Job-Application)
* 📺 YouTube Explanation:[ (insert your link here)](https://youtu.be/OTkdQPCt3IU)

---

## 🤝 Acknowledgements

This project was developed for the final assignment of **Discrete Mathematics (IF1220)** at Institut Teknologi Bandung. Special thanks to **Dr. Ir. Rinaldi, M.T.**, and all contributors.

---

## 📌 License

This project is for academic and educational purposes only.

```
