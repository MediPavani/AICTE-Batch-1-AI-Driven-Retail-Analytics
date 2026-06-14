import pandas as pd
import random
from datetime import datetime, timedelta

# Load items file
items = pd.read_csv("items.csv")

customers = list(range(1, 101))   # 100 customers
transactions = []

transaction_id = 10001
start_date = datetime(2024, 1, 1)

for _ in range(1200):  # 1200 transactions
    customer_id = random.choice(customers)
    
    # Random date & time
    days_offset = random.randint(0, 30)
    time_slot = random.choice(["morning", "afternoon", "evening"])
    
    if time_slot == "morning":
        hour = random.randint(7, 10)
    elif time_slot == "afternoon":
        hour = random.randint(12, 15)
    else:
        hour = random.randint(17, 21)
        
    timestamp = start_date + timedelta(days=days_offset, hours=hour)
    
    # Items per transaction
    num_items = random.randint(2, 6)
    selected_items = items.sample(num_items)
    
    for _, row in selected_items.iterrows():
        transactions.append([
            transaction_id,
            customer_id,
            timestamp.strftime("%Y-%m-%d %H:%M"),
            row["item_name"],
            random.randint(1, 3)
        ])
    
    transaction_id += 1

# Create DataFrame
transactions_df = pd.DataFrame(
    transactions,
    columns=["TransactionID", "CustomerID", "Timestamp", "item_name", "quantity"]
)

# Save CSV
transactions_df.to_csv("transactions.csv", index=False)

print("✅ 1200+ transactions generated successfully!")
