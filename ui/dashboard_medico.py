import flet as ft
import os
from src.user import User
from src.medico import Medico
from src.paziente import Paziente
from ui.dettaglio_paziente import show_paziente_detail
from ui.log_page import show_log_page

_loading = False

def show_doctor_dashboard(page: ft.Page, user: User, db_path: str = None):
    global _loading
    _loading = False  # Si ripristina ogni volta che la dashboard viene caricata

    # Usa il percorso passato, oppure un fallback
    if db_path is None:
        home = os.path.expanduser("~")
        db_path = os.path.join(home, ".glicocare", "glicocare.db")

    page.controls.clear()
    page.title = "GlicoCare - Medico"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    medico = Medico(user.id_ref, db_path)
    pazienti = medico.getPazientiConDettaglio()
    stats = medico.getStatistiche()

    # --- HEADER CON LOGOUT e LOG ---
    header = ft.Row([
        ft.Text("GlicoCare - Area Medico", size=24, weight=ft.FontWeight.BOLD, color="#1e293b"),
        ft.Row([
            ft.Container(
                width=120, height=36, bgcolor="#6366f1", border_radius=8,
                alignment=ft.alignment.center,
                on_click=lambda e: show_log_page(page, user, db_path=db_path),
                content=ft.Text("Log", size=13, color="white", weight=ft.FontWeight.BOLD)
            ),
            ft.Container(width=8),
            ft.Container(
                width=110, height=36, bgcolor="#ef4444", border_radius=8,
                alignment=ft.alignment.center,
                on_click=lambda e: show_login_page(page),
                content=ft.Text("Logout", size=13, color="white", weight=ft.FontWeight.BOLD)
            ),
        ])
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # --- COLONNA SINISTRA: Lista pazienti ---
    items = []
    for paz in pazienti:
        gravita = paz['gravita']
        if gravita > 5:
            gravita_color = "#ef4444"
        elif gravita > 0:
            gravita_color = "#f59e0b"
        else:
            gravita_color = "#10b981"

        if paz['tipo'] == "Glicemia + Terapia":
            icona = ft.Icon(ft.Icons.WARNING, color="#ef4444", size=20)
        elif paz['tipo'] == "Glicemia fuori soglia":
            icona = ft.Icon(ft.Icons.MONITOR_HEART, color="#f59e0b", size=20)
        elif paz['tipo'] == "Terapia non rispettata":
            icona = ft.Icon(ft.Icons.MEDICATION, color="#8b5cf6", size=20)
        else:
            icona = ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10b981", size=20)

        # Crea il pulsante occhio con la funzione anti-doppio-click
        occhio_btn = ft.IconButton(
            icon=ft.Icons.VISIBILITY, icon_color="#2563eb", icon_size=22,
            tooltip="Visualizza paziente",
            on_click=lambda e, pid=paz['id']: _apri_paziente(page, user, pid, db_path)
        )

        items.append(
            ft.Container(
                padding=12, bgcolor="white", border_radius=10,
                margin=ft.margin.only(bottom=8),
                shadow=ft.BoxShadow(blur_radius=6, color="rgba(0,0,0,0.04)"),
                content=ft.Row([
                    icona,
                    ft.Column([
                        ft.Text(f"{paz['nome']} {paz['cognome']}", weight=ft.FontWeight.BOLD, size=16, color="#1e293b"),
                        ft.Text(paz['tipo'], size=14, color="#64748b"),
                    ], expand=True, spacing=4),
                    ft.Container(
                        bgcolor=gravita_color, border_radius=20,
                        padding=ft.padding.symmetric(horizontal=14, vertical=6),
                        content=ft.Text(str(gravita), color="white", weight=ft.FontWeight.BOLD, size=15)
                    ),
                    occhio_btn
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )

    left_col = ft.Container(
        expand=2, padding=20, bgcolor="#FFFFFF", border_radius=16,
        content=ft.Column([
            ft.Text("I tuoi pazienti", size=22, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Text(f"Ordinati per gravità — {stats['totale']} totali", size=14, color="#64748b"),
            ft.Divider(color="#e2e8f0"),
            ft.ListView(controls=items, expand=True, spacing=0)
        ], expand=True)
    )

    card_width = 150
    card_padding = 14
    icon_size = 22
    value_size = 22
    title_size = 11

    right_col = ft.Container(
        expand=3, padding=30, bgcolor="#F8FAFC",
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column([
            ft.Text("Prospetto Generale", size=24, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0"),
            ft.Container(height=10),

            ft.Row([
                _card_stat("Pazienti totali", str(stats['totale']), "#2563eb", ft.Icons.PEOPLE,
                           width=card_width, padding=card_padding, icon_size=icon_size,
                           value_size=value_size, title_size=title_size),
                ft.Container(width=8),
                _card_stat("In regola", str(stats['in_regola']), "#10b981", ft.Icons.CHECK_CIRCLE,
                           width=card_width, padding=card_padding, icon_size=icon_size,
                           value_size=value_size, title_size=title_size),
                ft.Container(width=8),
                _card_stat("Con gravità", str(stats['gravi']), "#ef4444", ft.Icons.WARNING,
                           width=card_width, padding=card_padding, icon_size=icon_size,
                           value_size=value_size, title_size=title_size),
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),

            ft.Container(height=8),

            ft.Row([
                _card_stat("Glicemia fuori soglia", str(stats['solo_glicemia']), "#f59e0b", ft.Icons.MONITOR_HEART,
                           width=card_width, padding=card_padding, icon_size=icon_size,
                           value_size=value_size, title_size=title_size),
                ft.Container(width=8),
                _card_stat("Terapia non rispettata", str(stats['solo_terapia']), "#8b5cf6", ft.Icons.MEDICATION,
                           width=card_width, padding=card_padding, icon_size=icon_size,
                           value_size=value_size, title_size=title_size),
                ft.Container(width=8),
                _card_stat("Entrambi i problemi", str(stats['entrambi']), "#ef4444", ft.Icons.ERROR,
                           width=card_width, padding=card_padding, icon_size=icon_size,
                           value_size=value_size, title_size=title_size),
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),

            ft.Container(height=15),

            # Gravità media
            ft.Container(
                padding=12,
                bgcolor="white",
                border_radius=12,
                border=ft.border.all(1, "#e2e8f0"),
                content=ft.Row([
                    ft.Icon(ft.Icons.TRENDING_UP, color="#2563eb", size=24),
                    ft.Column([
                        ft.Text("Gravità media", size=13, color="#64748b"),
                        ft.Text(str(stats['gravita_media']), size=22, weight=ft.FontWeight.BOLD, color="#1e293b"),
                    ]),
                ], alignment=ft.MainAxisAlignment.START)
            ),
            ft.Container(height=12),

            ft.Text("Pazienti con gravità > 0", size=16, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0"),
            ft.Container(height=5),
            ft.Container(
                height=180,
                content=ft.ListView(
                    controls=[
                        ft.Container(
                            padding=8, bgcolor="white", border_radius=6,
                            margin=ft.margin.only(bottom=4),
                            content=ft.Row([
                                ft.Text(f"{p['nome']} {p['cognome']}", weight=ft.FontWeight.BOLD, size=13),
                                ft.Text(f"Gravità: {p['gravita']} ({p['tipo']})", size=12, color="#64748b")
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        )
                        for p in pazienti if p['gravita'] > 0
                    ],
                    expand=True,
                    spacing=0
                ) if stats['gravi'] > 0 else ft.Text("Nessun paziente con gravità.", color="#64748b", size=14)
            ),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )

    page.add(
        ft.Column([
            header,
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=8),
            ft.Row(controls=[left_col, right_col], expand=True, spacing=20)
        ], expand=True)
    )
    page.update()


def _apri_paziente(page: ft.Page, user: User, pid: int, db_path: str):
    """Apre la pagina del paziente in modo sicuro, evitando doppi click."""
    global _loading
    
    if _loading:
        return  # Già in caricamento, ignora click multipli
    
    _loading = True
    show_paziente_detail(page, user, pid, db_path=db_path)


def _card_stat(titolo: str, valore: str, colore: str, icona,
               width=180, padding=20, icon_size=28, value_size=28, title_size=12) -> ft.Container:
    return ft.Container(
        width=width, padding=padding, bgcolor="white", border_radius=10,
        shadow=ft.BoxShadow(blur_radius=6, color="rgba(0,0,0,0.04)"),
        content=ft.Column([
            ft.Icon(icona, color=colore, size=icon_size),
            ft.Text(valore, size=value_size, weight=ft.FontWeight.BOLD, color=colore),
            ft.Text(titolo, size=title_size, color="#64748b", text_align=ft.TextAlign.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)
    )


# --- SISTEMAZIONE DELL'IMPORT CIRCOLARE ---
def show_login_page(page: ft.Page):
    # Importo locale per evitare il loop
    from main import show_login_page as main_login
    main_login(page)