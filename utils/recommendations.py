import pandas as pd

def get_related_items(selected_items, customer_id, time_of_day, transactions_df, items_df, top_n=10):
    """
    Recommend items strictly from the same category as the selected items.
    Ignores unrelated co-occurrence from mixed baskets.
    """

    related_items = []
    for item in selected_items:
        # Find category of selected item
        item_row = items_df[items_df['item_name'].str.lower() == item.lower()]
        if item_row.empty:
            continue
        category = item_row.iloc[0]['category']

        # Get items in same category
        same_category_items = items_df[items_df['category'] == category]['item_name'].tolist()
        same_category_items = [i for i in same_category_items if i.lower() != item.lower()]

        # Add to recommendations
        related_items.extend(same_category_items)

    # Deduplicate and limit
    related_items = list(dict.fromkeys(related_items))[:top_n]
    return related_items