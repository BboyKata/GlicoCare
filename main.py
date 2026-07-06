import flet as ft
import os
import sys
import time
import sqlite3
from ui.dashboard_medico import show_doctor_dashboard
from src.user import User, CredenzialiNonValide
from ui.dashboard_paziente import show_patient_dashboard


def get_data_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        test_file = os.path.join(script_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print(f"Database verrà creato in: {script_dir}")
        return script_dir
    except (PermissionError, OSError):
        pass
    
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, ".glicocare")
    os.makedirs(data_dir, exist_ok=True)
    print(f"Database verrà creato in: {data_dir}")
    return data_dir


DATA_PATH = get_data_path()
db = os.path.join(DATA_PATH, "glicocare.db")


def init_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(script_dir, "database", "schema.sql")
    popola_path = os.path.join(script_dir, "database", "popola_test.sql")

    if os.path.exists(db):
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PAZIENTE'")
            if cursor.fetchone() is None:
                conn.close()
                os.remove(db)
            else:
                conn.close()
        except:
            pass
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
    except FileNotFoundError:
        print(f"ERRORE FATALE: File schema.sql non trovato in {schema_path}")
        return
    
    cursor.execute("SELECT COUNT(*) FROM PAZIENTE")
    if cursor.fetchone()[0] == 0:
        try:
            with open(popola_path, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
            print(f"Database popolato con dati di test in: {db}")
        except FileNotFoundError:
            print(f"ERRORE: File popola_test.sql non trovato in {popola_path}")
    else:
        print(f"Database già popolato in: {db}")
    
    conn.commit()
    conn.close()


def handle_login(e: ft.ControlEvent):
    global username_field, password_field, error_label

    username = username_field.value
    password = password_field.value
    
    try:
        error_label.value = ""
        error_label.update()
    except Exception:
        pass

    if not username or not password:
        try:
            error_label.value = "Inserisci username e password"
            error_label.color = "red"
            error_label.update()
        except Exception:
            pass
        return
    
    try:
        user = User(username, password, db)
        if user.is_paziente():
            show_patient_dashboard(e.page, user, db_path=db) 
        elif user.is_medico():
            show_doctor_dashboard(e.page, user, db_path=db)
    except CredenzialiNonValide:
        try:
            error_label.value = "Username o password errati"
            error_label.color = "red"
            error_label.update()
        except Exception:
            pass
    except Exception as ex:
        try:
            error_label.value = f"Errore: {str(ex)}"
            error_label.color = "red"
            error_label.update()
            error_label.selectable = True
        except Exception:
            pass


def show_login_page(page: ft.Page):
    global username_field, password_field, error_label

    page.controls.clear()
    page.title = "GlicoCare"
    page.bgcolor = "white"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.resizable = True
    page.window.maximized = True
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "img", "glicocare.png")
    
    # Fallback se l'immagine non esiste
    if os.path.exists(logo_path):
        logo_widget = ft.Image(src=logo_path, width=320, height=320)
    else:
        logo_widget = ft.Icon(ft.Icons.MEDICAL_SERVICES, size=200, color="#2563eb")
    
    left_col = ft.Container(
        content=ft.Column([
            logo_widget,
            ft.Text("Il tuo compagno per il\ncontrollo della glicemia", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#1e293b"),
            ft.Text("Monitoraggio semplice e sicuro", size=14, color="#475569", text_align=ft.TextAlign.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
        bgcolor="#EEF2FF", expand=2, padding=40
    )

    username_field = ft.TextField(label="Username", width=400, text_size=16, border_color="#cbd5e1", on_submit=handle_login)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=400, text_size=16, border_color="#cbd5e1", on_submit=handle_login)
    error_label = ft.Text("", size=14, selectable=True)
    login_btn = ft.Button(content=ft.Text("Accedi", size=18, weight=ft.FontWeight.BOLD, color="white"), width=400, height=55, bgcolor="#2563eb", on_click=handle_login)

    right_col = ft.Container(
        content=ft.Column([
            ft.Text("Bentornato", size=36, weight=ft.FontWeight.BOLD, color="#0f172a"),
            ft.Text("Inserisci le tue credenziali per accedere", size=16, color="#475569"),
            ft.Container(height=30),
            username_field,
            password_field,
            error_label,
            login_btn,
            ft.Container(height=20),
            ft.Text("© 2026 GlicoCare - Tutti i diritti riservati", size=12, color="#94a3b8")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        bgcolor="white", expand=3, padding=40
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=0))
    page.update()


def main(page: ft.Page):
    try:
        init_database()
        print(f"Database init: {os.path.abspath(db)}")
        page.window.maximized = True
        page.update()
        show_login_page(page)
    except Exception as e:
        print(f"ERRORE CRITICO: {e}")
        page.controls.clear()
        page.add(ft.Text(f"Errore durante l'avvio:\n{str(e)}", color="red", size=20))
        page.update()


if __name__ == "__main__":
    time.sleep(0.3)  # Previene conflitti di inizializzazione
    ft.app(target=main)