import flet as ft
import os
from datetime import datetime
from src.paziente import Paziente
from src.user import User
from src.graph_utils import crea_grafico_glicemia_matplotlib
from ui.registrazione import show_registrazione_page
from ui.assunzioni import show_assunzioni_page
from ui.sintomi import show_sintomi_page


def show_patient_dashboard(page: ft.Page, user: User, db_path: str = None): 
    page.controls.clear()
    
    # Usa il percorso passato, oppure un fallback
    if db_path is None:
        home = os.path.expanduser("~")
        db_path = os.path.join(home, ".glicocare", "glicocare.db")
    
    paziente = Paziente(user.id_ref, db_path=db_path)  
    page.title = "GlicoCare - Paziente"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    img_data = crea_grafico_glicemia_matplotlib(paziente.getRilevazioni())
    
    if img_data:
        grafico_widget = ft.Image(src_base64=img_data, fit=ft.ImageFit.CONTAIN)
    else:
        grafico_widget = ft.Container(
            content=ft.Text("Nessuna rilevazione disponibile.", size=16, color="#64748b"),
            bgcolor="white", padding=40, border_radius=16,
            alignment=ft.alignment.center
        )

    medico_info = paziente.getMedicoRiferimento()
    medico_nome = f"{medico_info[0]} {medico_info[1]}" if medico_info else "Medico non assegnato"
    medico_email = medico_info[2] if medico_info else "N/D"

    oggi_str = datetime.now().strftime("%Y-%m-%d")

    ultima_glicemia_oggi = None
    for g, o, gli, p in paziente.getRilevazioni():
        if g == oggi_str:
            ultima_glicemia_oggi = (g, o, gli, p)
            break

    ultima_assunzione_oggi = None
    for g, o, farmaco, quantita in paziente.getAssunzioni():
        if g == oggi_str:
            ultima_assunzione_oggi = (g, o, farmaco, quantita)
            break

    if ultima_glicemia_oggi:
        stato_glicemia = ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10b981", size=20),
            ft.Text(f"Glicemia: {ultima_glicemia_oggi[2]} mg/dL alle {ultima_glicemia_oggi[1]}", 
                   color="#166534", size=15, weight=ft.FontWeight.W_500)
        ])
    else:
        stato_glicemia = ft.Row([
            ft.Icon(ft.Icons.WARNING, color="#ef4444", size=20),
            ft.Text("Glicemia: Dato odierno mancante!", color="#991b1b", size=15, weight=ft.FontWeight.BOLD)
        ])

    if ultima_assunzione_oggi:
        stato_assunzione = ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10b981", size=20),
            ft.Text(f"Farmaco: {ultima_assunzione_oggi[2]} ({ultima_assunzione_oggi[3]})", 
                   color="#166534", size=15, weight=ft.FontWeight.W_500)
        ])
    else:
        stato_assunzione = ft.Row([
            ft.Icon(ft.Icons.WARNING, color="#ef4444", size=20),
            ft.Text("Farmaco: Nessuna assunzione oggi!", color="#991b1b", size=15, weight=ft.FontWeight.BOLD)
        ])

    box_segnalazioni = ft.Container(
        padding=20, bgcolor="#FFFFFF", border_radius=12,
        border=ft.border.all(1, "#e2e8f0"),
        shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.05)"),
        content=ft.Column([
            ft.Text("Riepilogo odierno", size=16, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=5),
            stato_glicemia,
            ft.Container(height=8),
            stato_assunzione
        ], spacing=2)
    )

    def btn_logout(e):
        from main import show_login_page
        show_login_page(page)

    # --- COLONNA SINISTRA (30%) ---
    left_col = ft.Container(
        expand=3,
        padding=30, 
        bgcolor="#FFFFFF",
        content=ft.ListView(
            controls=[
                ft.Text(
                    f"{'Benvenuta' if paziente.getSesso() == 'F' else 'Benvenuto'}, {paziente.getNome()}!", 
                    size=28, weight=ft.FontWeight.BOLD, color="#1e293b"
                ),                
                ft.Text("Cosa vuoi fare oggi?", size=16, color="#64748b"),
                ft.Container(height=25),
                box_segnalazioni,
                ft.Container(height=20),
                ft.Container(
                    height=65, bgcolor="#2563eb", border_radius=12,
                    alignment=ft.alignment.center, padding=10,
                    on_click=lambda e: show_registrazione_page(page, user,db_path),
                    content=ft.Text("Registrazione giornaliera", size=16, color="white", 
                                   weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                ),
                ft.Container(height=12),
                ft.Container(
                    height=65, bgcolor="#f59e0b", border_radius=12,
                    alignment=ft.alignment.center, padding=10,
                    on_click=lambda e: show_sintomi_page(page, user,db_path),
                    content=ft.Text("Aggiungi segnalazione", size=16, color="white", 
                                   weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                ),
                ft.Container(height=12),
                ft.Container(
                    height=65, bgcolor="#10b981", border_radius=12,
                    alignment=ft.alignment.center, padding=10,
                    on_click=lambda e: show_assunzioni_page(page, user,db_path),
                    content=ft.Text("Aggiungi assunzione farmaco", size=16, color="white", 
                                   weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                ),
                ft.Container(height=12),
                ft.Container(
                    height=55, bgcolor="#ef4444", border_radius=12,
                    alignment=ft.alignment.center,
                    on_click=btn_logout,
                    content=ft.Text("Logout", size=16, color="white", weight=ft.FontWeight.BOLD)
                )
            ],
            expand=True,
            spacing=0
        )
    )

    # --- COLONNA DESTRA (70%) ---
    # Lista terapie (scrollabile)
    terapie_complete = paziente.getTerapie()
    # getTerapie() restituisce già SOLO quelle attive
        
    terapia_items = []
    for t in terapie_complete:
        # t: (farmaco, assunzioniGiornaliere, quantita, indicazioni, id_med, data_inizio)
        # Mostra anche la data di inizio per contesto
        data_inizio_vis = t[5]  # data_inizio è l'ultimo elemento della tupla
        terapia_items.append(
            ft.Container(
                padding=10, bgcolor="#f1f5f9", border_radius=8,
                content=ft.Column([
                    ft.Row([
                        ft.Text(t[0], weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(t[2], size=12, color="#64748b"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"{t[1]} assunzioni/giorno", size=11, color="#64748b"),
                    ft.Text(f"Dal {data_inizio_vis}", size=10, color="#94a3b8", italic=True),
                    ft.Text(t[3] or "", size=11, color="#94a3b8", italic=True) if t[3] else ft.Text(""),
                ], spacing=2)
            )
        )
    if not terapia_items:
        terapia_items = [ft.Text("Nessuna terapia attiva prescritta", size=13, color="#94a3b8", italic=True)]

    terapie_lista = ft.Container(
        padding=10, bgcolor="white", border_radius=12,
        border=ft.border.all(1, "#e2e8f0"),
        expand=1,   # occupa 1 parte della Row
        content=ft.Column([
            ft.Text("Le tue Terapie Attive", size=16, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=5),
            ft.ListView(
                controls=terapia_items,
                expand=True,
                spacing=5
            )
        ])
    )

    # Grafico (senza altezza fissa, si espande)
    grafico_card = ft.Container(
        content=grafico_widget,
        bgcolor="#FFFFFF", padding=20, border_radius=16,
        shadow=ft.BoxShadow(blur_radius=20, color="rgba(0,0,0,0.1)"),
        expand=3   # occupa 3 parti della Row
    )

    # Riga terapie | grafico
    riga_terapie_grafico = ft.Row([
        terapie_lista,
        ft.Container(width=15),
        grafico_card
    ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc_img_path = os.path.join(current_dir, "img", "doc.png")
    
    right_col = ft.Container(
        expand=7,
        padding=30, 
        bgcolor="#F8FAFC",
        content=ft.Column([
            riga_terapie_grafico,
            ft.Container(height=20),
            ft.Container(
                bgcolor="#FFFFFF", padding=20, border_radius=16,
                shadow=ft.BoxShadow(blur_radius=15, color="rgba(0,0,0,0.05)"),
                content=ft.Row([
                    ft.Column([
                        ft.Text("Il tuo Medico di Riferimento", size=18, weight=ft.FontWeight.BOLD, color="#1e293b"),
                        ft.Divider(color="#e2e8f0"),
                        ft.Row([ft.Text("Nome:", weight=ft.FontWeight.BOLD, size=14, color="#475569"),
                                ft.Text(medico_nome, size=14, color="#1e293b", selectable=True)]),
                        ft.Row([ft.Text("Email:", weight=ft.FontWeight.BOLD, size=14, color="#475569"),
                                ft.Text(medico_email, size=14, color="#2563eb", selectable=True)]),
                    ], expand=True, alignment=ft.MainAxisAlignment.START),
                    ft.Container(
                        width=100, height=100, bgcolor="#f1f5f9", border_radius=50,
                        alignment=ft.alignment.center,
                        content=ft.Image(src=doc_img_path, width=90, height=90,
                                        fit=ft.ImageFit.COVER, border_radius=50)
                        if os.path.exists(doc_img_path) else ft.Text("👤", size=40)
                    )
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START, spacing=20)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=20))
    page.update()