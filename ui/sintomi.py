import flet as ft
from datetime import datetime
from src.paziente import Paziente
from src.user import User


def show_sintomi_page(page: ft.Page, user):
    """Pagina per gestire le segnalazioni (sintomi)."""
    from ui.dashboard_paziente import show_patient_dashboard

    page.controls.clear()

    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Segnalazioni"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    segnalazioni_raw = paziente.getSegnalazioni()
    terapie = paziente.getTerapie()
    segnalazioni_list = [{'giorno_inizio': gi, 'giorno_fine': gf, 'descrizione': d, 'terapia': t} 
                         for gi, gf, d, t in segnalazioni_raw]
    indice_modifica = -1

    terapia_options = [ft.dropdown.Option("", "Nessuna")] + [ft.dropdown.Option(t[0], t[0]) for t in terapie]

    input_data_inizio = ft.TextField(label="Data inizio", hint_text="dd-mm-yyyy", width=180, text_size=15)
    input_data_fine = ft.TextField(label="Data fine", hint_text="dd-mm-yyyy", width=180, text_size=15)
    input_descrizione = ft.TextField(
        hint_text="Descrivi il sintomo o la segnalazione...", 
        width=450, multiline=True, min_lines=4, max_lines=6, text_size=15
    )
    input_terapia = ft.Dropdown(options=terapia_options, width=300, label="Farmaco associato (opzionale)")

    def apri_date_picker_inizio(e):
        def on_change(e):
            input_data_inizio.value = e.control.value.strftime("%d-%m-%Y")
            input_data_inizio.update()
        page.open(ft.DatePicker(on_change=on_change))

    def apri_date_picker_fine(e):
        def on_change(e):
            input_data_fine.value = e.control.value.strftime("%d-%m-%Y")
            input_data_fine.update()
        page.open(ft.DatePicker(on_change=on_change))

    def popup_ok(msg):
        def chiudi(e):
            page.close(d)
            show_sintomi_page(page, user)
        d = ft.AlertDialog(
            title=ft.Text("✅ Operazione completata", color="#10b981"),
            content=ft.Text(msg),
            actions=[ft.TextButton("Ok", on_click=chiudi)]
        )
        page.open(d)

    def popup_err(msg):
        d = ft.AlertDialog(
            title=ft.Text("⚠️ Errore", color="#ef4444"),
            content=ft.Text(msg),
            actions=[ft.TextButton("Ok", on_click=lambda e: page.close(d))]
        )
        page.open(d)

    def popup_conferma_elimina(idx):
        """Popup di conferma prima di eliminare una segnalazione."""
        s = segnalazioni_list[idx]
        try:
            di = datetime.strptime(s['giorno_inizio'], "%Y-%m-%d").strftime("%d-%m-%Y")
            df = datetime.strptime(s['giorno_fine'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            di = s['giorno_inizio']
            df = s['giorno_fine']

        def elimina(e):
            page.close(dialog)
            try:
                paziente.eliminaSegnalazione(s['giorno_inizio'], s['giorno_fine'])
                popup_ok("Segnalazione eliminata con successo!")
            except Exception as ex:
                popup_err(str(ex))

        dialog = ft.AlertDialog(
            title=ft.Text("🗑️ Elimina Segnalazione", color="#ef4444"),
            content=ft.Text(
                f"Sei sicuro di voler eliminare la segnalazione\n"
                f"dal {di} al {df}?\n"
                f"Descrizione: {s['descrizione']}\n\n"
                f"Questa azione è irreversibile.",
                size=15
            ),
            actions=[
                ft.TextButton("Elimina", on_click=elimina, style=ft.ButtonStyle(color="#ef4444")),
                ft.TextButton("Annulla", on_click=lambda e: page.close(dialog))
            ]
        )
        page.open(dialog)

    def carica_modifica(idx):
        nonlocal indice_modifica
        indice_modifica = idx
        s = segnalazioni_list[idx]
        try:
            input_data_inizio.value = datetime.strptime(s['giorno_inizio'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            input_data_inizio.value = s['giorno_inizio']
        try:
            input_data_fine.value = datetime.strptime(s['giorno_fine'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            input_data_fine.value = s['giorno_fine']
        input_descrizione.value = s['descrizione']
        input_terapia.value = s['terapia'] if s['terapia'] else ""
        input_data_inizio.update(); input_data_fine.update(); input_descrizione.update(); input_terapia.update()

    def salva(e):
        nonlocal indice_modifica
        if not all([input_data_inizio.value, input_data_fine.value, input_descrizione.value]):
            popup_err("Data inizio, data fine e descrizione sono obbligatori.")
            return
        try:
            ndi = datetime.strptime(input_data_inizio.value, "%d-%m-%Y").strftime("%Y-%m-%d")
            ndf = datetime.strptime(input_data_fine.value, "%d-%m-%Y").strftime("%Y-%m-%d")
        except:
            popup_err("Date non valide. Usa il formato dd-mm-yyyy.")
            return
        
        # Verifica che data fine >= data inizio
        if ndf < ndi:
            popup_err("La data di fine non può essere precedente alla data di inizio.")
            return

        terapia_val = input_terapia.value if input_terapia.value else None

        if indice_modifica == -1:
            try:
                paziente.aggiungiSegnalazione(ndi, ndf, input_descrizione.value, terapia_val)
                popup_ok("Segnalazione registrata!")
            except Exception as ex:
                popup_err(str(ex))
        else:
            v = segnalazioni_list[indice_modifica]
            try:
                paziente.aggiornaSegnalazione(v['giorno_inizio'], v['giorno_fine'], 
                                              ndi, ndf, input_descrizione.value, terapia_val)
                popup_ok("Segnalazione aggiornata!")
            except Exception as ex:
                popup_err(str(ex))

    # Lista sinistra
    items = []
    for idx, s in enumerate(segnalazioni_list):
        try:
            di = datetime.strptime(s['giorno_inizio'], "%Y-%m-%d").strftime("%d-%m-%Y")
            df = datetime.strptime(s['giorno_fine'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            di = s['giorno_inizio']
            df = s['giorno_fine']
        terapia_str = f" — Farmaco: {s['terapia']}" if s['terapia'] else ""
        
        # Calcola durata
        try:
            d1 = datetime.strptime(s['giorno_inizio'], "%Y-%m-%d")
            d2 = datetime.strptime(s['giorno_fine'], "%Y-%m-%d")
            durata = (d2 - d1).days + 1
            durata_str = f"{durata} giorno{'i' if durata != 1 else ''}"
        except:
            durata_str = "N/D"
        
        items.append(
            ft.Container(
                padding=15, bgcolor="white", border_radius=12,
                margin=ft.margin.only(bottom=10),
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.05)"),
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{di} → {df} ({durata_str})", weight=ft.FontWeight.BOLD, size=15, color="#1e293b"),
                        ft.Text(f"{s['descrizione']}{terapia_str}", size=14, color="#475569")
                    ], expand=True),
                    ft.IconButton(
                        icon=ft.Icons.EDIT, icon_color="#f59e0b",
                        tooltip="Modifica",
                        on_click=lambda e, i=idx: carica_modifica(i)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE, icon_color="#ef4444",
                        tooltip="Elimina",
                        on_click=lambda e, i=idx: popup_conferma_elimina(i)
                    )
                ])
            )
        )

    page.add(ft.Row([
        ft.Container(expand=1, padding=20, bgcolor="white", border_radius=16,
            content=ft.Column([
                ft.Text("Segnalazioni", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListView(controls=items, expand=True)
            ], expand=True)
        ),
        ft.Container(expand=2, padding=40, bgcolor="white", border_radius=16,
            content=ft.Column([
                ft.Container(
                    content=ft.Text("← Torna alla Dashboard", size=16, color="#2563eb", weight=ft.FontWeight.BOLD),
                    on_click=lambda e: show_patient_dashboard(page, user), padding=10
                ),
                ft.Text("Nuova Segnalazione", size=26, weight=ft.FontWeight.BOLD),
                ft.Divider(), ft.Container(height=20),
                # Data inizio e fine sulla stessa linea
                ft.Row([
                    ft.Text("Inizio:", size=15, weight=ft.FontWeight.BOLD),
                    input_data_inizio,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker_inizio, icon_color="#f59e0b"),
                    ft.Text("Fine:", size=15, weight=ft.FontWeight.BOLD),
                    input_data_fine,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker_fine, icon_color="#f59e0b"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Row([
                    ft.Text("Farmaco associato:", size=15, weight=ft.FontWeight.BOLD), 
                    input_terapia
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Text("Descrizione:", size=15, weight=ft.FontWeight.BOLD),
                ft.Container(height=5), 
                input_descrizione,
                ft.Container(height=25),
                ft.Container(
                    width=300, height=55, bgcolor="#f59e0b", border_radius=12,
                    alignment=ft.alignment.center, on_click=salva,
                    content=ft.Text("Salva segnalazione", size=16, color="white", weight=ft.FontWeight.BOLD)
                )
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    ], expand=True, spacing=20))
    page.update()