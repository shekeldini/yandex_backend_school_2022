CREATE TABLE IF NOT EXISTS user_balance (
    user_id VARCHAR(50) PRIMARY KEY,
    balance BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS changes_history (
    id VARCHAR(50) PRIMARY KEY,
    context VARCHAR(100),
    user_id VARCHAR(50) NOT NULL REFERENCES user_balance(user_id),
    balance_change BIGINT NOT NULL,
    balance_old BIGINT NOT NULL,
    balance_new BIGINT NOT NULL,
    operation_timestamp TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS index_desc_timestamp ON changes_history (operation_timestamp DESC);
