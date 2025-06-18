import pandas as pd

# Load data
df = pd.read_csv("labels.csv")

# Hitung jumlah masing-masing tipe node
type_counts = df['accepted'].value_counts()
print(type_counts)
