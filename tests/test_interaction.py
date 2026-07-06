# tests/test_interaction.py
import pytest
from datetime import datetime, timedelta
from src.medico import Medico
from src.paziente import Paziente

class TestInteraction:
    def test_flusso_completo_prescrizione_assunzione(self, db_path, init_db):
        """Test end-to-end: medico prescrive -> paziente assume -> medico verifica"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        # Setup
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC001', 'Dr.', 'Smith', 'M', '1980-01-01', 'Roma', 'doc@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (100, 'DOC001')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ001', 'John', 'Doe', 'M', '1990-01-01', 'Milano', 'john@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (100, 0, 'PAZ001', 100)")
        conn.commit()
        
        # 1. Medico prescrive terapia
        medico = Medico(100, db_path)
        medico.prescriviTerapia(100, 'Metformina', 2, '500 mg', oggi)
        
        # 2. Paziente visualizza la terapia
        p = Paziente(100, db_path)
        terapie = p.getTerapie()
        assert len(terapie) == 1
        assert terapie[0][0] == 'Metformina'
        
        # 3. Paziente registra assunzione
        p.aggiungiAssunzione(oggi, '08:00', 'Metformina', '500 mg')
        
        # 4. Paziente registra glicemia
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        
        # 5. Medico verifica dashboard
        medico2 = Medico(100, db_path)
        dettaglio = medico2.getPazientiConDettaglio()
        assert len(dettaglio) == 1

    def test_interazione_due_medici_stesso_paziente(self, db_path, init_db):
        """Due medici visualizzano lo stesso paziente"""
        conn = init_db
        
        # Medico 1 (assegnatario)
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC101', 'Dr.', 'One', 'M', '1980-01-01', 'Roma', 'doc1@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (101, 'DOC101')")
        # Paziente assegnato a medico 101
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ101', 'Jane', 'Doe', 'F', '1990-01-01', 'Milano', 'jane@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (101, 0, 'PAZ101', 101)")
        conn.commit()
        
        # Medico assegnatario può vedere il paziente
        medico1 = Medico(101, db_path)
        p = medico1.getPazienteById(101)
        assert p is not None
        assert p.getNome() == 'Jane'
        
        # Il paziente ha il riferimento corretto al medico
        assert p.getMedicoId() == 101
        medico_ref = p.getMedicoRiferimento()
        assert medico_ref is not None
        assert medico_ref[0] == 'Dr.'
        assert medico_ref[1] == 'One'

    def test_operazione_genera_log(self, db_path, init_db):
        """Verifica che ogni operazione del medico generi un log"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('DOC102', 'Dr.', 'Log', 'M', '1980-01-01', 'Roma', 'doclog@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (102, 'DOC102')")
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('PAZ102', 'Log', 'Patient', 'M', '1990-01-01', 'Milano', 'logp@test.com')
        """)
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (102, 0, 'PAZ102', 102)")
        conn.commit()
        
        medico = Medico(102, db_path)
        
        # Prescrizione -> log
        medico.prescriviTerapia(102, 'FarmacoA', 1, '10 mg', oggi)
        log = medico.get_log_operazioni()
        assert len(log) >= 1
        
        azioni = [l[0] for l in log]
        assert 'PRESCRIZIONE_TERAPIA' in azioni
        
        # Interruzione -> log
        medico.interrompiTerapia(102, 'FarmacoA', oggi)
        log = medico.get_log_operazioni()
        assert len(log) >= 2
        
        azioni = [l[0] for l in log]
        assert 'INTERRUZIONE_TERAPIA' in azioni
        assert 'PRESCRIZIONE_TERAPIA' in azioni