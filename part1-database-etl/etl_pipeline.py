#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FlexiMart ETL Pipeline (MySQL)
- Extract: Read CSVs
- Transform: Clean, deduplicate, standardize, impute
- Load: Insert into MySQL with AUTO_INCREMENT surrogate keys
- Report: Write data_quality_report.txt with required counts
"""

import os
import sys
import logging
import re
from datetime import datetime
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine, text

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ---------------------------
# Files (place in project root)
# ---------------------------
CUSTOMERS_CSV = "customers_raw.csv"
PRODUCTS_CSV = "products_raw.csv"
SALES_CSV = "sales_raw.csv"
REPORT_FILE = "data_quality_report.txt"

# ---------------------------
# Category normalization
# ---------------------------
CATEGORY_MAP = {"electronics": "Electronics", "fashion": "Fashion", "groceries": "Groceries"}

# ---------------------------
# Utility functions
# ---------------------------

def standardize_phone(phone: str) -> str:
    """Standardize Indian phone numbers to +91-XXXXXXXXXX. Unparseable -> None."""
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    # Strip country/trunk prefixes if present; keep last 10 if longer
    if len(digits) > 10:
        digits = digits[-10:]
    if len(digits) != 10:
        return None
    return f"+91-{digits}"

def parse_date(date_str) -> pd.Timestamp:
    """Parse mixed date formats to Timestamp. Try US-first then day-first."""
    if pd.isna(date_str):
        return pd.NaT
    s = str(date_str).strip()
    ts = pd.to_datetime(s, errors="coerce", dayfirst=False)
    if pd.isna(ts):
        ts = pd.to_datetime(s, errors="coerce", dayfirst=True)
    return ts

def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Trim spaces and convert empty strings to NA on all object columns."""
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({"": pd.NA})
    return df

# ---------------------------
# Metrics helper
# ---------------------------

def init_metrics() -> Dict[str, int]:
    return {
        "customers_processed": 0,
        "customers_duplicates_removed": 0,
        "customers_missing_email_dropped": 0,
        "customers_phones_null": 0,
        "customers_dates_parsed": 0,
        "customers_loaded": 0,

        "products_processed": 0,
        "products_duplicates_removed": 0,
        "products_categories_standardized": 0,
        "products_missing_stock_filled": 0,
        "products_missing_prices_imputed": 0,
        "products_loaded": 0,

        "sales_processed": 0,
        "sales_duplicates_removed": 0,
        "sales_missing_ids_dropped": 0,
        "sales_dates_parsed": 0,
        "orders_loaded": 0,
        "order_items_loaded": 0
    }

# ---------------------------
# Extract
# ---------------------------

def extract():
    logging.info("Extracting CSVs...")
    customers = pd.read_csv(CUSTOMERS_CSV)
    products = pd.read_csv(PRODUCTS_CSV)
    sales = pd.read_csv(SALES_CSV)
    return customers, products, sales

# ---------------------------
# Transform: Customers
# ---------------------------

def transform_customers(df: pd.DataFrame, m: Dict[str, int]) -> pd.DataFrame:
    m["customers_processed"] = len(df)
    df = strip_strings(df)

    before = len(df)
    df = df.drop_duplicates(subset=["customer_id", "email"])
    m["customers_duplicates_removed"] = before - len(df)

    before = len(df)
    df = df.dropna(subset=["email"])
    m["customers_missing_email_dropped"] = before - len(df)

    df["phone"] = df["phone"].apply(standardize_phone)
    m["customers_phones_null"] = df["phone"].isna().sum()

    df["city"] = df["city"].astype(str).str.title()

    df["registration_date"] = df["registration_date"].apply(parse_date)
    m["customers_dates_parsed"] = df["registration_date"].notna().sum()

    tidy = df[["first_name", "last_name", "email", "phone", "city", "registration_date"]].copy()
    logging.info("Transformed customers: %d rows", len(tidy))
    return tidy

# ---------------------------
# Transform: Products
# ---------------------------

def transform_products(df: pd.DataFrame, m: Dict[str, int]) -> pd.DataFrame:
    m["products_processed"] = len(df)
    df = strip_strings(df)

    before = len(df)
    df = df.drop_duplicates(subset=["product_id", "product_name"])
    m["products_duplicates_removed"] = before - len(df)

    df["category"] = df["category"].apply(lambda x: CATEGORY_MAP.get(str(x).lower(), None))
    m["products_categories_standardized"] = df["category"].notna().sum()

    df["stock_quantity"] = pd.to_numeric(df["stock_quantity"], errors="coerce")
    missing_stock = df["stock_quantity"].isna().sum()
    df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)
    m["products_missing_stock_filled"] = missing_stock

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    medians = df.dropna(subset=["category"]).groupby("category")["price"].median()
    overall = df["price"].median()

    before_null = df["price"].isna().sum()
    df["price"] = df.apply(
        lambda r: r["price"]
        if pd.notna(r["price"])
        else medians.get(r["category"], overall),
        axis=1
    )
    after_null = df["price"].isna().sum()
    m["products_missing_prices_imputed"] = before_null - after_null

    df = df.dropna(subset=["category", "price"])

    tidy = df[["product_name", "category", "price", "stock_quantity"]].copy()
    logging.info("Transformed products: %d rows", len(tidy))
    return tidy

# ---------------------------
# Transform: Sales -> Orders + Order Items
# ---------------------------

def transform_sales(df: pd.DataFrame, m: Dict[str, int]):
    m["sales_processed"] = len(df)
    df = strip_strings(df)

    before = len(df)
    df = df.drop_duplicates(subset=["transaction_id"])
    m["sales_duplicates_removed"] = before - len(df)

    before = len(df)
    df = df.dropna(subset=["customer_id", "product_id"])
    m["sales_missing_ids_dropped"] = before - len(df)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["quantity", "unit_price"])
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] >= 0]

    df["transaction_date"] = df["transaction_date"].apply(parse_date)
    m["sales_dates_parsed"] = df["transaction_date"].notna().sum()
    df = df.dropna(subset=["transaction_date"])

    df["subtotal"] = df["quantity"] * df["unit_price"]

    orders = df[["customer_id", "transaction_date", "subtotal", "status", "transaction_id"]].copy()
    orders.rename(columns={
        "transaction_date": "order_date",
        "subtotal": "total_amount"
    }, inplace=True)

    items = df[["transaction_id", "product_id", "quantity", "unit_price", "subtotal"]].copy()
    items.rename(columns={
        "transaction_id": "external_order_key",
        "product_id": "external_product_key"
    }, inplace=True)

    logging.info("Transformed sales: orders=%d, items=%d", len(orders), len(items))
    return orders, items

# ---------------------------
# Load to MySQL
# ---------------------------

def ensure_schema(engine):
    """Create tables if not exist, per provided MySQL schema."""
    schema_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        city VARCHAR(50),
        registration_date DATE
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY AUTO_INCREMENT,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INT DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT NOT NULL,
        order_date DATE NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending',
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INT PRIMARY KEY AUTO_INCREMENT,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        unit_price DECIMAL(10,2) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """
    with engine.begin() as conn:
        for stmt in [s for s in schema_sql.split(";") if s.strip()]:
            conn.execute(text(stmt + ";"))

def load_mysql(engine, customers, products, orders, items, m: Dict[str, int]):
    """Insert cleaned data into MySQL with upserts and key resolution."""
    with engine.begin() as conn:
        # Upsert customers by unique email
        for _, r in customers.iterrows():
            conn.execute(text("""
                INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                VALUES (:fn, :ln, :em, :ph, :ct, :rd)
                ON DUPLICATE KEY UPDATE
                    phone = VALUES(phone),
                    city = VALUES(city),
                    registration_date = VALUES(registration_date)
            """), {
                "fn": r["first_name"],
                "ln": r["last_name"],
                "em": r["email"],
                "ph": r["phone"],
                "ct": r["city"],
                "rd": None if pd.isna(r["registration_date"]) else r["registration_date"].date()
            })
            m["customers_loaded"] += 1

        # Build external customer mapping (Cxxx -> surrogate id) via email lookup
        raw_customers = pd.read_csv(CUSTOMERS_CSV).dropna(subset=["email"]).drop_duplicates(subset=["customer_id", "email"])
        cust_map = {}
        for _, rc in raw_customers.iterrows():
            row = conn.execute(text("SELECT customer_id FROM customers WHERE email = :em"), {"em": rc["email"]}).fetchone()
            if row:
                cust_map[str(rc["customer_id"]).strip()] = int(row[0])

        # Upsert products by product_name
        for _, r in products.iterrows():
            conn.execute(text("""
                INSERT INTO products (product_name, category, price, stock_quantity)
                VALUES (:pn, :cat, :pr, :sq)
                ON DUPLICATE KEY UPDATE
                    category = VALUES(category),
                    price = VALUES(price),
                    stock_quantity = VALUES(stock_quantity)
            """), {
                "pn": r["product_name"],
                "cat": r["category"],
                "pr": float(r["price"]),
                "sq": int(r["stock_quantity"])
            })
            m["products_loaded"] += 1

        # Map external product codes (Pxxx -> surrogate id) via product_name
        raw_products = pd.read_csv(PRODUCTS_CSV).drop_duplicates(subset=["product_id", "product_name"])
        prod_map = {}
        for _, rp in raw_products.iterrows():
            row = conn.execute(text("SELECT product_id FROM products WHERE product_name = :pn"), {"pn": rp["product_name"]}).fetchone()
            if row:
                prod_map[str(rp["product_id"]).strip()] = int(row[0])

        # Insert orders and order_items
        order_map = {}
        for _, r in orders.iterrows():
            ext_cid = str(r["customer_id"]).strip()
            cust_id = cust_map.get(ext_cid)
            if not cust_id:
                continue
            conn.execute(text("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (:cid, :od, :ta, :st)
            """), {
                "cid": cust_id,
                "od": r["order_date"].date(),
                "ta": float(r["total_amount"]),
                "st": str(r["status"]) if not pd.isna(r["status"]) else "Pending"
            })
            order_id = conn.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
            order_map[str(r["transaction_id"]).strip()] = int(order_id)
            m["orders_loaded"] += 1

        for _, r in items.iterrows():
            order_id = order_map.get(str(r["external_order_key"]).strip())
            product_id = prod_map.get(str(r["external_product_key"]).strip())
            if not order_id or not product_id:
                continue
            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (:oid, :pid, :qty, :up, :sub)
            """), {
                "oid": order_id,
                "pid": product_id,
                "qty": int(r["quantity"]),
                "up": float(r["unit_price"]),
                "sub": float(r["subtotal"])
            })
            m["order_items_loaded"] += 1

# ---------------------------
# Reporting
# ---------------------------

def write_report(m: Dict[str, int]):
    lines = [
        "FlexiMart ETL Data Quality Report",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "Customers",
        f"- Records processed: {m['customers_processed']}",
        f"- Duplicates removed: {m['customers_duplicates_removed']}",
        f"- Missing emails dropped: {m['customers_missing_email_dropped']}",
        f"- Phones standardized to null (invalid): {m['customers_phones_null']}",
        f"- Dates parsed: {m['customers_dates_parsed']}",
        f"- Records loaded: {m['customers_loaded']}",
        "",
        "Products",
        f"- Records processed: {m['products_processed']}",
        f"- Duplicates removed: {m['products_duplicates_removed']}",
        f"- Categories standardized: {m['products_categories_standardized']}",
        f"- Missing stock filled with 0: {m['products_missing_stock_filled']}",
        f"- Missing prices imputed: {m['products_missing_prices_imputed']}",
        f"- Records loaded: {m['products_loaded']}",
        "",
        "Sales / Orders",
        f"- Records processed: {m['sales_processed']}",
        f"- Duplicates removed: {m['sales_duplicates_removed']}",
        f"- Missing customer/product IDs dropped: {m['sales_missing_ids_dropped']}",
        f"- Dates parsed: {m['sales_dates_parsed']}",
        f"- Orders loaded: {m['orders_loaded']}",
        f"- Order items loaded: {m['order_items_loaded']}",
    ]
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logging.info("Report written to %s", REPORT_FILE)

# ---------------------------
# Main
# ---------------------------

def main():
    db_url = os.getenv("DB_URL")
    if not db_url:
        sys.exit("Set DB_URL to mysql+pymysql://user:pass@host:3306/fleximart")

    engine = create_engine(db_url, future=True)

    # Initialize metrics
    m = init_metrics()

    # Ensure schema exists
    ensure_schema(engine)

    # Extract
    customers_raw, products_raw, sales_raw = extract()

    # Transform
    customers_tidy = transform_customers(customers_raw, m)
    products_tidy = transform_products(products_raw, m)
    orders_tidy, items_tidy = transform_sales(sales_raw, m)

    # Load
    load_mysql(engine, customers_tidy, products_tidy, orders_tidy, items_tidy, m)

    # Report
    write_report(m)

    logging.info("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
