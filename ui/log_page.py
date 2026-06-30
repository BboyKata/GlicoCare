import flet as ft
from src.medico import Medico
from src.user import User


def show_log_page(page: ft.Page, user: User):
    """Pagina per visualizzare il log delle operazioni del medico."""
    from ui.dashboard_medico import show_doctor_dashboard

    page.controls.clear()
    page.title = "GlicoCare - Log Operazioni"
    page.bgcolor = "#F8FAFC"
    page.padding = 20
    page.window.maximized = True

    medico = Medico(user.id_ref)
    logs = medico.get_log_operazioni(limite=100)

    items = []
    for azione, tabella, dettaglio, data_ora in logs:
        items.append(
            ft.Container(
                padding=12, bgcolor="white", border_radius=8,
                margin=ft.margin.only(bottom=8),
                border=ft.border.all(1, "#e2e8f0"),
                content=ft.Column([
                    ft.Row([
                        ft.Text(azione, weight=ft.FontWeight.BOLD, size=14, color="#1e293b", 
                                overflow=ft.TextOverflow.VISIBLE),
                        ft.Text(data_ora, size=12, color="#64748b"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Tabella: {tabella}", size=13, color="#475569", 
                            overflow=ft.TextOverflow.VISIBLE),
                    ft.Text(f"Dettaglio: {dettaglio or 'N/D'}", size=13, color="#475569", 
                            overflow=ft.TextOverflow.VISIBLE, no_wrap=False, width=None),
                ], spacing=5, expand=True)
            )
        )

    if not items:
        items = [ft.Text("Nessuna operazione registrata.", size=15, color="#94a3b8", italic=True)]

    page.add(
        ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK, color="#2563eb", size=20),
                        ft.Text("Torna alla Dashboard", size=16, color="#2563eb", weight=ft.FontWeight.BOLD),
                    ]),
                    on_click=lambda e: show_doctor_dashboard(page, user), padding=10
                ),
                ft.Text("Log Operazioni", size=24, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ]),
            ft.Divider(color="#e2e8f0"),
            ft.ListView(controls=items, expand=True, spacing=0)
        ], expand=True)
    )
    page.update()