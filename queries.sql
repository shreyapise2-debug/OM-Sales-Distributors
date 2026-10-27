-- OM Sales Distributors: common SQL operations and expected sample outputs
-- Run these after schema.sql and seed.sql.

-- 1. Display all products
SELECT product_id, product_name, category, selling_price, stock_quantity FROM products ORDER BY product_id;

-- 2. Products priced above Rs. 250
SELECT product_name, selling_price FROM products WHERE selling_price > 250 ORDER BY selling_price DESC;

-- 3. Sort products by stock quantity (lowest first)
SELECT product_name, stock_quantity FROM products ORDER BY stock_quantity ASC;

-- 4. Search products by category
SELECT product_name, selling_price FROM products WHERE category = 'Skincare';

-- 5. Aggregate: count products in each category
SELECT category, COUNT(*) AS product_count FROM products GROUP BY category ORDER BY category;

-- 6. Aggregate: average selling price by category
SELECT category, ROUND(AVG(selling_price),2) AS average_price FROM products GROUP BY category ORDER BY category;

-- 7. INNER JOIN: orders with retailer names
SELECT so.order_id, r.retailer_name, so.order_date, so.order_status, so.total_amount
FROM sales_orders so JOIN retailers r ON so.retailer_id = r.retailer_id ORDER BY so.order_id;

-- 8. INNER JOIN: products with supplier names
SELECT p.product_name, s.supplier_name, p.stock_quantity
FROM products p JOIN suppliers s ON p.supplier_id = s.supplier_id ORDER BY p.product_id;

-- 9. Find low stock products
SELECT product_name, stock_quantity FROM products WHERE stock_quantity < 50 ORDER BY stock_quantity;

-- 10. Total sales value excluding cancelled orders
SELECT SUM(total_amount) AS total_sales FROM sales_orders WHERE order_status <> 'Cancelled';

-- 11. Orders by status
SELECT order_status, COUNT(*) AS number_of_orders FROM sales_orders GROUP BY order_status ORDER BY order_status;

-- 12. Subquery: products priced above the overall average
SELECT product_name, selling_price FROM products
WHERE selling_price > (SELECT AVG(selling_price) FROM products) ORDER BY selling_price DESC;

-- 13. UPDATE example (run in a transaction, then rollback to preserve original sample)
BEGIN;
UPDATE products SET stock_quantity = stock_quantity + 10 WHERE product_id = 1;
SELECT product_id, product_name, stock_quantity FROM products WHERE product_id = 1;
ROLLBACK;

-- 14. DELETE example using a transaction (safe demonstration; rollback restores row)
BEGIN;
DELETE FROM purchases WHERE purchase_id = 20;
SELECT COUNT(*) AS purchases_after_delete FROM purchases;
ROLLBACK;

-- 15. INSERT example: use a distinct valid supplier and then remove it in same transaction
BEGIN;
INSERT INTO suppliers(supplier_name,contact_person,phone,email,city)
VALUES ('Demo Supplier','Demo Contact','9000000000','demo.supplier@example.com','Nagpur');
SELECT supplier_id,supplier_name FROM suppliers WHERE supplier_name='Demo Supplier';
ROLLBACK;
