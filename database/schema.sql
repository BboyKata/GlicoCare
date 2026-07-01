-- glicocare

CREATE TABLE IF NOT EXISTS ANAGRAFICA (
    CF CHAR(16) PRIMARY KEY,                          
    nome VARCHAR(50) NOT NULL,                        
    cognome VARCHAR(50) NOT NULL,                     
    sesso CHAR(1) CHECK(sesso IN ('M', 'F')) NOT NULL,
    dataNascita DATE NOT NULL,                        
    luogoNascita VARCHAR(100) NOT NULL,               
    indirizzo VARCHAR(200),                           
    email VARCHAR(100) UNIQUE,                        
    cel VARCHAR(20)                                   
);

CREATE TABLE IF NOT EXISTS MEDICO (
    id_med INTEGER PRIMARY KEY AUTOINCREMENT,         
    CF CHAR(16) NOT NULL UNIQUE,                      
    FOREIGN KEY (CF) REFERENCES ANAGRAFICA(CF) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PAZIENTE (
    id_paz INTEGER PRIMARY KEY AUTOINCREMENT,
    gravita INTEGER CHECK(gravita >= 0),
    annotazione TEXT,
    CF CHAR(16) NOT NULL UNIQUE,                     
    medico INTEGER NOT NULL,                        
    FOREIGN KEY (CF) REFERENCES ANAGRAFICA(CF) ON DELETE CASCADE,
    FOREIGN KEY (medico) REFERENCES MEDICO(id_med) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS USER (
    username VARCHAR(50) PRIMARY KEY,                 
    password CHAR(64) NOT NULL,
    tipo CHAR(1) CHECK(tipo IN ('P', 'M')) NOT NULL,
    id_ref INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS RILEVAZ_GIORN (
    id_paz INTEGER NOT NULL,                          
    giorno DATE NOT NULL,                             
    ora TIME NOT NULL,                                
    glicemia REAL NOT NULL,                           
    primaDopoPasto CHAR(1) CHECK(primaDopoPasto IN ('P', 'D')) NOT NULL,
    PRIMARY KEY (id_paz, giorno, ora),
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE
);

-- TERAPIA CON VALIDITÀ TEMPORALE
CREATE TABLE IF NOT EXISTS TERAPIA (
    id_paz INTEGER NOT NULL,                          
    farmaco VARCHAR(100) NOT NULL,                    
    assunzioniGiornaliere INTEGER NOT NULL CHECK(assunzioniGiornaliere > 0), 
    quantita VARCHAR(50) NOT NULL,                    
    indicazioni VARCHAR(500),                         
    id_med INTEGER NOT NULL,
    data_inizio DATE NOT NULL,                        
    data_fine DATE,
    PRIMARY KEY (id_paz, farmaco, data_inizio),      
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE,
    FOREIGN KEY (id_med) REFERENCES MEDICO(id_med) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS SEGNALAZIONE (
    id_paz INTEGER NOT NULL,                          
    giorno DATE NOT NULL,                             
    ora TIME NOT NULL,                                
    sintomo VARCHAR(200) NOT NULL,                    
    terapia VARCHAR(100),                             
    data_inizio DATE DEFAULT NULL,                    -- CAMBIATO DA NOT NULL A DEFAULT NULL
    PRIMARY KEY (id_paz, giorno, ora),
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE,
    FOREIGN KEY (id_paz, terapia, data_inizio) REFERENCES TERAPIA(id_paz, farmaco, data_inizio) ON DELETE SET NULL
);

-- ASSUNZIONE con data_inizio nella FK
CREATE TABLE IF NOT EXISTS ASSUNZIONE (
    id_paz INTEGER NOT NULL,                          
    giorno DATE NOT NULL,                             
    ora TIME NOT NULL,                                
    farmaco VARCHAR(100) NOT NULL,                    
    data_inizio DATE NOT NULL,                        -- Aggiunto per la FK
    quantita VARCHAR(50) NOT NULL,                    
    PRIMARY KEY (id_paz, giorno, ora, farmaco, data_inizio),
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE,
    FOREIGN KEY (id_paz, farmaco, data_inizio) REFERENCES TERAPIA(id_paz, farmaco, data_inizio) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS LOG_OPERAZIONI (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    id_med INTEGER NOT NULL,
    azione VARCHAR(50) NOT NULL,
    tabella VARCHAR(50) NOT NULL,
    id_record VARCHAR(50),
    dettaglio TEXT,
    data_ora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_med) REFERENCES MEDICO(id_med) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_rilevaz_paziente ON RILEVAZ_GIORN(id_paz);
CREATE INDEX IF NOT EXISTS idx_terapia_paziente ON TERAPIA(id_paz);
CREATE INDEX IF NOT EXISTS idx_segnalazione_paziente ON SEGNALAZIONE(id_paz);
CREATE INDEX IF NOT EXISTS idx_assunzione_paziente ON ASSUNZIONE(id_paz);

CREATE INDEX IF NOT EXISTS idx_paziente_medico ON PAZIENTE(medico);
CREATE INDEX IF NOT EXISTS idx_terapia_medico ON TERAPIA(id_med);
CREATE INDEX IF NOT EXISTS idx_terapia_validita ON TERAPIA(data_inizio, data_fine);