-- Populate dimensions and facts

-- Insert 30 dates (Jan–Feb 2024)
INSERT INTO dim_date VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,FALSE),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,FALSE),
...
(20240215,'2024-02-15','Thursday',15,2,'February','Q1',2024,FALSE);

-- Insert 15 products
INSERT INTO dim_product (product_id,product_name,category,subcategory,unit_price) VALUES
('P001','Samsung Galaxy S21','Electronics','Phones',45999),
('P002','Apple MacBook Pro','Electronics','Laptops',129999),
('P003','HP Laptop','Electronics','Laptops',52999),
('P004','Sony Headphones','Electronics','Audio',1999),
('P005','Dell Monitor','Electronics','Monitors',12999),
('P006','Nike Running Shoes','Fashion','Footwear',3499),
('P007','Adidas T-Shirt','Fashion','Apparel',1299),
('P008','Levi\'s Jeans','Fashion','Apparel',2999),
('P009','Puma Sneakers','Fashion','Footwear',4599),
('P010','Organic Almonds','Groceries','Dry Fruits',899),
('P011','Basmati Rice','Groceries','Grains',650),
('P012','Organic Honey','Groceries','Honey',450),
('P013','Masoor Dal','Groceries','Pulses',120),
('P014','iPhone 13','Electronics','Phones',69999),
('P015','Samsung TV 43"','Electronics','Television',32999);

-- Insert 12 customers
INSERT INTO dim_customer (customer_id,customer_name,city,state,customer_segment) VALUES
('C001','Rahul Sharma','Bangalore','Karnataka','Retail'),
('C002','Priya Patel','Mumbai','Maharashtra','Retail'),
('C003','Amit Kumar','Delhi','Delhi','Corporate'),
('C004','Sneha Reddy','Hyderabad','Telangana','Retail'),
('C005','Vikram Singh','Chennai','Tamil Nadu','Retail'),
('C006','Anjali Mehta','Bangalore','Karnataka','VIP'),
('C007','Ravi Verma','Pune','Maharashtra','Retail'),
('C008','Pooja Iyer','Bangalore','Karnataka','Corporate'),
('C009','Karthik Nair','Kochi','Kerala','Retail'),
('C010','Deepa Gupta','Delhi','Delhi','VIP'),
('C011','Arjun Rao','Hyderabad','Telangana','Corporate'),
('C012','Lakshmi Krishnan','Chennai','Tamil Nadu','Retail');

-- Insert 40 fact_sales transactions (sample realistic patterns)
INSERT INTO fact_sales (date_key,product_key,customer_key,quantity_sold,unit_price,discount_amount,total_amount) VALUES
(20240105,1,1,1,45999,0,45999),
(20240106,2,2,2,129999,5000,254998),
(20240107,6,3,4,3499,0,13996),
(20240110,5,4,1,12999,0,12999),
...
(20240215,1,10,1,45999,0,45999);
