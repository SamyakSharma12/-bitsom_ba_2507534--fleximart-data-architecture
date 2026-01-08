# Star Schema Design – FlexiMart Data Warehouse

## Section 1: Schema Overview

FACT TABLE: **fact_sales**  
- Grain: One row per product per order line item  
- Business Process: Sales transactions  

**Measures (Numeric Facts):**
- quantity_sold: Number of units sold  
- unit_price: Price per unit at time of sale  
- discount_amount: Discount applied  
- total_amount: Final amount (quantity × unit_price − discount)  

**Foreign Keys:**
- date_key → dim_date  
- product_key → dim_product  
- customer_key → dim_customer  

DIMENSION TABLE: **dim_date**  
- Purpose: Date dimension for time-based analysis  
- Type: Conformed dimension  
- Attributes:  
  - date_key (PK): Surrogate key (YYYYMMDD)  
  - full_date: Actual date  
  - day_of_week: Monday–Sunday  
  - day_of_month: 1–31  
  - month: 1–12  
  - month_name: January–December  
  - quarter: Q1–Q4  
  - year: 4-digit year  
  - is_weekend: Boolean  

DIMENSION TABLE: **dim_product**  
- Purpose: Product attributes for categorization and pricing  
- Attributes:  
  - product_key (PK, AUTO_INCREMENT)  
  - product_id: Source product code  
  - product_name: Descriptive name  
  - category: Electronics/Fashion/Groceries  
  - subcategory: Phones, Laptops, Apparel, etc.  
  - unit_price: Current list price  

DIMENSION TABLE: **dim_customer**  
- Purpose: Customer attributes for segmentation and geo analysis  
- Attributes:  
  - customer_key (PK, AUTO_INCREMENT)  
  - customer_id: Source customer code  
  - customer_name: Full name  
  - city: City  
  - state: State  
  - customer_segment: Retail, Corporate, VIP  

## Section 2: Design Decisions

We chose line-item granularity because it captures the most detailed view of sales, enabling accurate aggregation across products, customers, and time. Surrogate keys are used instead of natural keys to ensure stability: source IDs may change or be duplicated, while surrogate keys remain consistent. This design supports drill-down (year → quarter → month → day) and roll-up (product → category → subcategory, customer → city → state) operations. Measures are additive, making OLAP queries straightforward and efficient.

## Section 3: Sample Data Flow

**Source Transaction:**  
Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000  

**Warehouse Representation:**  
- fact_sales: `{date_key: 20240115, product_key: 5, customer_key: 12, quantity_sold: 2, unit_price: 50000, discount_amount: 0, total_amount: 100000}`  
- dim_date: `{date_key: 20240115, full_date: '2024-01-15', month: 1, quarter: 'Q1', year: 2024}`  
- dim_product: `{product_key: 5, product_name: 'Laptop', category: 'Electronics', subcategory: 'Laptops', unit_price: 50000}`  
- dim_customer: `{customer_key: 12, customer_name: 'John Doe', city: 'Mumbai', state: 'Maharashtra', customer_segment: 'Retail'}`  
