"""
GlicoCare - Applicazione Desktop per il Monitoraggio della Glicemia.
"""

import flet as ft
import os

from src.user import User, CredenzialiNonValide
from ui.dashboard_paziente import show_patient_dashboard
from ui.dashboard_medico import show_doctor_dashboard

db = os.path.join("database", "glicocare.db")


def init_database():
    import sqlite3
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())
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
            show_patient_dashboard(e.page, user)
        elif user.is_medico():
            show_doctor_dashboard(e.page, user)
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
        except Exception:
            pass


def show_login_page(page: ft.Page):
    global username_field, password_field, error_label

    page.controls.clear()

    page.title = "GlicoCare"
    page.bgcolor = "white"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- QUI LE IMPOSTAZIONI DELLA FINESTRA ---
    # page.window.width = 1100   # <-- Rimuovi (o commenta) queste righe
    # page.window.height = 700   # <-- Rimuovi (o commenta) queste righe
    page.window.resizable = True
    page.window.maximized = True  # <-- AGGIUNGI QUESTA RIGA
    # --------------------------------------------
    

    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "glicocare.png")
    left_col = ft.Container(
        content=ft.Column([
            ft.Image(src=logo_path, width=320, height=320),
            ft.Text("Il tuo compagno per il\ncontrollo della glicemia", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#1e293b"),
            ft.Text("Monitoraggio semplice e sicuro", size=14, color="#475569", text_align=ft.TextAlign.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
        bgcolor="#EEF2FF", expand=2, padding=40
    )

    username_field = ft.TextField(label="Username", width=400, text_size=16, border_color="#cbd5e1", on_submit=handle_login)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=400, text_size=16, border_color="#cbd5e1", on_submit=handle_login)
    error_label = ft.Text("", size=14)
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
            ft.Text("© 2024 GlicoCare - Tutti i diritti riservati", size=12, color="#94a3b8")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        bgcolor="white", expand=3, padding=40
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=0))
    page.update()


def main(page: ft.Page):
    show_login_page(page)


if __name__ == "__main__":
    init_database()
    print(f"Database init: {os.path.abspath(db)}")
    ft.app(target=main)