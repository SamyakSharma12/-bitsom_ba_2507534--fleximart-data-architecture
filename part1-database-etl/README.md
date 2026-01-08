# FlexiMart Data Engineering Assignment – Part 1

## Overview
This project implements a complete data pipeline for FlexiMart, an e‑commerce company.  
It covers:
- **ETL Pipeline:** Clean and load raw CSV data into MySQL.
- **Database Documentation:** Schema description, relationships, normalization.
- **Business Queries:** SQL queries answering specific business questions.

Deliverables:
- `etl_pipeline.py` – ETL script
- `data_quality_report.txt` – Generated report
- `schema_documentation.md` – Database schema documentation
- `business_queries.sql` – SQL queries

---

## ETL Pipeline

### Features
- **Extract:** Reads `customers_raw.csv`, `products_raw.csv`, `sales_raw.csv`.
- **Transform:**
  - Removes duplicates
  - Drops rows with missing emails or critical IDs
  - Fills missing stock with 0
  - Imputes missing prices with category median
  - Standardizes phone numbers to `+91-XXXXXXXXXX`
  - Normalizes category names (`Electronics`, `Fashion`, `Groceries`)
  - Converts dates to `YYYY-MM-DD`
- **Load:** Inserts into MySQL using provided schema
  - Surrogate keys via `AUTO_INCREMENT`
  - Upserts via `ON DUPLICATE KEY UPDATE`
  - Order IDs retrieved via `LAST_INSERT_ID()`
- **Report:** Logs counts and writes `data_quality_report.txt`

### Run Instructions
1. Install dependencies:
   ```bash
   pip install pandas sqlalchemy pymysql
