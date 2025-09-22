# Retail-Inventory-Order-Management-System-Core-Python-
# Retail-Inventory-Order-Management-System-Core-Python-
Retail Inventory & Order Management System

A core Python CLI project for managing products, customers, orders, payments, and generating reports using Supabase as the backend.

Features

Product Management

Add, update, delete, list, and restock products

Customer Management

Add, update, delete, search, and list customers

Order Management

Create, cancel, complete orders

List orders by customer

Payment Management

Process payments

Refund orders

Reporting

Top-selling products

Total revenue last month

Total orders by customer

Frequent customers

Setup

Clone the repository

git clone https://github.com/yourusername/Retail-Inventory-Order-Management-System-Core-Python.git
cd Retail-Inventory-Order-Management-System-Core-Python


Install dependencies

pip install -r requirements.txt


Configure Supabase

Create a .env file in the root folder:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key


Create tables in Supabase

Tables: products, customers, orders, order_items, payments

Make sure column names match the DAO queries in reporting_dao.py and services.

CLI Commands
Product
python -m src.cli.main product add --name "Laptop" --sku LAP123 --price 50000 --stock 10 --category Electronics
python -m src.cli.main product list
python -m src.cli.main product update --prod_id 1 --price 45000
python -m src.cli.main product delete --prod_id 1
python -m src.cli.main product restock --prod_id 1 --delta 5

Customer
python -m src.cli.main customer add --name "Rahul" --email rahul@example.com --phone 9999999999 --city Delhi
python -m src.cli.main customer list
python -m src.cli.main customer update --email rahul@example.com --city Mumbai
python -m src.cli.main customer delete --email rahul@example.com
python -m src.cli.main customer search --city Delhi

Order
python -m src.cli.main order create --customer 1 --item 1:2 2:1
python -m src.cli.main order show --order 1
python -m src.cli.main order cancel --order 1
python -m src.cli.main order complete --order 1
python -m src.cli.main order list-customer --customer 1

Payment
python -m src.cli.main payment process --order 1 --method Card
python -m src.cli.main payment refund --order 1

Reporting
python -m src.cli.main report top-products --top 5
python -m src.cli.main report revenue
python -m src.cli.main report orders-by-customer
python -m src.cli.main report frequent-customers --min 2

Based on the screenshot you provided, here is a directory structure that you can use for your `README.md` file.

```
RETAIL-INVENTORY-ORDER-MANAGEMENT-SYSTEM-Core-Python/
├─── src/
│   ├─── __pycache__/
│   ├─── cli/
│   │   └─── main.py
│   ├─── dao/
│   │   ├─── customer_dao.py
│   │   ├─── order_dao.py
│   │   ├─── payment_dao.py
│   │   ├─── product_dao.py
│   │   └─── reporting_dao.py
│   ├─── main.py
│   └─── services/
│       ├─── customer_service.py
│       ├─── order_service.py
│       ├─── payment_service.py
│       ├─── product_service.py
│       └─── reporting_service.py
├─── .env
├─── .gitignore
├─── README.md
└─── config.py

```
