import flet as ft
from datetime import datetime, timedelta
from src.paziente import Paziente
from src.medico import Medico
from src.user import User
from src.graph_utils import crea_grafico_glicemia_periodo


PERIODO_LABELS = {
    "7": "ultima settimana",
    "30": "ultimo mese",
    "90": "ultimi 3 mesi",
    "365": "ultimo anno",
}


def show_paziente_detail(page: ft.Page, user: User, id_paz: int):
    """Pagina di dettaglio del singolo paziente."""
    from ui.dashboard_medico import show_doctor_dashboard

    page.controls.clear()
    page.title = "GlicoCare - Dettaglio Paziente"
    page.bgcolor = "#F8FAFC"
    page.padding = 15
    page.window.maximized = True

    paziente = Paziente(id_paz)
    medico = Medico(user.id_ref)

    if id_paz not in medico.getPazientiIds():
        page.add(ft.Text("Paziente non assegnato a questo medico.", color="red", size=18))
        page.update()
        return

    # Registra l'accesso al dettaglio paziente
    medico.registra_operazione(
        azione="VISUALIZZA_DETTAGLIO",
        tabella="PAZIENTE",
        id_record=str(id_paz),
        dettaglio=f"Dettaglio paziente {paziente.getNome()} {paziente.getCognome()}"
    )

    # ==========================================================
    # FUNZIONI DI SUPPORTO
    # ==========================================================
    def filtra_rilevazioni(giorni):
        oggi = datetime.now().date()
        limite = oggi - timedelta(days=giorni)
        filtrate = []
        for g, o, v, p in paziente.getRilevazioni():
            try:
                data = datetime.strptime(g, "%Y-%m-%d").date()
                if data >= limite:
                    filtrate.append((g, o, v, p))
            except:
                pass
        return filtrate

    def aggiorna_grafico(giorni):
        label = PERIODO_LABELS.get(str(giorni), f"ultimi {giorni} giorni")
        dati = filtra_rilevazioni(giorni)
        img = crea_grafico_glicemia_periodo(dati, label)
        if img:
            grafico_container.content = ft.Image(src_base64=img, fit=ft.ImageFit.CONTAIN, height=350)
        else:
            grafico_container.content = ft.Container(
                content=ft.Text("Nessuna rilevazione nel periodo", size=18, color="#64748b"),
                bgcolor="white", padding=40, border_radius=12,
                alignment=ft.alignment.center, height=350
            )
        grafico_container.update()

    # ==========================================================
    # COLONNA SINISTRA (40%) — Azioni Medico
    # ==========================================================
    
    # --- TERAPIE ---
    terapie = paziente.getTerapie()
    terapie_items = []
    for t in terapie:
        terapie_items.append(
            ft.Container(
                padding=12, bgcolor="#f1f5f9", border_radius=8,
                content=ft.Column([
                    ft.Row([
                        ft.Text(t[0], weight=ft.FontWeight.BOLD, size=17),
                        ft.Text(t[2], size=15, color="#64748b"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"{t[1]} assunzioni/giorno", size=14, color="#64748b"),
                    ft.Text(t[3] or "", size=14, color="#94a3b8", italic=True) if t[3] else ft.Text(""),
                ], spacing=3)
            )
        )
    if not terapie_items:
        terapie_items = [ft.Text("Nessuna terapia", size=15, color="#94a3b8", italic=True)]

    terapie_card = _build_card(
        "Terapie Prescritte", 
        ft.Column(terapie_items, spacing=8),
        azioni=[
            ft.TextButton("+ Aggiungi/Modifica", 
                         on_click=lambda e: _popup_terapia(page, paziente, medico, id_paz, lambda: show_paziente_detail(page, user, id_paz)),
                         style=ft.ButtonStyle(color="#2563eb", text_style=ft.TextStyle(size=15)))
        ]
    )

    # --- INFO CLINICHE ---
    annotazione_attuale = paziente.getAnnotazione()
    input_annotazione = ft.TextField(
        value=annotazione_attuale,
        hint_text="Descrivi fattori di rischio, comorbidità, note cliniche...",
        multiline=True,
        min_lines=4,
        max_lines=8,
        text_size=15,
        width=500,
    )

    def salva_annotazione(e):
        paziente.aggiornaAnnotazione(input_annotazione.value)
        medico.registra_operazione(
            azione="MODIFICA_ANNOTAZIONE",
            tabella="PAZIENTE",
            id_record=str(id_paz),
            dettaglio=f"Annotazione aggiornata: {input_annotazione.value}"
        )
        page.snack_bar = ft.SnackBar(ft.Text("✅ Annotazione salvata con successo!", size=16))
        page.snack_bar.open = True
        page.update()

    info_card = _build_card(
        "Informazioni Cliniche",
        ft.Column([
            ft.Text("Fattori di rischio, comorbidità, note cliniche:", size=14, color="#64748b"),
            input_annotazione,
        ], spacing=8),
        azioni=[
            ft.TextButton("Salva", on_click=salva_annotazione, 
                         style=ft.ButtonStyle(color="#8b5cf6", text_style=ft.TextStyle(size=15)))
        ]
    )

    # --- ULTIME RILEVAZIONI ---
    rilevazioni = paziente.getRilevazioni()[:8]
    rilev_items = []
    for r in rilevazioni:
        try:
            dv = datetime.strptime(r[0], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dv = r[0]
        rilev_items.append(
            ft.Row([
                ft.Text(f"{dv}  {r[1]}", size=15, color="#64748b"),
                ft.Text(f"{r[2]} mg/dL", size=15, weight=ft.FontWeight.BOLD),
                ft.Text("Pre" if r[3] == 'P' else "Post", size=14, color="#94a3b8"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
    if not rilev_items:
        rilev_items = [ft.Text("Nessuna rilevazione", size=15, color="#94a3b8", italic=True)]

    rilev_card = _build_card("Ultime Rilevazioni", ft.Column(rilev_items, spacing=5))

    # --- STATO PAZIENTE ---
    gravita = paziente.getGravita()
    if gravita > 10:
        colore_g = "#ef4444"
        icona_g = ft.Icon(ft.Icons.ERROR, color="#ef4444", size=26)
    elif gravita > 0:
        colore_g = "#f59e0b"
        icona_g = ft.Icon(ft.Icons.WARNING, color="#f59e0b", size=26)
    else:
        colore_g = "#10b981"
        icona_g = ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10b981", size=26)

    stato_card = _build_card(
        "Stato Paziente",
        ft.Column([
            ft.Row([icona_g, ft.Text(f"Gravità: {gravita}", size=22, weight=ft.FontWeight.BOLD, color=colore_g)]),
            ft.ProgressBar(value=min(gravita / 20, 1.0), color=colore_g, bgcolor="#e2e8f0", height=10),
            ft.Row([
                ft.Text(f"Glicemia: {paziente.getPuntiGlicemia()}", size=16, color="#f59e0b", weight=ft.FontWeight.BOLD),
                ft.Text(f"Terapia: {paziente.getPuntiTerapia()}", size=16, color="#8b5cf6", weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ], spacing=10)
    )

    left_col = ft.Container(
        expand=4, padding=5,
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ARROW_BACK, color="#2563eb", size=22),
                    ft.Text("Torna alla Dashboard", size=17, color="#2563eb", weight=ft.FontWeight.BOLD),
                ]),
                on_click=lambda e: show_doctor_dashboard(page, user), padding=10
            ),
            ft.Text(f"{paziente.getNome()} {paziente.getCognome()}", size=26, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=8),
            stato_card,
            ft.Container(height=10),
            terapie_card,
            ft.Container(height=10),
            info_card,
            ft.Container(height=10),
            rilev_card,
        ], scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)
    )

    # ==========================================================
    # COLONNA DESTRA (60%) — Anagrafica + Grafico
    # ==========================================================
    
    periodo_dd = ft.Dropdown(
        options=[
            ft.dropdown.Option("7", "Ultima settimana"),
            ft.dropdown.Option("30", "Ultimo mese"),
            ft.dropdown.Option("90", "Ultimi 3 mesi"),
            ft.dropdown.Option("365", "Ultimo anno"),
        ],
        value="30",
        width=220,
        text_size=16,
        on_change=lambda e: aggiorna_grafico(int(periodo_dd.value))
    )

    img_data = crea_grafico_glicemia_periodo(filtra_rilevazioni(30), "ultimo mese")
    if img_data:
        grafico_content = ft.Image(src_base64=img_data, fit=ft.ImageFit.CONTAIN, height=350)
    else:
        grafico_content = ft.Container(
            content=ft.Text("Nessuna rilevazione nel periodo", size=18, color="#64748b"),
            bgcolor="white", padding=40, border_radius=12,
            alignment=ft.alignment.center, height=350
        )

    grafico_container = ft.Container(content=grafico_content)

    grafico_card = ft.Container(
        padding=20, bgcolor="white", border_radius=12,
        content=ft.Column([
            ft.Row([
                ft.Text("Andamento Glicemia", size=20, weight=ft.FontWeight.BOLD, color="#1e293b"),
                periodo_dd,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=10),
            grafico_container,
        ])
    )

    # Anagrafica (3 campi per riga)
    sesso = paziente.getSesso()
    anagrafica_card = ft.Container(
        padding=20, bgcolor="white", border_radius=12,
        content=ft.Column([
            ft.Text("Anagrafica", size=20, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=10),
            ft.Row([
                _anag_field("Nome", paziente.getNome()),
                _anag_field("Cognome", paziente.getCognome()),
                _anag_field("Sesso", sesso),
            ]),
            ft.Row([
                _anag_field("Data di nascita", paziente.getDataNascita()),
                _anag_field("Luogo di nascita", paziente.getLuogoNascita()),
                _anag_field("CF", paziente.getCf()),
            ]),
            ft.Row([
                _anag_field("Email", paziente.getEmail() or "N/D"),
                _anag_field("Cellulare", paziente.getCel() or "N/D"),
                _anag_field("Indirizzo", paziente.getIndirizzo() or "N/D"),
            ]),
        ], spacing=8)
    )

    right_col = ft.Container(
        expand=6, padding=5,
        content=ft.Column([
            anagrafica_card,
            ft.Container(height=10),
            grafico_card,
        ], scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=10))
    page.update()


def _build_card(titolo: str, contenuto, azioni: list = None) -> ft.Container:
    header = ft.Row([
        ft.Text(titolo, size=17, weight=ft.FontWeight.BOLD, color="#1e293b"),
    ])
    if azioni:
        header.controls.extend(azioni)
    
    return ft.Container(
        padding=14, bgcolor="white", border_radius=10,
        border=ft.border.all(1, "#e2e8f0"),
        content=ft.Column([
            header,
            ft.Divider(color="#e2e8f0", height=1),
            ft.Container(height=6),
            contenuto,
        ], spacing=0)
    )


def _anag_field(label: str, value: str):
    return ft.Container(
        expand=1, padding=8,
        content=ft.Column([
            ft.Text(label, size=13, color="#94a3b8", weight=ft.FontWeight.BOLD),
            ft.Text(value, size=17, color="#1e293b", weight=ft.FontWeight.W_500),
        ], spacing=3)
    )


def _popup_terapia(page: ft.Page, paziente: Paziente, medico: Medico, id_paz: int, ricarica_callback):
    terapie = paziente.getTerapie()
    terapia_options = [ft.dropdown.Option("__NUOVA__", "➕ Nuova terapia")] + \
                      [ft.dropdown.Option(t[0], f"{t[0]} ({t[2]})") for t in terapie]
    
    input_farmaco = ft.TextField(label="Nome farmaco", width=300, text_size=16)
    input_assunzioni = ft.TextField(label="N. assunzioni/giorno", width=160, text_size=16, value="1")
    input_quantita = ft.TextField(label="Quantità", width=200, text_size=16)
    input_indicazioni = ft.TextField(label="Indicazioni", width=420, text_size=16, multiline=True, max_lines=3)
    input_select = ft.Dropdown(options=terapia_options, width=300, label="Terapia esistente", text_size=15)
    
    def on_select(e):
        if input_select.value == "__NUOVA__":
            input_farmaco.value = ""
            input_assunzioni.value = "1"
            input_quantita.value = ""
            input_indicazioni.value = ""
        else:
            t = paziente.getTerapieByName(input_select.value)
            if t:
                input_farmaco.value = t[0]
                input_assunzioni.value = str(t[1])
                input_quantita.value = t[2]
                input_indicazioni.value = t[3] or ""
        input_farmaco.update(); input_assunzioni.update()
        input_quantita.update(); input_indicazioni.update()
    
    input_select.on_change = on_select

    def salva(e):
        if not input_farmaco.value or not input_quantita.value:
            return
        try:
            a = int(input_assunzioni.value)
            if a <= 0:
                return
        except:
            return
        # TODO: qui andrà il metodo per aggiungere/aggiornare terapia nel DB
        # Per ora registriamo solo il log e chiudiamo il popup

        azione = "AGGIUNTA_TERAPIA" if input_select.value == "__NUOVA__" else "MODIFICA_TERAPIA"
        medico.registra_operazione(
            azione=azione,
            tabella="TERAPIA",
            id_record=f"{id_paz}/{input_farmaco.value}",
            dettaglio=f"{input_farmaco.value} - {input_assunzioni.value}/die - {input_quantita.value}"
        )
        page.close(dialog)
        ricarica_callback()

    dialog = ft.AlertDialog(
        title=ft.Text("Gestione Terapia", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            input_select,
            ft.Divider(height=1),
            input_farmaco,
            ft.Row([input_assunzioni, input_quantita], spacing=10),
            input_indicazioni,
        ], spacing=12, width=460),
        actions=[
            ft.TextButton("Annulla", on_click=lambda e: page.close(dialog)),
            ft.Container(
                on_click=salva, padding=ft.padding.symmetric(horizontal=24, vertical=12),
                bgcolor="#2563eb", border_radius=8,
                content=ft.Text("Salva Terapia", color="white", weight=ft.FontWeight.BOLD, size=16)
            )
        ]
    )
    page.open(dialog)