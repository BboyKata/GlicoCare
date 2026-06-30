"""
Modello per la gestione degli utenti e dell'autenticazione.

Questo modulo definisce la classe User per la gestione delle credenziali
e la classe CredenzialiNonValide per la gestione delle eccezioni di login.
"""

import sqlite3
import hashlib


class CredenzialiNonValide(Exception):
    """
    Eccezione sollevata quando le credenziali di accesso non sono valide.
    """
    pass


class User:
    """
    Rappresenta un utente del sistema e gestisce l'autenticazione.

    Args:
        username (str): Nome utente da autenticare.
        password (str): Password in chiaro da verificare.
        db_path (str, optional): Percorso del file del database SQLite.
            Default: "glicocare.db".
    
    Raises:
        CredenzialiNonValide: Se le credenziali fornite non sono corrette.
    """

    def __init__(self, username: str, password: str, db_path: str = "glicocare.db"):
        self.username = username
        self.db_path = db_path
        self.tipo = None
        self.id_ref = None
        
        if not self._verifica_credenziali(password):
            raise CredenzialiNonValide(f"Username o password errati")
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Crea e restituisce una connessione al database.

        Returns:
            sqlite3.Connection: Oggetto connessione al database.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Calcola l'hash SHA-256 di una password.

        Args:
            password (str): Password in chiaro.

        Returns:
            str: Hash della password in formato esadecimale.
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verifica_credenziali(self, password: str) -> bool:
        """
        Verifica le credenziali dell'utente nel database.

        Se la verifica ha successo, gli attributi `tipo` e `id_ref` vengono
        popolati con i valori letti dal database.

        Args:
            password (str): Password in chiaro da verificare.

        Returns:
            bool: True se le credenziali sono valide, False altrimenti.
        """
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
    
    def get_user_info(self) -> dict:
        """
        Restituisce un dizionario con le informazioni dell'utente autenticato.

        Returns:
            dict: Dizionario con chiavi 'username', 'tipo' e 'id_ref'.
        """
        return {
            'username': self.username,
            'tipo': self.tipo,
            'id_ref': self.id_ref
        }
    
    def is_paziente(self) -> bool:
        """
        Verifica se l'utente è un paziente.

        Returns:
            bool: True se l'utente è di tipo 'P', False altrimenti.
        """
        return self.tipo == 'P'
    
    def is_medico(self) -> bool:
        """
        Verifica se l'utente è un medico.

        Returns:
            bool: True se l'utente è di tipo 'M', False altrimenti.
        """
        return self.tipo == 'M'
    
    def __str__(self) -> str:
        """
        Restituisce una rappresentazione leggibile dell'utente.

        Returns:
            str: Stringa riassuntiva dell'utente.
        """
        tipo_desc = "Paziente" if self.tipo == 'P' else "Medico"
        return f"User: {self.username} ({tipo_desc})"