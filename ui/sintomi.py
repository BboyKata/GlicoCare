import flet as ft
from datetime import datetime
from src.paziente import Paziente
from src.user import User


def show_sintomi_page(page: ft.Page, user):
    from ui.dashboard_paziente import show_patient_dashboard

    page.controls.clear()

    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Segnalazioni"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    # Recupera le segnalazioni: (giorno, ora, sintomo, terapia)
    segnalazioni_raw = paziente.getSegnalazioni()
    terapie = paziente.getTerapie()
    
    segnalazioni_list = [{'giorno': g, 'ora': o, 'sintomo': s, 'terapia': t} 
                         for g, o, s, t in segnalazioni_raw]
    indice_modifica = -1

    terapia_options = [ft.dropdown.Option("", "Nessuna")] + [ft.dropdown.Option(t[0], t[0]) for t in terapie]

    input_giorno = ft.TextField(label="Data", hint_text="dd-mm-yyyy", width=180, text_size=15)
    input_ora = ft.TextField(label="Ora", hint_text="HH:MM", width=180, text_size=15)
    input_sintomo = ft.TextField(
        hint_text="Descrivi il sintomo...", 
        width=450, multiline=True, min_lines=4, max_lines=6, text_size=15
    )
    input_terapia = ft.Dropdown(options=terapia_options, width=300, label="Farmaco associato (opzionale)")

    def apri_date_picker(e):
        def on_change(e):
            input_giorno.value = e.control.value.strftime("%d-%m-%Y")
            input_giorno.update()
        page.open(ft.DatePicker(on_change=on_change))

    def apri_time_picker(e):
        def on_change(e):
            input_ora.value = f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"
            input_ora.update()
        page.open(ft.TimePicker(on_change=on_change))

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
        s = segnalazioni_list[idx]
        try:
            dg = datetime.strptime(s['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dg = s['giorno']

        def elimina(e):
            page.close(dialog)
            try:
                paziente.eliminaSegnalazione(s['giorno'], s['ora'])
                popup_ok("Segnalazione eliminata con successo!")
            except Exception as ex:
                popup_err(str(ex))

        dialog = ft.AlertDialog(
            title=ft.Text("🗑️ Elimina Segnalazione", color="#ef4444"),
            content=ft.Text(
                f"Sei sicuro di voler eliminare la segnalazione del\n"
                f"{dg} alle {s['ora']}?\n"
                f"Sintomo: {s['sintomo']}\n\n"
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
            input_giorno.value = datetime.strptime(s['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            input_giorno.value = s['giorno']
        input_ora.value = s['ora']
        input_sintomo.value = s['sintomo']
        input_terapia.value = s['terapia'] if s['terapia'] else ""
        input_giorno.update(); input_ora.update(); input_sintomo.update(); input_terapia.update()

    def salva(e):
        nonlocal indice_modifica
        if not all([input_giorno.value, input_ora.value, input_sintomo.value]):
            popup_err("Data, ora e descrizione sono obbligatori.")
            return
        try:
            nd = datetime.strptime(input_giorno.value, "%d-%m-%Y").strftime("%Y-%m-%d")
            no = datetime.strptime(input_ora.value, "%H:%M").strftime("%H:%M")
        except:
            popup_err("Data o ora non validi. Usa dd-mm-yyyy e HH:MM.")
            return

        terapia_val = input_terapia.value if input_terapia.value else None

        if indice_modifica == -1:
            try:
                paziente.aggiungiSegnalazione(nd, no, input_sintomo.value, terapia_val)
                popup_ok("Segnalazione registrata!")
            except Exception as ex:
                popup_err(str(ex))
        else:
            v = segnalazioni_list[indice_modifica]
            try:
                paziente.aggiornaSegnalazione(v['giorno'], v['ora'], 
                                              nd, no, input_sintomo.value, terapia_val)
                popup_ok("Segnalazione aggiornata!")
            except Exception as ex:
                popup_err(str(ex))

    # Lista sinistra
    items = []
    for idx, s in enumerate(segnalazioni_list):
        try:
            dg = datetime.strptime(s['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dg = s['giorno']
        terapia_str = f" — Farmaco: {s['terapia']}" if s['terapia'] else ""
        
        items.append(
            ft.Container(
                padding=15, bgcolor="white", border_radius=12,
                margin=ft.margin.only(bottom=10),
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.05)"),
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{dg} - {s['ora']}", weight=ft.FontWeight.BOLD, size=15, color="#1e293b"),
                        ft.Text(f"{s['sintomo']}{terapia_str}", size=14, color="#475569")
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
                ft.Row([
                    ft.Text("Data:", size=15, weight=ft.FontWeight.BOLD), input_giorno,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker, icon_color="#f59e0b"),
                    ft.Text("Ora:", size=15, weight=ft.FontWeight.BOLD), input_ora,
                    ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=apri_time_picker, icon_color="#f59e0b"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Row([ft.Text("Farmaco associato:", size=15, weight=ft.FontWeight.BOLD), input_terapia], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Text("Descrizione sintomo:", size=15, weight=ft.FontWeight.BOLD),
                ft.Container(height=5), input_sintomo,
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