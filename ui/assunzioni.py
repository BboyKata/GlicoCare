import flet as ft
from datetime import datetime
from src.paziente import Paziente
from src.user import User


def show_assunzioni_page(page: ft.Page, user):
    from ui.dashboard_paziente import show_patient_dashboard

    page.controls.clear()

    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Assunzione Farmaci"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    assunzioni_list = [{'giorno': g, 'ora': o, 'farmaco': f, 'quantita': q} 
                       for g, o, f, q in paziente.getAssunzioni()]
    terapie = paziente.getTerapie()
    indice_modifica = -1

    farmaci_options = [ft.dropdown.Option(t[0], f"{t[0]} ({t[2]})") for t in terapie]
    if not farmaci_options:
        farmaci_options = [ft.dropdown.Option("", "Nessun farmaco prescritto")]

    input_data = ft.TextField(label="Data", hint_text="dd-mm-yyyy", width=180, text_size=15)
    input_ora = ft.TextField(label="Ora", hint_text="HH:MM", width=180, text_size=15)
    input_farmaco = ft.Dropdown(options=farmaci_options, width=200, label="Farmaco")
    input_quantita = ft.TextField(label="Quantità (es. 1 compressa)", width=200, text_size=15)

    def apri_date(e):
        page.open(ft.DatePicker(on_change=lambda e: (setattr(input_data, 'value', e.control.value.strftime("%d-%m-%Y")), input_data.update())))

    def apri_time(e):
        page.open(ft.TimePicker(on_change=lambda e: (setattr(input_ora, 'value', f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"), input_ora.update())))

    def popup_ok(msg):
        def chiudi(e):
            page.close(page.dialog)
            show_assunzioni_page(page, user)
        page.open(ft.AlertDialog(title=ft.Text("✅ Ok", color="#10b981"), content=ft.Text(msg), actions=[ft.TextButton("Ok", on_click=chiudi)]))

    def popup_err(msg):
        page.open(ft.AlertDialog(title=ft.Text("⚠️ Errore", color="#ef4444"), content=ft.Text(msg), actions=[ft.TextButton("Ok", on_click=lambda e: page.close(page.dialog))]))

    def carica_modifica(idx):
        nonlocal indice_modifica
        indice_modifica = idx
        a = assunzioni_list[idx]
        try:
            input_data.value = datetime.strptime(a['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            input_data.value = a['giorno']
        input_ora.value = a['ora']
        input_farmaco.value = a['farmaco']
        input_quantita.value = a['quantita']
        input_data.update(); input_ora.update(); input_farmaco.update(); input_quantita.update()

    def salva(e):
        nonlocal indice_modifica
        if not all([input_data.value, input_ora.value, input_farmaco.value, input_quantita.value]):
            popup_err("Tutti i campi obbligatori.")
            return
        try:
            nd = datetime.strptime(input_data.value, "%d-%m-%Y").strftime("%Y-%m-%d")
            no = datetime.strptime(input_ora.value, "%H:%M").strftime("%H:%M")
        except:
            popup_err("Data/ora non validi.")
            return

        if indice_modifica == -1:
            paziente.aggiungiAssunzione(nd, no, input_farmaco.value, input_quantita.value)
        else:
            v = assunzioni_list[indice_modifica]
            paziente.aggiornaAssunzione(v['giorno'], v['ora'], v['farmaco'], nd, no, input_farmaco.value, input_quantita.value)
        popup_ok("Assunzione salvata!")

    items = []
    for idx, a in enumerate(assunzioni_list):
        try:
            dv = datetime.strptime(a['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dv = a['giorno']
        items.append(ft.Container(
            padding=15, bgcolor="white", border_radius=12, margin=ft.margin.only(bottom=10),
            content=ft.Row([
                ft.Column([ft.Text(f"{dv} - {a['ora']}", weight=ft.FontWeight.BOLD, size=15),
                          ft.Text(f"{a['farmaco']} — {a['quantita']}", size=14)], expand=True),
                ft.IconButton(icon=ft.Icons.EDIT, icon_color="#10b981", on_click=lambda e, i=idx: carica_modifica(i))
            ])
        ))

    page.add(ft.Row([
        ft.Container(expand=1, padding=20, bgcolor="white", border_radius=16,
            content=ft.Column([ft.Text("Assunzioni registrate", size=22, weight=ft.FontWeight.BOLD),
                              ft.Divider(), ft.ListView(controls=items, expand=True)], expand=True)),
        ft.Container(expand=2, padding=40, bgcolor="white", border_radius=16,
            content=ft.Column([
                ft.Container(content=ft.Text("← Torna alla Dashboard", size=16, color="#2563eb", weight=ft.FontWeight.BOLD),
                            on_click=lambda e: show_patient_dashboard(page, user), padding=10),
                ft.Text("Registra Assunzione", size=26, weight=ft.FontWeight.BOLD),
                ft.Divider(), ft.Container(height=20),
                ft.Row([
                    ft.Text("Data:", size=15, weight=ft.FontWeight.BOLD), input_data,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date, icon_color="#10b981"),
                    ft.Text("Ora:", size=15, weight=ft.FontWeight.BOLD), input_ora,
                    ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=apri_time, icon_color="#10b981"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Row([
                    ft.Text("Farmaco:", size=15, weight=ft.FontWeight.BOLD), input_farmaco,
                    ft.Text("Quantità:", size=15, weight=ft.FontWeight.BOLD), input_quantita,
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.Container(width=300, height=55, bgcolor="#10b981", border_radius=12,
                            alignment=ft.alignment.center, on_click=salva,
                            content=ft.Text("Salva assunzione", size=16, color="white", weight=ft.FontWeight.BOLD))
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    ], expand=True, spacing=20))
    page.update()