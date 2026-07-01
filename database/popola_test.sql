-- database/popola_test.sql

-- INSERIMENTO MEDICO
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel)
VALUES ('RSSMRA80A01H501Z', 'Mario', 'Rossi', 'M', '1980-01-01', 'Roma', 'mario.rossi@email.com', '333-1234567');

INSERT OR IGNORE INTO MEDICO (CF) VALUES ('RSSMRA80A01H501Z');

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('dott.rossi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 1);

-- INSERIMENTO PAZIENTE
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('BNCLCA95A01H501U', 'Luca', 'Bianchi', 'M', '1995-01-01', 'Milano', 'Via Roma 10, Milano', 'luca.bianchi@email.com', '333-9876543');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) 
VALUES (0, 'BNCLCA95A01H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('luca.bianchi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 1);

-- --- TERAPIE CON DATA_INIZIO E DATA_FINE ---
-- Metformina: prescritta 30 giorni fa, ancora attiva (data_fine NULL)
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (1, 'Metformina', 2, '500 mg', 'Assumere dopo i pasti principali', 1, date('now', '-30 days'));

-- Insulina Lenta: prescritta 15 giorni fa, ancora attiva (data_fine NULL)
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (1, 'Insulina Lenta', 1, '10 UI', 'Assumere la sera prima di cena', 1, date('now', '-15 days'));

-- --- RILEVAZIONI (Ultimi 30 giorni) ---
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(1, date('now', '-30 days'), '08:00', 145.5, 'P'),
(1, date('now', '-29 days'), '08:00', 152.0, 'P'),
(1, date('now', '-28 days'), '20:00', 180.5, 'D'),
(1, date('now', '-27 days'), '08:00', 140.0, 'P'),
(1, date('now', '-26 days'), '20:00', 195.0, 'D'),
(1, date('now', '-25 days'), '08:00', 148.0, 'P'),
(1, date('now', '-24 days'), '14:00', 160.0, 'D'),
(1, date('now', '-23 days'), '08:00', 136.5, 'P'),
(1, date('now', '-22 days'), '20:00', 172.0, 'D'),
(1, date('now', '-21 days'), '08:00', 142.0, 'P');

INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(1, date('now', '-20 days'), '08:00', 130.5, 'P'),
(1, date('now', '-19 days'), '20:00', 158.0, 'D'),
(1, date('now', '-18 days'), '08:00', 125.0, 'P'),
(1, date('now', '-17 days'), '14:00', 165.0, 'D'),
(1, date('now', '-16 days'), '08:00', 120.0, 'P'),
(1, date('now', '-15 days'), '20:00', 145.0, 'D'),
(1, date('now', '-14 days'), '08:00', 118.5, 'P'),
(1, date('now', '-13 days'), '14:00', 148.0, 'D'),
(1, date('now', '-12 days'), '08:00', 110.0, 'P'),
(1, date('now', '-11 days'), '20:00', 135.0, 'D');

INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(1, date('now', '-10 days'), '08:00', 105.0, 'P'),
(1, date('now', '-9 days'), '20:00', 125.0, 'D'),
(1, date('now', '-8 days'), '08:00', 98.0, 'P'),
(1, date('now', '-7 days'), '14:00', 130.0, 'D'),
(1, date('now', '-6 days'), '08:00', 92.0, 'P'),
(1, date('now', '-5 days'), '20:00', 118.0, 'D'),
(1, date('now', '-4 days'), '08:00', 102.5, 'P'),
(1, date('now', '-3 days'), '14:00', 122.0, 'D'),
(1, date('now', '-2 days'), '08:00', 88.0, 'P'),
(1, date('now', '-1 days'), '20:00', 115.0, 'D');

-- --- ASSUNZIONI (ora richiedono data_inizio) ---
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(1, date('now', '-1 days'), '13:00', 'Metformina', date('now', '-30 days'), '500 mg'),
(1, date('now', '-1 days'), '20:00', 'Insulina Lenta', date('now', '-15 days'), '10 UI'),
(1, date('now', '-2 days'), '13:00', 'Metformina', date('now', '-30 days'), '500 mg'),
(1, date('now', '-2 days'), '20:00', 'Insulina Lenta', date('now', '-15 days'), '10 UI');

-- --- SEGNALAZIONE (con data_inizio) ---
INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno, ora, sintomo, terapia, data_inizio) VALUES 
(1, date('now', '-5 days'), '10:00', 'Lieve mal di testa dopo colazione', 'Metformina', date('now', '-30 days'));