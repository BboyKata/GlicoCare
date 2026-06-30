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
    """
    Rappresenta un paziente e fornisce metodi per interagire con i suoi dati.

    Args:
        id_ref (int): L'ID del paziente (corrisponde a `id_paz` nella tabella PAZIENTE).
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
        self._gravita = None
        self._medico_id = None
        
        self._rilevazioni = []
        self._terapie = []
        self._punti_glicemia = 0
        self._punti_terapia = 0 
        
        self._carica_dati()
        self._aggiorna_gravita_db()

    def _carica_dati(self):
        """
        Carica i dati anagrafici, le rilevazioni e le terapie del paziente dal DB.

        Questo metodo è privato e viene chiamato automaticamente dal costruttore.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        try:
            query_anagrafica = """
            SELECT 
                A.CF, A.nome, A.cognome, A.sesso, A.dataNascita, A.luogoNascita,
                A.indirizzo, A.email, A.cel,
                P.gravita, P.medico
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
             self._email, self._cel, self._gravita, self._medico_id) = row

            query_rilevazioni = """
            SELECT giorno, ora, glicemia, primaDopoPasto
            FROM RILEVAZ_GIORN
            WHERE id_paz = ?
            """
            cursor.execute(query_rilevazioni, (self._id_ref,))
            self._rilevazioni = cursor.fetchall()
            
            query_terapie = """
            SELECT farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med
            FROM TERAPIA
            WHERE id_paz = ?
            """
            cursor.execute(query_terapie, (self._id_ref,))
            self._terapie = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Errore database: {e}")
        finally:
            conn.close()
        
        # Ordina dopo aver caricato tutto
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
        Risultato: giorno più recente in cima, ore nello stesso giorno 
        dalla più mattutina alla più serale.
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
        - Ogni giorno con rilevazioni ma senza assunzioni complete = 1 punto
        
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
            cursor.execute(
                "SELECT farmaco, assunzioniGiornaliere FROM TERAPIA WHERE id_paz = ?",
                (self._id_ref,)
            )
            terapie = cursor.fetchall()
            
            if terapie:
                # Prendi solo i giorni in cui ci sono rilevazioni (giorni "attivi")
                cursor.execute(
                    "SELECT DISTINCT giorno FROM RILEVAZ_GIORN WHERE id_paz = ? ORDER BY giorno",
                    (self._id_ref,)
                )
                giorni_attivi = [row[0] for row in cursor.fetchall()]
                
                # Per ogni giorno con rilevazioni, verifica che tutte le assunzioni siano state fatte
                for giorno in giorni_attivi:
                    for farmaco, assunzioni_previste in terapie:
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
    # TERAPIE E MEDICO
    # ==========================================================
    def getTerapie(self) -> list:
        """
        Restituisce tutte le terapie farmacologiche del paziente.

        Returns:
            list: Lista di tuple nel formato 
                (farmaco (str), assunzioniGiornaliere (int), quantita (str), 
                 indicazioni (str), id_med (int)).
        """
        return self._terapie

    def getTerapieByName(self, farmaco: str) -> tuple:
        """
        Cerca una terapia specifica tramite il nome del farmaco.

        Args:
            farmaco (str): Il nome del farmaco da cercare.

        Returns:
            tuple | None: Tupla della terapia se trovata, altrimenti None.
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
    # INSERIMENTO / MODIFICA / ELIMINAZIONE RILEVAZIONI
    # ==========================================================
    def aggiungiRilevazioneGiornaliera(self, giorno: str, ora: str, glicemia: float, primaDopoPasto: str) -> None:
        """
        Aggiunge una nuova rilevazione della glicemia.

        Dopo l'inserimento, la lista delle rilevazioni viene ricaricata e
        la gravità del paziente viene ricalcolata.

        Args:
            giorno (str): Data della rilevazione nel formato 'YYYY-MM-DD'.
            ora (str): Ora della rilevazione nel formato 'HH:MM'.
            glicemia (float): Valore della glicemia in mg/dL.
            primaDopoPasto (str): 'P' per prima del pasto, 'D' per dopo il pasto.

        Raises:
            sqlite3.IntegrityError: Se esiste già una rilevazione con la stessa data e ora.
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

    def aggiornaRilevazioneGiornaliera(self, vecchio_giorno: str, vecchia_ora: str, nuovo_giorno: str, nuova_ora: str, glicemia: float, primaDopoPasto: str) -> None:
        """
        Aggiorna una rilevazione della glicemia esistente.

        Dopo l'aggiornamento, la lista delle rilevazioni viene ricaricata e
        la gravità del paziente viene ricalcolata.

        Args:
            vecchio_giorno (str): Data originale nel formato 'YYYY-MM-DD'.
            vecchia_ora (str): Ora originale nel formato 'HH:MM'.
            nuovo_giorno (str): Nuova data nel formato 'YYYY-MM-DD'.
            nuova_ora (str): Nuova ora nel formato 'HH:MM'.
            glicemia (float): Nuovo valore della glicemia.
            primaDopoPasto (str): 'P' o 'D'.
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

        Dopo l'eliminazione, la lista delle rilevazioni viene ricaricata e
        la gravità del paziente viene ricalcolata.

        Args:
            giorno (str): Data della rilevazione da eliminare ('YYYY-MM-DD').
            ora (str): Ora della rilevazione da eliminare ('HH:MM').
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
    # SEGNALAZIONI
    # ==========================================================
    def aggiungiSegnalazione(self, giorno_inizio: str, giorno_fine: str, descrizione: str, terapia: str = None) -> None:
        """
        Aggiunge una nuova segnalazione del paziente.

        Args:
            giorno_inizio (str): Data inizio nel formato 'YYYY-MM-DD'.
            giorno_fine (str): Data fine nel formato 'YYYY-MM-DD'.
            descrizione (str): Descrizione della segnalazione.
            terapia (str, optional): Nome del farmaco associato, se presente.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO SEGNALAZIONE (id_paz, giorno_inizio, giorno_fine, descrizione, terapia)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, giorno_inizio, giorno_fine, descrizione, terapia))
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
                (giorno_inizio (str), giorno_fine (str), descrizione (str), terapia (str|None)).
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            SELECT giorno_inizio, giorno_fine, descrizione, terapia
            FROM SEGNALAZIONE
            WHERE id_paz = ?
            ORDER BY giorno_inizio DESC, giorno_fine DESC
            """
            cursor.execute(query, (self._id_ref,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Errore recupero segnalazioni: {e}")
            return []
        finally:
            conn.close()

    def aggiornaSegnalazione(self, vecchio_inizio: str, vecchia_fine: str, 
                             nuovo_inizio: str, nuova_fine: str, descrizione: str, terapia: str) -> None:
        """
        Aggiorna una segnalazione esistente.

        Args:
            vecchio_inizio (str): Data inizio originale ('YYYY-MM-DD').
            vecchia_fine (str): Data fine originale ('YYYY-MM-DD').
            nuovo_inizio (str): Nuova data inizio ('YYYY-MM-DD').
            nuova_fine (str): Nuova data fine ('YYYY-MM-DD').
            descrizione (str): Nuova descrizione.
            terapia (str): Nuovo farmaco associato (può essere None).
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            UPDATE SEGNALAZIONE
            SET giorno_inizio = ?, giorno_fine = ?, descrizione = ?, terapia = ?
            WHERE id_paz = ? AND giorno_inizio = ? AND giorno_fine = ?
            """
            cursor.execute(query, (nuovo_inizio, nuova_fine, descrizione, terapia,
                                self._id_ref, vecchio_inizio, vecchia_fine))
            conn.commit()
            print("Segnalazione aggiornata con successo.")
        except sqlite3.Error as e:
            print(f"Errore aggiornamento segnalazione: {e}")
        finally:
            conn.close()

    def eliminaSegnalazione(self, giorno_inizio: str, giorno_fine: str) -> None:
        """
        Elimina una segnalazione esistente.

        Args:
            giorno_inizio (str): Data inizio della segnalazione ('YYYY-MM-DD').
            giorno_fine (str): Data fine della segnalazione ('YYYY-MM-DD').
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            DELETE FROM SEGNALAZIONE
            WHERE id_paz = ? AND giorno_inizio = ? AND giorno_fine = ?
            """
            cursor.execute(query, (self._id_ref, giorno_inizio, giorno_fine))
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
        Registra un'assunzione di un farmaco da parte del paziente.

        Verifica che il farmaco sia presente nella terapia del paziente prima di
        procedere con l'inserimento.

        Args:
            giorno (str): Data dell'assunzione nel formato 'YYYY-MM-DD'.
            ora (str): Ora dell'assunzione nel formato 'HH:MM'.
            farmaco (str): Nome del farmaco assunto.
            quantita (str): Quantità assunta (es. '1 compressa', '5 ml').
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM TERAPIA WHERE id_paz = ? AND farmaco = ?", (self._id_ref, farmaco))
            if cursor.fetchone() is None:
                print(f"Attenzione: Il farmaco '{farmaco}' non è presente nella terapia del paziente.")
                return

            query = """
            INSERT INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, giorno, ora, farmaco, quantita))
            conn.commit()
            print("Assunzione registrata con successo.")
        except sqlite3.Error as e:
            print(f"Errore nella registrazione dell'assunzione: {e}")
        finally:
            conn.close()
        
        self._aggiorna_gravita_db()

    def getAssunzioni(self) -> list:
        """
        Recupera tutte le assunzioni di farmaci del paziente.

        Returns:
            list: Lista di tuple nel formato 
                (giorno (str), ora (str), farmaco (str), quantita (str)).
        """
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
            print(f"Errore recupero assunzioni: {e}")
            return []
        finally:
            conn.close()

    def aggiornaAssunzione(self, vecchio_giorno: str, vecchia_ora: str, vecchio_farmaco: str, 
                        nuovo_giorno: str, nuova_ora: str, farmaco: str, quantita: str) -> None:
        """
        Aggiorna un'assunzione esistente.

        Args:
            vecchio_giorno (str): Data originale ('YYYY-MM-DD').
            vecchia_ora (str): Ora originale ('HH:MM').
            vecchio_farmaco (str): Nome originale del farmaco.
            nuovo_giorno (str): Nuova data ('YYYY-MM-DD').
            nuova_ora (str): Nuova ora ('HH:MM').
            farmaco (str): Nuovo nome del farmaco.
            quantita (str): Nuova quantità assunta.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            UPDATE ASSUNZIONE
            SET giorno = ?, ora = ?, farmaco = ?, quantita = ?
            WHERE id_paz = ? AND giorno = ? AND ora = ? AND farmaco = ?
            """
            cursor.execute(query, (nuovo_giorno, nuova_ora, farmaco, quantita,
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

        Args:
            giorno (str): Data dell'assunzione ('YYYY-MM-DD').
            ora (str): Ora dell'assunzione ('HH:MM').
            farmaco (str): Nome del farmaco assunto.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            DELETE FROM ASSUNZIONE
            WHERE id_paz = ? AND giorno = ? AND ora = ? AND farmaco = ?
            """
            cursor.execute(query, (self._id_ref, giorno, ora, farmaco))
            conn.commit()
            print("Assunzione eliminata con successo.")
        except sqlite3.Error as e:
            print(f"Errore eliminazione assunzione: {e}")
        finally:
            conn.close()
        
        self._aggiorna_gravita_db()

    def __str__(self) -> str:
        """
        Restituisce una rappresentazione leggibile del paziente.

        Returns:
            str: Stringa riassuntiva dei dati del paziente.
        """
        return (f"Paziente: {self._nome} {self._cognome} (CF: {self._cf})\n"
                f"Gravità: {self._gravita}\n"
                f"Medico ID: {self._medico_id}")