# tests/test_paziente.py
import pytest
from datetime import datetime, timedelta
from src.paziente import Paziente

class TestPaziente:
    def test_carica_dati_anagrafici(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC01', 'Dr.', 'One', 'M', '1980-01-01', 'Roma', 'doc01@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (1, 'DOC01')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ01', 'Mario', 'Rossi', 'M', '1990-01-01', 'Roma', 'mario@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (1, 0, 'PAZ01', 1)")
        conn.commit()
        
        p = Paziente(1, db_path)
        assert p.getNome() == 'Mario'
        assert p.getCognome() == 'Rossi'
        assert p.getSesso() == 'M'

    def test_get_terapie_senza_fine(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        ieri = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita)
        VALUES ('DOC02', 'Dr.', 'Two', 'M', '1980-01-01', 'Roma')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (2, 'DOC02')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita)
        VALUES ('PAZ02', 'Luca', 'Bianchi', 'M', '1995-01-01', 'Milano')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (2, 0, 'PAZ02', 2)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio, data_fine)
        VALUES (2, 'Metformina', 2, '500 mg', 2, ?, NULL)
        """, (oggi,))
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio, data_fine)
        VALUES (2, 'VecchioFarmaco', 1, '10 mg', 2, ?, ?)
        """, (ieri, ieri))
        conn.commit()
        
        p = Paziente(2, db_path)
        terapie = p.getTerapie()
        assert len(terapie) == 1
        assert terapie[0][0] == 'Metformina'

    def test_get_rilevazioni(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP01', 'Test', 'Rilev', 'M', '1990-01-01', 'Roma', 'p01@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (10, 'TESTP01')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (10, 0, 'TESTP01', 10)")
        conn.commit()
        
        p = Paziente(10, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 120.0, 'P')
        p.aggiungiRilevazioneGiornaliera(oggi, '12:00', 150.0, 'D')
        
        rilevazioni = p.getRilevazioni()
        assert len(rilevazioni) == 2

    def test_aggiungi_assunzione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP02', 'Test', 'Assunz', 'M', '1990-01-01', 'Roma', 'p02@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (11, 'TESTP02')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (11, 0, 'TESTP02', 11)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (11, 'Metformina', 2, '500 mg', 11, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(11, db_path)
        p.aggiungiAssunzione(oggi, '08:00', 'Metformina', '500 mg')
        
        assunzioni = p.getAssunzioni()
        assert len(assunzioni) == 1
        assert assunzioni[0][2] == 'Metformina'

    def test_aggiungi_segnalazione_con_terapia(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP03', 'Test', 'SegTer', 'M', '1990-01-01', 'Roma', 'p03@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (12, 'TESTP03')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (12, 0, 'TESTP03', 12)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (12, 'Insulina', 1, '10 UI', 12, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(12, db_path)
        p.aggiungiSegnalazione(oggi, '10:00', 'Vertigini', 'Insulina')
        
        segnalazioni = p.getSegnalazioni()
        assert len(segnalazioni) == 1
        assert segnalazioni[0][2] == 'Vertigini'
        assert segnalazioni[0][3] == 'Insulina'

    def test_aggiorna_annotazione(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP04', 'Test', 'Annot', 'M', '1990-01-01', 'Roma', 'p04@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (13, 'TESTP04')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (13, 0, 'TESTP04', 13)")
        conn.commit()
        
        p = Paziente(13, db_path)
        assert p.getAnnotazione() == ''
        
        p.aggiornaAnnotazione('Paziente diabetico tipo 2')
        assert p.getAnnotazione() == 'Paziente diabetico tipo 2'
        
        # Ricarica per verificare persistenza
        p2 = Paziente(13, db_path)
        assert p2.getAnnotazione() == 'Paziente diabetico tipo 2'

    def test_get_medico_riferimento(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel)
        VALUES ('DOCREF01', 'Dr.', 'Riferimento', 'M', '1980-01-01', 'Roma', 'docref@test.com', '123456789')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (14, 'DOCREF01')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP05', 'Test', 'MedRef', 'M', '1990-01-01', 'Roma', 'p05@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (14, 0, 'TESTP05', 14)")
        conn.commit()
        
        p = Paziente(14, db_path)
        medico = p.getMedicoRiferimento()
        assert medico is not None
        assert medico[0] == 'Dr.'
        assert medico[1] == 'Riferimento'
        assert medico[2] == 'docref@test.com'

    def test_get_terapie_complete(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        ieri = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP06', 'Test', 'TerCompl', 'M', '1990-01-01', 'Roma', 'p06@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (15, 'TESTP06')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (15, 0, 'TESTP06', 15)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio, data_fine)
        VALUES (15, 'Farmaco1', 1, '10 mg', 15, ?, NULL)
        """, (oggi,))
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio, data_fine)
        VALUES (15, 'Farmaco2', 2, '20 mg', 15, ?, ?)
        """, (ieri, ieri))
        conn.commit()
        
        p = Paziente(15, db_path)
        terapie = p.getTerapieComplete()
        assert len(terapie) == 2

    def test_get_terapie_by_name(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP07', 'Test', 'ByName', 'M', '1990-01-01', 'Roma', 'p07@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (16, 'TESTP07')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (16, 0, 'TESTP07', 16)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (16, 'Metformina', 2, '500 mg', 16, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(16, db_path)
        t = p.getTerapieByName('Metformina')
        assert t is not None
        assert t[0] == 'Metformina'
        
        t_none = p.getTerapieByName('Insulina')
        assert t_none is None

    def test_elimina_rilevazione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP08', 'Test', 'ElimRil', 'M', '1990-01-01', 'Roma', 'p08@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (17, 'TESTP08')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (17, 0, 'TESTP08', 17)")
        conn.commit()
        
        p = Paziente(17, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 120.0, 'P')
        assert len(p.getRilevazioni()) == 1
        
        p.eliminaRilevazioneGiornaliera(oggi, '08:00')
        assert len(p.getRilevazioni()) == 0

    def test_aggiorna_rilevazione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP09', 'Test', 'AggRil', 'M', '1990-01-01', 'Roma', 'p09@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (18, 'TESTP09')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (18, 0, 'TESTP09', 18)")
        conn.commit()
        
        p = Paziente(18, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 120.0, 'P')
        p.aggiornaRilevazioneGiornaliera(oggi, '08:00', oggi, '08:00', 150.0, 'D')
        
        rilevazioni = p.getRilevazioni()
        assert len(rilevazioni) == 1
        assert rilevazioni[0][2] == 150.0
        assert rilevazioni[0][3] == 'D'

    def test_elimina_assunzione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP10', 'Test', 'ElimAss', 'M', '1990-01-01', 'Roma', 'p10@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (19, 'TESTP10')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (19, 0, 'TESTP10', 19)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (19, 'Metformina', 2, '500 mg', 19, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(19, db_path)
        p.aggiungiAssunzione(oggi, '08:00', 'Metformina', '500 mg')
        assert len(p.getAssunzioni()) == 1
        
        p.eliminaAssunzione(oggi, '08:00', 'Metformina')
        assert len(p.getAssunzioni()) == 0

    def test_aggiorna_assunzione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP11', 'Test', 'AggAss', 'M', '1990-01-01', 'Roma', 'p11@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (20, 'TESTP11')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (20, 0, 'TESTP11', 20)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (20, 'Metformina', 2, '500 mg', 20, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(20, db_path)
        p.aggiungiAssunzione(oggi, '08:00', 'Metformina', '500 mg')
        p.aggiornaAssunzione(oggi, '08:00', 'Metformina', oggi, '09:00', 'Metformina', '1000 mg')
        
        assunzioni = p.getAssunzioni()
        assert len(assunzioni) == 1
        assert assunzioni[0][1] == '09:00'
        assert assunzioni[0][3] == '1000 mg'

    def test_elimina_segnalazione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP12', 'Test', 'ElimSeg', 'M', '1990-01-01', 'Roma', 'p12@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (21, 'TESTP12')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (21, 0, 'TESTP12', 21)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (21, 'Insulina', 1, '10 UI', 21, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(21, db_path)
        p.aggiungiSegnalazione(oggi, '10:00', 'Vertigini', 'Insulina')
        assert len(p.getSegnalazioni()) == 1
        
        p.eliminaSegnalazione(oggi, '10:00')
        assert len(p.getSegnalazioni()) == 0

    def test_aggiorna_segnalazione(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP13', 'Test', 'AggSeg', 'M', '1990-01-01', 'Roma', 'p13@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (22, 'TESTP13')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (22, 0, 'TESTP13', 22)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (22, 'Insulina', 1, '10 UI', 22, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(22, db_path)
        p.aggiungiSegnalazione(oggi, '10:00', 'Vertigini', 'Insulina')
        p.aggiornaSegnalazione(oggi, '10:00', oggi, '11:00', 'Nausea', 'Insulina')
        
        segnalazioni = p.getSegnalazioni()
        assert len(segnalazioni) == 1
        assert segnalazioni[0][1] == '11:00'
        assert segnalazioni[0][2] == 'Nausea'

    def test_getters(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel, indirizzo)
        VALUES ('TESTP14', 'Anna', 'Bianchi', 'F', '1985-03-20', 'Napoli', 'anna@test.com', '333111222', 'Via Roma 1')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (23, 'TESTP14')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (23, 0, 'TESTP14', 23)")
        conn.commit()
        
        p = Paziente(23, db_path)
        assert p.getIdRef() == 23
        assert p.getCf() == 'TESTP14'
        assert p.getNome() == 'Anna'
        assert p.getCognome() == 'Bianchi'
        assert p.getSesso() == 'F'
        assert p.getDataNascita() == '1985-03-20'
        assert p.getLuogoNascita() == 'Napoli'
        assert p.getEmail() == 'anna@test.com'
        assert p.getCel() == '333111222'
        assert p.getIndirizzo() == 'Via Roma 1'
        assert p.getMedicoId() == 23
        assert p.getGravita() == 0

    def test_str(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP15', 'Carlo', 'Neri', 'M', '1992-07-10', 'Torino', 'carlo@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (24, 'TESTP15')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (24, 0, 'TESTP15', 24)")
        conn.commit()
        
        p = Paziente(24, db_path)
        str_repr = str(p)
        assert 'Carlo' in str_repr
        assert 'Neri' in str_repr
        assert 'TESTP15' in str_repr

    # ============================================================
    # TEST AGGIUNTIVI - Casi limite ed errori
    # ============================================================

    def test_aggiungi_rilevazione_glicemia_negativa(self, db_path, init_db):
        """Test che venga sollevata eccezione per glicemia negativa"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP30', 'Test', 'Neg', 'M', '1990-01-01', 'Roma', 'p30@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (30, 'TESTP30')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (30, 0, 'TESTP30', 30)")
        conn.commit()
        
        p = Paziente(30, db_path)
        with pytest.raises(ValueError, match="glicemia non può essere negativa"):
            p.aggiungiRilevazioneGiornaliera(oggi, '08:00', -50.0, 'P')

    def test_aggiungi_rilevazione_glicemia_zero(self, db_path, init_db):
        """Test rilevazione con glicemia zero"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP31', 'Test', 'Zero', 'M', '1990-01-01', 'Roma', 'p31@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (31, 'TESTP31')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (31, 0, 'TESTP31', 31)")
        conn.commit()
        
        p = Paziente(31, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 0.0, 'P')
        assert len(p.getRilevazioni()) == 1
        assert p.getPuntiGlicemia() == 1  # 0 è sotto 80

    def test_aggiungi_rilevazione_glicemia_molto_alta(self, db_path, init_db):
        """Test rilevazione con glicemia molto alta"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP32', 'Test', 'High', 'M', '1990-01-01', 'Roma', 'p32@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (32, 'TESTP32')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (32, 0, 'TESTP32', 32)")
        conn.commit()
        
        p = Paziente(32, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 500.0, 'P')
        assert len(p.getRilevazioni()) == 1
        assert p.getPuntiGlicemia() == 1

    def test_paziente_inesistente(self, db_path, init_db):
        """Test creazione paziente con id inesistente"""
        with pytest.raises(ValueError, match="non trovato"):
            Paziente(99999, db_path)

    def test_aggiungi_assunzione_senza_terapia(self, db_path, init_db):
        """Test aggiunta assunzione senza terapia associata"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP33', 'Test', 'NoTer', 'M', '1990-01-01', 'Roma', 'p33@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (33, 'TESTP33')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (33, 0, 'TESTP33', 33)")
        conn.commit()
        
        p = Paziente(33, db_path)
        # Non dovrebbe crashare, solo non registrare nulla
        p.aggiungiAssunzione(oggi, '08:00', 'FarmacoInesistente', '10 mg')
        assunzioni = p.getAssunzioni()
        assert len(assunzioni) == 0

    def test_elimina_rilevazione_inesistente(self, db_path, init_db):
        """Test eliminazione rilevazione inesistente (non deve crashare)"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP34', 'Test', 'DelNot', 'M', '1990-01-01', 'Roma', 'p34@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (34, 'TESTP34')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (34, 0, 'TESTP34', 34)")
        conn.commit()
        
        p = Paziente(34, db_path)
        p.eliminaRilevazioneGiornaliera(oggi, '08:00')
        assert len(p.getRilevazioni()) == 0

    def test_annotazione_vuota(self, db_path, init_db):
        """Test aggiornamento con annotazione vuota"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP35', 'Test', 'EmptyAnn', 'M', '1990-01-01', 'Roma', 'p35@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (35, 'TESTP35')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico, annotazione) VALUES (35, 0, 'TESTP35', 35, 'Vecchia annotazione')")
        conn.commit()
        
        p = Paziente(35, db_path)
        assert p.getAnnotazione() == 'Vecchia annotazione'
        p.aggiornaAnnotazione('')
        assert p.getAnnotazione() == ''

    def test_annotazione_molto_lunga(self, db_path, init_db):
        """Test annotazione con testo molto lungo"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP36', 'Test', 'LongAnn', 'M', '1990-01-01', 'Roma', 'p36@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (36, 'TESTP36')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (36, 0, 'TESTP36', 36)")
        conn.commit()
        
        p = Paziente(36, db_path)
        testo_lungo = 'A' * 1000
        p.aggiornaAnnotazione(testo_lungo)
        assert p.getAnnotazione() == testo_lungo

    def test_ora_formato_strano(self, db_path, init_db):
        """Test rilevazione con formato ora non standard"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP37', 'Test', 'BadTime', 'M', '1990-01-01', 'Roma', 'p37@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (37, 'TESTP37')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (37, 0, 'TESTP37', 37)")
        conn.commit()
        
        p = Paziente(37, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '25:00', 120.0, 'P')
        assert len(p.getRilevazioni()) == 1

    def test_elimina_assunzione_inesistente(self, db_path, init_db):
        """Test eliminazione assunzione inesistente"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP38', 'Test', 'ElimAssNot', 'M', '1990-01-01', 'Roma', 'p38@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (38, 'TESTP38')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (38, 0, 'TESTP38', 38)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (38, 'Metformina', 2, '500 mg', 38, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(38, db_path)
        # Non deve crashare
        p.eliminaAssunzione(oggi, '08:00', 'Metformina')
        assert len(p.getAssunzioni()) == 0

    def test_elimina_segnalazione_inesistente(self, db_path, init_db):
        """Test eliminazione segnalazione inesistente"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP39', 'Test', 'ElimSegNot', 'M', '1990-01-01', 'Roma', 'p39@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (39, 'TESTP39')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (39, 0, 'TESTP39', 39)")
        conn.commit()
        
        p = Paziente(39, db_path)
        # Non deve crashare
        p.eliminaSegnalazione(oggi, '10:00')
        assert len(p.getSegnalazioni()) == 0

    def test_get_terapie_paziente_senza_terapie(self, db_path, init_db):
        """Test getTerapie su paziente senza terapie"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP40', 'Test', 'NoTer', 'M', '1990-01-01', 'Roma', 'p40@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (40, 'TESTP40')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (40, 0, 'TESTP40', 40)")
        conn.commit()
        
        p = Paziente(40, db_path)
        assert p.getTerapie() == []
        assert p.getTerapieComplete() == []

    def test_get_rilevazioni_paziente_senza_rilevazioni(self, db_path, init_db):
        """Test getRilevazioni su paziente senza rilevazioni"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP41', 'Test', 'NoRil', 'M', '1990-01-01', 'Roma', 'p41@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (41, 'TESTP41')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (41, 0, 'TESTP41', 41)")
        conn.commit()
        
        p = Paziente(41, db_path)
        assert p.getRilevazioni() == []

    def test_get_assunzioni_paziente_senza_assunzioni(self, db_path, init_db):
        """Test getAssunzioni su paziente senza assunzioni"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP42', 'Test', 'NoAss', 'M', '1990-01-01', 'Roma', 'p42@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (42, 'TESTP42')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (42, 0, 'TESTP42', 42)")
        conn.commit()
        
        p = Paziente(42, db_path)
        assert p.getAssunzioni() == []

    def test_get_segnalazioni_paziente_senza_segnalazioni(self, db_path, init_db):
        """Test getSegnalazioni su paziente senza segnalazioni"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP43', 'Test', 'NoSeg', 'M', '1990-01-01', 'Roma', 'p43@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (43, 'TESTP43')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (43, 0, 'TESTP43', 43)")
        conn.commit()
        
        p = Paziente(43, db_path)
        assert p.getSegnalazioni() == []

    def test_annotazione_null_iniziale(self, db_path, init_db):
        """Test che annotazione None venga convertita in stringa vuota"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP44', 'Test', 'NullAnn', 'M', '1990-01-01', 'Roma', 'p44@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (44, 'TESTP44')")
        # Non impostare annotazione (sarà NULL)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (44, 0, 'TESTP44', 44)")
        conn.commit()
        
        p = Paziente(44, db_path)
        assert p.getAnnotazione() == ''

    def test_rilevazione_ordine(self, db_path, init_db):
        """Test che le rilevazioni siano ordinate per giorno decrescente"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        ieri = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTP45', 'Test', 'Ordine', 'M', '1990-01-01', 'Roma', 'p45@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (45, 'TESTP45')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (45, 0, 'TESTP45', 45)")
        conn.commit()
        
        p = Paziente(45, db_path)
        p.aggiungiRilevazioneGiornaliera(ieri, '08:00', 100.0, 'P')
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 120.0, 'P')
        
        rilevazioni = p.getRilevazioni()
        assert len(rilevazioni) == 2
        # La più recente (oggi) deve essere prima
        assert rilevazioni[0][0] == oggi
        assert rilevazioni[1][0] == ieri