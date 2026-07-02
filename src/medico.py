import sqlite3
import os
from datetime import datetime
from src.paziente import Paziente


class Medico:
    """
    Rappresenta un medico e fornisce metodi per gestire i suoi pazienti.

    Args:
        id_ref (int): L'ID del medico (corrisponde a `id_med` nella tabella MEDICO).
        db_path (str, optional): Percorso del file del database SQLite. 
            Default: "database/glicocare.db".
    """

    def __init__(self, id_ref, db_path=None):
        self._id_ref = id_ref
        if db_path is None:
            home = os.path.expanduser("~")
            self._db_path = os.path.join(home, ".glicocare", "glicocare.db")
        else:
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
            # Dati anagrafici del medico
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
        return self._id_ref

    def getCf(self) -> str:
        return self._cf

    def getNome(self) -> str:
        return self._nome

    def getCognome(self) -> str:
        return self._cognome

    def getSesso(self) -> str:
        return self._sesso

    def getDataNascita(self) -> str:
        return self._data_nascita

    def getLuogoNascita(self) -> str:
        return self._luogo_nascita

    def getIndirizzo(self) -> str:
        return self._indirizzo

    def getEmail(self) -> str:
        return self._email

    def getCel(self) -> str:
        return self._cel

    # ==========================================================
    # GESTIONE PAZIENTI
    # ==========================================================
    def getPazientiIds(self) -> list:
        return self._pazienti_ids

    def getPazienti(self) -> list:
        pazienti = [Paziente(pid, self._db_path) for pid in self._pazienti_ids]
        pazienti.sort(key=lambda p: p.getGravita(), reverse=True)
        return pazienti

    def getPazientiConDettaglio(self) -> list:
        """
        Restituisce una lista di dizionari con i dettagli di ogni paziente,
        ordinati per gravità decrescente.
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
        
        result.sort(key=lambda x: x['gravita'], reverse=True)
        return result

    def getPazienteById(self, id_paz: int):
        if id_paz not in self._pazienti_ids:
            return None
        return Paziente(id_paz, self._db_path)

    def getStatistiche(self) -> dict:
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

    def registra_operazione(self, azione: str, tabella: str, id_record: str = None, dettaglio: str = None) -> None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO LOG_OPERAZIONI (id_med, azione, tabella, id_record, dettaglio)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, azione, tabella, id_record, dettaglio))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Errore registrazione log: {e}")
        finally:
            conn.close()

    def get_log_operazioni(self, limite=50):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT azione, tabella, dettaglio, data_ora FROM LOG_OPERAZIONI WHERE id_med=? ORDER BY data_ora DESC LIMIT ?",
                (self._id_ref, limite)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore recupero log: {e}")
            return []
        finally:
            conn.close()

    # ==========================================================
    # GESTIONE TERAPIE
    # ==========================================================

    def prescriviTerapia(self, id_paz: int, farmaco: str, assunzioniGiornaliere: int, quantita: str, data_inizio: str, data_fine: str = None, indicazioni: str = None):
        """Prescrive una nuova terapia (INSERT)."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, self._id_ref, data_inizio, data_fine))
            conn.commit()
            self.registra_operazione("PRESCRIZIONE_TERAPIA", "TERAPIA", f"{id_paz}/{farmaco}", f"Nuova terapia {farmaco}")
        except sqlite3.Error as e:
            print(f"ERRORE PRESCRIZIONE: {e}")
        finally:
            conn.close()
        self._aggiorna_gravita_paziente(id_paz)

    def modificaTerapia(self, id_paz: int, vecchio_farmaco: str, nuovo_farmaco: str, assunzioniGiornaliere: int, quantita: str, data_inizio: str, data_fine: str = None, indicazioni: str = None):
        """
        Modifica una terapia esistente.
        CASO A: Stesso farmaco -> UPDATE diretto (modifica dose, data_fine, ecc.)
        CASO B: Farmaco diverso -> Chiudi vecchia (data_fine=oggi) e crea nuova riga.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            oggi = datetime.now().strftime("%Y-%m-%d")

            # CASO A: Stesso farmaco (solo modifica quantità, data_fine, ecc.)
            if vecchio_farmaco == nuovo_farmaco:
                cursor.execute("""
                UPDATE TERAPIA
                SET assunzioniGiornaliere = ?, quantita = ?, indicazioni = ?, data_fine = ?
                WHERE id_paz = ? AND farmaco = ? AND data_inizio = ?
                """, (assunzioniGiornaliere, quantita, indicazioni, data_fine, id_paz, vecchio_farmaco, data_inizio))
                conn.commit()
                self.registra_operazione("MODIFICA_TERAPIA", "TERAPIA", f"{id_paz}/{vecchio_farmaco}", f"Aggiornata {vecchio_farmaco} (data_fine={data_fine})")
            
            # CASO B: Farmaco diverso
            else:
                # 1. Chiudi la vecchia terapia (data_fine = oggi)
                cursor.execute("UPDATE TERAPIA SET data_fine=? WHERE id_paz=? AND farmaco=? AND data_inizio=?", (oggi, id_paz, vecchio_farmaco, data_inizio))
                # 2. Inserisci la nuova terapia
                cursor.execute("""
                INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_paz, nuovo_farmaco, assunzioniGiornaliere, quantita, indicazioni, self._id_ref, oggi, data_fine))
                conn.commit()
                self.registra_operazione("MODIFICA_TERAPIA", "TERAPIA", f"{id_paz}/{nuovo_farmaco}", f"Sostituito {vecchio_farmaco}→{nuovo_farmaco}")
            
        except sqlite3.Error as e:
            print(f"ERRORE MODIFICA: {e}")
        finally:
            conn.close()
        self._aggiorna_gravita_paziente(id_paz)

    def interrompiTerapia(self, id_paz: int, farmaco: str, data_fine: str = None):
        """Imposta la data di fine di una terapia (senza cancellarla)."""
        if data_fine is None:
            data_fine = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE TERAPIA SET data_fine=? WHERE id_paz=? AND farmaco=? AND data_fine IS NULL", (data_fine, id_paz, farmaco))
            conn.commit()
            self.registra_operazione("INTERRUZIONE_TERAPIA", "TERAPIA", f"{id_paz}/{farmaco}", f"Interrotta con data_fine={data_fine}")
        except sqlite3.Error as e:
            print(f"ERRORE INTERRUZIONE: {e}")
        finally:
            conn.close()
        self._aggiorna_gravita_paziente(id_paz)

    def eliminaTerapiaDefinitiva(self, id_paz: int, farmaco: str):
        """Cancella fisicamente una terapia dal database."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM TERAPIA WHERE id_paz=? AND farmaco=?", (id_paz, farmaco))
            conn.commit()
            self.registra_operazione("ELIMINAZIONE_DEFINITIVA", "TERAPIA", f"{id_paz}/{farmaco}", f"Eliminata definitivamente {farmaco}")
        except sqlite3.Error as e:
            print(f"ERRORE ELIMINAZIONE: {e}")
        finally:
            conn.close()
        self._aggiorna_gravita_paziente(id_paz)

    def _aggiorna_gravita_paziente(self, id_paz: int):
        """
        Forza il ricalcolo della gravità per un paziente specifico.
        """
        p = Paziente(id_paz, self._db_path)
        p._aggiorna_gravita_db()

    def __str__(self) -> str:
        return (f"Dr. {self._nome} {self._cognome}\n"
                f"Pazienti assegnati: {len(self._pazienti_ids)}")