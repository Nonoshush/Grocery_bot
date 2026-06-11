import re
import streamlit as st
import sqlite3
from datetime import datetime

# Improvements
#   - leave the store or clear the basket on sending the order
#   - and maybe make order Id's and ofcourse user Id's
#   - also maybe make the database online instead of on here

st.image("isle1.jpg", caption="Get your stuff here in Isle 1", width=700, clamp=True)

st.title("Welcome to the Grocery Store")

# database setup
db = sqlite3.connect("orders.db", check_same_thread=False)
cursor = db.cursor()
#automatically creates  db.commit() first time app runs
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    name TEXT,
    item TEXT,
    quantity INTEGER,
    price_each INTEGER,
    item_total INTEGER,
    order_total INTEGER
)
""")

db.commit()

# session state setup
if "started" not in st.session_state:
    st.session_state.started = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "basket" not in st.session_state:
    st.session_state.basket = {}

if "total" not in st.session_state:
    st.session_state.total = 0

def leave_store():
    st.session_state.started = False
    st.session_state.name = ""
    st.session_state.basket.clear()
    st.session_state.total = 0
    st.rerun()


# name input (Here we will ignore all the caps, symbols and numbers in the name)
if st.session_state.started == False:
    name = st.text_input("First of all, type your name:")

    if st.button("Start Shopping"):
        cleaned_name = name.lower()
        cleaned_name = re.sub(r'[^a-z\s]', '', cleaned_name)

        if cleaned_name.strip() == "":
            st.warning("Please type a valid name.")
        else:
            st.session_state.name = cleaned_name
            st.session_state.started = True
            st.rerun()

else:
    st.write("Hello", st.session_state.name)

    # Sections and items
    sections = {
        "Snacks": {
            "Chips": 150,
            "Chocolate Bar": 120,
            "Cookies": 200
        },
        "Fruits": {
            "Apple": 100,
            "Banana": 80,
            "Grapes": 250
        },
        "Veggies": {
            "Carrot": 60,
            "Tomato": 90,
            "Cucumber": 70
        }
    }

    # send order to database
    def send_order_to_database():

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item, qty in st.session_state.basket.items():

            price = 0

            # find price from sections
            for sec_items in sections.values():
                if item in sec_items:
                    price = sec_items[item]

            cursor.execute("""
            INSERT INTO orders (
                timestamp,
                name,
                item,
                quantity,
                price_each,
                item_total,
                order_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                st.session_state.name,
                item,
                qty,
                price,
                price * qty,
                st.session_state.total
            ))

        db.commit()

    # display items with buttons
    for section, items in sections.items():
        st.write(section)

        for item, price in items.items():
            if st.button(f"{item} - ¥{price}"):
                if item in st.session_state.basket:
                    st.session_state.basket[item] += 1
                else:
                    st.session_state.basket[item] = 1

                st.session_state.total += price

    # display basket
    st.write("Your basket:")

    if st.session_state.basket:
        for item, qty in st.session_state.basket.items():

            price = 0

            # find price from sections
            for sec_items in sections.values():
                if item in sec_items:
                    price = sec_items[item]

            st.write(f"{item}: {qty} pcs (¥{price} each, ¥{price * qty} total)")

        st.write("Total amount: ¥", st.session_state.total)

    else:
        st.write("Your basket is empty.")

# clear basket, send order and leave buttons
col1, col2, col3 = st.columns(3)


with col1:
    if st.button("Clear Basket"):
        st.session_state.basket.clear()
        st.session_state.total = 0
        st.rerun()

with col2:
    if st.button("SEND ORDER"):
        if not st.session_state.basket:
            st.warning("Your basket is empty.")
        else:
            send_order_to_database()

            st.success("Order sent successfully!")

            st.session_state.basket.clear()
            st.session_state.total = 0

with col3:
    if st.button("Leave Store"):
        leave_store()

    # # show saved orders
    # if st.button("Show Orders"):
    #     orders = cursor.execute("""
    #     SELECT timestamp, name, item, quantity, price_each, item_total, order_total
    #     FROM orders
    #     """).fetchall()

    #     st.write("Saved orders:")
    #     st.write(orders)

# python -m streamlit run grocery_bot.py