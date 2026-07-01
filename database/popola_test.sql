-- database/popola_test.sql

-- =====================================================================
-- 1. INSERIMENTO MEDICI E ANAGRAFICA
-- =====================================================================

-- Dott.ssa Jessica Devescovi
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel)
VALUES ('DVSCST85A01H501Z', 'Jessica', 'Devescovi', 'F', '1985-01-01', 'Verona', 'jessica.devescovi@email.com', '333-1112223');

INSERT OR IGNORE INTO MEDICO (CF) VALUES ('DVSCST85A01H501Z');

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('dott.ssa.jessica', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 1);
-- password: password

-- Dott. Mattia Mantovani
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel)
VALUES ('MNVMTT90B01H501Z', 'Mattia', 'Mantovani', 'M', '1990-02-02', 'Milano', 'mattia.mantovani@email.com', '333-4445556');

INSERT OR IGNORE INTO MEDICO (CF) VALUES ('MNVMTT90B01H501Z');

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('dott.mattia', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 2);
-- password: password


-- =====================================================================
-- 2. PAZIENTI DEL DOTT.SSA JESSICA (6 pazienti)
-- =====================================================================

-- PAZIENTE 1: Luca Bianchi (M) - Glicemia alta, terapia regolare
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('BNCLCA95A01H501U', 'Luca', 'Bianchi', 'M', '1995-01-01', 'Milano', 'Via Roma 10, Milano', 'luca.bianchi@email.com', '333-9876543');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (5, 'BNCLCA95A01H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('luca.bianchi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 1);

-- Terapie di Luca
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (1, 'Metformina', 2, '500 mg', 'Assumere dopo i pasti principali', 1, date('now', '-60 days'), NULL);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (1, 'Insulina Lenta', 1, '10 UI', 'Assumere la sera prima di cena', 1, date('now', '-30 days'), NULL);

-- RILEVAZIONI DI LUCA (30 giorni, con fuori soglia)
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
(1, date('now', '-21 days'), '08:00', 142.0, 'P'),
(1, date('now', '-20 days'), '08:00', 130.5, 'P'),
(1, date('now', '-19 days'), '20:00', 158.0, 'D'),
(1, date('now', '-18 days'), '08:00', 125.0, 'P'),
(1, date('now', '-17 days'), '14:00', 165.0, 'D'),
(1, date('now', '-16 days'), '08:00', 120.0, 'P'),
(1, date('now', '-15 days'), '20:00', 145.0, 'D'),
(1, date('now', '-14 days'), '08:00', 118.5, 'P'),
(1, date('now', '-13 days'), '14:00', 148.0, 'D'),
(1, date('now', '-12 days'), '08:00', 110.0, 'P'),
(1, date('now', '-11 days'), '20:00', 135.0, 'D'),
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

-- Assunzioni di Luca (ultimi 5 giorni)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(1, date('now', '-1 days'), '13:00', 'Metformina', date('now', '-60 days'), '500 mg'),
(1, date('now', '-1 days'), '20:00', 'Insulina Lenta', date('now', '-30 days'), '10 UI'),
(1, date('now', '-2 days'), '13:00', 'Metformina', date('now', '-60 days'), '500 mg'),
(1, date('now', '-2 days'), '20:00', 'Insulina Lenta', date('now', '-30 days'), '10 UI'),
(1, date('now', '-3 days'), '13:00', 'Metformina', date('now', '-60 days'), '500 mg'),
(1, date('now', '-3 days'), '20:00', 'Insulina Lenta', date('now', '-30 days'), '10 UI'),
(1, date('now', '-4 days'), '13:00', 'Metformina', date('now', '-60 days'), '500 mg'),
(1, date('now', '-4 days'), '20:00', 'Insulina Lenta', date('now', '-30 days'), '10 UI');

-- Segnalazioni di Luca
INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno, ora, sintomo, terapia, data_inizio) VALUES 
(1, date('now', '-5 days'), '10:00', 'Lieve mal di testa dopo colazione', 'Metformina', date('now', '-60 days')),
(1, date('now', '-12 days'), '18:00', 'Sensazione di stanchezza', NULL, NULL);


-- PAZIENTE 2: Sara Rossi (F) - Glicemia perfetta, terapia rispettata
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('RSSSRA92B02H501U', 'Sara', 'Rossi', 'F', '1992-02-02', 'Roma', 'Via Garibaldi 5, Roma', 'sara.rossi@email.com', '333-1112223');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (0, 'RSSSRA92B02H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('sara.rossi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 2);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (2, 'Metformina', 1, '500 mg', 'Assumere a colazione', 1, date('now', '-30 days'));

-- RILEVAZIONI DI SARA (30 giorni, tutte in regola)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(2, date('now', '-30 days'), '08:00', 95.0, 'P'),
(2, date('now', '-29 days'), '08:00', 102.0, 'P'),
(2, date('now', '-28 days'), '20:00', 120.0, 'D'),
(2, date('now', '-27 days'), '08:00', 88.0, 'P'),
(2, date('now', '-26 days'), '20:00', 115.0, 'D'),
(2, date('now', '-25 days'), '08:00', 92.0, 'P'),
(2, date('now', '-24 days'), '20:00', 118.0, 'D'),
(2, date('now', '-23 days'), '08:00', 97.0, 'P'),
(2, date('now', '-22 days'), '20:00', 125.0, 'D'),
(2, date('now', '-21 days'), '08:00', 100.0, 'P'),
(2, date('now', '-20 days'), '08:00', 105.0, 'P'),
(2, date('now', '-19 days'), '20:00', 130.0, 'D'),
(2, date('now', '-18 days'), '08:00', 98.0, 'P'),
(2, date('now', '-17 days'), '20:00', 125.0, 'D'),
(2, date('now', '-16 days'), '08:00', 88.0, 'P'),
(2, date('now', '-15 days'), '20:00', 118.0, 'D'),
(2, date('now', '-14 days'), '08:00', 92.0, 'P'),
(2, date('now', '-13 days'), '20:00', 122.0, 'D'),
(2, date('now', '-12 days'), '08:00', 97.0, 'P'),
(2, date('now', '-11 days'), '20:00', 120.0, 'D'),
(2, date('now', '-10 days'), '08:00', 95.0, 'P'),
(2, date('now', '-9 days'), '20:00', 125.0, 'D'),
(2, date('now', '-8 days'), '08:00', 100.0, 'P'),
(2, date('now', '-7 days'), '20:00', 130.0, 'D'),
(2, date('now', '-6 days'), '08:00', 98.0, 'P'),
(2, date('now', '-5 days'), '20:00', 125.0, 'D'),
(2, date('now', '-4 days'), '08:00', 88.0, 'P'),
(2, date('now', '-3 days'), '20:00', 118.0, 'D'),
(2, date('now', '-2 days'), '08:00', 92.0, 'P'),
(2, date('now', '-1 days'), '20:00', 122.0, 'D');

-- Assunzioni di Sara
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(2, date('now', '-1 days'), '08:00', 'Metformina', date('now', '-30 days'), '500 mg'),
(2, date('now', '-2 days'), '08:00', 'Metformina', date('now', '-30 days'), '500 mg'),
(2, date('now', '-3 days'), '08:00', 'Metformina', date('now', '-30 days'), '500 mg');


-- PAZIENTE 3: Marco Verdi (M) - Glicemia fuori soglia, terapia non rispettata
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('VRDMCO88C03H501U', 'Marco', 'Verdi', 'M', '1988-03-03', 'Torino', 'Via Verdi 8, Torino', 'marco.verdi@email.com', '333-5556667');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (8, 'VRDMCO88C03H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('marco.verdi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 3);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (3, 'Metformina', 2, '500 mg', 'Assumere dopo i pasti', 1, date('now', '-60 days'), date('now', '-10 days'));

-- RILEVAZIONI MARCO (30 giorni, tutte fuori soglia)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(3, date('now', '-30 days'), '08:00', 220.0, 'P'),
(3, date('now', '-29 days'), '08:00', 210.0, 'P'),
(3, date('now', '-28 days'), '20:00', 260.0, 'D'),
(3, date('now', '-27 days'), '08:00', 180.0, 'P'),
(3, date('now', '-26 days'), '20:00', 250.0, 'D'),
(3, date('now', '-25 days'), '08:00', 215.0, 'P'),
(3, date('now', '-24 days'), '14:00', 230.0, 'D'),
(3, date('now', '-23 days'), '08:00', 195.0, 'P'),
(3, date('now', '-22 days'), '20:00', 270.0, 'D'),
(3, date('now', '-21 days'), '08:00', 200.0, 'P'),
(3, date('now', '-20 days'), '08:00', 185.0, 'P'),
(3, date('now', '-19 days'), '20:00', 240.0, 'D'),
(3, date('now', '-18 days'), '08:00', 170.0, 'P'),
(3, date('now', '-17 days'), '14:00', 210.0, 'D'),
(3, date('now', '-16 days'), '08:00', 190.0, 'P'),
(3, date('now', '-15 days'), '20:00', 230.0, 'D'),
(3, date('now', '-14 days'), '08:00', 160.0, 'P'),
(3, date('now', '-13 days'), '14:00', 200.0, 'D'),
(3, date('now', '-12 days'), '08:00', 180.0, 'P'),
(3, date('now', '-11 days'), '20:00', 220.0, 'D'),
(3, date('now', '-10 days'), '08:00', 150.0, 'P'),
(3, date('now', '-9 days'), '20:00', 190.0, 'D'),
(3, date('now', '-8 days'), '08:00', 140.0, 'P'),
(3, date('now', '-7 days'), '14:00', 180.0, 'D'),
(3, date('now', '-6 days'), '08:00', 130.0, 'P'),
(3, date('now', '-5 days'), '20:00', 170.0, 'D'),
(3, date('now', '-4 days'), '08:00', 120.0, 'P'),
(3, date('now', '-3 days'), '14:00', 160.0, 'D'),
(3, date('now', '-2 days'), '08:00', 110.0, 'P'),
(3, date('now', '-1 days'), '20:00', 150.0, 'D');


-- PAZIENTE 4: Giulia Neri (F) - Glicemia ok, terapia non rispettata
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('NRIGLU90D04H501U', 'Giulia', 'Neri', 'F', '1990-04-04', 'Firenze', 'Via Dante 12, Firenze', 'giulia.neri@email.com', '333-7778889');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (3, 'NRIGLU90D04H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('giulia.neri', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 4);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (4, 'Insulina Lenta', 1, '10 UI', 'Assumere prima di cena', 1, date('now', '-20 days'));

-- RILEVAZIONI GIULIA (pochi dati, ma in regola)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(4, date('now', '-30 days'), '08:00', 92.0, 'P'),
(4, date('now', '-29 days'), '08:00', 88.0, 'P'),
(4, date('now', '-28 days'), '20:00', 118.0, 'D'),
(4, date('now', '-27 days'), '08:00', 97.0, 'P'),
(4, date('now', '-26 days'), '20:00', 122.0, 'D'),
(4, date('now', '-25 days'), '08:00', 100.0, 'P'),
(4, date('now', '-24 days'), '20:00', 125.0, 'D'),
(4, date('now', '-23 days'), '08:00', 98.0, 'P'),
(4, date('now', '-22 days'), '20:00', 130.0, 'D'),
(4, date('now', '-21 days'), '08:00', 88.0, 'P'),
(4, date('now', '-20 days'), '20:00', 118.0, 'D'),
(4, date('now', '-19 days'), '08:00', 92.0, 'P'),
(4, date('now', '-18 days'), '20:00', 122.0, 'D'),
(4, date('now', '-17 days'), '08:00', 97.0, 'P'),
(4, date('now', '-16 days'), '20:00', 125.0, 'D'),
(4, date('now', '-15 days'), '08:00', 100.0, 'P'),
(4, date('now', '-14 days'), '20:00', 130.0, 'D'),
(4, date('now', '-13 days'), '08:00', 98.0, 'P'),
(4, date('now', '-12 days'), '20:00', 118.0, 'D'),
(4, date('now', '-11 days'), '08:00', 92.0, 'P'),
(4, date('now', '-10 days'), '20:00', 122.0, 'D'),
(4, date('now', '-9 days'), '08:00', 97.0, 'P'),
(4, date('now', '-8 days'), '20:00', 125.0, 'D'),
(4, date('now', '-7 days'), '08:00', 100.0, 'P'),
(4, date('now', '-6 days'), '20:00', 130.0, 'D'),
(4, date('now', '-5 days'), '08:00', 98.0, 'P'),
(4, date('now', '-4 days'), '20:00', 118.0, 'D'),
(4, date('now', '-3 days'), '08:00', 92.0, 'P'),
(4, date('now', '-2 days'), '20:00', 122.0, 'D'),
(4, date('now', '-1 days'), '08:00', 97.0, 'P');


-- PAZIENTE 5: Alessandro Conti (M)
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('CNTLSN91E05H501U', 'Alessandro', 'Conti', 'M', '1991-05-05', 'Bologna', 'Via Emilia 15, Bologna', 'alessandro.conti@email.com', '333-9990001');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (5, 'CNTLSN91E05H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('alessandro.conti', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 5);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (5, 'Insulina Lenta', 1, '10 UI', 'Assumere prima di cena', 1, date('now', '-15 days'));

-- RILEVAZIONI ALESSANDRO
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(5, date('now', '-30 days'), '08:00', 195.0, 'P'),
(5, date('now', '-29 days'), '08:00', 180.0, 'P'),
(5, date('now', '-28 days'), '20:00', 220.0, 'D'),
(5, date('now', '-27 days'), '08:00', 190.0, 'P'),
(5, date('now', '-26 days'), '20:00', 210.0, 'D'),
(5, date('now', '-25 days'), '08:00', 175.0, 'P'),
(5, date('now', '-24 days'), '20:00', 230.0, 'D'),
(5, date('now', '-23 days'), '08:00', 165.0, 'P'),
(5, date('now', '-22 days'), '20:00', 200.0, 'D'),
(5, date('now', '-21 days'), '08:00', 155.0, 'P'),
(5, date('now', '-20 days'), '20:00', 190.0, 'D'),
(5, date('now', '-19 days'), '08:00', 145.0, 'P'),
(5, date('now', '-18 days'), '20:00', 180.0, 'D'),
(5, date('now', '-17 days'), '08:00', 135.0, 'P'),
(5, date('now', '-16 days'), '20:00', 170.0, 'D'),
(5, date('now', '-15 days'), '08:00', 125.0, 'P'),
(5, date('now', '-14 days'), '20:00', 160.0, 'D'),
(5, date('now', '-13 days'), '08:00', 115.0, 'P'),
(5, date('now', '-12 days'), '20:00', 150.0, 'D'),
(5, date('now', '-11 days'), '08:00', 105.0, 'P'),
(5, date('now', '-10 days'), '20:00', 140.0, 'D'),
(5, date('now', '-9 days'), '08:00', 95.0, 'P'),
(5, date('now', '-8 days'), '20:00', 130.0, 'D'),
(5, date('now', '-7 days'), '08:00', 85.0, 'P'),
(5, date('now', '-6 days'), '20:00', 120.0, 'D'),
(5, date('now', '-5 days'), '08:00', 75.0, 'P'),
(5, date('now', '-4 days'), '20:00', 110.0, 'D'),
(5, date('now', '-3 days'), '08:00', 65.0, 'P'),
(5, date('now', '-2 days'), '20:00', 100.0, 'D'),
(5, date('now', '-1 days'), '08:00', 55.0, 'P');


-- PAZIENTE 6: Elena Moretti (F) - In regola
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('MRTLNE93F06H501U', 'Elena', 'Moretti', 'F', '1993-06-06', 'Genova', 'Via Colombo 20, Genova', 'elena.moretti@email.com', '333-2223334');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (0, 'MRTLNE93F06H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('elena.moretti', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 6);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (6, 'Metformina', 1, '500 mg', 'Assumere a colazione', 1, date('now', '-30 days'));

-- RILEVAZIONI ELENA (in regola)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(6, date('now', '-30 days'), '08:00', 95.0, 'P'),
(6, date('now', '-29 days'), '08:00', 102.0, 'P'),
(6, date('now', '-28 days'), '20:00', 120.0, 'D'),
(6, date('now', '-27 days'), '08:00', 88.0, 'P'),
(6, date('now', '-26 days'), '20:00', 115.0, 'D'),
(6, date('now', '-25 days'), '08:00', 92.0, 'P'),
(6, date('now', '-24 days'), '20:00', 118.0, 'D'),
(6, date('now', '-23 days'), '08:00', 97.0, 'P'),
(6, date('now', '-22 days'), '20:00', 125.0, 'D'),
(6, date('now', '-21 days'), '08:00', 100.0, 'P'),
(6, date('now', '-20 days'), '08:00', 105.0, 'P'),
(6, date('now', '-19 days'), '20:00', 130.0, 'D'),
(6, date('now', '-18 days'), '08:00', 98.0, 'P'),
(6, date('now', '-17 days'), '20:00', 125.0, 'D'),
(6, date('now', '-16 days'), '08:00', 88.0, 'P'),
(6, date('now', '-15 days'), '20:00', 118.0, 'D'),
(6, date('now', '-14 days'), '08:00', 92.0, 'P'),
(6, date('now', '-13 days'), '20:00', 122.0, 'D'),
(6, date('now', '-12 days'), '08:00', 97.0, 'P'),
(6, date('now', '-11 days'), '20:00', 120.0, 'D'),
(6, date('now', '-10 days'), '08:00', 95.0, 'P'),
(6, date('now', '-9 days'), '20:00', 125.0, 'D'),
(6, date('now', '-8 days'), '08:00', 100.0, 'P'),
(6, date('now', '-7 days'), '20:00', 130.0, 'D'),
(6, date('now', '-6 days'), '08:00', 98.0, 'P'),
(6, date('now', '-5 days'), '20:00', 125.0, 'D'),
(6, date('now', '-4 days'), '08:00', 88.0, 'P'),
(6, date('now', '-3 days'), '20:00', 118.0, 'D'),
(6, date('now', '-2 days'), '08:00', 92.0, 'P'),
(6, date('now', '-1 days'), '20:00', 122.0, 'D');


-- =====================================================================
-- 3. PAZIENTI DEL DOTT. MATTIA (6 pazienti)
-- =====================================================================

-- PAZIENTE 7: Francesco Bianco (M) - Glicemia alta
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('BNCFRC94G07H501U', 'Francesco', 'Bianco', 'M', '1994-07-07', 'Palermo', 'Via Roma 30, Palermo', 'francesco.bianco@email.com', '333-4445556');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (6, 'BNCFRC94G07H501U', 2);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('francesco.bianco', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 7);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (7, 'Metformina', 2, '500 mg', 'Dopo i pasti', 2, date('now', '-30 days'));

-- RILEVAZIONI FRANCESCO
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(7, date('now', '-30 days'), '08:00', 155.0, 'P'),
(7, date('now', '-29 days'), '08:00', 165.0, 'P'),
(7, date('now', '-28 days'), '20:00', 190.0, 'D'),
(7, date('now', '-27 days'), '08:00', 145.0, 'P'),
(7, date('now', '-26 days'), '20:00', 200.0, 'D'),
(7, date('now', '-25 days'), '08:00', 135.0, 'P'),
(7, date('now', '-24 days'), '20:00', 180.0, 'D'),
(7, date('now', '-23 days'), '08:00', 125.0, 'P'),
(7, date('now', '-22 days'), '20:00', 170.0, 'D'),
(7, date('now', '-21 days'), '08:00', 115.0, 'P'),
(7, date('now', '-20 days'), '20:00', 160.0, 'D'),
(7, date('now', '-19 days'), '08:00', 105.0, 'P'),
(7, date('now', '-18 days'), '20:00', 150.0, 'D'),
(7, date('now', '-17 days'), '08:00', 95.0, 'P'),
(7, date('now', '-16 days'), '20:00', 140.0, 'D'),
(7, date('now', '-15 days'), '08:00', 85.0, 'P'),
(7, date('now', '-14 days'), '20:00', 130.0, 'D'),
(7, date('now', '-13 days'), '08:00', 75.0, 'P'),
(7, date('now', '-12 days'), '20:00', 120.0, 'D'),
(7, date('now', '-11 days'), '08:00', 65.0, 'P'),
(7, date('now', '-10 days'), '20:00', 110.0, 'D'),
(7, date('now', '-9 days'), '08:00', 55.0, 'P'),
(7, date('now', '-8 days'), '20:00', 100.0, 'D'),
(7, date('now', '-7 days'), '08:00', 45.0, 'P'),
(7, date('now', '-6 days'), '20:00', 90.0, 'D'),
(7, date('now', '-5 days'), '08:00', 35.0, 'P'),
(7, date('now', '-4 days'), '20:00', 80.0, 'D'),
(7, date('now', '-3 days'), '08:00', 25.0, 'P'),
(7, date('now', '-2 days'), '20:00', 70.0, 'D'),
(7, date('now', '-1 days'), '08:00', 15.0, 'P');


-- PAZIENTE 8: Laura Verdi (F)
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('VRDLRA95H08H501U', 'Laura', 'Verdi', 'F', '1995-08-08', 'Napoli', 'Via Toledo 25, Napoli', 'laura.verdi@email.com', '333-6667778');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (2, 'VRDLRA95H08H501U', 2);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('laura.verdi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 8);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (8, 'Insulina Lenta', 1, '10 UI', 'Prima di cena', 2, date('now', '-30 days'));

-- RILEVAZIONI LAURA
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(8, date('now', '-30 days'), '08:00', 98.0, 'P'),
(8, date('now', '-29 days'), '08:00', 105.0, 'P'),
(8, date('now', '-28 days'), '20:00', 122.0, 'D'),
(8, date('now', '-27 days'), '08:00', 88.0, 'P'),
(8, date('now', '-26 days'), '20:00', 115.0, 'D'),
(8, date('now', '-25 days'), '08:00', 92.0, 'P'),
(8, date('now', '-24 days'), '20:00', 118.0, 'D'),
(8, date('now', '-23 days'), '08:00', 97.0, 'P'),
(8, date('now', '-22 days'), '20:00', 125.0, 'D'),
(8, date('now', '-21 days'), '08:00', 100.0, 'P'),
(8, date('now', '-20 days'), '08:00', 105.0, 'P'),
(8, date('now', '-19 days'), '20:00', 130.0, 'D'),
(8, date('now', '-18 days'), '08:00', 98.0, 'P'),
(8, date('now', '-17 days'), '20:00', 125.0, 'D'),
(8, date('now', '-16 days'), '08:00', 88.0, 'P'),
(8, date('now', '-15 days'), '20:00', 118.0, 'D'),
(8, date('now', '-14 days'), '08:00', 92.0, 'P'),
(8, date('now', '-13 days'), '20:00', 122.0, 'D'),
(8, date('now', '-12 days'), '08:00', 97.0, 'P'),
(8, date('now', '-11 days'), '20:00', 120.0, 'D'),
(8, date('now', '-10 days'), '08:00', 95.0, 'P'),
(8, date('now', '-9 days'), '20:00', 125.0, 'D'),
(8, date('now', '-8 days'), '08:00', 100.0, 'P'),
(8, date('now', '-7 days'), '20:00', 130.0, 'D'),
(8, date('now', '-6 days'), '08:00', 98.0, 'P'),
(8, date('now', '-5 days'), '20:00', 125.0, 'D'),
(8, date('now', '-4 days'), '08:00', 88.0, 'P'),
(8, date('now', '-3 days'), '20:00', 118.0, 'D'),
(8, date('now', '-2 days'), '08:00', 92.0, 'P'),
(8, date('now', '-1 days'), '20:00', 122.0, 'D');


-- PAZIENTE 9: Marco Neri (M)
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('NRIMRC96I09H501U', 'Marco', 'Neri', 'M', '1996-09-09', 'Bari', 'Via Dante 18, Bari', 'marco.neri@email.com', '333-8889990');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (4, 'NRIMRC96I09H501U', 2);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('marco.neri', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 9);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (9, 'Metformina', 2, '500 mg', 'Dopo i pasti', 2, date('now', '-10 days'));

-- RILEVAZIONI MARCO
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(9, date('now', '-30 days'), '08:00', 89.0, 'P'),
(9, date('now', '-29 days'), '08:00', 93.0, 'P'),
(9, date('now', '-28 days'), '20:00', 112.0, 'D'),
(9, date('now', '-27 days'), '08:00', 85.0, 'P'),
(9, date('now', '-26 days'), '20:00', 115.0, 'D'),
(9, date('now', '-25 days'), '08:00', 92.0, 'P'),
(9, date('now', '-24 days'), '20:00', 118.0, 'D'),
(9, date('now', '-23 days'), '08:00', 97.0, 'P'),
(9, date('now', '-22 days'), '20:00', 125.0, 'D'),
(9, date('now', '-21 days'), '08:00', 100.0, 'P'),
(9, date('now', '-20 days'), '08:00', 105.0, 'P'),
(9, date('now', '-19 days'), '20:00', 130.0, 'D'),
(9, date('now', '-18 days'), '08:00', 98.0, 'P'),
(9, date('now', '-17 days'), '20:00', 125.0, 'D'),
(9, date('now', '-16 days'), '08:00', 88.0, 'P'),
(9, date('now', '-15 days'), '20:00', 118.0, 'D'),
(9, date('now', '-14 days'), '08:00', 92.0, 'P'),
(9, date('now', '-13 days'), '20:00', 122.0, 'D'),
(9, date('now', '-12 days'), '08:00', 97.0, 'P'),
(9, date('now', '-11 days'), '20:00', 120.0, 'D'),
(9, date('now', '-10 days'), '08:00', 95.0, 'P'),
(9, date('now', '-9 days'), '20:00', 125.0, 'D'),
(9, date('now', '-8 days'), '08:00', 100.0, 'P'),
(9, date('now', '-7 days'), '20:00', 130.0, 'D'),
(9, date('now', '-6 days'), '08:00', 98.0, 'P'),
(9, date('now', '-5 days'), '20:00', 125.0, 'D'),
(9, date('now', '-4 days'), '08:00', 88.0, 'P'),
(9, date('now', '-3 days'), '20:00', 118.0, 'D'),
(9, date('now', '-2 days'), '08:00', 92.0, 'P'),
(9, date('now', '-1 days'), '20:00', 122.0, 'D');


-- PAZIENTE 10: Giulia Rossi (F)
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('RSSGLU97J10H501U', 'Giulia', 'Rossi', 'F', '1997-10-10', 'Cagliari', 'Via Garibaldi 22, Cagliari', 'giulia.rossi@email.com', '333-0001112');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (1, 'RSSGLU97J10H501U', 2);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('giulia.rossi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 10);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (10, 'Metformina', 1, '500 mg', 'Colazione', 2, date('now', '-20 days'));

-- RILEVAZIONI GIULIA
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(10, date('now', '-30 days'), '08:00', 95.0, 'P'),
(10, date('now', '-29 days'), '08:00', 102.0, 'P'),
(10, date('now', '-28 days'), '20:00', 120.0, 'D'),
(10, date('now', '-27 days'), '08:00', 88.0, 'P'),
(10, date('now', '-26 days'), '20:00', 115.0, 'D'),
(10, date('now', '-25 days'), '08:00', 92.0, 'P'),
(10, date('now', '-24 days'), '20:00', 118.0, 'D'),
(10, date('now', '-23 days'), '08:00', 97.0, 'P'),
(10, date('now', '-22 days'), '20:00', 125.0, 'D'),
(10, date('now', '-21 days'), '08:00', 100.0, 'P'),
(10, date('now', '-20 days'), '08:00', 105.0, 'P'),
(10, date('now', '-19 days'), '20:00', 130.0, 'D'),
(10, date('now', '-18 days'), '08:00', 98.0, 'P'),
(10, date('now', '-17 days'), '20:00', 125.0, 'D'),
(10, date('now', '-16 days'), '08:00', 88.0, 'P'),
(10, date('now', '-15 days'), '20:00', 118.0, 'D'),
(10, date('now', '-14 days'), '08:00', 92.0, 'P'),
(10, date('now', '-13 days'), '20:00', 122.0, 'D'),
(10, date('now', '-12 days'), '08:00', 97.0, 'P'),
(10, date('now', '-11 days'), '20:00', 120.0, 'D'),
(10, date('now', '-10 days'), '08:00', 95.0, 'P'),
(10, date('now', '-9 days'), '20:00', 125.0, 'D'),
(10, date('now', '-8 days'), '08:00', 100.0, 'P'),
(10, date('now', '-7 days'), '20:00', 130.0, 'D'),
(10, date('now', '-6 days'), '08:00', 98.0, 'P'),
(10, date('now', '-5 days'), '20:00', 125.0, 'D'),
(10, date('now', '-4 days'), '08:00', 88.0, 'P'),
(10, date('now', '-3 days'), '20:00', 118.0, 'D'),
(10, date('now', '-2 days'), '08:00', 92.0, 'P'),
(10, date('now', '-1 days'), '20:00', 122.0, 'D');


-- PAZIENTE 11: Carlo Bianchi (M)
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('BNCCRL98K11H501U', 'Carlo', 'Bianchi', 'M', '1998-11-11', 'Trieste', 'Via Roma 15, Trieste', 'carlo.bianchi@email.com', '333-3334445');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (0, 'BNCCRL98K11H501U', 2);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('carlo.bianchi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 11);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (11, 'Metformina', 1, '500 mg', 'Colazione', 2, date('now', '-30 days'));

-- RILEVAZIONI CARLO
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(11, date('now', '-30 days'), '08:00', 92.0, 'P'),
(11, date('now', '-29 days'), '08:00', 97.0, 'P'),
(11, date('now', '-28 days'), '20:00', 112.0, 'D'),
(11, date('now', '-27 days'), '08:00', 88.0, 'P'),
(11, date('now', '-26 days'), '20:00', 115.0, 'D'),
(11, date('now', '-25 days'), '08:00', 92.0, 'P'),
(11, date('now', '-24 days'), '20:00', 118.0, 'D'),
(11, date('now', '-23 days'), '08:00', 97.0, 'P'),
(11, date('now', '-22 days'), '20:00', 125.0, 'D'),
(11, date('now', '-21 days'), '08:00', 100.0, 'P'),
(11, date('now', '-20 days'), '08:00', 105.0, 'P'),
(11, date('now', '-19 days'), '20:00', 130.0, 'D'),
(11, date('now', '-18 days'), '08:00', 98.0, 'P'),
(11, date('now', '-17 days'), '20:00', 125.0, 'D'),
(11, date('now', '-16 days'), '08:00', 88.0, 'P'),
(11, date('now', '-15 days'), '20:00', 118.0, 'D'),
(11, date('now', '-14 days'), '08:00', 92.0, 'P'),
(11, date('now', '-13 days'), '20:00', 122.0, 'D'),
(11, date('now', '-12 days'), '08:00', 97.0, 'P'),
(11, date('now', '-11 days'), '20:00', 120.0, 'D'),
(11, date('now', '-10 days'), '08:00', 95.0, 'P'),
(11, date('now', '-9 days'), '20:00', 125.0, 'D'),
(11, date('now', '-8 days'), '08:00', 100.0, 'P'),
(11, date('now', '-7 days'), '20:00', 130.0, 'D'),
(11, date('now', '-6 days'), '08:00', 98.0, 'P'),
(11, date('now', '-5 days'), '20:00', 125.0, 'D'),
(11, date('now', '-4 days'), '08:00', 88.0, 'P'),
(11, date('now', '-3 days'), '20:00', 118.0, 'D'),
(11, date('now', '-2 days'), '08:00', 92.0, 'P'),
(11, date('now', '-1 days'), '20:00', 122.0, 'D');


-- PAZIENTE 12: Anna Neri (F) - Con una terapia conclusa e una attiva
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('NRINNA99L12H501U', 'Anna', 'Neri', 'F', '1999-12-12', 'Ancona', 'Via Dante 30, Ancona', 'anna.neri@email.com', '333-5556667');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) VALUES (2, 'NRINNA99L12H501U', 2);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('anna.neri', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 12);

-- Terapia passata
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (12, 'Metformina', 2, '500 mg', 'Dopo i pasti', 2, date('now', '-90 days'), date('now', '-30 days'));

-- Terapia attuale
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
VALUES (12, 'Insulina Lenta', 1, '10 UI', 'Prima di cena', 2, date('now', '-30 days'));


-- =====================================================================
-- 4. LOG OPERAZIONI (esempi)
-- =====================================================================

INSERT INTO LOG_OPERAZIONI (id_med, azione, tabella, id_record, dettaglio) VALUES
(1, 'PRESCRIZIONE_TERAPIA', 'TERAPIA', '1/Metformina', 'Prescritta Metformina 500 mg per Luca Bianchi'),
(1, 'MODIFICA_ANNOTAZIONE', 'PAZIENTE', '1', 'Annotazione aggiornata: Rischio cardiovascolare moderato'),
(2, 'INTERRUZIONE_TERAPIA', 'TERAPIA', '12/Metformina', 'Interrotta Metformina per Anna Neri'),
(2, 'VISUALIZZA_DETTAGLIO', 'PAZIENTE', '8', 'Visualizzato dettaglio Laura Verdi');