import flet as ft
from datetime import datetime
from src.paziente import Paziente
from src.user import User


def show_registrazione_page(page: ft.Page, user):
    from ui.dashboard_paziente import show_patient_dashboard

    page.controls.clear()

    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Registrazione Giornaliera"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    rilevazioni_originali = paziente.getRilevazioni()
    rilevazioni_list = [{'giorno': g, 'ora': o, 'glicemia': gli, 'pasto': p} 
                        for g, o, gli, p in rilevazioni_originali]
    # Ordina dal più recente al meno recente
    rilevazioni_list.sort(key=lambda x: (x['giorno'], x['ora']), reverse=True)
    
    indice_modifica = -1
    
    input_data = ft.TextField(label="Data", hint_text="dd-mm-yyyy", width=180, text_size=15)
    input_ora = ft.TextField(label="Ora", hint_text="HH:MM", width=180, text_size=15)
    input_glicemia = ft.TextField(label="Glicemia (mg/dL)", width=220, text_size=15)
    input_pasto = ft.Dropdown(
        options=[ft.dropdown.Option("P", "Prima del pasto"), ft.dropdown.Option("D", "Dopo il pasto")],
        width=220, label="Rilevazione"
    )

    def apri_date_picker(e):
        def on_change(e):
            input_data.value = e.control.value.strftime("%d-%m-%Y")
            input_data.update()
        page.open(ft.DatePicker(on_change=on_change))

    def apri_time_picker(e):
        def on_change(e):
            input_ora.value = f"{e.control.value.hour:02d}:{e.control.value.minute:02d}"
            input_ora.update()
        page.open(ft.TimePicker(on_change=on_change))
        
    # === POPUP ===
    def popup_ok(msg, ricarica=True):
        def chiudi(e):
            page.close(dialog)
            if ricarica:
                show_registrazione_page(page, user)
        dialog = ft.AlertDialog(
            title=ft.Text("✅ Operazione completata", color="#10b981"),
            content=ft.Text(msg, size=15),
            actions=[ft.TextButton("Ok", on_click=chiudi)]
        )
        page.open(dialog)

    def popup_err(msg):
        def chiudi(e):
            page.close(dialog)
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Errore", color="#ef4444"),
            content=ft.Text(msg, size=15),
            actions=[ft.TextButton("Ok", on_click=chiudi)]
        )
        page.open(dialog)

    def popup_conferma_elimina(idx):
        r = rilevazioni_list[idx]
        try:
            dv = datetime.strptime(r['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dv = r['giorno']

        def elimina(e):
            page.close(dialog)
            try:
                paziente.eliminaRilevazioneGiornaliera(r['giorno'], r['ora'])
                popup_ok("Rilevazione eliminata con successo!")
            except Exception as ex:
                popup_err(str(ex))

        dialog = ft.AlertDialog(
            title=ft.Text("🗑️ Elimina Rilevazione", color="#ef4444"),
            content=ft.Text(
                f"Sei sicuro di voler eliminare la rilevazione del\n"
                f"{dv} alle {r['ora']}?\n"
                f"Glicemia: {r['glicemia']} mg/dL\n\n"
                f"Questa azione è irreversibile.",
                size=15
            ),
            actions=[
                ft.TextButton("Elimina", on_click=elimina, style=ft.ButtonStyle(color="#ef4444")),
                ft.TextButton("Annulla", on_click=lambda e: page.close(dialog))
            ]
        )
        page.open(dialog)

    def popup_conferma_modifica(index, nuova_data_ymd, nuova_ora):
        def aggiungi(e):
            page.close(dialog)
            try:
                paziente.aggiungiRilevazioneGiornaliera(nuova_data_ymd, nuova_ora, float(input_glicemia.value), input_pasto.value)
                popup_ok("Nuova registrazione aggiunta!")
            except Exception as ex:
                popup_err(str(ex))

        def sposta(e):
            page.close(dialog)
            try:
                paziente.aggiornaRilevazioneGiornaliera(
                    rilevazioni_list[index]['giorno'], rilevazioni_list[index]['ora'],
                    nuova_data_ymd, nuova_ora, float(input_glicemia.value), input_pasto.value
                )
                popup_ok("Registrazione aggiornata!")
            except Exception as ex:
                popup_err(str(ex))

        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Modifica Data/Ora", color="#f59e0b"),
            content=ft.Text(
                f"La rilevazione del {rilevazioni_list[index]['giorno']} alle {rilevazioni_list[index]['ora']} "
                "ha subito modifiche.\n\nVuoi AGGIUNGERE o SPOSTARE?",
                size=15
            ),
            actions=[
                ft.TextButton("Aggiungi Nuova", on_click=aggiungi),
                ft.TextButton("Sposta (Modifica)", on_click=sposta),
                ft.TextButton("Annulla", on_click=lambda e: page.close(dialog))
            ]
        )
        page.open(dialog)

    def carica_modifica(idx):
        nonlocal indice_modifica
        indice_modifica = idx
        r = rilevazioni_list[idx]
        try:
            input_data.value = datetime.strptime(r['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            input_data.value = r['giorno']
        input_ora.value = r['ora']
        input_glicemia.value = str(r['glicemia'])
        input_pasto.value = r['pasto']
        input_data.update(); input_ora.update(); input_glicemia.update(); input_pasto.update()

    def salva(e):
        nonlocal indice_modifica
        if not all([input_data.value, input_ora.value, input_glicemia.value, input_pasto.value]):
            popup_err("Tutti i campi devono essere compilati.")
            return

        try:
            data_obj = datetime.strptime(input_data.value, "%d-%m-%Y")
            nuova_data = data_obj.strftime("%Y-%m-%d")
            if data_obj.date() > datetime.now().date():
                popup_err("Non puoi inserire una rilevazione per una data futura!")
                return
        except ValueError:
            popup_err("Data non valida. Usa il formato dd-mm-yyyy.")
            return

        try:
            nuova_ora = datetime.strptime(input_ora.value, "%H:%M").strftime("%H:%M")
        except ValueError:
            popup_err("Ora non valida. Usa il formato HH:MM.")
            return

        try:
            glicemia_val = float(input_glicemia.value)
            if glicemia_val <= 0:
                popup_err("La glicemia deve essere positiva.")
                return
        except ValueError:
            popup_err("La glicemia deve essere un numero valido.")
            return

        if indice_modifica == -1:
            try:
                paziente.aggiungiRilevazioneGiornaliera(nuova_data, nuova_ora, glicemia_val, input_pasto.value)
                popup_ok("Nuova registrazione salvata!")
            except Exception as ex:
                popup_err(str(ex))
        else:
            v = rilevazioni_list[indice_modifica]
            if nuova_data != v['giorno'] or nuova_ora != v['ora']:
                popup_conferma_modifica(indice_modifica, nuova_data, nuova_ora)
            else:
                try:
                    paziente.aggiornaRilevazioneGiornaliera(v['giorno'], v['ora'], nuova_data, nuova_ora, glicemia_val, input_pasto.value)
                    popup_ok("Registrazione aggiornata!")
                except Exception as ex:
                    popup_err(str(ex))

    # Lista sinistra
    items = []
    for idx, r in enumerate(rilevazioni_list):
        try:
            dv = datetime.strptime(r['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            dv = r['giorno']
        items.append(
            ft.Container(
                padding=15, bgcolor="white", border_radius=12, margin=ft.margin.only(bottom=10),
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.05)"),
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{dv} - {r['ora']}", weight=ft.FontWeight.BOLD, size=15, color="#1e293b"),
                        ft.Text(f"Glicemia: {r['glicemia']} mg/dL ({'Prima' if r['pasto']=='P' else 'Dopo'} pasto)", 
                               size=14, color="#475569")
                    ], expand=True),
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color="#2563eb",
                                  tooltip="Modifica",
                                  on_click=lambda e, i=idx: carica_modifica(i)),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color="#ef4444",
                                  tooltip="Elimina",
                                  on_click=lambda e, i=idx: popup_conferma_elimina(i))
                ])
            )
        )

    page.add(ft.Row([
        ft.Container(expand=1, padding=20, bgcolor="white", border_radius=16,
            content=ft.Column([
                ft.Text("Le tue registrazioni", size=22, weight=ft.FontWeight.BOLD),
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
                ft.Text("Nuova Registrazione", size=26, weight=ft.FontWeight.BOLD),
                ft.Divider(), ft.Container(height=20),
                ft.Row([
                    ft.Text("Data (dd-mm-yyyy):", size=15, weight=ft.FontWeight.BOLD), input_data,
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker, icon_color="#2563eb")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row([
                    ft.Text("Ora (HH:MM):", size=15, weight=ft.FontWeight.BOLD), input_ora,
                    ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=apri_time_picker, icon_color="#2563eb")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row([ft.Text("Glicemia (mg/dL):", size=15, weight=ft.FontWeight.BOLD), input_glicemia], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row([ft.Text("Rilevazione:", size=15, weight=ft.FontWeight.BOLD), input_pasto], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.Container(
                    width=300, height=55, bgcolor="#2563eb", border_radius=12,
                    alignment=ft.alignment.center, on_click=salva,
                    content=ft.Text("Salva registrazione", size=16, color="white", weight=ft.FontWeight.BOLD)
                )
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    ], expand=True, spacing=20))
    page.update()