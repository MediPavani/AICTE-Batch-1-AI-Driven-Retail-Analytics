# import streamlit as st
# import pandas as pd
# from utils.recommendations import get_related_items
# from chatbot.chatbot_model import chatbot_response

# # Load datasets
# transactions = pd.read_csv("data/transactions.csv")
# items = pd.read_csv("data/items.csv")

# st.set_page_config(page_title="Smart Retail Recommendation Engine", layout="wide")
# st.title("🛒 Smart Retail Recommendation Engine")

# # -------------------------------
# # Step 1: New User or Existing User
# # -------------------------------
# user_type = st.radio("Select User Type:", ["New User", "Select ID"])
# time_of_day = st.selectbox("Select Time of Day", ["Morning", "Afternoon", "Evening", "Night"])

# # -------------------------------
# # NEW USER
# # -------------------------------
# if user_type == "New User":
#     st.subheader("👋 Welcome New Customer!")
#     st.write("Select the items you are planning to buy:")

#     # Show all items as multiselect
#     selected_items = st.multiselect("Choose items you want to buy:", items["item_name"].tolist())

#     if st.button("Get Related Recommendations (New Customer)"):
#         if selected_items:
#             related_items = get_related_items(
#                 selected_items,
#                 customer_id=-1,
#                 time_of_day=time_of_day,
#                 transactions_df=transactions,
#                 items_df=items
#             )
#             st.markdown("### Recommendations Based on Your Selection")
#             for item in related_items:
#                 item_info = items[items["item_name"] == item]
#                 if not item_info.empty:
#                     item_info = item_info.iloc[0]
#                     st.markdown(f"""
#                     <div style='border:2px solid #4CAF50; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f0fff0'>
#                     <h4>{item_info['item_name']}</h4>
#                     <p>Category: {item_info['category']} | Price: ₹{item_info['price']} | Available: {item_info['packets_available']}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
#         else:
#             st.warning("Select at least one item to get recommendations!")

# # -------------------------------
# # EXISTING USER
# # -------------------------------
# else:
#     existing_customers = transactions["CustomerID"].unique().tolist()
#     customer_id = st.selectbox("Select Customer ID:", options=existing_customers)

#     # Filter transactions for this customer and time of day
#     df = transactions.copy()
#     df["time_of_day"] = pd.to_datetime(df["Timestamp"]).dt.hour.apply(
#         lambda x: "Morning" if 5 <= x <= 11 else (
#             "Afternoon" if 12 <= x <= 16 else (
#                 "Evening" if 17 <= x <= 21 else "Night"
#             )
#         )
#     )

#     user_items = df[(df["CustomerID"] == customer_id) & (df["time_of_day"] == time_of_day)]["item_name"].unique().tolist()

#     if user_items:
#         st.subheader(f"Select items bought by Customer {customer_id} in {time_of_day}:")
#         selected_items = st.multiselect("Choose items for recommendations:", user_items)

#         if st.button("Get Related Recommendations"):
#             if selected_items:
#                 related_items = get_related_items(
#                     selected_items,
#                     customer_id,
#                     time_of_day,
#                     transactions_df=transactions,
#                     items_df=items
#                 )
#                 st.markdown("### Recommendations Based on Your Selection")
#                 for item in related_items:
#                     item_info = items[items["item_name"] == item]
#                     if not item_info.empty:
#                         item_info = item_info.iloc[0]
#                         st.markdown(f"""
#                         <div style='border:2px solid #4CAF50; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f0fff0'>
#                         <h4>{item_info['item_name']}</h4>
#                         <p>Category: {item_info['category']} | Price: ₹{item_info['price']} | Available: {item_info['packets_available']}</p>
#                         </div>
#                         """, unsafe_allow_html=True)
#             else:
#                 st.warning("Select at least one item to get recommendations!")
#     else:
#         st.info("No transactions found for this customer at this time.")

# # -------------------------------
# # Chatbot Section
# # -------------------------------
# st.header("💬 Store Chatbot")
# user_query = st.text_input("Ask about item availability or budget:")

# if st.button("Ask Bot"):
#     response = chatbot_response(user_query, items)
#     st.info(response)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.recommendations import get_related_items
from chatbot.chatbot_model import chatbot_response

# Load datasets
transactions = pd.read_csv("data/transactions.csv")
items = pd.read_csv("data/items.csv")

st.set_page_config(page_title="Smart Retail Recommendation Engine", layout="wide")
st.title("🛒 Smart Retail Recommendation Engine")

# -------------------------------
# User Type Selection
# -------------------------------
user_type = st.radio("Select User Type:", ["New User", "Select ID"])
time_of_day = st.selectbox("Select Time of Day", ["Morning", "Afternoon", "Evening", "Night"])


# -------------------------------
# Function to Display Recommendations + Compact Graphs
# -------------------------------
def display_recommendations(related_items):
    if not related_items:
        st.warning("No recommendations found!")
        return

    st.markdown("## 🛍 Recommended Items")

    rec_df = items[items["item_name"].isin(related_items)]

    # -------------------------------
    # Display Item Cards
    # -------------------------------
    for _, item_info in rec_df.iterrows():
        st.markdown(f"""
        <div style='border:1px solid #4CAF50; padding:8px; border-radius:8px; margin-bottom:8px; background-color:#f9fff9'>
        <h5>{item_info['item_name']}</h5>
        <p style='font-size:12px;'>Category: {item_info['category']} | Price: ₹{item_info['price']} | Stock: {item_info['packets_available']}</p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------
    # Compact Charts Side-by-Side
    # -------------------------------
    col1, col2 = st.columns(2)

    # 💰 Price Chart (Small)
    with col1:
        st.markdown("#### 💰 Price Comparison")
        fig1, ax1 = plt.subplots(figsize=(4,2.5))
        ax1.bar(rec_df["item_name"], rec_df["price"])
        ax1.tick_params(axis='x', rotation=45, labelsize=7)
        ax1.tick_params(axis='y', labelsize=7)
        ax1.set_ylabel("Price (₹)", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig1)

    # 📦 Stock Chart (Small)
    with col2:
        st.markdown("#### 📦 Stock Availability")
        fig2, ax2 = plt.subplots(figsize=(4,2.5))
        ax2.bar(rec_df["item_name"], rec_df["packets_available"])
        ax2.tick_params(axis='x', rotation=45, labelsize=7)
        ax2.tick_params(axis='y', labelsize=7)
        ax2.set_ylabel("Stock", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig2)

    # -------------------------------
    # Very Small Centered Pie Chart
    # -------------------------------
    st.markdown("#### 📂 Category Distribution")

    center_col = st.columns([1,2,1])[1]  # center alignment

    with center_col:
        fig3, ax3 = plt.subplots(figsize=(3,3))
        category_counts = rec_df["category"].value_counts()
        ax3.pie(
            category_counts,
            labels=category_counts.index,
            autopct='%1.1f%%',
            textprops={'fontsize':6}
        )
        plt.tight_layout()
        st.pyplot(fig3)


# -------------------------------
# NEW USER
# -------------------------------
if user_type == "New User":
    st.subheader("👋 Welcome New Customer!")
    selected_items = st.multiselect(
        "Choose items you want to buy:",
        items["item_name"].tolist()
    )

    if st.button("Get Related Recommendations (New Customer)"):
        if selected_items:
            related_items = get_related_items(
                selected_items,
                customer_id=-1,
                time_of_day=time_of_day,
                transactions_df=transactions,
                items_df=items
            )
            display_recommendations(related_items)
        else:
            st.warning("Select at least one item to get recommendations!")


# -------------------------------
# EXISTING USER
# -------------------------------
else:
    existing_customers = transactions["CustomerID"].unique().tolist()
    customer_id = st.selectbox("Select Customer ID:", options=existing_customers)

    df = transactions.copy()
    df["time_of_day"] = pd.to_datetime(df["Timestamp"]).dt.hour.apply(
        lambda x: "Morning" if 5 <= x <= 11 else (
            "Afternoon" if 12 <= x <= 16 else (
                "Evening" if 17 <= x <= 21 else "Night"
            )
        )
    )

    user_items = df[
        (df["CustomerID"] == customer_id) &
        (df["time_of_day"] == time_of_day)
    ]["item_name"].unique().tolist()

    if user_items:
        st.subheader(f"Select items bought by Customer {customer_id} in {time_of_day}:")
        selected_items = st.multiselect(
            "Choose items for recommendations:",
            user_items
        )

        if st.button("Get Related Recommendations"):
            if selected_items:
                related_items = get_related_items(
                    selected_items,
                    customer_id,
                    time_of_day,
                    transactions_df=transactions,
                    items_df=items
                )
                display_recommendations(related_items)
            else:
                st.warning("Select at least one item to get recommendations!")
    else:
        st.info("No transactions found for this customer at this time.")


# -------------------------------
# Chatbot Section
# -------------------------------
st.header("💬 Store Chatbot")
user_query = st.text_input("Ask about item availability or budget:")

if st.button("Ask Bot"):
    response = chatbot_response(user_query, items)
    st.info(response)