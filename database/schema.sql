CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    website TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

CREATE TABLE IF NOT EXISTS sectors (
    company_id TEXT,
    sector TEXT,
    industry TEXT
);

CREATE TABLE IF NOT EXISTS market_cap (
    company_id TEXT,
    market_cap REAL
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    company_id TEXT,
    ratio_name TEXT,
    ratio_value REAL
);

CREATE TABLE IF NOT EXISTS peer_groups (
    company_id TEXT,
    peer_group TEXT
);

CREATE TABLE IF NOT EXISTS stock_prices (
    company_id TEXT,
    date TEXT,
    close_price REAL
);

CREATE TABLE IF NOT EXISTS profitandloss (
    company_id TEXT,
    year TEXT
);

CREATE TABLE IF NOT EXISTS balancesheet (
    company_id TEXT,
    year TEXT
);

CREATE TABLE IF NOT EXISTS cashflow (
    company_id TEXT,
    year TEXT
);

CREATE TABLE IF NOT EXISTS analysis (
    company_id TEXT,
    remarks TEXT
);