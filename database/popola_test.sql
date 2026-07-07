INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('CCCMRN85M01L781V', 'Mariano', 'Ceccato', 'M', '1985-08-01', 'Verona', 'Via dell_Artigliere 8, Verona', 'mariano.ceccato@univr.it', '348-1234567');

INSERT OR IGNORE INTO MEDICO (CF) VALUES ('CCCMRN85M01L781V');

-- Password: IngegneriaDelSoftware!
INSERT OR IGNORE INTO USER (username, password, tipo, id_ref)
VALUES ('dott.ceccato', 'a4586977f1ca790adcdf81270c0a972a9498259897a206c570567f642ae78318', 'M', 1);

INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('BLZMTT90A01L781X', 'Matteo', 'Balzerani', 'M', '1990-01-01', 'Verona', 'Via Lungadige 15, Verona', 'matteo.balzerani@univr.it', '347-1112223');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico, annotazione) VALUES (
    0,
    'BLZMTT90A01L781X',
    1,
    'Paziente diabetico di tipo 2 con scarso controllo glicemico. Familiarità per diabete (padre e nonna materna). Obesità di II grado (BMI 32.4). Ipertensione arteriosa in trattamento con ACE-inibitori. Fumatore (15 sigarette/die). Scarsa aderenza alla terapia farmacologica e alla dieta ipocalorica prescritta. Riferisce stress lavorativo elevato. Ultimo fundus oculi: retinopatia diabetica lieve non proliferante. Microalbuminuria presente (30 mg/g creatinina).'
);

-- Password: password
INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('matteo.balzerani', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 1);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (1, 'Metformina', 2, '500 mg', 'Assumere dopo i pasti principali (colazione e cena).', 1, date('now', '-180 days'), date('now', '-90 days'));

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (1, 'Metformina', 2, '1000 mg', 'Assumere dopo i pasti principali (colazione e cena). Aumentato dosaggio per scarso controllo.', 1, date('now', '-90 days'), NULL);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (1, 'Insulina Glargine', 1, '20 UI', 'Somministrare per via sottocutanea la sera alle 22:00. Ruotare i siti di iniezione.', 1, date('now', '-60 days'), NULL);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (1, 'Ramipril', 1, '5 mg', 'Assumere al mattino a digiuno per controllo pressione arteriosa.', 1, date('now', '-120 days'), NULL);

INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(1, date('now', '-30 days'), '08:00', 185.0, 'P'),
(1, date('now', '-29 days'), '08:00', 195.0, 'P'),
(1, date('now', '-28 days'), '08:00', 178.0, 'P'),
(1, date('now', '-27 days'), '08:00', 205.0, 'P'),
(1, date('now', '-26 days'), '08:00', 168.0, 'P'),
(1, date('now', '-25 days'), '08:00', 190.0, 'P'),
(1, date('now', '-24 days'), '08:00', 175.0, 'P'),
(1, date('now', '-23 days'), '08:00', 200.0, 'P'),
(1, date('now', '-22 days'), '08:00', 182.0, 'P'),
(1, date('now', '-21 days'), '08:00', 195.0, 'P'),
(1, date('now', '-20 days'), '08:00', 170.0, 'P'),
(1, date('now', '-19 days'), '08:00', 188.0, 'P'),
(1, date('now', '-18 days'), '08:00', 192.0, 'P'),
(1, date('now', '-17 days'), '08:00', 180.0, 'P'),
(1, date('now', '-16 days'), '08:00', 198.0, 'P'),
(1, date('now', '-15 days'), '08:00', 185.0, 'P'),
(1, date('now', '-14 days'), '08:00', 176.0, 'P'),
(1, date('now', '-13 days'), '08:00', 202.0, 'P'),
(1, date('now', '-12 days'), '08:00', 190.0, 'P'),
(1, date('now', '-11 days'), '08:00', 210.0, 'P'),
(1, date('now', '-10 days'), '08:00', 165.0, 'P'),
(1, date('now', '-9 days'), '08:00', 195.0, 'P'),
(1, date('now', '-8 days'), '08:00', 220.0, 'P'),
(1, date('now', '-7 days'), '08:00', 230.0, 'P'),
(1, date('now', '-6 days'), '08:00', 178.0, 'P'),
(1, date('now', '-5 days'), '08:00', 205.0, 'P'),
(1, date('now', '-4 days'), '08:00', 188.0, 'P'),
(1, date('now', '-3 days'), '08:00', 215.0, 'P'),
(1, date('now', '-2 days'), '08:00', 240.0, 'P'),
(1, date('now', '-1 days'), '08:00', 198.0, 'P');

INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(1, date('now', '-1 days'), '13:00', 'Metformina', date('now', '-90 days'), '1000 mg'),
(1, date('now', '-3 days'), '13:00', 'Metformina', date('now', '-90 days'), '1000 mg'),
(1, date('now', '-5 days'), '22:00', 'Insulina Glargine', date('now', '-60 days'), '20 UI'),
(1, date('now', '-7 days'), '08:00', 'Ramipril', date('now', '-120 days'), '5 mg'),
(1, date('now', '-10 days'), '13:00', 'Metformina', date('now', '-90 days'), '1000 mg');

INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno, ora, sintomo, terapia, data_inizio) VALUES 
(1, date('now', '-2 days'), '09:30', 'Vertigini al risveglio, possibile ipoglicemia notturna', 'Insulina Glargine', date('now', '-60 days')),
(1, date('now', '-8 days'), '15:00', 'Nausea dopo assunzione Metformina', 'Metformina', date('now', '-90 days')),
(1, date('now', '-15 days'), '11:00', 'Vista offuscata temporanea', NULL, NULL);



INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('DVSCST85A01H501Z', 'Jessica', 'Devescovi', 'F', '1985-01-01', 'Verona', 'Corso Porta Nuova 42, Verona', 'jessica.devescovi@univr.it', '347-3334445');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico, annotazione) VALUES (
    0,
    'DVSCST85A01H501Z',
    1,
    'Paziente con diabete mellito di tipo 1 diagnosticato all_età di 12 anni. In terapia insulinica multi-iniettiva. Buona compliance terapeutica ma difficoltà nel mantenere stabili i livelli glicemici a causa di attività sportiva intensa (corsa e nuoto 4 volte/settimana). Riferisce episodi di ipoglicemia post-esercizio. Nessuna complicanza cronica rilevata all_ultimo screening. Emoglobina glicata (HbA1c): 7.8%. In programma corso di educazione alimentare per sportivi diabetici.'
);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('jessica.devescovi', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 2);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (2, 'Insulina Lispro', 3, '6-8 UI', 'Somministrare prima dei pasti principali. Dose variabile in base al conteggio carboidrati e glicemia pre-prandiale.', 1, date('now', '-365 days'), NULL);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (2, 'Insulina Glargine', 1, '14 UI', 'Somministrare alle 22:00. Dose fissa serale.', 1, date('now', '-365 days'), NULL);

INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(2, date('now', '-15 days'), '08:00', 145.0, 'P'),
(2, date('now', '-14 days'), '08:00', 98.0, 'P'),
(2, date('now', '-13 days'), '08:00', 155.0, 'P'),
(2, date('now', '-12 days'), '08:00', 88.0, 'P'),
(2, date('now', '-11 days'), '08:00', 165.0, 'P'),
(2, date('now', '-10 days'), '08:00', 102.0, 'P'),
(2, date('now', '-9 days'), '08:00', 92.0, 'P'),
(2, date('now', '-8 days'), '08:00', 148.0, 'P'),
(2, date('now', '-7 days'), '08:00', 85.0, 'P'),
(2, date('now', '-6 days'), '08:00', 110.0, 'P'),
(2, date('now', '-5 days'), '08:00', 138.0, 'P'),
(2, date('now', '-4 days'), '08:00', 95.0, 'P'),
(2, date('now', '-3 days'), '08:00', 160.0, 'P'),
(2, date('now', '-2 days'), '08:00', 100.0, 'P'),
(2, date('now', '-1 days'), '08:00', 128.0, 'P');

INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(2, date('now', '-1 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-1 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-1 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-1 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-2 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-2 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-2 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-2 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-3 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-3 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-3 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-3 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-4 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-4 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-4 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-4 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-5 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-5 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-5 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-5 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-6 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-6 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-6 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-6 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-7 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-7 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-7 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-7 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-8 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-8 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-8 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-8 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-9 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-9 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-9 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-9 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-10 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-10 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-10 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-10 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-11 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-11 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-11 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-11 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-12 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-12 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-12 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-12 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-13 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-13 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-13 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-13 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-14 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-14 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-14 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-14 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI'),
(2, date('now', '-15 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-15 days'), '13:00', 'Insulina Lispro', date('now', '-365 days'), '6 UI'),
(2, date('now', '-15 days'), '20:00', 'Insulina Lispro', date('now', '-365 days'), '8 UI'),
(2, date('now', '-15 days'), '22:00', 'Insulina Glargine', date('now', '-365 days'), '14 UI');

INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno, ora, sintomo, terapia, data_inizio) VALUES 
(2, date('now', '-1 days'), '17:00', 'Ipoglicemia dopo sessione di nuoto (glicemia 55 mg/dL). Assunta bustina di zucchero.', 'Insulina Lispro', date('now', '-365 days')),
(2, date('now', '-10 days'), '19:00', 'Tremori e sudorazione prima di cena', NULL, NULL);



INSERT OR IGNORE INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, indirizzo, email, cel)
VALUES ('MNVMTT90B01H501Z', 'Mattia', 'Mantovani', 'M', '1990-02-02', 'Milano', 'Via Solferino 10, Milano', 'mattia.mantovani@univr.it', '347-5556667');

INSERT OR IGNORE INTO PAZIENTE (gravita, CF, medico, annotazione) VALUES (
    0,
    'MNVMTT90B01H501Z',
    1,
    'Paziente con diabete mellito di tipo 2 diagnosticato 2 anni fa. Ottimo controllo glicemico ottenuto con sola Metformina. Stile di vita attivo (camminata 5 km/die). Dieta mediterranea seguita con regolarità. Non fumatore, consumo moderato di alcol (1 bicchiere di vino rosso ai pasti). HbA1c: 6.2%. Peso nella norma (BMI 23.8). Nessuna complicanza. Screening annuale delle complicanze nella norma. Paziente modello.'
);

INSERT OR IGNORE INTO USER (username, password, tipo, id_ref) VALUES ('mattia.mantovani', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 3);

INSERT OR IGNORE INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio, data_fine)
VALUES (3, 'Metformina', 1, '500 mg', 'Assumere a colazione con abbondante acqua.', 1, date('now', '-180 days'), NULL);

INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(3, date('now', '-20 days'), '08:00', 95.0, 'P'),
(3, date('now', '-19 days'), '08:00', 92.0, 'P'),
(3, date('now', '-18 days'), '08:00', 98.0, 'P'),
(3, date('now', '-17 days'), '08:00', 88.0, 'P'),
(3, date('now', '-16 days'), '08:00', 102.0, 'P'),
(3, date('now', '-15 days'), '08:00', 90.0, 'P'),
(3, date('now', '-14 days'), '08:00', 96.0, 'P'),
(3, date('now', '-13 days'), '08:00', 85.0, 'P'),
(3, date('now', '-12 days'), '08:00', 100.0, 'P'),
(3, date('now', '-11 days'), '08:00', 93.0, 'P'),
(3, date('now', '-10 days'), '08:00', 97.0, 'P'),
(3, date('now', '-9 days'), '08:00', 89.0, 'P'),
(3, date('now', '-8 days'), '08:00', 94.0, 'P'),
(3, date('now', '-7 days'), '08:00', 91.0, 'P'),
(3, date('now', '-6 days'), '08:00', 99.0, 'P'),
(3, date('now', '-5 days'), '08:00', 87.0, 'P'),
(3, date('now', '-4 days'), '08:00', 95.0, 'P'),
(3, date('now', '-3 days'), '08:00', 92.0, 'P'),
(3, date('now', '-2 days'), '08:00', 98.0, 'P'),
(3, date('now', '-1 days'), '08:00', 96.0, 'P');

INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(3, date('now', '-1 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-2 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-3 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-4 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-5 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-6 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-7 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-8 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-9 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-10 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-11 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-12 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-13 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-14 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-15 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-16 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-17 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-18 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-19 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-20 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg');

INSERT OR IGNORE INTO SEGNALAZIONE (id_paz, giorno, ora, sintomo, terapia, data_inizio) VALUES 
(3, date('now', '-20 days'), '10:00', 'Lieve nausea mattutina risolta spontaneamente', 'Metformina', date('now', '-180 days'));


INSERT INTO LOG_OPERAZIONI (id_med, azione, tabella, id_record, dettaglio) VALUES
(1, 'PRESCRIZIONE_TERAPIA', 'TERAPIA', '1/Metformina', 'Aumentato dosaggio Metformina a 1000 mg per Matteo Balzerani'),
(1, 'PRESCRIZIONE_TERAPIA', 'TERAPIA', '1/Insulina Glargine', 'Aggiunta Insulina Glargine 20 UI per scarso controllo glicemico'),
(1, 'MODIFICA_ANNOTAZIONE', 'PAZIENTE', '2', 'Aggiornata annotazione Jessica Devescovi con ultimo HbA1c'),
(1, 'PRESCRIZIONE_TERAPIA', 'TERAPIA', '3/Metformina', 'Prescritta Metformina 500 mg per Mattia Mantovani'),
(1, 'VISUALIZZA_DETTAGLIO', 'PAZIENTE', '1', 'Visualizzato dettaglio Matteo Balzerani');


INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(2, date('now', '-350 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-340 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-330 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-320 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-310 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-300 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-290 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-280 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-270 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-260 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-250 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-240 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-230 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-220 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-210 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-200 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-190 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-180 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-170 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-160 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-150 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-140 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-130 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-120 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-110 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-100 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-90 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-80 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-70 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-60 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-50 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-40 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-35 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-25 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-20 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI');

INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(3, date('now', '-350 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-320 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-290 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-260 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-230 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-200 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-170 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-140 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-110 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-80 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-50 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg');


INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(1, date('now', '-340 days'), '08:00', 172.0, 'P'),
(1, date('now', '-320 days'), '08:00', 198.0, 'D'),
(1, date('now', '-310 days'), '08:00', 185.0, 'P'),
(1, date('now', '-290 days'), '08:00', 205.0, 'P'),
(1, date('now', '-280 days'), '08:00', 178.0, 'P'),
(1, date('now', '-260 days'), '08:00', 192.0, 'P'),
(1, date('now', '-250 days'), '08:00', 215.0, 'D'),
(1, date('now', '-230 days'), '08:00', 168.0, 'P'),
(1, date('now', '-220 days'), '08:00', 200.0, 'P'),
(1, date('now', '-200 days'), '08:00', 188.0, 'D'),
(1, date('now', '-190 days'), '08:00', 195.0, 'D'),
(1, date('now', '-170 days'), '08:00', 210.0, 'D'),
(1, date('now', '-160 days'), '08:00', 182.0, 'D'),
(1, date('now', '-140 days'), '08:00', 198.0, 'D'),
(1, date('now', '-130 days'), '08:00', 175.0, 'P'),
(1, date('now', '-110 days'), '08:00', 205.0, 'P'),
(1, date('now', '-100 days'), '08:00', 190.0, 'D'),
(1, date('now', '-80 days'), '08:00', 185.0, 'P'),
(1, date('now', '-70 days'), '08:00', 200.0, 'D'),
(1, date('now', '-50 days'), '08:00', 178.0, 'P'),
(1, date('now', '-40 days'), '08:00', 195.0, 'P');


INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(2, date('now', '-345 days'), '08:00', 108.0, 'P'),
(2, date('now', '-335 days'), '08:00', 142.0, 'P'),
(2, date('now', '-325 days'), '08:00', 95.0, 'P'),
(2, date('now', '-315 days'), '08:00', 152.0, 'D'),
(2, date('now', '-305 days'), '08:00', 88.0, 'P'),
(2, date('now', '-295 days'), '08:00', 138.0, 'P'),
(2, date('now', '-285 days'), '08:00', 100.0, 'P'),
(2, date('now', '-275 days'), '08:00', 145.0, 'D'),
(2, date('now', '-265 days'), '08:00', 192.0, 'D'),
(2, date('now', '-255 days'), '08:00', 155.0, 'P'),
(2, date('now', '-245 days'), '08:00', 90.0, 'P'),
(2, date('now', '-235 days'), '08:00', 148.0, 'P'),
(2, date('now', '-225 days'), '08:00', 98.0, 'P'),
(2, date('now', '-215 days'), '08:00', 140.0, 'P'),
(2, date('now', '-205 days'), '08:00', 85.0, 'P'),
(2, date('now', '-195 days'), '08:00', 150.0, 'P'),
(2, date('now', '-185 days'), '08:00', 95.0, 'P'),
(2, date('now', '-175 days'), '08:00', 142.0, 'P'),
(2, date('now', '-165 days'), '08:00', 90.0, 'P'),
(2, date('now', '-155 days'), '08:00', 148.0, 'D'),
(2, date('now', '-145 days'), '08:00', 188.0, 'D'),
(2, date('now', '-135 days'), '08:00', 152.0, 'D'),
(2, date('now', '-125 days'), '08:00', 97.0, 'P'),
(2, date('now', '-115 days'), '08:00', 140.0, 'P'),
(2, date('now', '-105 days'), '08:00', 92.0, 'P'),
(2, date('now', '-95 days'), '08:00', 145.0, 'P'),
(2, date('now', '-85 days'), '08:00', 100.0, 'P'),
(2, date('now', '-75 days'), '08:00', 138.0, 'P'),
(2, date('now', '-65 days'), '08:00', 90.0, 'P'),
(2, date('now', '-55 days'), '08:00', 150.0, 'D'),
(2, date('now', '-45 days'), '08:00', 195.0, 'D'),
(2, date('now', '-30 days'), '08:00', 142.0, 'P'),
(2, date('now', '-18 days'), '08:00', 88.0, 'P'),
(2, date('now', '-8 days'), '08:00', 148.0, 'P');

INSERT OR IGNORE INTO RILEVAZ_GIORN (id_paz, giorno, ora, glicemia, primaDopoPasto) VALUES 
(3, date('now', '-340 days'), '08:00', 94.0, 'P'),
(3, date('now', '-330 days'), '08:00', 90.0, 'P'),
(3, date('now', '-310 days'), '08:00', 168.0, 'D'),
(3, date('now', '-300 days'), '08:00', 177.0, 'D'),
(3, date('now', '-280 days'), '08:00', 165.0, 'D'),
(3, date('now', '-270 days'), '08:00', 172.0, 'D'),
(3, date('now', '-250 days'), '08:00', 179.0, 'D'),
(3, date('now', '-240 days'), '08:00', 176.0, 'D'),
(3, date('now', '-220 days'), '08:00', 177.0, 'D'),
(3, date('now', '-210 days'), '08:00', 171.0, 'D'),
(3, date('now', '-190 days'), '08:00', 164.0, 'D'),
(3, date('now', '-180 days'), '08:00', 158.0, 'D'),
(3, date('now', '-160 days'), '08:00', 96.0, 'P'),
(3, date('now', '-150 days'), '08:00', 90.0, 'P'),
(3, date('now', '-130 days'), '08:00', 98.0, 'P'),
(3, date('now', '-120 days'), '08:00', 85.0, 'P'),
(3, date('now', '-100 days'), '08:00', 93.0, 'P'),
(3, date('now', '-90 days'), '08:00', 97.0, 'P'),
(3, date('now', '-70 days'), '08:00', 89.0, 'P'),
(3, date('now', '-60 days'), '08:00', 95.0, 'P'),
(3, date('now', '-40 days'), '08:00', 91.0, 'P'),
(3, date('now', '-30 days'), '08:00', 88.0, 'P');


INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(2, date('now', '-345 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-335 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-325 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-315 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-305 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-295 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-285 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-275 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-265 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-255 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-245 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-235 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-225 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-215 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-205 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-195 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-185 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-175 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-165 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-155 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-145 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-135 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-125 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-115 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-105 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-95 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-85 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-75 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-65 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-55 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-45 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-30 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-18 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI'),
(2, date('now', '-8 days'), '08:00', 'Insulina Lispro', date('now', '-365 days'), '7 UI');

INSERT OR IGNORE INTO ASSUNZIONE (id_paz, giorno, ora, farmaco, data_inizio, quantita) VALUES 
(3, date('now', '-340 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-330 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-310 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-300 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-280 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-270 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-250 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-240 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-220 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-210 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-190 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-180 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-160 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-150 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-130 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-120 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-100 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-90 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-70 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-60 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-40 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg'),
(3, date('now', '-30 days'), '08:00', 'Metformina', date('now', '-180 days'), '500 mg');


