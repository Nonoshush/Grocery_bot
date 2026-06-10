# Grocery Store App
This is a simple grocery store application made with Streamlit for a school assignment.

The user can:
* Enter their name
* Add products to a basket
* See the total price
* Clear the basket
* Send an order
* Leave the store so another customer can use the application

Orders are saved in a SQLite database (`orders.db`) together with the customer's name, order details, total price, and timestamp.

## How to run
Install Streamlit:
```bash
pip install streamlit
```
Run the application:
```bash
py -m streamlit run grocery_bot.py
```

or

```bash
python -m streamlit run grocery_bot.py
```

Made by Badr.
