"""
Modello per la gestione del paziente.

Questo modulo definisce la classe Paziente, che si occupa di interagire
con il database SQLite per recuperare e modificare tutte le informazioni
relative a un singolo paziente (anagrafica, rilevazioni, terapie, sintomi).
"""

import os
import sqlite3
from datetime import datetime, timedelta


class Paziente:
    def __init__(self, id_ref, db_path=None):
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
        self._gravita = None
        self._medico_id = None
        self._annotazione = ""
        
        self._rilevazioni = []
        self._terapie = []
        self._punti_glicemia = 0
        self._punti_terapia = 0 

        if db_path is None:
            home = os.path.expanduser("~")
            self._db_path = os.path.join(home, ".glicocare", "glicocare.db")
        else:
            self._db_path = db_path

        self._carica_dati()
        self._aggiorna_gravita_db()

    # ==========================================================
    # CARICAMENTO DATI
    # ==========================================================
    def _carica_dati(self):
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        try:
            # Anagrafica
            query_anagrafica = """
            SELECT 
                A.CF, A.nome, A.cognome, A.sesso, A.dataNascita, A.luogoNascita,
                A.indirizzo, A.email, A.cel,
                P.gravita, P.medico, P.annotazione
            FROM PAZIENTE P
            JOIN ANAGRAFICA A ON P.CF = A.CF
            WHERE P.id_paz = ?
            """
            cursor.execute(query_anagrafica, (self._id_ref,))
            row = cursor.fetchone()
            
            if row is None:
                raise ValueError(f"Paziente con id_ref {self._id_ref} non trovato nel database.")

            (self._cf, self._nome, self._cognome, self._sesso, 
             self._data_nascita, self._luogo_nascita, self._indirizzo, 
             self._email, self._cel, self._gravita, self._medico_id,
             self._annotazione) = row
            if self._annotazione is None:
                self._annotazione = ""

            # Rilevazioni
            query_rilevazioni = """
            SELECT giorno, ora, glicemia, primaDopoPasto
            FROM RILEVAZ_GIORN
            WHERE id_paz = ?
            """
            cursor.execute(query_rilevazioni, (self._id_ref,))
            self._rilevazioni = cursor.fetchall()
            
            # --- CORREZIONE QUI: Aggiungi data_inizio ---
            query_terapie = """
            SELECT farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio
            FROM TERAPIA
            WHERE id_paz = ? AND data_fine IS NULL
            """
            cursor.execute(query_terapie, (self._id_ref,))
            self._terapie = cursor.fetchall()
            # ------------------------------------------

        except sqlite3.Error as e:
            print(f"Errore database: {e}")
        finally:
            conn.close()
        
        self._ordina_rilevazioni()

    def _refresh_rilevazioni(self):
        """
        Ricarica la lista delle rilevazioni dal database dopo una modifica.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            SELECT giorno, ora, glicemia, primaDopoPasto
            FROM RILEVAZ_GIORN
            WHERE id_paz = ?
            """
            cursor.execute(query, (self._id_ref,))
            self._rilevazioni = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore refresh rilevazioni: {e}")
        finally:
            conn.close()
        
        # Ordina dopo il refresh
        self._ordina_rilevazioni()

    def _ordina_rilevazioni(self):
        """
        Ordina le rilevazioni per giorno decrescente e ora crescente.
        """
        # Converti ora in minuti per ordinamento numerico corretto
        def _minuti(ora_str):
            try:
                h, m = ora_str.split(':')
                return int(h) * 60 + int(m)
            except:
                return 0
        
        # Ordina per giorno decrescente, e a parità di giorno per ora crescente
        self._rilevazioni.sort(key=lambda x: (_minuti(x[1]), x[0]))
        self._rilevazioni.sort(key=lambda x: x[0], reverse=True)

    # ==========================================================
    # CALCOLO GRAVITÀ
    # ==========================================================
    def _calcola_gravita(self):
        """
        Calcola la gravità del paziente:
        - Ogni valore glicemico fuori soglia = 1 punto
        - Ogni giorno con rilevazioni dove manca almeno un'assunzione (basato sulle terapie attive) = 1 punto
        
        Returns:
            tuple: (punteggio_totale, punti_glicemia, punti_terapia)
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        
        punti_glicemia = 0
        punti_terapia = 0
        
        try:
            # --- PUNTI GLICEMIA: tutti i valori fuori soglia ---
            cursor.execute(
                "SELECT glicemia, primaDopoPasto FROM RILEVAZ_GIORN WHERE id_paz = ?",
                (self._id_ref,)
            )
            for glicemia, tipo_pasto in cursor.fetchall():
                if tipo_pasto == 'P' and (glicemia < 80 or glicemia > 130):
                    punti_glicemia += 1
                elif tipo_pasto == 'D' and glicemia > 180:
                    punti_glicemia += 1
            
            # --- PUNTI TERAPIA: solo giorni con rilevazioni ---
            # Prende solo le terapie ATTIVE (quelle che il paziente deve seguire oggi)
            cursor.execute(
                "SELECT farmaco, assunzioniGiornaliere FROM TERAPIA WHERE id_paz = ? AND data_fine IS NULL",
                (self._id_ref,)
            )
            terapie_attive = cursor.fetchall()
            
            if terapie_attive:
                # Prendi solo i giorni in cui ci sono rilevazioni (giorni "attivi")
                cursor.execute(
                    "SELECT DISTINCT giorno FROM RILEVAZ_GIORN WHERE id_paz = ? ORDER BY giorno",
                    (self._id_ref,)
                )
                giorni_attivi = [row[0] for row in cursor.fetchall()]
                
                # Per ogni giorno con rilevazioni, verifica che tutte le assunzioni siano state fatte
                for giorno in giorni_attivi:
                    for farmaco, assunzioni_previste in terapie_attive:
                        cursor.execute(
                            "SELECT COUNT(*) FROM ASSUNZIONE WHERE id_paz = ? AND giorno = ? AND farmaco = ?",
                            (self._id_ref, giorno, farmaco)
                        )
                        assunzioni_fatte = cursor.fetchone()[0]
                        if assunzioni_fatte < assunzioni_previste:
                            punti_terapia += 1
                            break  # basta un farmaco mancante per penalizzare il giorno
            
        except sqlite3.Error as e:
            print(f"Errore calcolo gravità: {e}")
        finally:
            conn.close()
        
        return (punti_glicemia + punti_terapia, punti_glicemia, punti_terapia)

    def _aggiorna_gravita_db(self):
        """
        Ricalcola la gravità e la aggiorna nel database e nell'oggetto.
        """
        punteggio, punti_glicemia, punti_terapia = self._calcola_gravita()
        
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE PAZIENTE SET gravita = ? WHERE id_paz = ?",
                (punteggio, self._id_ref)
            )
            conn.commit()
            self._gravita = punteggio
            self._punti_glicemia = punti_glicemia
            self._punti_terapia = punti_terapia
        except sqlite3.Error as e:
            print(f"Errore aggiornamento gravità: {e}")
        finally:
            conn.close()

    # ==========================================================
    # GETTER
    # ==========================================================
    def getIdRef(self) -> int:
        """Restituisce l'ID di riferimento del paziente."""
        return self._id_ref

    def getCf(self) -> str:
        """Restituisce il codice fiscale del paziente."""
        return self._cf

    def getNome(self) -> str:
        """Restituisce il nome del paziente."""
        return self._nome

    def getCognome(self) -> str:
        """Restituisce il cognome del paziente."""
        return self._cognome

    def getSesso(self) -> str:
        """Restituisce il sesso del paziente ('M' o 'F')."""
        return self._sesso

    def getDataNascita(self) -> str:
        """Restituisce la data di nascita del paziente."""
        return self._data_nascita

    def getLuogoNascita(self) -> str:
        """Restituisce il luogo di nascita del paziente."""
        return self._luogo_nascita

    def getIndirizzo(self) -> str:
        """Restituisce l'indirizzo del paziente."""
        return self._indirizzo

    def getEmail(self) -> str:
        """Restituisce l'email del paziente."""
        return self._email

    def getCel(self) -> str:
        """Restituisce il numero di cellulare del paziente."""
        return self._cel

    def getGravita(self) -> int:
        """Restituisce il livello di gravità calcolato."""
        return self._gravita

    def getMedicoId(self) -> int:
        """Restituisce l'ID del medico di riferimento."""
        return self._medico_id

    def getRilevazioni(self) -> list:
        """
        Restituisce tutte le rilevazioni della glicemia del paziente.

        Returns:
            list: Lista di tuple nel formato 
                (giorno (str), ora (str), glicemia (float), primaDopoPasto (str)).
        """
        return self._rilevazioni

    def getPuntiGlicemia(self) -> int:
        """Restituisce i punti gravità legati alla glicemia fuori soglia."""
        return self._punti_glicemia
    
    def getPuntiTerapia(self) -> int:
        """Restituisce i punti gravità legati alla terapia non rispettata."""
        return self._punti_terapia

    # ==========================================================
    # TERAPIE (Lettura)
    # ==========================================================
    def getTerapie(self) -> list:
        """
        Restituisce le terapie farmacologiche ATTIVE del paziente.
        
        Returns:
            list: Lista di tuple nel formato 
                (farmaco (str), assunzioniGiornaliere (int), quantita (str), 
                 indicazioni (str), id_med (int), data_inizio (str)).
        """
        return self._terapie

    # ==========================================================
    # --- NUOVO METODO: Recupera tutto lo storico (attive e passate) ---
    def getTerapieComplete(self) -> list:
        """
        Restituisce TUTTE le terapie (attive e passate) per lo storico.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            SELECT farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine
            FROM TERAPIA
            WHERE id_paz = ?
            ORDER BY data_inizio DESC
            """
            cursor.execute(query, (self._id_ref,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore storico terapie: {e}")
            return []
        finally:
            conn.close()
    # -----------------------------------------------------------

    def getTerapieByName(self, farmaco: str) -> tuple:
        """
        Cerca la terapia ATTIVA specifica tramite il nome del farmaco.
        Restituisce la tupla a 6 elementi se trovata.
        """
        for terapia in self._terapie:
            if terapia[0] == farmaco:
                return terapia
        return None

    def getMedicoRiferimento(self) -> tuple:
        """
        Recupera i dati anagrafici del medico di riferimento del paziente.

        Returns:
            tuple | None: Tupla nel formato (nome, cognome, email, cel) 
                del medico, oppure None se non trovato.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            SELECT A.nome, A.cognome, A.email, A.cel
            FROM MEDICO M
            JOIN ANAGRAFICA A ON M.CF = A.CF
            WHERE M.id_med = ?
            """
            cursor.execute(query, (self._medico_id,))
            row = cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print(f"Errore recupero medico: {e}")
            return None
        finally:
            conn.close()

    # ==========================================================
    # RILEVAZIONI (Scrittura)
    # ==========================================================
    def aggiungiRilevazioneGiornaliera(self, giorno: str, ora: str, glicemia: float, primaDopoPasto: str) -> None:
        """
        Aggiunge una nuova rilevazione della glicemia.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, giorno, ora, glicemia, primaDopoPasto))
            conn.commit()
            print("Rilevazione aggiunta con successo.")
        except sqlite3.Error as e:
            print(f"Errore nell'aggiunta della rilevazione: {e}")
        finally:
            conn.close()
        self._refresh_rilevazioni()
        self._aggiorna_gravita_db()

    def aggiornaRilevazioneGiornaliera(self, vecchio_giorno, vecchia_ora, nuovo_giorno, nuova_ora, glicemia, primaDopoPasto):
        """
        Aggiorna una rilevazione della glicemia esistente.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            UPDATE RILEVAZ_GIORN
            SET giorno = ?, ora = ?, glicemia = ?, primaDopoPasto = ?
            WHERE id_paz = ? AND giorno = ? AND ora = ?
            """
            cursor.execute(query, (nuovo_giorno, nuova_ora, glicemia, primaDopoPasto, self._id_ref, vecchio_giorno, vecchia_ora))
            conn.commit()
            print("Rilevazione aggiornata con successo.")
        except sqlite3.Error as e:
            print(f"Errore nell'aggiornamento della rilevazione: {e}")
        finally:
            conn.close()
        self._refresh_rilevazioni()
        self._aggiorna_gravita_db()

    def eliminaRilevazioneGiornaliera(self, giorno: str, ora: str) -> None:
        """
        Elimina una rilevazione della glicemia.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            DELETE FROM RILEVAZ_GIORN
            WHERE id_paz = ? AND giorno = ? AND ora = ?
            """
            cursor.execute(query, (self._id_ref, giorno, ora))
            conn.commit()
            print("Rilevazione eliminata con successo.")
        except sqlite3.Error as e:
            print(f"Errore nell'eliminazione della rilevazione: {e}")
        finally:
            conn.close()
        self._refresh_rilevazioni()
        self._aggiorna_gravita_db()

    # ==========================================================
    # SEGNALAZIONI (MODELLO PUNTUALE: giorno, ora, sintomo)
    # ==========================================================
    def aggiungiSegnalazione(self, giorno: str, ora: str, sintomo: str, terapia: str = None) -> None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            # Recupera data_inizio solo se c'è una terapia
            data_inizio_val = None
            if terapia:
                cursor.execute(
                    "SELECT data_inizio FROM TERAPIA WHERE id_paz = ? AND farmaco = ? AND data_fine IS NULL",
                    (self._id_ref, terapia)
                )
                row = cursor.fetchone()
                if row:
                    data_inizio_val = row[0]

            # IMPORTANTE: Se non c'è terapia, data_inizio_val deve essere None
            query = """
            INSERT INTO SEGNALAZIONE (id_paz, giorno, ora, sintomo, terapia, data_inizio)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, giorno, ora, sintomo, terapia, data_inizio_val))
            conn.commit()
            print("Segnalazione aggiunta con successo.")
        except sqlite3.Error as e:
            print(f"Errore nell'aggiunta della segnalazione: {e}")
        finally:
            conn.close()

    def getSegnalazioni(self) -> list:
        """
        Recupera tutte le segnalazioni del paziente.
        
        Returns:
            list: Lista di tuple nel formato 
                (giorno (str), ora (str), sintomo (str), terapia (str|None)).
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            SELECT giorno, ora, sintomo, terapia
            FROM SEGNALAZIONE
            WHERE id_paz = ?
            ORDER BY giorno DESC, ora DESC
            """
            cursor.execute(query, (self._id_ref,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore recupero segnalazioni: {e}")
            return []
        finally:
            conn.close()

    def aggiornaSegnalazione(self, vecchio_giorno: str, vecchia_ora: str, 
                             nuovo_giorno: str, nuova_ora: str, sintomo: str, terapia: str) -> None:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            data_inizio_val = None
            if terapia:
                cursor.execute(
                    "SELECT data_inizio FROM TERAPIA WHERE id_paz = ? AND farmaco = ? AND data_fine IS NULL",
                    (self._id_ref, terapia)
                )
                row = cursor.fetchone()
                if row:
                    data_inizio_val = row[0]

            query = """
            UPDATE SEGNALAZIONE
            SET giorno = ?, ora = ?, sintomo = ?, terapia = ?, data_inizio = ?
            WHERE id_paz = ? AND giorno = ? AND ora = ?
            """
            cursor.execute(query, (nuovo_giorno, nuova_ora, sintomo, terapia, data_inizio_val,
                                    self._id_ref, vecchio_giorno, vecchia_ora))
            conn.commit()
            print("Segnalazione aggiornata con successo.")
        except sqlite3.Error as e:
            print(f"Errore aggiornamento segnalazione: {e}")
        finally:
            conn.close()

    def eliminaSegnalazione(self, giorno: str, ora: str) -> None:
        """
        Elimina una segnalazione esistente.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            DELETE FROM SEGNALAZIONE
            WHERE id_paz = ? AND giorno = ? AND ora = ?
            """
            cursor.execute(query, (self._id_ref, giorno, ora))
            conn.commit()
            print("Segnalazione eliminata con successo.")
        except sqlite3.Error as e:
            print(f"Errore eliminazione segnalazione: {e}")
        finally:
            conn.close()

    # ==========================================================
    # ASSUNZIONI
    # ==========================================================
    def aggiungiAssunzione(self, giorno: str, ora: str, farmaco: str, quantita: str) -> None:
        """
        Registra un'assunzione di un farmaco.
        Recupera automaticamente data_inizio dalla terapia attiva.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            # 1. Recupera la data_inizio della terapia attiva per questo farmaco
            cursor.execute(
                "SELECT data_inizio FROM TERAPIA WHERE id_paz = ? AND farmaco = ? AND data_fine IS NULL",
                (self._id_ref, farmaco)
            )
            row = cursor.fetchone()
            
            if row is None:
                print(f"Errore: Nessuna terapia attiva per il farmaco '{farmaco}'.")
                return

            data_inizio_val = row[0]  # <--- QUI PRENDIAMO LA DATA_INIZIO

            # 2. Inserisci l'assunzione con data_inizio
            query = """
            INSERT INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita, data_inizio)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, giorno, ora, farmaco, quantita, data_inizio_val))
            conn.commit()
            print("Assunzione registrata con successo.")
        except sqlite3.Error as e:
            print(f"Errore nella registrazione dell'assunzione: {e}")
        finally:
            conn.close()
        
        self._aggiorna_gravita_db()

    def getAssunzioni(self) -> list:
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            SELECT giorno, ora, farmaco, quantita
            FROM ASSUNZIONE
            WHERE id_paz = ?
            ORDER BY giorno DESC, ora DESC
            """
            cursor.execute(query, (self._id_ref,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore: {e}")
            return []
        finally:
            conn.close()

    def aggiornaAssunzione(self, vecchio_giorno: str, vecchia_ora: str, vecchio_farmaco: str, 
                           nuovo_giorno: str, nuova_ora: str, farmaco: str, quantita: str) -> None:
        """
        Aggiorna un'assunzione esistente.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            # Recupera la data_inizio della terapia attiva per questo farmaco
            cursor.execute(
                "SELECT data_inizio FROM TERAPIA WHERE id_paz = ? AND farmaco = ? AND data_fine IS NULL",
                (self._id_ref, farmaco)
            )
            row = cursor.fetchone()
            
            if row is None:
                print(f"Errore: Nessuna terapia attiva per il farmaco '{farmaco}'.")
                return

            data_inizio_val = row[0]  # <--- QUI PRENDIAMO LA DATA_INIZIO

            query = """
            UPDATE ASSUNZIONE
            SET giorno = ?, ora = ?, farmaco = ?, quantita = ?, data_inizio = ?
            WHERE id_paz = ? AND giorno = ? AND ora = ? AND farmaco = ?
            """
            cursor.execute(query, (nuovo_giorno, nuova_ora, farmaco, quantita, data_inizio_val,
                                   self._id_ref, vecchio_giorno, vecchia_ora, vecchio_farmaco))
            conn.commit()
            print("Assunzione aggiornata con successo.")
        except sqlite3.Error as e:
            print(f"Errore aggiornamento assunzione: {e}")
        finally:
            conn.close()
        
        self._aggiorna_gravita_db()

    def eliminaAssunzione(self, giorno: str, ora: str, farmaco: str) -> None:
        """
        Elimina un'assunzione esistente.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            # Recupera la data_inizio della terapia attiva
            cursor.execute(
                "SELECT data_inizio FROM TERAPIA WHERE id_paz = ? AND farmaco = ? AND data_fine IS NULL",
                (self._id_ref, farmaco)
            )
            row = cursor.fetchone()
            if row is None:
                print(f"Errore: Impossibile trovare data_inizio per il farmaco '{farmaco}'.")
                return
            data_inizio_val = row[0]

            query = """
            DELETE FROM ASSUNZIONE
            WHERE id_paz = ? AND giorno = ? AND ora = ? AND farmaco = ? AND data_inizio = ?
            """
            cursor.execute(query, (self._id_ref, giorno, ora, farmaco, data_inizio_val))
            conn.commit()
            print("Assunzione eliminata con successo.")
        except sqlite3.Error as e:
            print(f"Errore eliminazione assunzione: {e}")
        finally:
            conn.close()
        
        self._aggiorna_gravita_db()

    # ==========================================================
    # ANNOTAZIONE CLINICA
    # ==========================================================
    def getAnnotazione(self) -> str:
        """Restituisce l'annotazione clinica del paziente."""
        return self._annotazione

    def aggiornaAnnotazione(self, testo: str) -> None:
        """Aggiorna l'annotazione clinica nel database e in memoria."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE PAZIENTE SET annotazione = ? WHERE id_paz = ?",
                (testo, self._id_ref)
            )
            conn.commit()
            self._annotazione = testo
        except sqlite3.Error as e:
            print(f"Errore: {e}")
        finally:
            conn.close()

    def __str__(self) -> str:
        return (f"Paziente: {self._nome} {self._cognome} (CF: {self._cf})\n"
                f"Gravità: {self._gravita}\n"
                f"Medico ID: {self._medico_id}")