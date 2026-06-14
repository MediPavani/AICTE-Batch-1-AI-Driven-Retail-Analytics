import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors

transactions = pd.read_csv("data/transactions.csv")
# preprocess transactions and generate customer-item matrix
basket = transactions.pivot_table(index='CustomerID', columns='item_name', aggfunc='size', fill_value=0)
model = NearestNeighbors(n_neighbors=5, metric='cosine').fit(basket)

# Save model
with open("models/personalized_model.pkl", "wb") as f:
    pickle.dump(model, f)
