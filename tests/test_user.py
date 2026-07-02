# tests/test_user.py
import pytest
from src.user import User, CredenzialiNonValide

class TestUser:
    def test_login_successo(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTDOC01', 'Dr.', 'Test', 'M', '1980-01-01', 'Roma', 'doc@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (1, 'TESTDOC01')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('test_user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 1)
        """)
        conn.commit()
        
        user = User('test_user', 'password', db_path)
        assert user.is_paziente() == True
        assert user.is_medico() == False

    def test_login_password_sbagliata(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita)
        VALUES ('TESTDOC02', 'Dr.', 'Test', 'M', '1980-01-01', 'Roma')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (2, 'TESTDOC02')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('test_user2', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 2)
        """)
        conn.commit()
        
        with pytest.raises(CredenzialiNonValide):
            User('test_user2', 'wrong_password', db_path)

    def test_login_username_inesistente(self, db_path, init_db):
        with pytest.raises(CredenzialiNonValide):
            User('inesistente', 'password', db_path)

    def test_is_medico(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU02', 'User', 'Doc', 'M', '1980-01-01', 'Milano', 'u02@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (3, 'TESTU02')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('med_user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 3)
        """)
        conn.commit()
        
        user = User('med_user', 'password', db_path)
        assert user.is_medico() == True
        assert user.is_paziente() == False

    def test_get_user_info(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU03', 'Info', 'Test', 'M', '1990-01-01', 'Roma', 'u03@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (4, 'TESTU03')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('info_user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 4)
        """)
        conn.commit()
        
        user = User('info_user', 'password', db_path)
        info = user.get_user_info()
        assert info['username'] == 'info_user'
        assert info['tipo'] == 'M'
        assert info['id_ref'] == 4

    def test_str_paziente(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU04', 'Str', 'Test', 'M', '1990-01-01', 'Roma', 'u04@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (5, 'TESTU04')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('str_user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 5)
        """)
        conn.commit()
        
        user = User('str_user', 'password', db_path)
        assert 'Paziente' in str(user)
        assert 'str_user' in str(user)

    def test_str_medico(self, db_path, init_db):
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU05', 'Str', 'Med', 'M', '1990-01-01', 'Roma', 'u05@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (6, 'TESTU05')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('str_med', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'M', 6)
        """)
        conn.commit()
        
        user = User('str_med', 'password', db_path)
        assert 'Medico' in str(user)
        assert 'str_med' in str(user)

    def test_hash_password(self):
        from src.user import User
        hash1 = User._hash_password('test')
        hash2 = User._hash_password('test')
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 hex chars
        assert hash1 != User._hash_password('different')

    def test_password_vuota(self, db_path, init_db):
        """Test login con password vuota"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU10', 'Test', 'Empty', 'M', '1990-01-01', 'Roma', 'u10@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (10, 'TESTU10')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('empty_pass', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 10)
        """)
        conn.commit()
        
        with pytest.raises(CredenzialiNonValide):
            User('empty_pass', '', db_path)

    def test_username_vuoto(self, db_path, init_db):
        """Test login con username vuoto"""
        with pytest.raises(CredenzialiNonValide):
            User('', 'password', db_path)

    def test_login_con_spazi(self, db_path, init_db):
        """Test login con spazi nella password"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU11', 'Test', 'Spaces', 'M', '1990-01-01', 'Roma', 'u11@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (11, 'TESTU11')")
        # Hash di 'password' (senza spazi)
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('space_user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 11)
        """)
        conn.commit()
        
        # Password con spazi non deve funzionare
        with pytest.raises(CredenzialiNonValide):
            User('space_user', ' password ', db_path)

    def test_hash_password_diversi(self):
        """Test che password diverse producano hash diversi"""
        from src.user import User
        hash1 = User._hash_password('password1')
        hash2 = User._hash_password('password2')
        assert hash1 != hash2
        assert len(hash1) == 64
        assert len(hash2) == 64

    def test_login_case_sensitive_username(self, db_path, init_db):
        """Test che l'username sia case-sensitive"""
        conn = init_db
        conn.execute("""
        INSERT INTO ANAGRAFICA (CF, nome, cognome, sesso, dataNascita, luogoNascita, email)
        VALUES ('TESTU12', 'Test', 'Case', 'M', '1990-01-01', 'Roma', 'u12@test.com')
        """)
        conn.execute("INSERT INTO MEDICO (id_med, CF) VALUES (12, 'TESTU12')")
        conn.execute("""
        INSERT INTO USER (username, password, tipo, id_ref)
        VALUES ('CaseUser', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'P', 12)
        """)
        conn.commit()
        
        # Username corretto
        user = User('CaseUser', 'password', db_path)
        assert user.is_paziente()
        
        # Username con case diverso deve fallire
        with pytest.raises(CredenzialiNonValide):
            User('caseuser', 'password', db_path)

    def test_login_db_non_esistente(self):
        """Test connessione a database inesistente"""
        with pytest.raises(CredenzialiNonValide):
            User('test_user', 'password', '/tmp/db_inesistente_12345.db')