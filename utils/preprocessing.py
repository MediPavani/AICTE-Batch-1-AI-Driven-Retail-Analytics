import pandas as pd

def preprocess_transactions(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['TimeOfDay'] = pd.cut(
        df['Timestamp'].dt.hour,
        bins=[-1, 11, 17, 23],
        labels=['Morning', 'Afternoon', 'Evening']
    )
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    return df

def categorize_transactions(transactions_df, items_df):
    """
    Add category information to each transaction by joining with items.csv
    """
    categorized_df = transactions_df.merge(
        items_df[['item_name', 'category']],
        on='item_name',
        how='left'
    )
    return categorized_df