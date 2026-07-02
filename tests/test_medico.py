# tests/test_medico.py
import pytest
from datetime import datetime, timedelta
from src.medico import Medico
from src.paziente import Paziente

class TestMedico:
    def test_prescrivi_terapia(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita)
        VALUES ('DOC03', 'Dr.', 'Three', 'M', '1980-01-01', 'Roma')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (3, 'DOC03')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ03', 'Paziente', 'Test', 'M', '1990-01-01', 'Milano', 'paz@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (3, 0, 'PAZ03', 3)")
        conn.commit()
        
        medico = Medico(3, db_path)
        medico.prescriviTerapia(3, 'Metformina', 2, '500 mg', oggi)
        
        p = Paziente(3, db_path)
        terapie = p.getTerapie()
        assert len(terapie) == 1

    def test_get_pazienti_ids(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC10', 'Dr.', 'Ten', 'M', '1980-01-01', 'Roma', 'doc10@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (10, 'DOC10')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ10', 'Paz', 'One', 'M', '1990-01-01', 'Roma', 'paz10@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (10, 0, 'PAZ10', 10)")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ11', 'Paz', 'Two', 'F', '1995-01-01', 'Milano', 'paz11@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (11, 2, 'PAZ11', 10)")
        conn.commit()
        
        medico = Medico(10, db_path)
        ids = medico.getPazientiIds()
        assert len(ids) == 2
        assert 10 in ids
        assert 11 in ids

    def test_get_pazienti(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC11', 'Dr.', 'Eleven', 'M', '1980-01-01', 'Roma', 'doc11@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (11, 'DOC11')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ12', 'Paz', 'Three', 'M', '1990-01-01', 'Roma', 'paz12@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (12, 0, 'PAZ12', 11)")
        conn.commit()
        
        medico = Medico(11, db_path)
        pazienti = medico.getPazienti()
        assert len(pazienti) == 1
        assert pazienti[0].getNome() == 'Paz'

    def test_get_paziente_by_id(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC12', 'Dr.', 'Twelve', 'M', '1980-01-01', 'Roma', 'doc12@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (12, 'DOC12')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ13', 'Paz', 'Four', 'M', '1990-01-01', 'Roma', 'paz13@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (13, 0, 'PAZ13', 12)")
        conn.commit()
        
        medico = Medico(12, db_path)
        p = medico.getPazienteById(13)
        assert p is not None
        assert p.getCognome() == 'Four'
        
        p_inesistente = medico.getPazienteById(999)
        assert p_inesistente is None

    def test_modifica_terapia_stesso_farmaco(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC13', 'Dr.', 'Thirteen', 'M', '1980-01-01', 'Roma', 'doc13@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (13, 'DOC13')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ14', 'Paz', 'Five', 'M', '1990-01-01', 'Roma', 'paz14@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (14, 0, 'PAZ14', 13)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (14, 'Metformina', 2, '500 mg', 13, ?)
        """, (oggi,))
        conn.commit()
        
        medico = Medico(13, db_path)
        medico.modificaTerapia(14, 'Metformina', 'Metformina', 3, '1000 mg', oggi)
        
        p = Paziente(14, db_path)
        terapie = p.getTerapie()
        assert len(terapie) == 1
        assert terapie[0][1] == 3  # assunzioniGiornaliere aggiornate

    def test_modifica_terapia_farmaco_diverso(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC14', 'Dr.', 'Fourteen', 'M', '1980-01-01', 'Roma', 'doc14@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (14, 'DOC14')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ15', 'Paz', 'Six', 'M', '1990-01-01', 'Roma', 'paz15@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (15, 0, 'PAZ15', 14)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (15, 'Metformina', 2, '500 mg', 14, ?)
        """, (oggi,))
        conn.commit()
        
        medico = Medico(14, db_path)
        medico.modificaTerapia(15, 'Metformina', 'Insulina', 1, '10 UI', oggi)
        
        p = Paziente(15, db_path)
        terapie = p.getTerapieComplete()
        assert len(terapie) == 2  # Vecchia chiusa + nuova

    def test_interrompi_terapia(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        ieri = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC15', 'Dr.', 'Fifteen', 'M', '1980-01-01', 'Roma', 'doc15@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (15, 'DOC15')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ16', 'Paz', 'Seven', 'M', '1990-01-01', 'Roma', 'paz16@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (16, 0, 'PAZ16', 15)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (16, 'Metformina', 2, '500 mg', 15, ?)
        """, (ieri,))
        conn.commit()
        
        medico = Medico(15, db_path)
        medico.interrompiTerapia(16, 'Metformina', oggi)
        
        p = Paziente(16, db_path)
        terapie = p.getTerapieComplete()
        # La terapia deve avere data_fine impostata
        assert len(terapie) == 1
        assert terapie[0][6] == oggi  # data_fine

    def test_elimina_terapia_definitiva(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC16', 'Dr.', 'Sixteen', 'M', '1980-01-01', 'Roma', 'doc16@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (16, 'DOC16')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ17', 'Paz', 'Eight', 'M', '1990-01-01', 'Roma', 'paz17@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (17, 0, 'PAZ17', 16)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (17, 'Metformina', 2, '500 mg', 16, ?)
        """, (oggi,))
        conn.commit()
        
        medico = Medico(16, db_path)
        medico.eliminaTerapiaDefinitiva(17, 'Metformina')
        
        p = Paziente(17, db_path)
        terapie = p.getTerapieComplete()
        assert len(terapie) == 0

    def test_get_statistiche(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC17', 'Dr.', 'Seventeen', 'M', '1980-01-01', 'Roma', 'doc17@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (17, 'DOC17')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ18', 'Paz', 'Nine', 'M', '1990-01-01', 'Roma', 'paz18@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (18, 0, 'PAZ18', 17)")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ19', 'Paz', 'Ten', 'F', '1995-01-01', 'Milano', 'paz19@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (19, 0, 'PAZ19', 17)")
        conn.commit()
        
        # Aggiungi rilevazione fuori soglia per PAZ19
        p_grave = Paziente(19, db_path)
        p_grave.aggiungiRilevazioneGiornaliera(oggi, '08:00', 200.0, 'P')
        
        medico = Medico(17, db_path)
        stats = medico.getStatistiche()
        assert stats['totale'] == 2
        assert stats['in_regola'] == 1  # PAZ18
        assert stats['gravi'] == 1      # PAZ19

    def test_get_pazienti_con_dettaglio(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC18', 'Dr.', 'Eighteen', 'M', '1980-01-01', 'Roma', 'doc18@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (18, 'DOC18')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ20', 'Paz', 'Eleven', 'M', '1990-01-01', 'Roma', 'paz20@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (20, 0, 'PAZ20', 18)")
        conn.commit()
        
        # Aggiungi rilevazione fuori soglia e terapia non rispettata
        p = Paziente(20, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 150.0, 'P')
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (20, 'Metformina', 2, '500 mg', 18, ?)
        """, (oggi,))
        conn.commit()
        p._aggiorna_gravita_db()
        
        medico = Medico(18, db_path)
        dettaglio = medico.getPazientiConDettaglio()
        assert len(dettaglio) == 1
        assert dettaglio[0]['nome'] == 'Paz'
        assert dettaglio[0]['cognome'] == 'Eleven'
        assert dettaglio[0]['gravita'] >= 1

    def test_registra_operazione(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC19', 'Dr.', 'Nineteen', 'M', '1980-01-01', 'Roma', 'doc19@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (19, 'DOC19')")
        conn.commit()
        
        medico = Medico(19, db_path)
        medico.registra_operazione('TEST', 'TEST_TABLE', '1', 'Test operazione')
        
        log = medico.get_log_operazioni()
        assert len(log) >= 1
        assert log[0][0] == 'TEST'
        assert log[0][2] == 'Test operazione'

    def test_get_log_operazioni_limite(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC20', 'Dr.', 'Twenty', 'M', '1980-01-01', 'Roma', 'doc20@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (20, 'DOC20')")
        conn.commit()
        
        medico = Medico(20, db_path)
        for i in range(5):
            medico.registra_operazione(f'TEST{i}', 'TEST', str(i), f'Op {i}')
        
        log = medico.get_log_operazioni(limite=3)
        assert len(log) == 3

    def test_str_medico(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC21', 'Mario', 'Rossi', 'M', '1980-01-01', 'Roma', 'doc21@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (21, 'DOC21')")
        conn.commit()
        
        medico = Medico(21, db_path)
        str_repr = str(medico)
        assert 'Mario' in str_repr
        assert 'Rossi' in str_repr

    def test_getters(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel)
        VALUES ('DOC22', 'Giuseppe', 'Verdi', 'M', '1975-05-15', 'Milano', 'g.verdi@test.com', '333123456')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (22, 'DOC22')")
        conn.commit()
        
        medico = Medico(22, db_path)
        assert medico.getIdRef() == 22
        assert medico.getNome() == 'Giuseppe'
        assert medico.getCognome() == 'Verdi'
        assert medico.getSesso() == 'M'
        assert medico.getDataNascita() == '1975-05-15'
        assert medico.getLuogoNascita() == 'Milano'
        assert medico.getEmail() == 'g.verdi@test.com'
        assert medico.getCel() == '333123456'

    def test_prescrivi_terapia_quantita_zero(self, db_path, init_db):
        """Test prescrizione con quantità zero - non deve essere inserita"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC30', 'Dr.', 'Thirty', 'M', '1980-01-01', 'Roma', 'doc30@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (30, 'DOC30')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ30', 'Paz', 'Zero', 'M', '1990-01-01', 'Roma', 'paz30@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (30, 0, 'PAZ30', 30)")
        conn.commit()
        
        medico = Medico(30, db_path)
        medico.prescriviTerapia(30, 'FarmacoZero', 0, '0 mg', oggi)
        
        # La terapia NON deve essere stata inserita
        p = Paziente(30, db_path)
        terapie = p.getTerapie()
        assert len(terapie) == 0

    def test_prescrivi_terapia_paziente_non_assegnato(self, db_path, init_db):
        """Test prescrizione a paziente non assegnato al medico"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        # Medico 31
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC31', 'Dr.', 'ThirtyOne', 'M', '1980-01-01', 'Roma', 'doc31@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (31, 'DOC31')")
        # Medico 32 (proprietario del paziente)
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC32', 'Dr.', 'ThirtyTwo', 'M', '1980-01-01', 'Roma', 'doc32@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (32, 'DOC32')")
        # Paziente assegnato al medico 32
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ31', 'Paz', 'Other', 'M', '1990-01-01', 'Roma', 'paz31@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (31, 0, 'PAZ31', 32)")
        conn.commit()
        
        # Medico 31 prova a prescrivere al paziente del medico 32
        medico = Medico(31, db_path)
        # Non dovrebbe crashare, ma la prescrizione viene comunque inserita
        medico.prescriviTerapia(31, 'Farmaco', 1, '10 mg', oggi)
        
        p = Paziente(31, db_path)
        terapie = p.getTerapie()
        assert len(terapie) == 1

    def test_interrompi_terapia_inesistente(self, db_path, init_db):
        """Test interruzione terapia inesistente"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC33', 'Dr.', 'ThirtyThree', 'M', '1980-01-01', 'Roma', 'doc33@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (33, 'DOC33')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ32', 'Paz', 'NoTer', 'M', '1990-01-01', 'Roma', 'paz32@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (32, 0, 'PAZ32', 33)")
        conn.commit()
        
        medico = Medico(33, db_path)
        # Non dovrebbe crashare
        medico.interrompiTerapia(32, 'FarmacoInesistente', oggi)

    def test_elimina_terapia_inesistente(self, db_path, init_db):
        """Test eliminazione terapia inesistente"""
        conn = init_db
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC34', 'Dr.', 'ThirtyFour', 'M', '1980-01-01', 'Roma', 'doc34@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (34, 'DOC34')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ33', 'Paz', 'NoDel', 'M', '1990-01-01', 'Roma', 'paz33@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (33, 0, 'PAZ33', 34)")
        conn.commit()
        
        medico = Medico(34, db_path)
        # Non dovrebbe crashare
        medico.eliminaTerapiaDefinitiva(33, 'FarmacoInesistente')

    def test_paziente_senza_medico(self, db_path, init_db):
        """Test caricamento medico senza pazienti"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC35', 'Dr.', 'Empty', 'M', '1980-01-01', 'Roma', 'doc35@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (35, 'DOC35')")
        conn.commit()
        
        medico = Medico(35, db_path)
        assert medico.getPazientiIds() == []
        assert medico.getPazienti() == []
        
        stats = medico.getStatistiche()
        assert stats['totale'] == 0

    def test_getters_medico(self, db_path, init_db):
        """Test getters medico con tutti i campi"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email, cel, indirizzo)
        VALUES ('DOC36', 'Giovanni', 'Bianchi', 'M', '1970-01-15', 'Firenze', 'g.bianchi@test.com', '333000111', 'Via Medici 5')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (36, 'DOC36')")
        conn.commit()
        
        medico = Medico(36, db_path)
        assert medico.getIdRef() == 36
        assert medico.getCf() == 'DOC36'
        assert medico.getNome() == 'Giovanni'
        assert medico.getCognome() == 'Bianchi'
        assert medico.getSesso() == 'M'
        assert medico.getDataNascita() == '1970-01-15'
        assert medico.getLuogoNascita() == 'Firenze'
        assert medico.getEmail() == 'g.bianchi@test.com'
        assert medico.getCel() == '333000111'
        assert medico.getIndirizzo() == 'Via Medici 5'

    def test_prescrivi_terapia_con_data_fine(self, db_path, init_db):
        """Test prescrizione con data_fine esplicita"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        fine = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC37', 'Dr.', 'DateEnd', 'M', '1980-01-01', 'Roma', 'doc37@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (37, 'DOC37')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ34', 'Paz', 'DateEnd', 'M', '1990-01-01', 'Roma', 'paz34@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (34, 0, 'PAZ34', 37)")
        conn.commit()
        
        medico = Medico(37, db_path)
        medico.prescriviTerapia(34, 'Antibiotico', 3, '500 mg', oggi, fine, 'Dopo i pasti')
        
        p = Paziente(34, db_path)
        terapie = p.getTerapieComplete()
        assert len(terapie) == 1
        assert terapie[0][0] == 'Antibiotico'
        assert terapie[0][6] == fine  # data_fine