import sqlite3
import hashlib

class CredenzialiNonValide(Exception):
    pass

class User:
    def __init__(self, username, password, db_path="glicocare.db"):
        self.username = username
        self.db_path = db_path
        self.tipo = None
        self.id_ref = None
        
        if not self._verifica_credenziali(password):
            raise CredenzialiNonValide(f"Username o password errati")
    
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verifica_credenziali(self, password):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "SELECT password, tipo, id_ref FROM USER WHERE username = ?"
            cursor.execute(query, (self.username,))
            result = cursor.fetchone()
            
            if result is None:
                conn.close()
                return False
            
            hashed_input = self._hash_password(password)
            if hashed_input == result['password']:
                self.tipo = result['tipo']
                self.id_ref = result['id_ref']
                conn.close()
                return True
            
            conn.close()
            return False
            
        except sqlite3.Error as e:
            return False
    
    def get_user_info(self):
        return {
            'username': self.username,
            'tipo': self.tipo,
            'id_ref': self.id_ref
        }
    
    def is_paziente(self):
        return self.tipo == 'P'
    
    def is_medico(self):
        return self.tipo == 'M'
    
    def __str__(self):
        tipo_desc = "Paziente" if self.tipo == 'P' else "Medico"
        return f"User: {self.username} ({tipo_desc})"