-- Elimina la tabella se esiste (per ricrearla da zero)
DROP TABLE IF EXISTS users;

-- Crea tabella users con la colonna email
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);