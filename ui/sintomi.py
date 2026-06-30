import flet as ft
from datetime import datetime
from src.paziente import Paziente
from src.user import User


def show_sintomi_page(page: ft.Page, user):
    from ui.dashboard_paziente import show_patient_dashboard

    page.controls.clear()

    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Segnalazione Sintomi"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    sintomi_list = [{'giorno': g, 'ora': o, 'sintomo': s, 'terapia': t} 
                    for g, o, s, t in paziente.getSintomi()]
    terapie = paziente.getTerapie()
    indice_modifica = -1

    terapia_options = [ft.dropdown.Option("", "Nessuna")] + [ft.dropdown.Option(t[0], t[0]) for t in terapie]

    input_data = ft.TextField(label="Data", hint_text="dd-mm-yyyy", width=180, text_size=15)
    input_ora = ft.TextField(label="Ora", hint_text="HH:MM", width=180, text_size=15)
    input_sintomo = ft.TextField(hint_text="Descrivi il sintomo...", width=450, multiline=True, min_lines=4, max_lines=6, text_size=15)
    input_terapia = ft.Dropdown(options=terapia_options, width=300, label="Farmaco associato (opzionale)")

    def apri_date(e):
        page.open(ft.DatePicker(on_change=lambda e: (setattr(input_data, 'value', e.control.value.strftime("%d-%m-%Y")), input_data.update())))

    def apri_time(e):
        page.open(ft.TimePicker(on_change=lambda e: (setattr(input_ora, 'value', f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"), input_ora.update())))

    # === POPUP CON SINTASSI UNIFICATA ===
    def popup_ok(msg, ricarica=True):
        dialog = ft.AlertDialog(
            title=ft.Text("✅ Operazione completata", color="#10b981"),
            content=ft.Text(msg, size=15),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: page.close(dialog) or (show_sintomi_page(page, user) if ricarica else None))
            ]
        )
        page.open(dialog)

    def popup_err(msg):
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Errore", color="#ef4444"),
            content=ft.Text(msg, size=15),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: page.close(dialog))
            ]
        )
        page.open(dialog)

    def carica_modifica(idx):
        nonlocal indice_modifica
        indice_modifica = idx
        s = sintomi_list[idx]
        try:
            input_data.value = datetime.strptime(s['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            input_data.value = s['giorno']
        input_ora.value = s['ora']
        input_sintomo.value = s['sintomo']
        input_terapia.value = s['terapia'] or ""
        input_data.update(); input_ora.update(); input_sintomo.update(); input_terapia.update()

    def salva(e):
        nonlocal indice_modifica
        if not all([input_data.value, input_ora.value, input_sintomo.value]):
            popup_err("Data, ora e descrizione obbligatori.")
            return

        # --- VALIDAZIONE DATA (Incluso blocco date future) ---
        try:
            data_obj = datetime.strptime(input_data.value, "%d-%m-%Y")
            nuova_data = data_obj.strftime("%Y-%m-%d")
            
            # VINCOLO: Blocca le date future
            if data_obj.date() > datetime.now().date():
                popup_err("Non puoi inserire un sintomo per una data futura!")
                return
        except ValueError:
            popup_err("Data non valida. Usa il formato dd-mm-yyyy.")
            return

        # --- VALIDAZIONE ORA ---
        try:
            nuova_ora = datetime.strptime(input_ora.value, "%H:%M").strftime("%H:%M")
        except ValueError:
            popup_err("Ora non valida. Usa il formato HH:MM.")
            return

        terapia_val = input_terapia.value or None

        if indice_modifica == -1:
            paziente.aggiungiSintomo(nuova_data, nuova_ora, input_sintomo.value, terapia_val)
        else:
            v = sintomi_list[indice_modifica]
            paziente.aggiornaSintomo(v['giorno'], v['ora'], nuova_data, nuova_ora, input_sintomo.value, terapia_val)
        popup_ok("Sintomo salvato con successo!")

    items = []
    for idx, s in enumerate(sintomi_list):
        try:
            dv = datetime.strptime(s['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dv = s['giorno']
        t_str = f" — Farmaco: {s['terapia']}" if s['terapia'] else ""
        items.append(ft.Container(
            padding=15, bgcolor="white", border_radius=12, margin=ft.margin.only(bottom=10),
            content=ft.Row([
                ft.Column([ft.Text(f"{dv} - {s['ora']}", weight=ft.FontWeight.BOLD, size=15),
                          ft.Text(f"{s['sintomo']}{t_str}", size=14)], expand=True),
                ft.IconButton(icon=ft.Icons.EDIT, icon_color="#f59e0b", on_click=lambda e, i=idx: carica_modifica(i))
            ])
        ))

    page.add(ft.Row([
        ft.Container(expand=1, padding=20, bgcolor="white", border_radius=16,
            content=ft.Column([ft.Text("Sintomi registrati", size=22, weight=ft.FontWeight.BOLD),
                              ft.Divider(), ft.ListView(controls=items, expand=True)], expand=True)),
        ft.Container(expand=2, padding=40, bgcolor="white", border_radius=16,
            content=ft.Column([
                ft.Container(content=ft.Text("← Torna alla Dashboard", size=16, color="#2563eb", weight=ft.FontWeight.BOLD),
                            on_click=lambda e: show_patient_dashboard(page, user), padding=10),
                ft.Text("Segnala Sintomo", size=26, weight=ft.FontWeight.BOLD),
                ft.Divider(), ft.Container(height=20),
                ft.Row([
                    ft.Text("Data:", size=15, weight=ft.FontWeight.BOLD), input_data,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date, icon_color="#f59e0b"),
                    ft.Text("Ora:", size=15, weight=ft.FontWeight.BOLD), input_ora,
                    ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=apri_time, icon_color="#f59e0b"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Row([ft.Text("Farmaco associato:", size=15, weight=ft.FontWeight.BOLD), input_terapia], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Text("Descrizione sintomo:", size=15, weight=ft.FontWeight.BOLD),
                ft.Container(height=5), input_sintomo,
                ft.Container(height=25),
                ft.Container(width=300, height=55, bgcolor="#f59e0b", border_radius=12,
                            alignment=ft.alignment.center, on_click=salva,
                            content=ft.Text("Salva sintomo", size=16, color="white", weight=ft.FontWeight.BOLD))
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    ], expand=True, spacing=20))
    page.update()