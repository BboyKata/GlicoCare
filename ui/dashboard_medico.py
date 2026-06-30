import flet as ft
from src.user import User
from src.medico import Medico
from src.paziente import Paziente


def show_doctor_dashboard(page: ft.Page, user: User):
    from main import show_login_page

    page.controls.clear()
    page.title = "GlicoCare - Medico"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    medico = Medico(user.id_ref)
    pazienti = medico.getPazientiConDettaglio()
    stats = medico.getStatistiche()

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
            icona = ft.Icon(ft.Icons.WARNING, color="#ef4444", size=18)
        elif paz['tipo'] == "Glicemia fuori soglia":
            icona = ft.Icon(ft.Icons.MONITOR_HEART, color="#f59e0b", size=18)
        elif paz['tipo'] == "Terapia non rispettata":
            icona = ft.Icon(ft.Icons.MEDICATION, color="#8b5cf6", size=18)
        else:
            icona = ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10b981", size=18)

        items.append(
            ft.Container(
                padding=15, bgcolor="white", border_radius=12,
                margin=ft.margin.only(bottom=10),
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.05)"),
                content=ft.Row([
                    icona,
                    ft.Column([
                        ft.Text(f"{paz['nome']} {paz['cognome']}", weight=ft.FontWeight.BOLD, size=15, color="#1e293b"),
                        ft.Text(paz['tipo'], size=13, color="#64748b"),
                    ], expand=True),
                    ft.Container(
                        bgcolor=gravita_color, border_radius=20,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        content=ft.Text(str(gravita), color="white", weight=ft.FontWeight.BOLD, size=14)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY, icon_color="#2563eb",
                        tooltip="Visualizza paziente",
                        on_click=lambda e, pid=paz['id']: show_paziente_detail(page, user, pid)
                    )
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )

    left_col = ft.Container(
        expand=2, padding=20, bgcolor="#FFFFFF", border_radius=16,
        content=ft.Column([
            ft.Text("I tuoi pazienti", size=24, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Text(f"Ordinati per gravità — {stats['totale']} totali", size=14, color="#64748b"),
            ft.Divider(color="#e2e8f0"),
            ft.ListView(controls=items, expand=True, spacing=0)
        ], expand=True)
    )

    # --- COLONNA DESTRA: Prospetto ---
    right_col = ft.Container(
        expand=3, padding=40, bgcolor="#F8FAFC",
        content=ft.Column([
            ft.Text("Prospetto Generale", size=26, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0"),
            ft.Container(height=20),

            ft.Row([
                _card_stat("Pazienti totali", str(stats['totale']), "#2563eb", ft.Icons.PEOPLE),
                _card_stat("In regola", str(stats['in_regola']), "#10b981", ft.Icons.CHECK_CIRCLE),
                _card_stat("Con gravità", str(stats['gravi']), "#ef4444", ft.Icons.WARNING),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),

            ft.Container(height=20),

            ft.Row([
                _card_stat("Glicemia fuori soglia", str(stats['solo_glicemia']), "#f59e0b", ft.Icons.MONITOR_HEART),
                _card_stat("Terapia non rispettata", str(stats['solo_terapia']), "#8b5cf6", ft.Icons.MEDICATION),
                _card_stat("Entrambi i problemi", str(stats['entrambi']), "#ef4444", ft.Icons.ERROR),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),

            ft.Container(height=30),

            ft.Container(
                padding=20, bgcolor="white", border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.05)"),
                content=ft.Row([
                    ft.Icon(ft.Icons.TRENDING_UP, color="#2563eb", size=28),
                    ft.Column([
                        ft.Text("Gravità media", size=14, color="#64748b"),
                        ft.Text(str(stats['gravita_media']), size=24, weight=ft.FontWeight.BOLD, color="#1e293b"),
                    ]),
                ], alignment=ft.MainAxisAlignment.START)
            ),

            ft.Container(height=20),

            ft.Text("Pazienti con gravità > 0", size=18, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0"),
            ft.Container(height=10),
            ft.ListView(
                controls=[
                    ft.Container(
                        padding=10, bgcolor="white", border_radius=8,
                        margin=ft.margin.only(bottom=8),
                        content=ft.Row([
                            ft.Text(f"{p['nome']} {p['cognome']}", weight=ft.FontWeight.BOLD, size=14),
                            ft.Text(f"Gravità: {p['gravita']} ({p['tipo']})", size=13, color="#64748b")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
                    for p in pazienti if p['gravita'] > 0
                ],
                expand=True
            ) if stats['gravi'] > 0 else ft.Text("Nessun paziente con gravità.", color="#64748b", size=14),

            ft.Container(height=20),
            ft.Container(
                width=250, height=50, bgcolor="#ef4444", border_radius=12,
                alignment=ft.alignment.center,
                on_click=lambda e: show_login_page(page),
                content=ft.Text("Logout", size=16, color="white", weight=ft.FontWeight.BOLD)
            )
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=20))
    page.update()


def _card_stat(titolo: str, valore: str, colore: str, icona) -> ft.Container:
    """Crea una card statistica per il prospetto."""
    return ft.Container(
        width=180, padding=20, bgcolor="white", border_radius=12,
        shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.05)"),
        content=ft.Column([
            ft.Icon(icona, color=colore, size=28),
            ft.Text(valore, size=28, weight=ft.FontWeight.BOLD, color=colore),
            ft.Text(titolo, size=12, color="#64748b", text_align=ft.TextAlign.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )


def show_paziente_detail(page: ft.Page, user: User, id_paz: int):
    """Pagina di dettaglio del singolo paziente."""
    from ui.dashboard_medico import show_doctor_dashboard

    page.controls.clear()
    page.title = "GlicoCare - Dettaglio Paziente"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    paziente = Paziente(id_paz)
    medico = Medico(user.id_ref)

    # Verifica che il paziente sia assegnato a questo medico
    if id_paz not in medico.getPazientiIds():
        page.add(ft.Text("Paziente non assegnato a questo medico.", color="red"))
        page.update()
        return

    page.add(ft.Column([
        ft.Container(
            content=ft.Text("← Torna alla Dashboard Medico", size=16, color="#2563eb", weight=ft.FontWeight.BOLD),
            on_click=lambda e: show_doctor_dashboard(page, user), padding=10
        ),
        ft.Text(f"Dettaglio Paziente: {paziente.getNome()} {paziente.getCognome()}", size=26, weight=ft.FontWeight.BOLD),
        ft.Text(f"Gravità totale: {paziente.getGravita()} | "
               f"Glicemia: {paziente.getPuntiGlicemia()} | "
               f"Terapia: {paziente.getPuntiTerapia()}", size=16),
        ft.Text("(Funzionalità in sviluppo)", size=14, color="#64748b"),
    ], alignment=ft.MainAxisAlignment.START))
    page.update()