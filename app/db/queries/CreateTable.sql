CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,

    contract_id UUID NOT NULL,   

    vendor TEXT NOT NULL,
    value NUMERIC,
    risk_level TEXT,
    summary TEXT,
    status TEXT,                 

    record_hash TEXT,            

    is_current BOOLEAN DEFAULT TRUE,
    start_date TIMESTAMP DEFAULT NOW(),
    end_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW()
);
