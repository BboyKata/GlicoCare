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
-- PAZIENTE 1: Luca Bianchi — Gravità media
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
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), 'Metformina', 2, '500 mg', 'Dopo i pasti principali', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z')),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), 'Insulina Lenta', 1, '10 UI', 'Sera prima di cena', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Luca: copertura ~90 giorni (circa 40 rilevazioni)
-- Periodo -90..-31 giorni
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-88 days'), '08:00', 148.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-85 days'), '20:00', 178.5, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-81 days'), '08:00', 155.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-78 days'), '14:00', 162.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-74 days'), '08:00', 142.5, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-71 days'), '20:00', 159.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-67 days'), '08:00', 138.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-64 days'), '14:00', 175.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-60 days'), '08:00', 132.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-57 days'), '20:00', 188.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-53 days'), '08:00', 141.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-50 days'), '14:00', 169.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-46 days'), '08:00', 127.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-43 days'), '20:00', 154.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-39 days'), '08:00', 136.5, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-36 days'), '14:00', 182.0, 'D');

-- Periodo -30..-8 giorni (già presenti alcune; aggiungiamo altre)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-30 days'), '08:00', 145.5, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-28 days'), '20:00', 185.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-25 days'), '08:00', 152.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-23 days'), '14:00', 170.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-20 days'), '14:00', 195.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-18 days'), '08:00', 129.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-15 days'), '08:00', 125.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-13 days'), '20:00', 168.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-10 days'), '08:00', 110.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-8 days'), '14:00', 149.0, 'D');

-- Ultima settimana (giorni -7..-1, più fitte)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-7 days'), '08:00', 118.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-6 days'), '20:00', 142.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-5 days'), '20:00', 140.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-4 days'), '08:00', 105.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-3 days'), '14:00', 132.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-2 days'), '08:00', 98.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '08:00', 135.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '20:00', 163.0, 'D');

-- Assunzioni Luca (alcuni giorni mancanti per generare punti terapia)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '13:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-1 days'), '20:00', 'Insulina Lenta', '10 UI'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-3 days'), '13:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-4 days'), '20:00', 'Insulina Lenta', '10 UI'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-7 days'), '13:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-7 days'), '20:00', 'Insulina Lenta', '10 UI'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-10 days'), '13:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-10 days'), '20:00', 'Insulina Lenta', '10 UI'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-15 days'), '13:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-15 days'), '20:00', 'Insulina Lenta', '10 UI');

-- Segnalazioni Luca
INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno_inizio, giorno_fine, descrizione, terapia) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-12 days'), date('now', '-10 days'), 'Lieve mal di testa dopo colazione', 'Metformina'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'BNCLCA95A01H501U'), date('now', '-5 days'), date('now', '-3 days'), 'Sensazione di stanchezza pomeridiana', NULL);

-- Annotazione Luca
UPDATE PAZIENTE SET annotazione = 'Fumatore (10 sigarette/die). Lieve ipertensione. Familiarità per diabete di tipo 2 (padre). BMI: 28.5.'
WHERE CF = 'BNCLCA95A01H501U';


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
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), 'Metformina', 1, '500 mg', 'Dopo colazione', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Maria: aggiungiamo dati per 60 giorni (1 misura ogni 2-3 gg)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-58 days'), '08:00', 102.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-55 days'), '20:00', 118.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-51 days'), '08:00', 96.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-48 days'), '14:00', 125.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-44 days'), '08:00', 91.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-41 days'), '20:00', 112.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-37 days'), '08:00', 99.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-34 days'), '14:00', 131.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-30 days'), '08:00', 95.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-27 days'), '20:00', 122.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-23 days'), '08:00', 88.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-20 days'), '14:00', 116.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-16 days'), '08:00', 104.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-13 days'), '20:00', 119.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-10 days'), '08:00', 93.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-7 days'), '08:00', 105.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-5 days'), '08:00', 98.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-3 days'), '20:00', 120.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-1 days'), '08:00', 92.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-1 days'), '20:00', 115.0, 'D');

-- Assunzioni Maria (sempre in regola: 1 al giorno nei giorni con rilevazioni)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-58 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-51 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-44 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-37 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-30 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-23 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-16 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-10 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-7 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-5 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-3 days'), '09:00', 'Metformina', '500 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'VRDMRA85B02H502X'), date('now', '-1 days'), '09:00', 'Metformina', '500 mg');

-- Nessuna segnalazione per Maria

-- Annotazione Maria
UPDATE PAZIENTE SET annotazione = 'Paziente regolare, nessuna comorbidità rilevante.'
WHERE CF = 'VRDMRA85B02H502X';


-- ==========================================================
-- PAZIENTE 3: Paolo Neri — GRAVE
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
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), 'Metformina', 3, '850 mg', 'Dopo ogni pasto', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z')),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), 'Glimepiride', 1, '2 mg', 'Prima di colazione', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Paolo: copertura 90 giorni (circa 30 misurazioni)
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-85 days'), '08:00', 185.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-80 days'), '20:00', 210.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-75 days'), '08:00', 172.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-70 days'), '14:00', 225.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-65 days'), '08:00', 168.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-60 days'), '20:00', 218.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-55 days'), '08:00', 195.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-50 days'), '14:00', 205.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-45 days'), '08:00', 180.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-40 days'), '20:00', 230.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-35 days'), '08:00', 178.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-30 days'), '14:00', 215.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-25 days'), '08:00', 190.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-20 days'), '20:00', 240.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-14 days'), '08:00', 175.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-12 days'), '08:00', 168.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-10 days'), '20:00', 220.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-8 days'), '08:00', 182.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-6 days'), '14:00', 210.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-4 days'), '08:00', 160.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-2 days'), '20:00', 198.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-1 days'), '08:00', 205.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-1 days'), '20:00', 235.0, 'D');

-- Assunzioni Paolo (pochissime)
INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, quantita) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-2 days'), '09:00', 'Metformina', '850 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-10 days'), '09:00', 'Glimepiride', '2 mg'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-25 days'), '09:00', 'Metformina', '850 mg');

-- Segnalazioni Paolo
INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno_inizio, giorno_fine, descrizione, terapia) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-10 days'), date('now', '-8 days'), 'Vertigini e nausea dopo i pasti', 'Metformina'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'NRLPLA70C03H503Y'), date('now', '-4 days'), date('now', '-2 days'), 'Ipoglicemia notturna', 'Glimepiride');

-- Annotazione Paolo
UPDATE PAZIENTE SET annotazione = 'Ex-fumatore (da 5 anni). Ipertensione in trattamento con ACE-inibitori. Dislipidemia. Pregresso IMA nel 2019. BMI: 32.1 (obeso).'
WHERE CF = 'NRLPLA70C03H503Y';


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
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), 'Metformina', 2, '500 mg', 'Dopo i pasti', (SELECT id_med FROM MEDICO WHERE CF = 'RSSMRA80A01H501Z'));

-- Rilevazioni Anna: copertura 60 giorni
INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-58 days'), '08:00', 102.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-54 days'), '20:00', 108.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-50 days'), '08:00', 97.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-46 days'), '14:00', 115.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-42 days'), '08:00', 91.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-38 days'), '20:00', 112.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-34 days'), '08:00', 94.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-30 days'), '14:00', 121.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-26 days'), '08:00', 89.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-22 days'), '20:00', 117.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-18 days'), '08:00', 96.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-14 days'), '14:00', 125.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-10 days'), '08:00', 100.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-6 days'), '08:00', 100.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-4 days'), '08:00', 95.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-2 days'), '20:00', 110.0, 'D'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-1 days'), '08:00', 88.0, 'P'),
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-1 days'), '20:00', 109.0, 'D');

-- Nessuna assunzione per Anna (terapia completamente non rispettata)

-- Segnalazioni Anna
INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno_inizio, giorno_fine, descrizione, terapia) VALUES 
((SELECT id_paz FROM PAZIENTE WHERE CF = 'RSSNNA90D04H504Z'), date('now', '-6 days'), date('now', '-4 days'), 'Lieve nausea mattutina', 'Metformina');

-- Annotazione Anna
UPDATE PAZIENTE SET annotazione = 'Nulla da segnalare. Paziente regolare.'
WHERE CF = 'RSSNNA90D04H504Z';