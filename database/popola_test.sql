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
VALUES (2, 'BNCLCA95A01H501U', 1);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('luca.bianchi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 1);

-- TERAPIE
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med)
VALUES 
(1, 'Metformina', 2, '500 mg', 'Assumere dopo i pasti principali', 1),
(1, 'Insulina Lenta', 1, '10 UI', 'Assumere la sera prima di cena', 1);

-- RILEVAZIONI (Ultimi 30 giorni)
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

-- ASSUNZIONI
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
(1, date('now', '-1 days'), '13:00', 'Metformina', '500 mg'),
(1, date('now', '-1 days'), '20:00', 'Insulina Lenta', '10 UI'),
(1, date('now', '-2 days'), '13:00', 'Metformina', '500 mg'),
(1, date('now', '-2 days'), '20:00', 'Insulina Lenta', '10 UI');

-- SINTOMI
INSERT OR IGNORE INTO SINTOMO (id_paz, giorno, ora, sintomo, terapia) VALUES 
(1, date('now', '-5 days'), '10:00', 'Lieve mal di testa dopo colazione', 'Metformina'),
(1, date('now', '-12 days'), '18:00', 'Sensazione di stanchezza', NULL);

-- database/popola_test.sql

-- ==========================================================
-- MEDICO
-- ==========================================================
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel)
VALUES ('RSSMRA80A01H501Z', 'Mario', 'Rossi', 'M', '1980-01-01', 'Roma', 'mario.rossi@email.com', '333-1234567');

INSERT OR IGNORE INTO MEDICO (CF) VALUES ('RSSMRA80A01H501Z');

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('dott.rossi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 
        (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));


-- ==========================================================
-- PAZIENTE 1: Luca Bianchi — Gravità media (glicemia fuori soglia + terapia)
-- ==========================================================
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('BNCLCA95A01H501U', 'Luca', 'Bianchi', 'M', '1995-01-01', 'Milano', 'Via Roma 10, Milano', 'luca.bianchi@email.com', '333-9876543');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) 
VALUES (0, 'BNCLCA95A01H501U', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('luca.bianchi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P',
        (SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'));

-- Terapie Luca
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med)
VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), 'Metformina', 2, '500 mg', 'Dopo i pasti principali', 
 (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z')),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), 'Insulina Lenta', 1, '10 UI', 'Sera prima di cena', 
 (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Luca (alcune fuori soglia)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-30 days'), '08:00', 145.5, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-28 days'), '20:00', 185.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-25 days'), '08:00', 152.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-20 days'), '14:00', 195.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-15 days'), '08:00', 125.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-10 days'), '08:00', 110.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-5 days'), '20:00', 140.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '08:00', 135.0, 'P');

-- Assunzioni Luca (giorni mancanti = terapia non rispettata)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '13:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '20:00', 'Insulina Lenta', '10 UI'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-3 days'), '13:00', 'Metformina', '500 mg');

-- Sintomi Luca
INSERT OR IGNORE INTO SINTOMO (id_paz, giorno, ora, sintomo, terapia) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-10 days'), '10:00', 'Lieve mal di testa', 'Metformina'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-3 days'), '18:00', 'Stanchezza pomeridiana', NULL);


-- ==========================================================
-- PAZIENTE 2: Maria Verdi — IN REGOLA
-- ==========================================================
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('VRDMRA85B02H502X', 'Maria', 'Verdi', 'F', '1985-06-15', 'Napoli', 'Corso Italia 25, Napoli', 'maria.verdi@email.com', '333-1112223');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) 
VALUES (0, 'VRDMRA85B02H502X', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('maria.verdi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P',
        (SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'));

-- Terapia Maria
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med)
VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), 'Metformina', 1, '500 mg', 'Dopo colazione', 
 (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Maria (tutte in soglia)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-7 days'), '08:00', 105.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-5 days'), '08:00', 98.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-3 days'), '20:00', 120.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-1 days'), '08:00', 92.0, 'P');

-- Assunzioni Maria (tutte regolari)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-7 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-5 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-3 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-1 days'), '09:00', 'Metformina', '500 mg');


-- ==========================================================
-- PAZIENTE 3: Paolo Neri — GRAVE (glicemia molto fuori soglia)
-- ==========================================================
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('NRLPLA70C03H503Y', 'Paolo', 'Neri', 'M', '1970-03-20', 'Torino', 'Via Garibaldi 5, Torino', 'paolo.neri@email.com', '333-4445556');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) 
VALUES (0, 'NRLPLA70C03H503Y', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('paolo.neri', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P',
        (SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'));

-- Terapia Paolo
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med)
VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), 'Metformina', 3, '850 mg', 'Dopo ogni pasto', 
 (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z')),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), 'Glimepiride', 1, '2 mg', 'Prima di colazione', 
 (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Paolo (molte fuori soglia)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-14 days'), '08:00', 175.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-12 days'), '08:00', 168.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-10 days'), '20:00', 220.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-8 days'), '08:00', 182.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-6 days'), '14:00', 210.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-4 days'), '08:00', 160.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-2 days'), '20:00', 198.0, 'D');

-- Assunzioni Paolo (pochissime = terapia gravemente non rispettata)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-2 days'), '09:00', 'Metformina', '850 mg');


-- ==========================================================
-- PAZIENTE 4: Anna Russo — SOLO TERAPIA non rispettata
-- ==========================================================
INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('RSSNNA90D04H504Z', 'Anna', 'Russo', 'F', '1990-04-10', 'Firenze', 'Via dei Pini 8, Firenze', 'anna.russo@email.com', '333-7778889');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico) 
VALUES (0, 'RSSNNA90D04H504Z', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('anna.russo', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P',
        (SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'));

-- Terapia Anna
INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med)
VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), 'Metformina', 2, '500 mg', 'Dopo i pasti', 
 (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Anna (tutte in soglia)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-6 days'), '08:00', 100.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-4 days'), '08:00', 95.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-2 days'), '20:00', 110.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-1 days'), '08:00', 88.0, 'P');

-- Assunzioni Anna (nessuna! terapia completamente non rispettata)
-- NESSUNA ASSUNZIONE