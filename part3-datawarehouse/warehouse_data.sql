-- Populate dimensions and facts for FlexiMart DW

-- Clear existing data
DELETE FROM fact_sales;
DELETE FROM dim_customer;
DELETE FROM dim_product;
DELETE FROM dim_date;

-- 1) dim_date: 30 dates (Jan 1–Jan 30, 2024)
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,FALSE),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,FALSE),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,FALSE),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,FALSE),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,FALSE),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,TRUE),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,TRUE),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,FALSE),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,FALSE),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,FALSE),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,FALSE),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,FALSE),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,TRUE),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,TRUE),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,FALSE),
(20240116,'2024-01-16','Tuesday',16,1,'January','Q1',2024,FALSE),
(20240117,'2024-01-17','Wednesday',17,1,'January','Q1',2024,FALSE),
(20240118,'2024-01-18','Thursday',18,1,'January','Q1',2024,FALSE),
(20240119,'2024-01-19','Friday',19,1,'January','Q1',2024,FALSE),
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,TRUE),
(20240121,'2024-01-21','Sunday',21,1,'January','Q1',2024,TRUE),
(20240122,'2024-01-22','Monday',22,1,'January','Q1',2024,FALSE),
(20240123,'2024-01-23','Tuesday',23,1,'January','Q1',2024,FALSE),
(20240124,'2024-01-24','Wednesday',24,1,'January','Q1',2024,FALSE),
(20240125,'2024-01-25','Thursday',25,1,'January','Q1',2024,FALSE),
(20240126,'2024-01-26','Friday',26,1,'January','Q1',2024,FALSE),
(20240127,'2024-01-27','Saturday',27,1,'January','Q1',2024,TRUE),
(20240128,'2024-01-28','Sunday',28,1,'January','Q1',2024,TRUE),
(20240129,'2024-01-29','Monday',29,1,'January','Q1',2024,FALSE),
(20240130,'2024-01-30','Tuesday',30,1,'January','Q1',2024,FALSE);

-- 2) dim_product: 15 products
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

-- 3) dim_customer: 12 customers
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

-- 4) fact_sales: 40 transactions
INSERT INTO fact_sales (date_key,product_key,customer_key,quantity_sold,unit_price,discount_amount,total_amount) VALUES
(20240105,1,1,1,45999,0,45999),
(20240106,2,2,2,129999,5000,254998),
(20240107,6,3,4,3499,0,13996),
(20240110,5,4,1,12999,0,12999),
(20240112,4,5,2,1999,200,3798),
(20240113,9,6,3,4599,0,13797),
(20240114,10,7,5,899,90,4405),
(20240115,3,8,1,52999,0,52999),
(20240116,7,9,2,1299,0,2598),
(20240117,8,10,2,2999,0,5998),
(20240118,11,11,3,650,0,1950),
(20240119,12,12,4,450,18,1782),
(20240120,13,1,6,120,0,720),
(20240121,14,2,1,69999,0,69999),
(20240122,15,3,1,32999,0,32999),
(20240123,1,4,1,45999,0,45999),
(20240124,6,5,5,3499,175,17320),
(20240125,2,6,1,129999,0,129999),
(20240126,5,7,2,12999,0,25998),
(20240127,4,8,2,1999,0,3998),
(20240128,9,9,2,4599,0,9198),
(20240129,10,10,6,899,54,5240),
(20240130,11,11,4,650,0,2600),
(20240106,12,
