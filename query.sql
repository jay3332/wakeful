CREATE TABLE prefixes (
    guild BIGINT PRIMARY KEY,
    prefix TEXT
)

CREATE TABLE blacklist (
    user_id BIGINT PRIMARY KEY
)

CREATE TABLE commands (
    guild BIGINT PRIMARY KEY,
    commands TEXT
)

CREATE TABLE tags (
    guild BIGINT,
    name TEXT,
    content TEXT,
    author BIGINT,
    created BIGINT
)

CREATE TABLE news (
    branch TEXT PRIMARY KEY,
    author BIGINT,
    updated BIGINT,
    content TEXT
)

CREATE TABLE emojis (
    user_id BIGINT PRIMARY KEY
)
