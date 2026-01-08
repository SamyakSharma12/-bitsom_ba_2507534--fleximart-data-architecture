# Schema documentation

## Entity-relationship description

### customers
- **Purpose:** Customer master used for attribution, retention, and segmentation.
- **Attributes:**
  - **customer_id:** INT, PK, AUTO_INCREMENT
  - **first_name:** VARCHAR(50), required
  - **last_name:** VARCHAR(50), required
  - **email:** VARCHAR(100), required, unique
  - **phone:** VARCHAR(20), standardized to +91-XXXXXXXXXX or null
  - **city:** VARCHAR(50), title-case
  - **registration_date:** DATE

### products
- **Purpose:** Product catalog referenced by order items.
- **Attributes:**
  - **product_id:** INT, PK, AUTO_INCREMENT
  - **product_name:** VARCHAR(100), required
  - **category:** VARCHAR(50), normalized: Electronics, Fashion, Groceries
  - **price:** DECIMAL(10,2), required (imputed when missing)
  - **stock_quantity:** INT, default 0

### orders
- **Purpose:** Order header per customer and date.
- **Attributes:**
  - **order_id:** INT, PK, AUTO_INCREMENT
  - **customer_id:** INT, FK → customers
  - **order_date:** DATE
  - **total_amount:** DECIMAL(10,2)
  - **status:** VARCHAR(20) (Pending/Completed/Cancelled)

### order_items
- **Purpose:** Line items within an order.
- **Attributes:**
  - **order_item_id:** INT, PK, AUTO_INCREMENT
  - **order_id:** INT, FK → orders
  - **product_id:** INT, FK → products
  - **quantity:** INT, > 0
  - **unit_price:** DECIMAL(10,2), ≥ 0
  - **subtotal:** DECIMAL(10,2) = quantity × unit_price

### Relationships
- customers 1 — N orders
- orders 1 — N order_items
- products 1 — N order_items

## Normalization explanation (3NF)

This schema satisfies Third Normal Form. In each table, non-key attributes depend solely on the primary key, and there are no transitive dependencies among non-key attributes. For **customers**, {first_name, last_name, email, phone, city, registration_date} are fully dependent on customer_id; email uniqueness prevents duplicates and supports upserts. For **products**, {product_name, category, price, stock_quantity} depend only on product_id; category is standardized to eliminate inconsistent values. For **orders**, {customer_id, order_date, total_amount, status} depend on order_id; customer_id is a foreign key and does not determine other non-key attributes. For **order_items**, {order_id, product_id, quantity, unit_price, subtotal} depend on order_item_id; subtotal is derived from quantity and unit_price but remains stored for performance and audit.

Functional dependencies:
- customers: customer_id → first_name, last_name, email, phone, city, registration_date
- products: product_id → product_name, category, price, stock_quantity
- orders: order_id → customer_id, order_date, total_amount, status
- order_items: order_item_id → order_id, product_id, quantity, unit_price, subtotal

Anomaly avoidance:
- Update anomalies are minimized: product price changes occur in products; order_items capture transactional unit_price for history.
- Insert anomalies are prevented: customers and products can exist without orders.
- Delete anomalies are avoided: deleting an order does not delete customer or product master; foreign keys preserve referential integrity.

## Sample data representation

### customers
| customer_id | first_name | last_name | email                  | phone         | city      | registration_date |
|-------------|------------|-----------|------------------------|---------------|-----------|-------------------|
| 1           | Rahul      | Sharma    | rahul.sharma@gmail.com| +91-9876543210| Bangalore | 2023-01-15        |
| 2           | Priya      | Patel     | priya.patel@yahoo.com | +91-9988776655| Mumbai    | 2023-02-20        |

### products
| product_id | product_name        | category     | price    | stock_quantity |
|------------|---------------------|--------------|----------|----------------|
| 1          | Samsung Galaxy S21  | Electronics  | 45999.00 | 150            |
| 2          | Nike Running Shoes  | Fashion      | 3499.00  | 80             |

### orders
| order_id | customer_id | order_date  | total_amount | status    |
|----------|-------------|-------------|--------------|-----------|
| 1        | 1           | 2024-01-15  | 45999.00     | Completed |
| 2        | 2           | 2024-01-16  | 5998.00      | Completed |

### order_items
| order_item_id | order_id | product_id | quantity | unit_price | subtotal  |
|---------------|----------|------------|----------|------------|-----------|
| 1             | 1        | 1          | 1        | 45999.00   | 45999.00  |
| 2             | 2        | 2          | 2        | 2999.00    | 5998.00   |
