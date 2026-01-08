# Part 2 – NoSQL Database Analysis

This module explores the suitability of MongoDB for FlexiMart’s diverse product catalog and implements basic operations.

## Contents
- **nosql_analysis.md** – Theory report covering:
  - Limitations of RDBMS for diverse product attributes and nested reviews
  - Benefits of MongoDB (flexible schema, embedded documents, scalability)
  - Trade‑offs compared to MySQL
- **mongodb_operations.js** – Practical MongoDB operations:
  1. Load data from JSON file
  2. Query products in Electronics category under ₹50,000
  3. Aggregate average ratings from reviews
  4. Update product with a new review
  5. Complex aggregation: average price by category
- **products_catalog.json** – Sample dataset with 10 products across Electronics and Fashion categories

## Run Instructions

### 1. Load Sample Data
Use `mongoimport` to load the JSON file into MongoDB:
```bash
mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray
