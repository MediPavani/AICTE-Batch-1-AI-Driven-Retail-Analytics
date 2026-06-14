from mlxtend.frequent_patterns import apriori, association_rules

def get_association_rules(selected_items, df_transactions, min_support=0.01, min_confidence=0.2):
    basket = df_transactions.groupby(['CustomerID', 'item_name'])['item_name'].count().unstack().fillna(0)
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    
    recommended = rules[rules['antecedents'].apply(lambda x: selected_items[0] in x)]['consequents']
    return [list(x)[0] for x in recommended] if not recommended.empty else []
