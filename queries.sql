-- queries.sql

-- 1. View the first 100 records to understand the structure.
SELECT *
FROM ecommerce_data
LIMIT 100;

-- 2. Calculate key metrics: Total Revenue and Number of Orders.
SELECT
    SUM(SalePrice) AS TotalRevenue,
    COUNT(DISTINCT OrderID) AS NumberOfOrders
FROM ecommerce_data;

-- 3. Analyze sales performance by Country.
SELECT
    Country,
    SUM(SalePrice) AS TotalRevenue
FROM ecommerce_data
GROUP BY Country
ORDER BY TotalRevenue DESC
LIMIT 15; -- Show top 15 countries

-- 4. Find the top 20 best-selling products.
SELECT
    ProductName,
    SUM(Quantity) AS TotalQuantitySold,
    SUM(SalePrice) AS TotalRevenue
FROM ecommerce_data
GROUP BY ProductName
ORDER BY TotalRevenue DESC
LIMIT 20;

-- 5. Analyze the monthly sales trend to see seasonality.
SELECT
    strftime('%Y-%m', OrderDate) AS SalesMonth,
    SUM(SalePrice) AS MonthlyRevenue
FROM ecommerce_data
GROUP BY SalesMonth
ORDER BY SalesMonth;
