CREATE TABLE exchange_data_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    source TEXT,
    published_at TIMESTAMP,
    data JSONB,
    insert_dt TIMESTAMP,
    INDEX idx_source_insert_dt (source, insert_dt)
);
