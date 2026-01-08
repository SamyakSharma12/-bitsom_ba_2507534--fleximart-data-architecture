// MongoDB Operations for FlexiMart Product Catalog

// Operation 1: Load Data (1 mark)
// Import the provided JSON file into collection 'products'
// Run in shell: mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

// Operation 2: Basic Query (2 marks)
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { name: 1, price: 1, stock: 1, _id: 0 }
);

// Operation 3: Review Analysis (2 marks)
// Find all products that have average rating >= 4.0
db.products.aggregate([
  { $unwind: "$reviews" },
  { $group: { _id: "$product_id", name: { $first: "$name" }, avgRating: { $avg: "$reviews.rating" } } },
  { $match: { avgRating: { $gte: 4.0 } } }
]);

// Operation 4: Update Operation (2 marks)
// Add a new review to product "ELEC001"
db.products.updateOne(
  { product_id: "ELEC001" },
  { $push: { reviews: { user: "U999", rating: 4, comment: "Good value", date: new Date() } } }
);

// Operation 5: Complex Aggregation (3 marks)
// Calculate average price by category, return category, avg_price, product_count, sorted by avg_price descending
db.products.aggregate([
  { $group: { _id: "$category", avg_price: { $avg: "$price" }, product_count: { $sum: 1 } } },
  { $sort: { avg_price: -1 } }
]);
