CREATE TABLE social_media_feeds_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    source TEXT,
    published_at TIMESTAMP,
    data JSONB,
    insert_dt TIMESTAMP,
    INDEX idx_source_insert_dt (source, insert_dt)
);