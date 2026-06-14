
from chatbot.intent_recognition import parse_query

def chatbot_response(query, items_df):
    intent = parse_query(query)

    # =====================================
    # OPTION 1: PRODUCT AVAILABILITY
    # =====================================
    if intent['type'] == 'availability':

        response = []
        alternatives = []

        for item in intent['items']:
            row = items_df[items_df['item_name'].str.lower() == item.lower()]

            if not row.empty:
                response.append(f"✅ {item} is available")
            else:
                response.append(f"❌ {item} is not available")

        return " | ".join(response)

    # =====================================
    # OPTION 2: BUDGET + REQUIRED ITEMS
    # =====================================
    elif intent['type'] == 'budget':

        budget = intent['budget']
        required_items = intent['items']

        purchased_items = []
        alternatives = []
        total_cost = 0

        for item in required_items:
            row = items_df[items_df['item_name'].str.lower() == item.lower()]

            if not row.empty:
                price = row.iloc[0]['price']

                if total_cost + price <= budget:
                    total_cost += price
                    purchased_items.append(item)
                else:
                    # Find cheaper alternative in same category
                    category = row.iloc[0]['category']
                    cheaper = items_df[
                        (items_df['category'] == category) &
                        (items_df['price'] < price)
                    ]

                    alternatives.extend(cheaper['item_name'].tolist())

        response = ""

        if purchased_items:
            response += (
                f"Items you can buy within ₹{budget}: "
                f"{', '.join(purchased_items)} (Total: ₹{total_cost}). "
            )

        if alternatives:
            response += (
                f"Cheaper alternatives suggested: "
                f"{', '.join(set(alternatives))}"
            )

        if not purchased_items and not alternatives:
            response = "Budget is too low for the selected items."

        return response

    # =====================================
    # DEFAULT
    # =====================================
    return (
        "I can help with:\n"
        "1️⃣ Checking product availability\n"
        "2️⃣ Suggesting items within your budget"
    )
