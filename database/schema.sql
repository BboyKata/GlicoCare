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

CREATE TABLE IF NOT EXISTS TERAPIA (
    id_paz INTEGER NOT NULL,                          
    farmaco VARCHAR(100) NOT NULL,                    
    assunzioniGiornaliere INTEGER NOT NULL CHECK(assunzioniGiornaliere > 0), 
    quantita VARCHAR(50) NOT NULL,                    
    indicazioni VARCHAR(500),                         
    id_med INTEGER NOT NULL,
    PRIMARY KEY (id_paz, farmaco),
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE,
    FOREIGN KEY (id_med) REFERENCES MEDICO(id_med) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS SINTOMO (
    id_paz INTEGER NOT NULL,                          
    giorno DATE NOT NULL,                             
    ora TIME NOT NULL,                                
    sintomo VARCHAR(200) NOT NULL,                    
    terapia VARCHAR(100),                             
    PRIMARY KEY (id_paz, giorno, ora),
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE,
    FOREIGN KEY (id_paz, terapia) REFERENCES TERAPIA(id_paz, farmaco) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ASSUNZIONE (
    id_paz INTEGER NOT NULL,                          
    giorno DATE NOT NULL,                             
    ora TIME NOT NULL,                                
    farmaco VARCHAR(100) NOT NULL,                    
    quantita VARCHAR(50) NOT NULL,                    
    PRIMARY KEY (id_paz, giorno, ora),
    FOREIGN KEY (id_paz) REFERENCES PAZIENTE(id_paz) ON DELETE CASCADE,
    FOREIGN KEY (id_paz, farmaco) REFERENCES TERAPIA(id_paz, farmaco) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_rilevaz_paziente ON RILEVAZ_GIORN(id_paz);
CREATE INDEX IF NOT EXISTS idx_terapia_paziente ON TERAPIA(id_paz);
CREATE INDEX IF NOT EXISTS idx_sintomo_paziente ON SINTOMO(id_paz);
CREATE INDEX IF NOT EXISTS idx_assunzione_paziente ON ASSUNZIONE(id_paz);

CREATE INDEX IF NOT EXISTS idx_paziente_medico ON PAZIENTE(medico);
CREATE INDEX IF NOT EXISTS idx_terapia_medico ON TERAPIA(id_med);

CREATE INDEX IF NOT EXISTS idx_rilevaz_data ON RILEVAZ_GIORN(giorno);
CREATE INDEX IF NOT EXISTS idx_sintomo_data ON SINTOMO(giorno);
CREATE INDEX IF NOT EXISTS idx_assunzione_data ON ASSUNZIONE(giorno);