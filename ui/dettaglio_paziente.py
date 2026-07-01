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


def show_paziente_detail(page: ft.Page, user: User, id_paz: int, db_path: str = None):
    """Pagina di dettaglio del singolo paziente."""
    from ui.dashboard_medico import show_doctor_dashboard
    
    if db_path is None:
        import os
        home = os.path.expanduser("~")
        db_path = os.path.join(home, ".glicocare", "glicocare.db")

    page.controls.clear()
    page.title = "GlicoCare - Dettaglio Paziente"
    page.bgcolor = "#F8FAFC"
    page.padding = 15
    page.window.maximized = True

    paziente = Paziente(id_paz, db_path)
    medico = Medico(user.id_ref, db_path)

    if id_paz not in medico.getPazientiIds():
        page.add(ft.Text("Paziente non assegnato a questo medico.", color="red", size=18))
        page.update()
        return

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
    # --- MODIFICATO: USA getTerapieComplete() E LOGICA CORRETTA PER ATTIVA/CONCLUSA ---
    terapie = paziente.getTerapieComplete()
    terapie_items = []
    oggi_date = datetime.now().date()
    
    for t in terapie:
        farmaco, ass, qta, ind, _, inizio, fine = t
        is_attiva = False
        
        # LOGICA CORRETTA:
        if fine is None:
            is_attiva = True
        else:
            try:
                data_fine_obj = datetime.strptime(fine, "%Y-%m-%d").date()
                if data_fine_obj >= oggi_date:
                    is_attiva = True
                else:
                    is_attiva = False
            except:
                is_attiva = False

        if is_attiva:
            stato = ft.Container(bgcolor="#10b981", border_radius=12, padding=ft.padding.symmetric(horizontal=8, vertical=2), content=ft.Text("Attiva", color="white", size=11, weight=ft.FontWeight.BOLD))
            date_text = f"Dal {inizio}" + (f" al {fine}" if fine else "")
        else:
            stato = ft.Container(bgcolor="#94a3b8", border_radius=12, padding=ft.padding.symmetric(horizontal=8, vertical=2), content=ft.Text("Conclusa", color="white", size=11, weight=ft.FontWeight.BOLD))
            date_text = f"Dal {inizio} al {fine}"

        terapie_items.append(
            ft.Container(
                padding=12, bgcolor="#f1f5f9", border_radius=8,
                content=ft.Column([
                    ft.Row([
                        ft.Text(farmaco, weight=ft.FontWeight.BOLD, size=17),
                        ft.Text(qta, size=15, color="#64748b"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text(f"{ass} assunzioni/giorno", size=14, color="#64748b"),
                        stato,
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(date_text, size=13, color="#94a3b8", italic=True),
                    ft.Text(ind or "", size=14, color="#94a3b8", italic=True) if ind else ft.Text(""),
                ], spacing=3)
            )
        )
    if not terapie_items:
        terapie_items = [ft.Text("Nessuna terapia prescritta", size=15, color="#94a3b8", italic=True)]

    terapie_card = _build_card(
        "Storico Terapie", 
        ft.Column(terapie_items, spacing=8),
        azioni=[
            ft.TextButton("+ Aggiungi/Modifica", 
                         on_click=lambda e: _popup_terapia(page, paziente, medico, id_paz, lambda: show_paziente_detail(page, user, id_paz, db_path)),
                         style=ft.ButtonStyle(color="#2563eb", text_style=ft.TextStyle(size=15)))
        ]
    )
    # ---------------------------------------------------------------------

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
                on_click=lambda e: show_doctor_dashboard(page, user, db_path=db_path), padding=10
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


# =====================================================================
# POPUP TERAPIA - AGGIUNGI O MODIFICA (CORRETTO PER DATE PERSONALIZZATE)
# =====================================================================
def _popup_terapia(page: ft.Page, paziente: Paziente, medico: Medico, id_paz: int, ricarica_callback):
    # --- 1. Recupera tutte le terapie attive ---
    # --- 1. Recupera tutte le terapie attive (per il menu a tendina) ---
    tutte_terapie = paziente.getTerapieComplete()
    oggi_date = datetime.now().date()
    terapie_attive = []
    
    for t in tutte_terapie:
        farmaco, ass, qta, ind, _, inizio, fine = t
        # Una terapia è attiva SE:
        # 1. non ha data_fine
        # 2. OPPURE ha data_fine futura (>= oggi)
        if fine is None:
            terapie_attive.append(t)
        else:
            try:
                data_fine_obj = datetime.strptime(fine, "%Y-%m-%d").date()
                if data_fine_obj >= oggi_date:
                    terapie_attive.append(t)
            except:
                pass

    terapia_options = [ft.dropdown.Option("__NUOVA__", "➕ Nuova terapia")] + \
                      [ft.dropdown.Option(t[0], f"{t[0]} ({t[2]})") for t in terapie_attive]

    input_farmaco = ft.TextField(label="Nome farmaco", width=300, text_size=16)
    input_assunzioni = ft.TextField(label="N. assunzioni/giorno", width=160, text_size=16, value="1")
    input_quantita = ft.TextField(label="Quantità", width=200, text_size=16)
    input_indicazioni = ft.TextField(label="Indicazioni", width=420, text_size=16, multiline=True, max_lines=3)
    input_select = ft.Dropdown(options=terapia_options, width=300, label="Terapia esistente", text_size=15)

    oggi_date = datetime.now().date()
    oggi_str = oggi_date.strftime("%Y-%m-%d")

    # --- CAMPI DATA (MODIFICABILI A MANO) ---
    data_inizio_field = ft.TextField(
        label="Data inizio terapia (gg-mm-aaaa)",
        value=oggi_date.strftime("%d-%m-%Y"),
        width=300,
        text_size=16,
        read_only=False  # <--- Ora puoi scrivere a mano!
    )
    data_fine_field = ft.TextField(
        label="Data fine (lascia vuoto per attiva)",
        value="",
        width=300,
        text_size=16,
        read_only=False  # <--- Anche questa modificabile a mano!
    )

    # Pulsante per cancellare la data fine (utile se hai scritto a mano)
    def cancella_data_fine(e):
        data_fine_field.value = ""
        data_fine_field.update()

    btn_cancella_fine = ft.IconButton(
        icon=ft.Icons.CLOSE, 
        icon_color="#ef4444", 
        tooltip="Rimuovi data fine (terapia attiva)",
        on_click=cancella_data_fine
    )

    def apri_date_picker_inizio(e):
        page.open(
            ft.DatePicker(
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2030, 12, 31),
                value=oggi_date,
                on_change=lambda e: setattr(data_inizio_field, 'value', e.control.value.strftime("%d-%m-%Y")) or data_inizio_field.update()
            )
        )
    
    def apri_date_picker_fine(e):
        page.open(
            ft.DatePicker(
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2030, 12, 31),
                value=oggi_date,
                on_change=lambda e: setattr(data_fine_field, 'value', e.control.value.strftime("%d-%m-%Y")) or data_fine_field.update()
            )
        )

    status_label = ft.Text("", size=14, color="#ef4444")

    def mostra_errore(msg):
        status_label.value = f"❌ {msg}"
        status_label.color = "#ef4444"
        status_label.update()

    btn_inizio = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker_inizio, icon_color="#2563eb")
    btn_fine = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker_fine, icon_color="#ef4444")

    btn_elimina = ft.Container(
        width=120, height=36, bgcolor="#e2e8f0", border_radius=8,
        alignment=ft.alignment.center,
        content=ft.Text("Elimina", color="#94a3b8", weight=ft.FontWeight.BOLD, size=14),
        on_click=None
    )

    is_initialized = False

    def on_select(e):
        nonlocal is_initialized
        if input_select.value == "__NUOVA__":
            input_farmaco.value = ""
            input_assunzioni.value = "1"
            input_quantita.value = ""
            input_indicazioni.value = ""
            data_inizio_field.value = oggi_date.strftime("%d-%m-%Y")
            data_fine_field.value = ""
            btn_elimina.on_click = None
            btn_elimina.bgcolor = "#e2e8f0"
            btn_elimina.content.color = "#94a3b8"
            status_label.value = ""
            status_label.update()
        else:
            terapia_selezionata = None
            for t in terapie_attive:
                if t[0] == input_select.value:
                    terapia_selezionata = t
                    break
            
            if terapia_selezionata:
                input_farmaco.value = terapia_selezionata[0]
                input_assunzioni.value = str(terapia_selezionata[1])
                input_quantita.value = terapia_selezionata[2]
                input_indicazioni.value = terapia_selezionata[3] or ""
                data_inizio_field.value = datetime.strptime(terapia_selezionata[5], "%Y-%m-%d").strftime("%d-%m-%Y")
                data_fine_field.value = terapia_selezionata[6] if terapia_selezionata[6] else ""
                btn_elimina.on_click = lambda e: _elimina_terapia()
                btn_elimina.bgcolor = "#ef4444"
                btn_elimina.content.color = "white"
                status_label.value = ""
                status_label.update()
        
        if is_initialized:
            input_farmaco.update(); input_assunzioni.update()
            input_quantita.update(); input_indicazioni.update()
            data_inizio_field.update(); data_fine_field.update()
            btn_elimina.update()
            status_label.update()

    input_select.on_change = on_select

    def _elimina_terapia():
        if input_select.value == "__NUOVA__" or not input_select.value:
            return
        farmaco_da_cancellare = input_select.value
        medico.eliminaTerapiaDefinitiva(id_paz, farmaco_da_cancellare)
        page.close(dialog)
        ricarica_callback()

    def salva(e):
        status_label.value = ""
        status_label.update()

        if not input_farmaco.value or not input_quantita.value:
            mostra_errore("Nome farmaco e Quantità sono obbligatori.")
            return
        
        try:
            a = int(input_assunzioni.value)
            if a <= 0:
                mostra_errore("Le assunzioni giornaliere devono essere >= 1.")
                return
        except:
            mostra_errore("Assunzioni giornaliere deve essere un numero.")
            return

        try:
            data_inizio_obj = datetime.strptime(data_inizio_field.value, "%d-%m-%Y")
            data_inizio_str = data_inizio_obj.strftime("%Y-%m-%d")
        except ValueError:
            mostra_errore("Data inizio non valida. Usa formato gg-mm-aaaa.")
            return
            
        data_fine_str = None
        if data_fine_field.value and data_fine_field.value.strip():
            try:
                data_fine_obj = datetime.strptime(data_fine_field.value, "%d-%m-%Y")
                data_fine_str = data_fine_obj.strftime("%Y-%m-%d")
            except ValueError:
                mostra_errore("Data fine non valida. Usa formato gg-mm-aaaa.")
                return

            if data_inizio_str >= data_fine_str:
                mostra_errore("La data di fine deve essere successiva alla data di inizio.")
                return

        # === CONTROLLO ANTICIPATO DEI DUPLICATI ===
        # Prendi tutte le terapie attive (solo quelle senza data fine o con fine futura)
        tutte_terapie = paziente.getTerapieComplete()
        oggi_date = datetime.now().date()
        terapie_attive = [t for t in tutte_terapie if t[6] is None or (t[6] and datetime.strptime(t[6], "%Y-%m-%d").date() >= oggi_date)]
        
        # Se è una nuova prescrizione, controlla che il farmaco non esista già
        if input_select.value == "__NUOVA__":
            for t in terapie_attive:
                if t[0].lower() == input_farmaco.value.lower():
                    mostra_errore(f"❌ Il farmaco '{input_farmaco.value}' è già attivo. Modificalo invece di crearne uno nuovo.")
                    return
        # ======================================================

        try:
            if input_select.value == "__NUOVA__":
                medico.prescriviTerapia(
                    id_paz=id_paz,
                    farmaco=input_farmaco.value,
                    assunzioniGiornaliere=a,
                    quantita=input_quantita.value,
                    data_inizio=data_inizio_str,
                    data_fine=data_fine_str,
                    indicazioni=input_indicazioni.value or None
                )
            else:
                vecchio_nome = input_select.value
                medico.modificaTerapia(
                    id_paz=id_paz,
                    vecchio_farmaco=vecchio_nome,
                    nuovo_farmaco=input_farmaco.value,
                    assunzioniGiornaliere=a,
                    quantita=input_quantita.value,
                    data_inizio=data_inizio_str,
                    data_fine=data_fine_str,
                    indicazioni=input_indicazioni.value or None
                )

            page.close(dialog)
            ricarica_callback()

        except sqlite3.IntegrityError as ex:
            print(f"❌ UNIQUE ERROR: {ex}")
            mostra_errore("❌ Esiste già una terapia con questo farmaco che inizia in questa data. Scegli una data di inizio diversa.")
        except Exception as ex:
            print(f"❌ ERRORE DB: {ex}")
            mostra_errore(f"Errore sistema: {str(ex)}")

    dialog = ft.AlertDialog(
        title=ft.Text("Gestione Terapia", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            input_select,
            ft.Divider(height=1),
            input_farmaco,
            ft.Row([input_assunzioni, input_quantita], spacing=10),
            input_indicazioni,
            ft.Row([data_inizio_field, btn_inizio], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([data_fine_field, btn_fine, btn_cancella_fine], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            status_label,
        ], spacing=12, width=460),
        actions=[
            btn_elimina,
            ft.TextButton("Annulla", on_click=lambda e: page.close(dialog)),
            ft.Container(
                on_click=salva, padding=ft.padding.symmetric(horizontal=24, vertical=12),
                bgcolor="#2563eb", border_radius=8,
                content=ft.Text("Salva Terapia", color="white", weight=ft.FontWeight.BOLD, size=16)
            )
        ]
    )

    if terapia_options:
        input_select.value = terapia_options[0].key
    page.open(dialog)
    is_initialized = True
    if input_select.value:
        on_select(None)