import os
import sqlite3

class Paziente:
    def __init__(self, id_ref, db_path="database/glicocare.db"):
        """
        Inizializza il paziente recuperando tutti i suoi dati dal database.

        Args:
            id_ref (int): L'id del paziente (id_paz nella tabella PAZIENTE).
            db_path (str): Percorso del file database (default: database/glicocare.db).
        """
        self._id_ref = id_ref
        self._db_path = db_path
        
        # Variabili dove salveremo i dati
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
        
        # Liste per i dati recuperati
        self._rilevazioni = []
        self._terapie = []
        
        # Carica i dati dal database appena l'oggetto viene creato
        self._carica_dati()

    def _carica_dati(self):
        """
        Metodo interno (privato) che esegue le query SQL per popolare l'oggetto.
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        try:
            # --- 1. Recupera i dati anagrafici e del paziente (JOIN) ---
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

            # --- 2. Recupera le rilevazioni della glicemia ---
            query_rilevazioni = """
            SELECT giorno, ora, glicemia, primaDopoPasto
            FROM RILEVAZ_GIORN
            WHERE id_paz = ?
            ORDER BY giorno DESC, ora DESC
            """
            cursor.execute(query_rilevazioni, (self._id_ref,))
            self._rilevazioni = cursor.fetchall()
            
            # --- 3. Recupera le terapie del paziente ---
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

    # ==========================================================
    # METODI GETTER (Stile classico getAttributo)
    # ==========================================================
    def getIdRef(self): return self._id_ref
    def getCf(self): return self._cf
    def getNome(self): return self._nome
    def getCognome(self): return self._cognome
    def getSesso(self): return self._sesso
    def getDataNascita(self): return self._data_nascita
    def getLuogoNascita(self): return self._luogo_nascita
    def getIndirizzo(self): return self._indirizzo
    def getEmail(self): return self._email
    def getCel(self): return self._cel
    def getGravita(self): return self._gravita
    def getMedicoId(self): return self._medico_id
    def getRilevazioni(self):
        """Restituisce una lista di tuple (giorno, ora, glicemia, tipo_pasto)"""
        return self._rilevazioni

    def updatePaziente(self):
        print("Calcolo gravità etc")

    # ==========================================================
    # METODI DI RECUPERO DATI (Terapie, Medico, Assunzioni)
    # ==========================================================
    def getTerapie(self):
        """
        Restituisce la lista completa delle terapie del paziente.
        
        Returns:
            list: Lista di tuple (farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med)
        """
        return self._terapie

    def getTerapieByName(self, farmaco):
        """
        Recupera una specifica terapia tramite il nome del farmaco.

        Args:
            farmaco_id (str): Il nome del farmaco (chiave primaria con id_paz).

        Returns:
            tuple|None: Tuple con i dati della terapia (farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med) o None se non trovata.
        """
        for terapia in self._terapie:
            if terapia[0] == farmaco:
                return terapia
        return None

    def getMedicoRiferimento(self):
        """
        Recupera i dati anagrafici del medico di riferimento del paziente.

        Returns:
            tuple: (nome, cognome, email, cel) del medico, oppure None se non trovato.
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
    # METODI DI INSERIMENTO DATI
    # ==========================================================
    def aggiungiRilevazioneGiornaliera(self, giorno, ora, glicemia, primaDopoPasto):
        """
        Aggiunge una nuova rilevazione della glicemia.

        Args:
            giorno (str): Data in formato 'YYYY-MM-DD'.
            ora (str): Ora in formato 'HH:MM'.
            glicemia (float): Valore della glicemia.
            primaDopoPasto (str): 'P' per prima del pasto, 'D' per dopo il pasto.
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

    def aggiungiSintomo(self, giorno, ora, sintomo, terapia=None):
        """
        Aggiunge un nuovo sintomo riportato dal paziente.

        Args:
            giorno (str): Data in formato 'YYYY-MM-DD'.
            ora (str): Ora in formato 'HH:MM'.
            sintomo (str): Descrizione del sintomo.
            terapia (str, optional): Nome del farmaco associato al sintomo (se presente).
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO SINTOMO (id_paz, giorno, ora, sintomo, terapia)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (self._id_ref, giorno, ora, sintomo, terapia))
            conn.commit()
            print("Sintomo aggiunto con successo.")
        except sqlite3.Error as e:
            print(f"Errore nell'aggiunta del sintomo: {e}")
        finally:
            conn.close()

    def aggiungiAssunzione(self, giorno, ora, farmaco, quantita):
        """
        Registra l'assunzione di un farmaco da parte del paziente.

        Args:
            giorno (str): Data in formato 'YYYY-MM-DD'.
            ora (str): Ora in formato 'HH:MM'.
            farmaco (str): Nome del farmaco assunto.
            quantita (str): Quantità assunta (es. '1 compressa', '5 ml').
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        try:
            # Verifica che il farmaco esista nella terapia del paziente
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

    # --- Metodo per stampare un riepilogo del paziente ---
    def __str__(self):
        return (f"Paziente: {self._nome} {self._cognome} (CF: {self._cf})\n"
                f"Gravità: {self._gravita}\n"
                f"Medico ID: {self._medico_id}")