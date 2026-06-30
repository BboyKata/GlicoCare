"""
Modello per la gestione del medico.

Questo modulo definisce la classe Medico, che si occupa di interagire
con il database SQLite per recuperare e gestire i pazienti assegnati.
"""

import sqlite3
from src.paziente import Paziente


class Medico:
    """
    Rappresenta un medico e fornisce metodi per gestire i suoi pazienti.

    Args:
        id_ref (int): L'ID del medico (corrisponde a `id_med` nella tabella MEDICO).
        db_path (str, optional): Percorso del file del database SQLite. 
            Default: "database/glicocare.db".
    """

    def __init__(self, id_ref, db_path="database/glicocare.db"):
        self._id_ref = id_ref
        self._db_path = db_path
        
        self._cf = None
        self._nome = None
        self._cognome = None
        self._sesso = None
        self._data_nascita = None
        self._luogo_nascita = None
        self._indirizzo = None
        self._email = None
        self._cel = None
        
        self._pazienti_ids = []
        
        self._carica_dati()

    def _carica_dati(self):
        """
        Carica i dati anagrafici del medico e la lista dei suoi pazienti dal DB.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        try:
            # Dati anagrafici del medico (senza specializzazione, non presente nello schema)
            query_anagrafica = """
            SELECT 
                A.CF, A.nome, A.cognome, A.sesso, A.dataNascita, A.luogoNascita,
                A.indirizzo, A.email, A.cel
            FROM MEDICO M
            JOIN ANAGRAFICA A ON M.CF = A.CF
            WHERE M.id_med = ?
            """
            cursor.execute(query_anagrafica, (self._id_ref,))
            row = cursor.fetchone()
            
            if row is None:
                raise ValueError(f"Medico con id_ref {self._id_ref} non trovato nel database.")

            (self._cf, self._nome, self._cognome, self._sesso, 
             self._data_nascita, self._luogo_nascita, self._indirizzo, 
             self._email, self._cel) = row

            # Lista degli ID dei pazienti assegnati, ordinati per gravità
            query_pazienti = """
            SELECT id_paz FROM PAZIENTE WHERE medico = ? ORDER BY gravita DESC
            """
            cursor.execute(query_pazienti, (self._id_ref,))
            self._pazienti_ids = [row[0] for row in cursor.fetchall()]

        except sqlite3.Error as e:
            print(f"Errore database: {e}")
        finally:
            conn.close()

    # ==========================================================
    # GETTER
    # ==========================================================
    def getIdRef(self) -> int:
        """Restituisce l'ID di riferimento del medico."""
        return self._id_ref

    def getCf(self) -> str:
        """Restituisce il codice fiscale del medico."""
        return self._cf

    def getNome(self) -> str:
        """Restituisce il nome del medico."""
        return self._nome

    def getCognome(self) -> str:
        """Restituisce il cognome del medico."""
        return self._cognome

    def getSesso(self) -> str:
        """Restituisce il sesso del medico ('M' o 'F')."""
        return self._sesso

    def getDataNascita(self) -> str:
        """Restituisce la data di nascita del medico."""
        return self._data_nascita

    def getLuogoNascita(self) -> str:
        """Restituisce il luogo di nascita del medico."""
        return self._luogo_nascita

    def getIndirizzo(self) -> str:
        """Restituisce l'indirizzo del medico."""
        return self._indirizzo

    def getEmail(self) -> str:
        """Restituisce l'email del medico."""
        return self._email

    def getCel(self) -> str:
        """Restituisce il numero di cellulare del medico."""
        return self._cel

    # ==========================================================
    # GESTIONE PAZIENTI
    # ==========================================================
    def getPazientiIds(self) -> list:
        """
        Restituisce la lista degli ID dei pazienti assegnati,
        ordinati per gravità decrescente.
        
        Returns:
            list: Lista di int (id_paz).
        """
        return self._pazienti_ids

    def getPazienti(self) -> list:
        """
        Restituisce la lista di tutti i pazienti come oggetti Paziente,
        ordinati per gravità decrescente.
        """
        pazienti = [Paziente(pid, self._db_path) for pid in self._pazienti_ids]
        pazienti.sort(key=lambda p: p.getGravita(), reverse=True)
        return pazienti

    def getPazientiConDettaglio(self) -> list:
        """
        Restituisce una lista di dizionari con i dettagli di ogni paziente,
        ordinati per gravità decrescente.
        
        Returns:
            list: Lista di dict ordinata per gravità decrescente.
        """
        result = []
        for pid in self._pazienti_ids:
            p = Paziente(pid, self._db_path)
            punti_g = p.getPuntiGlicemia()
            punti_t = p.getPuntiTerapia()
            
            if punti_g > 0 and punti_t > 0:
                tipo = "Glicemia + Terapia"
            elif punti_g > 0:
                tipo = "Glicemia fuori soglia"
            elif punti_t > 0:
                tipo = "Terapia non rispettata"
            else:
                tipo = "In regola"
            
            result.append({
                'id': pid,
                'nome': p.getNome(),
                'cognome': p.getCognome(),
                'gravita': p.getGravita(),
                'punti_glicemia': punti_g,
                'punti_terapia': punti_t,
                'tipo': tipo,
            })
        
        # RIORDINA per gravità decrescente (dopo il ricalcolo)
        result.sort(key=lambda x: x['gravita'], reverse=True)
        
        return result

    def getPazienteById(self, id_paz: int):
        """
        Recupera un paziente specifico tramite il suo ID.
        
        Args:
            id_paz (int): ID del paziente.
            
        Returns:
            Paziente | None: Oggetto Paziente, o None se non assegnato a questo medico.
        """
        if id_paz not in self._pazienti_ids:
            return None
        return Paziente(id_paz, self._db_path)

    def getStatistiche(self) -> dict:
        """
        Calcola le statistiche generali dei pazienti del medico.
        
        Returns:
            dict: Dizionario con chiavi:
                totale, in_regola, gravi, solo_glicemia, solo_terapia, 
                entrambi, gravita_media
        """
        pazienti = self.getPazientiConDettaglio()
        
        totale = len(pazienti)
        in_regola = sum(1 for p in pazienti if p['gravita'] == 0)
        gravi = totale - in_regola
        solo_glicemia = sum(1 for p in pazienti if p['punti_glicemia'] > 0 and p['punti_terapia'] == 0)
        solo_terapia = sum(1 for p in pazienti if p['punti_terapia'] > 0 and p['punti_glicemia'] == 0)
        entrambi = sum(1 for p in pazienti if p['punti_glicemia'] > 0 and p['punti_terapia'] > 0)
        gravita_media = sum(p['gravita'] for p in pazienti) / totale if totale > 0 else 0
        
        return {
            'totale': totale,
            'in_regola': in_regola,
            'gravi': gravi,
            'solo_glicemia': solo_glicemia,
            'solo_terapia': solo_terapia,
            'entrambi': entrambi,
            'gravita_media': round(gravita_media, 1)
        }

    def __str__(self) -> str:
        """
        Restituisce una rappresentazione leggibile del medico.
        """
        return (f"Dr. {self._nome} {self._cognome}\n"
                f"Pazienti assegnati: {len(self._pazienti_ids)}")