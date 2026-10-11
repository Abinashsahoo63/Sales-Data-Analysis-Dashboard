CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    order_id VARCHAR(20) NOT NULL,
    product VARCHAR(80) NOT NULL,
    category VARCHAR(40) NOT NULL,
    region VARCHAR(40) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_percent DECIMAL(5,2) NOT NULL DEFAULT 0
);
