-- Total companies
SELECT COUNT(*) FROM companies;

-- Top 10 companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Top 10 companies by ROCE
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- Total stock price records
SELECT COUNT(*) FROM stock_prices;

-- Total balance sheet records
SELECT COUNT(*) FROM balancesheet;

-- Total cashflow records
SELECT COUNT(*) FROM cashflow;

-- Total profit and loss records
SELECT COUNT(*) FROM profitandloss;

-- Companies with ROE > 20
SELECT company_name, roe_percentage
FROM companies
WHERE roe_percentage > 20;

-- Companies with ROCE > 20
SELECT company_name, roce_percentage
FROM companies
WHERE roce_percentage > 20;

-- Total records in each major table
SELECT 'companies' AS table_name, COUNT(*) AS rows_count FROM companies
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss;