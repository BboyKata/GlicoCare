"""
GlicoCare - Applicazione Desktop per il Monitoraggio della Glicemia.

Questo modulo implementa l'interfaccia grafica (GUI) dell'applicazione GlicoCare
utilizzando il framework Flet. Fornisce le schermate per l'autenticazione
di Medici e Pazienti, e la gestione delle rispettive dashboard.

L'applicazione si connette a un database SQLite per gestire le credenziali
e i dati degli utenti.

Typical usage example:
    from app_flet import main
    ft.run(main)
"""

import flet as ft
import os
import sqlite3

from src.user import User, CredenzialiNonValide

# Costante globale per il percorso del database (ORA DENTRO LA CARTELLA database/)
db = os.path.join("database", "glicocare.db")


def init_database():
    """
    Inizializza e configura il database SQLite.

    Questa funzione si connette al database specificato dalla variabile globale 'db',
    attiva il supporto per le chiavi esterne (foreign keys) ed esegue lo script
    SQL contenuto nel file 'database/schema.sql' per creare le tabelle necessarie
    se non esistono già.

    Returns:
        None
    """
    # Assicuriamoci che la cartella 'database' esista prima di creare il file
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Percorso dello schema aggiornato
    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()


def show_patient_dashboard(page: ft.Page, user: User):
    """
    Visualizza la dashboard per l'utente Paziente.

    Pulisce la pagina corrente e costruisce l'interfaccia dedicata al paziente,
    mostrando un messaggio di benvenuto e un pulsante per effettuare il logout.

    Args:
        page (ft.Page): L'oggetto pagina di Flet su cui costruire l'interfaccia.
        user (User): L'oggetto utente autenticato, contenente i dati del paziente.
    
    Returns:
        None
    """
    page.clean()
    page.title = "GlicoCare - Paziente"
    
    content = ft.Column(
        controls=[
            ft.Text("Area Paziente", size=40, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Text("Benvenuto! Qui potrai visualizzare i tuoi dati.", size=18, color="#64748b"),
            ft.Container(height=20),
            ft.Button(
                content=ft.Text("Logout", size=16, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor="#ef4444", 
                width=200, height=50,
                on_click=lambda e: show_login(e.page)
            )
        ],
        alignment="center",
        horizontal_alignment="center"
    )
    page.add(content)
    page.update()


def show_doctor_dashboard(page: ft.Page, user: User):
    """
    Visualizza la dashboard per l'utente Medico.

    Pulisce la pagina corrente e costruisce l'interfaccia dedicata al medico,
    mostrando un messaggio di benvenuto personalizzato e un pulsante per il logout.

    Args:
        page (ft.Page): L'oggetto pagina di Flet su cui costruire l'interfaccia.
        user (User): L'oggetto utente autenticato, contenente i dati del medico.

    Returns:
        None
    """
    page.clean()
    page.title = "GlicoCare - Medico"
    
    content = ft.Column(
        controls=[
            ft.Text("Area Medico", size=40, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Text("Benvenuto Dottore! Gestisci i tuoi pazienti qui.", size=18, color="#64748b"),
            ft.Container(height=20),
            ft.Button(
                content=ft.Text("Logout", size=16, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor="#ef4444", 
                width=200, height=50,
                on_click=lambda e: show_login(e.page)
            )
        ],
        alignment="center",
        horizontal_alignment="center"
    )
    page.add(content)
    page.update()


def handle_login(e: ft.ControlEvent):
    """
    Gestisce la logica di autenticazione dell'utente.

    Questa funzione viene attivata al clic del pulsante "Accedi" o alla pressione
    del tasto "Invio" nei campi di input. Recupera Username e Password,
    valida i campi, e tenta l'autenticazione tramite la classe User.
    In caso di successo, reindirizza alla dashboard corretta. In caso di fallimento,
    mostra un messaggio di errore a schermo.

    Args:
        e (ft.ControlEvent): L'oggetto evento generato da Flet. Contiene il riferimento
            alla pagina attuale tramite `e.page`.
    
    Returns:
        None
    
    Raises:
        CredenzialiNonValide: Se le credenziali fornite non corrispondono a nessun utente.
        Exception: Per qualsiasi altro errore imprevisto durante l'autenticazione.
    """
    global username_field, password_field, error_label

    username = username_field.value
    password = password_field.value
    error_label.value = ""
    error_label.update()
    
    if not username or not password:
        error_label.value = "Inserisci username e password"
        error_label.color = "red"
        error_label.update()
        return
    
    try:
        user = User(username, password, db)
        
        if user.is_paziente():
            show_patient_dashboard(e.page, user)
        elif user.is_medico():
            show_doctor_dashboard(e.page, user)
            
    except CredenzialiNonValide:
        error_label.value = "Username o password errati"
        error_label.color = "red"
        error_label.update()
    except Exception as e:
        error_label.value = f"Errore: {str(e)}"
        error_label.color = "red"
        error_label.update()


def show_login(page: ft.Page):
    """
    Costruisce e visualizza la schermata di login.

    Questa funzione pulisce la pagina corrente e disegna l'interfaccia a due colonne:
    - Colonna sinistra: Branding, logo e slogan.
    - Colonna destra: Form di login con campi Username, Password e pulsante Accedi.

    Args:
        page (ft.Page): L'oggetto pagina di Flet su cui costruire l'interfaccia.

    Returns:
        None
    """
    global username_field, password_field, error_label

    page.clean()
    page.title = "GlicoCare"
    page.window.width = 1100
    page.window.height = 700
    page.window.resizable = True
    page.padding = 0 
    page.bgcolor = "white"
    page.theme_mode = ft.ThemeMode.LIGHT

    # COLONNA SINISTRA (Branding)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "img", "glicocare.png")
    
    left_col = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(src=logo_path, width=320, height=320),
                ft.Text("Il tuo compagno per il\ncontrollo della glicemia", 
                        size=24, weight=ft.FontWeight.BOLD, text_align="center", color="#1e293b"),
                ft.Text("Monitoraggio semplice e sicuro", 
                        size=14, color="#475569", text_align="center")
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20
        ),
        bgcolor="#eef2ff", 
        expand=2,
        padding=40
    )

    # COLONNA DESTRA (Form di Login)
    username_field = ft.TextField(
        label="Username",
        width=400,
        text_size=16,
        border_color="#cbd5e1",
        on_submit=handle_login
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=400,
        text_size=16,
        border_color="#cbd5e1",
        on_submit=handle_login
    )

    error_label = ft.Text("", size=14)

    login_btn = ft.Button(
        content=ft.Text("Accedi", size=18, weight=ft.FontWeight.BOLD, color="white"),
        width=400,
        height=55,
        bgcolor="#2563eb",
        on_click=handle_login
    )

    right_col = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Bentornato", size=36, weight=ft.FontWeight.BOLD, color="#0f172a"),
                ft.Text("Inserisci le tue credenziali per accedere", size=16, color="#475569"),
                ft.Container(height=30),
                username_field,
                password_field,
                error_label,
                login_btn,
                ft.Container(height=20),
                ft.Text("© 2024 GlicoCare - Tutti i diritti riservati", size=12, color="#94a3b8")
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=15
        ),
        bgcolor="white",
        expand=3,
        padding=40
    )

    page.add(
        ft.Row(
            controls=[left_col, right_col],
            expand=True,
            spacing=0
        )
    )
    
    page.update()


def main(page: ft.Page):
    """
    Funzione principale dell'applicazione Flet.

    È il punto d'ingresso dell'interfaccia grafica. Chiama la funzione 
    per costruire la schermata di login.

    Args:
        page (ft.Page): L'oggetto pagina passato da Flet al momento dell'avvio.
    
    Returns:
        None
    """
    show_login(page)


if __name__ == "__main__":
    """
    Esegue l'inizializzazione del database e avvia l'applicazione Flet.
    """
    init_database()
    print(f"Database init: {os.path.abspath(db)}")
    ft.run(main)