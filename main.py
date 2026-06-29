"""
GlicoCare - Applicazione Desktop per il Monitoraggio della Glicemia.
"""

import flet as ft
import os
import sqlite3
import io
import base64
from datetime import datetime

from src.user import User, CredenzialiNonValide
from src.paziente import Paziente

db = os.path.join("database", "glicocare.db")


def init_database():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()


def crea_grafico_glicemia_matplotlib(rilevazioni):
    oggi = datetime.now().date()
    giorni_x = []
    valori_y = []
    
    for giorno_str, ora_str, glicemia, _ in rilevazioni:
        try:
            data_rilev = datetime.strptime(giorno_str, "%Y-%m-%d").date()
            if (oggi - data_rilev).days <= 30:
                giorni_x.append(giorno_str[-5:])
                valori_y.append(glicemia)
        except ValueError:
            continue
    
    if not giorni_x:
        return None

    giorni_x.reverse()
    valori_y.reverse()

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(9, 4.5), facecolor='#F8FAFC')
        ax = plt.axes()
        ax.set_facecolor('#FFFFFF')
        
        plt.plot(giorni_x, valori_y, marker='o', color='#2563eb', linestyle='-', linewidth=2, markersize=6)
        plt.title("Andamento Glicemia (Ultimi 30 giorni)", fontsize=14, fontweight='bold', color='#1e293b')
        plt.ylabel("mg/dL", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.5)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_data
    except Exception as e:
        print(f"Errore grafico: {e}")
        return None


def show_patient_dashboard(page: ft.Page, user: User):
    while len(page.controls) > 0:
        page.controls.pop()
    
    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Paziente"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    img_data = crea_grafico_glicemia_matplotlib(paziente.getRilevazioni())
    
    if img_data:
        grafico_widget = ft.Image(
            src_base64=img_data,
            fit=ft.ImageFit.CONTAIN,
            width=700, 
            height=350
        )
    else:
        grafico_widget = ft.Container(
            content=ft.Text("Nessuna rilevazione disponibile.", size=16, color="#64748b"),
            bgcolor="white", padding=40, border_radius=16,
            alignment=ft.alignment.center
        )

    medico_info = paziente.getMedicoRiferimento()
    medico_nome = f"{medico_info[0]} {medico_info[1]}" if medico_info else "Medico non assegnato"
    medico_email = medico_info[2] if medico_info else "N/D"
    medico_cel = medico_info[3] if medico_info else "N/D"

    def btn_click(e, nome):
        print(f"Cliccato {nome}")

    # --- COLONNA SINISTRA ---
    left_col = ft.Container(
        expand=1, 
        padding=40, 
        bgcolor="#FFFFFF",
        content=ft.Column(
            controls=[
                ft.Text(f"Benvenuto, {paziente.getNome()}!", size=28, weight=ft.FontWeight.BOLD, color="#1e293b"),
                ft.Text("Cosa vuoi fare oggi?", size=16, color="#64748b"),
                ft.Container(height=20),
                
                # PULSANTE 1 (Blu) - Testo più lungo va a capo
                ft.Container(
                    width=280,
                    height=60,
                    bgcolor="#2563eb",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=10,
                    on_click=lambda e: btn_click(e, "Registrazione"),
                    content=ft.Text(
                        "Registrazione giornaliera", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    )
                ),
                ft.Container(height=10),
                
                # PULSANTE 2 (Arancione)
                ft.Container(
                    width=280,
                    height=60,
                    bgcolor="#f59e0b",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=10,
                    on_click=lambda e: btn_click(e, "Sintomi"),
                    content=ft.Text(
                        "Segnala sintomi", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    )
                ),
                ft.Container(height=10),
                
                # PULSANTE 3 (Verde)
                ft.Container(
                    width=280,
                    height=60,
                    bgcolor="#10b981",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=10,
                    on_click=lambda e: btn_click(e, "Contatta"),
                    content=ft.Text(
                        "Contatta Medico", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    )
                ),
                
                ft.Container(expand=True),
                
                # LOGOUT (Rosso)
                ft.Container(
                    width=280,
                    height=50,
                    bgcolor="#ef4444",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    on_click=lambda e: show_login_page(e.page),
                    content=ft.Text(
                        "Logout", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.START, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # --- COLONNA DESTRA ---
    right_col = ft.Container(
        expand=2, padding=40, bgcolor="#F8FAFC",
        content=ft.Column(
            controls=[
                ft.Container(
                    content=grafico_widget,
                    bgcolor="#FFFFFF", padding=20, border_radius=16,
                    shadow=ft.BoxShadow(blur_radius=20, color="rgba(0,0,0,0.1)"),
                    width=700
                ),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Il tuo Medico di Riferimento", size=18, weight=ft.FontWeight.BOLD, color="#1e293b"),
                        ft.Divider(color="#e2e8f0"),
                        ft.Row([ft.Text("Nome:", weight=ft.FontWeight.BOLD, size=14, color="#475569"), ft.Text(medico_nome, size=14, color="#1e293b")]),
                        ft.Row([ft.Text("Email:", weight=ft.FontWeight.BOLD, size=14, color="#475569"), ft.Text(medico_email, size=14, color="#2563eb")]),
                        ft.Row([ft.Text("Telefono:", weight=ft.FontWeight.BOLD, size=14, color="#475569"), ft.Text(medico_cel, size=14, color="#1e293b")]),
                    ]),
                    bgcolor="#FFFFFF", padding=20, border_radius=16, width=700,
                    shadow=ft.BoxShadow(blur_radius=15, color="rgba(0,0,0,0.05)")
                )
            ], 
            alignment=ft.MainAxisAlignment.START, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=0))
    page.update()


def show_doctor_dashboard(page: ft.Page, user: User):
    while len(page.controls) > 0:
        page.controls.pop()
        
    page.title = "GlicoCare - Medico"
    page.bgcolor = "#F8FAFC"
    page.padding = 0
    content = ft.Column(
        controls=[
            ft.Text("Area Medico", size=40, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Text("Benvenuto Dottore! Gestisci i tuoi pazienti qui.", size=18, color="#64748b"),
            ft.Container(height=20),
            ft.Button(
                content=ft.Text("Logout", size=16, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor="#ef4444", width=200, height=50,
                on_click=lambda e: show_login_page(e.page)
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.add(content)
    page.update()


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

    while len(page.controls) > 0:
        page.controls.pop()

    page.title = "GlicoCare"
    page.bgcolor = "white"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.width = 1100
    page.window.height = 700
    page.window.resizable = True

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