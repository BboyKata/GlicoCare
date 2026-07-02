# tests/test_gravita.py
import pytest
from datetime import datetime, timedelta
from src.paziente import Paziente

class TestGravita:
    def test_gravita_aumenta_con_glicemia_fuori_soglia(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG01', 'Test', 'User', 'M', '1990-01-01', 'Roma', 'test@mail.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (1, 'TESTG01')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (1, 0, 'TESTG01', 1)")
        conn.commit()
        
        p = Paziente(1, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 150.0, 'P')
        
        assert p.getGravita() == 1
        assert p.getPuntiGlicemia() == 1
        assert p.getPuntiTerapia() == 0

    def test_gravita_aumenta_con_terapia_non_rispettata(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita)
        VALUES ('TESTG02', 'Test', 'User', 'M', '1990-01-01', 'Milano')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (2, 'TESTG02')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (2, 0, 'TESTG02', 2)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (2, 'Metformina', 2, '500 mg', 2, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(2, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        
        assert p.getGravita() == 1
        assert p.getPuntiGlicemia() == 0
        assert p.getPuntiTerapia() == 1

    def test_gravita_terapia_con_data_fine_futura_e_attiva(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        fine_futura = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita)
        VALUES ('TESTG03', 'Test', 'User', 'M', '1990-01-01', 'Torino')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (3, 'TESTG03')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (3, 0, 'TESTG03', 3)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio, data_fine)
        VALUES (3, 'Insulina', 1, '10 UI', 3, ?, ?)
        """, (oggi, fine_futura))
        conn.commit()
        
        p = Paziente(3, db_path)
        assert p.getGravita() == 0
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        
        assert p.getPuntiTerapia() == 1

    def test_gravita_glicemia_pre_prandiale_bassa(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG10', 'Test', 'Grav10', 'M', '1990-01-01', 'Roma', 'g10@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (10, 'TESTG10')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (10, 0, 'TESTG10', 10)")
        conn.commit()
        
        p = Paziente(10, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 70.0, 'P')
        assert p.getGravita() == 1
        assert p.getPuntiGlicemia() == 1

    def test_gravita_glicemia_post_prandiale_alta(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG11', 'Test', 'Grav11', 'M', '1990-01-01', 'Roma', 'g11@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (11, 'TESTG11')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (11, 0, 'TESTG11', 11)")
        conn.commit()
        
        p = Paziente(11, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '14:00', 200.0, 'D')
        assert p.getGravita() == 1
        assert p.getPuntiGlicemia() == 1

    def test_gravita_combinata(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG12', 'Test', 'Grav12', 'M', '1990-01-01', 'Roma', 'g12@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (12, 'TESTG12')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (12, 0, 'TESTG12', 12)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (12, 'Metformina', 2, '500 mg', 12, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(12, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 150.0, 'P')
        assert p.getGravita() >= 2
        assert p.getPuntiGlicemia() == 1
        assert p.getPuntiTerapia() == 1

    def test_gravita_zero_con_glicemia_ok(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG13', 'Test', 'Grav13', 'M', '1990-01-01', 'Roma', 'g13@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (13, 'TESTG13')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (13, 0, 'TESTG13', 13)")
        conn.commit()
        
        p = Paziente(13, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        assert p.getGravita() == 0
        assert p.getPuntiGlicemia() == 0
        assert p.getPuntiTerapia() == 0

    def test_gravita_multiple_rilevazioni(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG14', 'Test', 'Grav14', 'M', '1990-01-01', 'Roma', 'g14@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (14, 'TESTG14')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (14, 0, 'TESTG14', 14)")
        conn.commit()
        
        p = Paziente(14, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 150.0, 'P')  # +1 glicemia
        p.aggiungiRilevazioneGiornaliera(oggi, '12:00', 200.0, 'D')  # +1 glicemia
        p.aggiungiRilevazioneGiornaliera(oggi, '18:00', 90.0, 'P')   # OK
        
        assert p.getPuntiGlicemia() == 2
        assert p.getGravita() == 2

    def test_gravita_con_assunzione_parziale(self, db_path, init_db):
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG15', 'Test', 'Grav15', 'M', '1990-01-01', 'Roma', 'g15@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (15, 'TESTG15')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (15, 0, 'TESTG15', 15)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (15, 'Metformina', 3, '500 mg', 15, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(15, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        p.aggiungiAssunzione(oggi, '08:00', 'Metformina', '500 mg')
        # Solo 1 assunzione su 3 previste -> terapia non rispettata
        
        assert p.getPuntiTerapia() == 1
        assert p.getGravita() == 1

    def test_gravita_giorno_senza_rilevazioni(self, db_path, init_db):
        """Test gravità per giorno senza rilevazioni"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        ieri = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG20', 'Test', 'NoRil', 'M', '1990-01-01', 'Roma', 'g20@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (20, 'TESTG20')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (20, 5, 'TESTG20', 20)")
        conn.commit()
        
        p = Paziente(20, db_path)
        # La gravità viene ricalcolata a 0 perché non ci sono rilevazioni
        assert p.getGravita() == 0

    def test_gravita_solo_assunzioni_complete(self, db_path, init_db):
        """Test gravità zero quando tutte le assunzioni sono fatte"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG21', 'Test', 'AllAss', 'M', '1990-01-01', 'Roma', 'g21@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (21, 'TESTG21')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (21, 0, 'TESTG21', 21)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (21, 'Metformina', 2, '500 mg', 21, ?)
        """, (oggi,))
        conn.commit()
        
        p = Paziente(21, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        p.aggiungiAssunzione(oggi, '08:00', 'Metformina', '500 mg')
        p.aggiungiAssunzione(oggi, '20:00', 'Metformina', '500 mg')
        
        assert p.getPuntiTerapia() == 0
        assert p.getGravita() == 0

    def test_gravita_glicemia_pre_prandiale_limite_inferiore(self, db_path, init_db):
        """Test glicemia pre-prandiale esattamente a 80 (limite)"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG22', 'Test', 'Lim80', 'M', '1990-01-01', 'Roma', 'g22@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (22, 'TESTG22')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (22, 0, 'TESTG22', 22)")
        conn.commit()
        
        p = Paziente(22, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 80.0, 'P')
        assert p.getPuntiGlicemia() == 0  # 80 è il limite, non sotto

    def test_gravita_glicemia_pre_prandiale_limite_superiore(self, db_path, init_db):
        """Test glicemia pre-prandiale esattamente a 130 (limite)"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG23', 'Test', 'Lim130', 'M', '1990-01-01', 'Roma', 'g23@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (23, 'TESTG23')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (23, 0, 'TESTG23', 23)")
        conn.commit()
        
        p = Paziente(23, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 130.0, 'P')
        assert p.getPuntiGlicemia() == 0  # 130 è il limite, non sopra

    def test_gravita_glicemia_post_prandiale_limite(self, db_path, init_db):
        """Test glicemia post-prandiale esattamente a 180 (limite)"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG24', 'Test', 'Lim180', 'M', '1990-01-01', 'Roma', 'g24@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (24, 'TESTG24')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (24, 0, 'TESTG24', 24)")
        conn.commit()
        
        p = Paziente(24, db_path)
        p.aggiungiRilevazioneGiornaliera(oggi, '14:00', 180.0, 'D')
        assert p.getPuntiGlicemia() == 0  # 180 è il limite, non sopra

    def test_gravita_piu_giorni(self, db_path, init_db):
        """Test gravità con rilevazioni in giorni diversi"""
        conn = init_db
        oggi = datetime.now().strftime("%Y-%m-%d")
        ieri = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTG25', 'Test', 'MultiDay', 'M', '1990-01-01', 'Roma', 'g25@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (25, 'TESTG25')")
        conn.execute("INSERT INTO PAZIENTE (id_paz, gravita, CF, medico) VALUES (25, 0, 'TESTG25', 25)")
        conn.execute("""
        INSERT INTO TERAPIA (id_paz, farmaco, assunzioniGiornaliere, quantita, id_med, data_inizio)
        VALUES (25, 'Metformina', 2, '500 mg', 25, ?)
        """, (ieri,))
        conn.commit()
        
        p = Paziente(25, db_path)
        # Ieri: glicemia fuori soglia + terapia non rispettata
        p.aggiungiRilevazioneGiornaliera(ieri, '08:00', 150.0, 'P')
        # Oggi: glicemia OK ma ancora terapia non rispettata
        p.aggiungiRilevazioneGiornaliera(oggi, '08:00', 100.0, 'P')
        
        # 1 punto glicemia (ieri) + 2 punti terapia (ieri e oggi)
        assert p.getPuntiGlicemia() == 1
        assert p.getPuntiTerapia() == 2
        assert p.getGravita() == 3