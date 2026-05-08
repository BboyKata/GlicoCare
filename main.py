import sqlite3
from pathlib import Path

class Database:
    def __init__(self):
        # USA IL DATABASE NELLA CARTELLA DEL PROGETTO
        # Invece di ~/.mia_app/myapp.db
        self.db_path = Path(__file__).parent / "database" / "myapp.db"
        
        # Crea la cartella database se non esiste
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Crea il DB se non esiste
        if not self.db_path.exists():
            self.init_database()
    
    def init_database(self):
        """Crea il database da zero con schema.sql"""
        conn = sqlite3.connect(self.db_path)
        
        # Leggi lo schema dal file nella cartella database/
        schema_path = Path(__file__).parent / "database" / "schema.sql"
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
        
        conn.commit()  # IMPORTANTE: salva le modifiche
        conn.close()
        print(f"✅ Database creato in: {self.db_path}")
    
    # ... resto dei metodi uguali ...
    
    def aggiungi_utente(self, username, email=None):
        """Aggiunge un nuovo utente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email)
            )
            conn.commit()
            print(f"✅ Utente '{username}' aggiunto!")
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"❌ Utente '{username}' esiste già!")
            return None
        finally:
            conn.close()
    
    def stampa_tutti_utenti(self):
        """Stampa tutti gli utenti nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
        conn.close()
        
        if not users:
            print("📭 Nessun utente trovato.")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<5} {'Username':<25} {'Email':<30} {'Creato il':<20}")
        print("="*70)
        
        for user in users:
            id, username, email, created_at = user
            email_display = email if email else "-"
            print(f"{id:<5} {username:<25} {email_display:<30} {created_at:<20}")
        
        print("="*70)
        print(f"Totale: {len(users)} utenti\n")
    
    def aggiungi_4_utenti_esempio(self):
        """Aggiunge 4 utenti di esempio"""
        utenti = [
            ("Mario Rossi", "mario.rossi@email.com"),
            ("Luigi Verdi", "luigi.verdi@email.com"),
            ("Giulia Bianchi", "giulia.bianchi@email.com"),
            ("Anna Neri", "anna.neri@email.com")
        ]
        
        print("\n📝 Aggiunta 4 utenti di esempio...")
        for username, email in utenti:
            self.aggiungi_utente(username, email)


# Codice per testare direttamente
if __name__ == "__main__":
    # Crea istanza del database
    db = Database()
    
    # Aggiungi 4 utenti
    db.aggiungi_4_utenti_esempio()
    
    # Stampa tutti gli utenti
    db.stampa_tutti_utenti()