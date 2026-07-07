import pytest
import sqlite3
import os

@pytest.fixture(scope="function")
def db_path():
    """Crea un database temporaneo su file per i test."""
    import tempfile
    tmpfile = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    path = tmpfile.name
    tmpfile.close()
    yield path
    # Cleanup dopo il test
    try:
        os.unlink(path)
    except:
        pass

@pytest.fixture(scope="function")
def init_db(db_path):
    """Inizializza il database con lo schema e restituisce una connessione."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, "database", "schema.sql")
    
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema SQL non trovato: {schema_path}")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    conn.executescript(schema_sql)
    conn.commit()
    
    yield conn
    
    conn.close()