"""
GlicoCare - Applicazione Desktop per il Monitoraggio della Glicemia.
"""

import flet as ft
import os
import sqlite3
import io
import base64
from datetime import datetime

from src.user import User, CredenzialiNonValide
from src.paziente import Paziente

db = os.path.join("database", "glicocare.db")


def init_database():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()


def crea_grafico_glicemia_matplotlib(rilevazioni):
    oggi = datetime.now().date()
    giorni_x = []
    valori_y = []
    
    for giorno_str, ora_str, glicemia, _ in rilevazioni:
        try:
            data_rilev = datetime.strptime(giorno_str, "%Y-%m-%d").date()
            if (oggi - data_rilev).days <= 30:
                giorni_x.append(giorno_str[-5:])
                valori_y.append(glicemia)
        except ValueError:
            continue
    
    if not giorni_x:
        return None

    giorni_x.reverse()
    valori_y.reverse()

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(9, 4.5), facecolor='#F8FAFC')
        ax = plt.axes()
        ax.set_facecolor('#FFFFFF')
        
        plt.plot(giorni_x, valori_y, marker='o', color='#2563eb', linestyle='-', linewidth=2, markersize=6)
        plt.title("Andamento Glicemia (Ultimi 30 giorni)", fontsize=14, fontweight='bold', color='#1e293b')
        plt.ylabel("mg/dL", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.5)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_data
    except Exception as e:
        print(f"Errore grafico: {e}")
        return None

def show_registrazione_page(page: ft.Page, user: User):
    """
    Pagina per la gestione (visualizzazione, creazione, modifica) delle rilevazioni.
    """
    while len(page.controls) > 0:
        page.controls.pop()

    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Registrazione Giornaliera"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    # --- VARIABILI DI STATO ---
    rilevazioni_originali = paziente.getRilevazioni()
    rilevazioni_list = []
    for g, o, gli, p in rilevazioni_originali:
        rilevazioni_list.append({'giorno': g, 'ora': o, 'glicemia': gli, 'pasto': p})

    indice_modifica = -1
    
    # --- CAMPI INPUT ---
    input_data = ft.TextField(
        label="Data", 
        hint_text="dd-mm-yyyy",
        width=200,
        read_only=False
    )
    input_ora = ft.TextField(
        label="Ora", 
        hint_text="HH:MM",
        width=200,
        read_only=False
    )
    input_glicemia = ft.TextField(label="Glicemia (mg/dL)", width=200)
    input_pasto = ft.Dropdown(
        options=[
            ft.dropdown.Option("P", "Prima del pasto"),
            ft.dropdown.Option("D", "Dopo il pasto"),
        ],
        width=200,
        label="Rilevazione"
    )

    # --- FUNZIONI DI SUPPORTO ---
    def apri_date_picker(e):
        def on_date_change(e):
            input_data.value = date_picker.value.strftime("%d-%m-%Y")
            input_data.update()
        date_picker = ft.DatePicker(on_change=on_date_change)
        page.open(date_picker)

    def apri_time_picker(e):
        def on_time_change(e):
            input_ora.value = f"{time_picker.value.hour:02d}:{time_picker.value.minute:02d}"
            input_ora.update()
        time_picker = ft.TimePicker(on_change=on_time_change)
        page.open(time_picker)

    # ==========================================================
    # POPUP CON page.open() / page.close() PER FLET 0.27+
    # ==========================================================

    def mostra_popup_successo(messaggio):
        """Apre un popup di successo."""
        def chiudi_successo(e):
            page.close(dialog)
            show_registrazione_page(page, user)

        dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text("✅ Operazione completata", color="#10b981"),
            content=ft.Text(messaggio, size=15),
            actions=[
                ft.TextButton("Ok", on_click=chiudi_successo)
            ]
        )
        page.open(dialog)

    def mostra_popup_errore(messaggio):
        """Apre un popup di errore."""
        def chiudi_errore(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text("⚠️ Errore", color="#ef4444"),
            content=ft.Text(messaggio, size=15),
            actions=[
                ft.TextButton("Ok", on_click=chiudi_errore)
            ]
        )
        page.open(dialog)

    def mostra_popup_conferma(index, nuova_data_ymd, nuova_ora):
        """Apre un popup per la conferma di modifica."""
        def azione_aggiungi(e):
            page.close(dialog)
            try:
                paziente.aggiungiRilevazioneGiornaliera(
                    nuova_data_ymd, nuova_ora,
                    float(input_glicemia.value),
                    input_pasto.value
                )
                mostra_popup_successo("Nuova registrazione aggiunta con successo!")
            except Exception as ex:
                mostra_popup_errore(str(ex))

        def azione_sposta(e):
            page.close(dialog)
            try:
                paziente.aggiornaRilevazioneGiornaliera(
                    rilevazioni_list[index]['giorno'],
                    rilevazioni_list[index]['ora'],
                    nuova_data_ymd,
                    nuova_ora,
                    float(input_glicemia.value),
                    input_pasto.value
                )
                mostra_popup_successo("Registrazione spostata e aggiornata con successo!")
            except Exception as ex:
                mostra_popup_errore(str(ex))

        def azione_annulla(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text("⚠️ Modifica Data/Ora", color="#f59e0b"),
            content=ft.Text(
                f"La rilevazione del {rilevazioni_list[index]['giorno']} alle {rilevazioni_list[index]['ora']} ha subito modifiche.\n\n"
                "Vuoi AGGIUNGERE una nuova rilevazione o SPOSTARE quella esistente?",
                size=15
            ),
            actions=[
                ft.TextButton("Aggiungi Nuova", on_click=azione_aggiungi),
                ft.TextButton("Sposta (Modifica)", on_click=azione_sposta),
                ft.TextButton("Annulla", on_click=azione_annulla)
            ]
        )
        page.open(dialog)

    def carica_dati_per_modifica(index):
        nonlocal indice_modifica
        indice_modifica = index
        rilevazione = rilevazioni_list[index]
        try:
            data_obj = datetime.strptime(rilevazione['giorno'], "%Y-%m-%d")
            data_formattata = data_obj.strftime("%d-%m-%Y")
        except ValueError:
            data_formattata = rilevazione['giorno']
        input_data.value = data_formattata
        input_ora.value = rilevazione['ora']
        input_glicemia.value = str(rilevazione['glicemia'])
        input_pasto.value = rilevazione['pasto']
        input_data.update()
        input_ora.update()
        input_glicemia.update()
        input_pasto.update()

    def salva_registrazione(e):
        nonlocal indice_modifica
        
        # --- VALIDAZIONE ---
        if not input_data.value or not input_ora.value or not input_glicemia.value or not input_pasto.value:
            mostra_popup_errore("Tutti i campi devono essere compilati.")
            return

        try:
            data_obj = datetime.strptime(input_data.value, "%d-%m-%Y")
            nuova_data_ymd = data_obj.strftime("%Y-%m-%d")
        except ValueError:
            mostra_popup_errore("Data non valida. Usa il formato dd-mm-yyyy (es. 15-06-2026).")
            return

        try:
            ora_obj = datetime.strptime(input_ora.value, "%H:%M")
            nuova_ora = ora_obj.strftime("%H:%M")
        except ValueError:
            mostra_popup_errore("Ora non valida. Usa il formato HH:MM (es. 14:30).")
            return

        try:
            glicemia_val = float(input_glicemia.value)
            if glicemia_val <= 0:
                mostra_popup_errore("La glicemia deve essere un numero positivo.")
                return
        except ValueError:
            mostra_popup_errore("La glicemia deve essere un numero valido (es. 120.5).")
            return

        # --- SALVATAGGIO ---
        if indice_modifica == -1:
            try:
                paziente.aggiungiRilevazioneGiornaliera(
                    nuova_data_ymd, nuova_ora, glicemia_val, input_pasto.value
                )
                mostra_popup_successo("Nuova registrazione salvata con successo!")
            except Exception as ex:
                mostra_popup_errore(f"Errore: {str(ex)}")
        else:
            vecchia_data = rilevazioni_list[indice_modifica]['giorno']
            vecchia_ora = rilevazioni_list[indice_modifica]['ora']
            if nuova_data_ymd != vecchia_data or nuova_ora != vecchia_ora:
                mostra_popup_conferma(indice_modifica, nuova_data_ymd, nuova_ora)
            else:
                try:
                    paziente.aggiornaRilevazioneGiornaliera(
                        vecchia_data, vecchia_ora,
                        nuova_data_ymd, nuova_ora,
                        glicemia_val, input_pasto.value
                    )
                    mostra_popup_successo("Registrazione aggiornata con successo!")
                except Exception as ex:
                    mostra_popup_errore(f"Errore: {str(ex)}")

    # --- UI: COLONNA SINISTRA (Lista) ---
    lista_items = []
    for idx, r in enumerate(rilevazioni_list):
        try:
            data_vis = datetime.strptime(r['giorno'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            data_vis = r['giorno']
            
        casella = ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=12,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.05)"),
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(f"{data_vis} - {r['ora']}", weight=ft.FontWeight.BOLD, size=14, color="#1e293b"),
                            ft.Text(f"Glicemia: {r['glicemia']} mg/dL ({'Prima' if r['pasto'] == 'P' else 'Dopo'} pasto)", size=13, color="#475569")
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="#2563eb",
                        tooltip="Modifica registrazione",
                        on_click=lambda e, idx_c=idx: carica_dati_per_modifica(idx_c)
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        lista_items.append(casella)

    lista_scrollabile = ft.ListView(
        controls=lista_items,
        expand=True,
        spacing=0,
        padding=ft.padding.only(right=10)
    )

    left_col = ft.Container(
        expand=1,
        padding=20,
        bgcolor="#FFFFFF",
        border_radius=16,
        content=ft.Column(
            controls=[
                ft.Text("Le tue registrazioni", size=22, weight=ft.FontWeight.BOLD, color="#1e293b"),
                ft.Divider(color="#e2e8f0"),
                lista_scrollabile
            ],
            expand=True
        )
    )

    # --- UI: COLONNA DESTRA (Form) ---
    btn_data = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=apri_date_picker, icon_color="#2563eb")
    btn_ora = ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=apri_time_picker, icon_color="#2563eb")

    btn_salva = ft.Container(
        width=280, height=50, bgcolor="#2563eb", border_radius=12,
        alignment=ft.alignment.center,
        on_click=salva_registrazione,
        content=ft.Text("Salva registrazione", size=16, color="white", weight=ft.FontWeight.BOLD)
    )

    btn_indietro = ft.Container(
        content=ft.Text("← Torna alla Dashboard", size=16, color="#2563eb", weight=ft.FontWeight.BOLD),
        on_click=lambda e: show_patient_dashboard(page, user),
        padding=10
    )

    right_col = ft.Container(
        expand=2,
        padding=40,
        bgcolor="#FFFFFF",
        border_radius=16,
        content=ft.Column(
            controls=[
                btn_indietro,
                ft.Text("Nuova Registrazione", size=24, weight=ft.FontWeight.BOLD, color="#1e293b"),
                ft.Divider(color="#e2e8f0"),
                ft.Container(height=20),
                ft.Row(controls=[ft.Text("Data (dd-mm-yyyy):", size=14, weight=ft.FontWeight.BOLD), input_data, btn_data], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row(controls=[ft.Text("Ora (HH:MM):", size=14, weight=ft.FontWeight.BOLD), input_ora, btn_ora], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row(controls=[ft.Text("Glicemia (mg/dL):", size=14, weight=ft.FontWeight.BOLD), input_glicemia], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Row(controls=[ft.Text("Rilevazione:", size=14, weight=ft.FontWeight.BOLD), input_pasto], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=30),
                btn_salva
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(
        ft.Row(
            controls=[left_col, right_col],
            expand=True,
            spacing=20
        )
    )
    page.update()

def show_patient_dashboard(page: ft.Page, user: User):
    while len(page.controls) > 0:
        page.controls.pop()
    
    paziente = Paziente(user.id_ref)
    page.title = "GlicoCare - Paziente"
    page.bgcolor = "#F8FAFC"
    page.padding = 20

    img_data = crea_grafico_glicemia_matplotlib(paziente.getRilevazioni())
    
    if img_data:
        grafico_widget = ft.Image(
            src_base64=img_data,
            fit=ft.ImageFit.CONTAIN,
            width=700, 
            height=350
        )
    else:
        grafico_widget = ft.Container(
            content=ft.Text("Nessuna rilevazione disponibile.", size=16, color="#64748b"),
            bgcolor="white", padding=40, border_radius=16,
            alignment=ft.alignment.center
        )

    medico_info = paziente.getMedicoRiferimento()
    medico_nome = f"{medico_info[0]} {medico_info[1]}" if medico_info else "Medico non assegnato"
    medico_email = medico_info[2] if medico_info else "N/D"

    def btn_click(e, nome):
        print(f"Cliccato {nome}")

    # --- COLONNA SINISTRA ---
    left_col = ft.Container(
        expand=1, 
        padding=40, 
        bgcolor="#FFFFFF",
        content=ft.Column(
            controls=[
                ft.Text(
                    f"{'Benvenuta' if paziente.getSesso() == 'F' else 'Benvenuto'}, {paziente.getNome()}!", 
                    size=28, 
                    weight=ft.FontWeight.BOLD, 
                    color="#1e293b"
                ),                
                ft.Text("Cosa vuoi fare oggi?", size=16, color="#64748b"),
                ft.Container(height=20),
                
                # PULSANTE 1 (Blu) - Testo più lungo va a capo
                ft.Container(
                    width=280,
                    height=60,
                    bgcolor="#2563eb",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=10,
                    on_click=lambda e: show_registrazione_page(page, user),
                    content=ft.Text(
                        "Registrazione giornaliera", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    )
                ),
                ft.Container(height=10),
                
                # PULSANTE 2 (Arancione)
                ft.Container(
                    width=280,
                    height=60,
                    bgcolor="#f59e0b",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=10,
                    on_click=lambda e: btn_click(e, "Sintomi"),
                    content=ft.Text(
                        "Segnala sintomi", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    )
                ),
                ft.Container(height=10),
                
                # PULSANTE 3 (Verde)
                ft.Container(
                    width=280,
                    height=60,
                    bgcolor="#10b981",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    padding=10,
                    on_click=lambda e: btn_click(e, "Contatta"),
                    content=ft.Text(
                        "Contatta Medico", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    )
                ),
                
                ft.Container(expand=True),
                
                # LOGOUT (Rosso)
                ft.Container(
                    width=280,
                    height=50,
                    bgcolor="#ef4444",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    on_click=lambda e: show_login_page(e.page),
                    content=ft.Text(
                        "Logout", 
                        size=14, 
                        color="white", 
                        weight=ft.FontWeight.BOLD
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.START, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # --- COLONNA DESTRA ---
    # Percorso dell'immagine del medico
    current_dir = os.path.dirname(os.path.abspath(__file__))
    doc_img_path = os.path.join(current_dir, "img", "doc.png")
    
    right_col = ft.Container(
        expand=2, padding=40, bgcolor="#F8FAFC",
        content=ft.Column(
            controls=[
                ft.Container(
                    content=grafico_widget,
                    bgcolor="#FFFFFF", padding=20, border_radius=16,
                    shadow=ft.BoxShadow(blur_radius=20, color="rgba(0,0,0,0.1)"),
                    width=700
                ),
                ft.Container(height=20),
                
                # --- SCHEDA MEDICO CON IMMAGINE ---
                ft.Container(
                    width=700,
                    bgcolor="#FFFFFF", 
                    padding=20, 
                    border_radius=16,
                    shadow=ft.BoxShadow(blur_radius=15, color="rgba(0,0,0,0.05)"),
                    content=ft.Row(
                        controls=[
                            # Colonna Testi (occupa la maggior parte dello spazio)
                            ft.Column(
                                controls=[
                                    ft.Text("Il tuo Medico di Riferimento", size=18, weight=ft.FontWeight.BOLD, color="#1e293b"),
                                    ft.Divider(color="#e2e8f0"),
                                    ft.Row([
                                        ft.Text("Nome:", weight=ft.FontWeight.BOLD, size=14, color="#475569"),
                                        ft.Text(medico_nome, size=14, color="#1e293b", selectable=True)
                                    ]),
                                    ft.Row([
                                        ft.Text("Email:", weight=ft.FontWeight.BOLD, size=14, color="#475569"),
                                        ft.Text(medico_email, size=14, color="#2563eb", selectable=True)
                                    ]),
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.START
                            ),
                            
                            # Colonna Immagine (a destra)
                            ft.Container(
                                width=100,
                                height=100,
                                bgcolor="#f1f5f9",
                                border_radius=50,
                                alignment=ft.alignment.center,
                                content=ft.Image(
                                    src=doc_img_path,
                                    width=90,
                                    height=90,
                                    fit=ft.ImageFit.COVER,
                                    border_radius=50
                                ) if os.path.exists(doc_img_path) else ft.Text("👤", size=40)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=20
                    )
                )
                # --- FINE SCHEDA MEDICO ---
            ], 
            alignment=ft.MainAxisAlignment.START, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=0))
    page.update()


def show_doctor_dashboard(page: ft.Page, user: User):
    while len(page.controls) > 0:
        page.controls.pop()
        
    page.title = "GlicoCare - Medico"
    page.bgcolor = "#F8FAFC"
    page.padding = 0
    content = ft.Column(
        controls=[
            ft.Text("Area Medico", size=40, weight=ft.FontWeight.BOLD, color="#1e293b"),
            ft.Text("Benvenuto Dottore! Gestisci i tuoi pazienti qui.", size=18, color="#64748b"),
            ft.Container(height=20),
            ft.Button(
                content=ft.Text("Logout", size=16, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor="#ef4444", width=200, height=50,
                on_click=lambda e: show_login_page(e.page)
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.add(content)
    page.update()


def handle_login(e: ft.ControlEvent):
    global username_field, password_field, error_label

    username = username_field.value
    password = password_field.value
    
    try:
        error_label.value = ""
        error_label.update()
    except Exception:
        pass

    if not username or not password:
        try:
            error_label.value = "Inserisci username e password"
            error_label.color = "red"
            error_label.update()
        except Exception:
            pass
        return
    
    try:
        user = User(username, password, db)
        if user.is_paziente():
            show_patient_dashboard(e.page, user)
        elif user.is_medico():
            show_doctor_dashboard(e.page, user)
    except CredenzialiNonValide:
        try:
            error_label.value = "Username o password errati"
            error_label.color = "red"
            error_label.update()
        except Exception:
            pass
    except Exception as ex:
        try:
            error_label.value = f"Errore: {str(ex)}"
            error_label.color = "red"
            error_label.update()
        except Exception:
            pass


def show_login_page(page: ft.Page):
    global username_field, password_field, error_label

    while len(page.controls) > 0:
        page.controls.pop()

    page.title = "GlicoCare"
    page.bgcolor = "white"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.width = 1100
    page.window.height = 700
    page.window.resizable = True

    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "glicocare.png")
    left_col = ft.Container(
        content=ft.Column([
            ft.Image(src=logo_path, width=320, height=320),
            ft.Text("Il tuo compagno per il\ncontrollo della glicemia", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#1e293b"),
            ft.Text("Monitoraggio semplice e sicuro", size=14, color="#475569", text_align=ft.TextAlign.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
        bgcolor="#EEF2FF", expand=2, padding=40
    )

    username_field = ft.TextField(label="Username", width=400, text_size=16, border_color="#cbd5e1", on_submit=handle_login)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=400, text_size=16, border_color="#cbd5e1", on_submit=handle_login)
    error_label = ft.Text("", size=14)
    login_btn = ft.Button(content=ft.Text("Accedi", size=18, weight=ft.FontWeight.BOLD, color="white"), width=400, height=55, bgcolor="#2563eb", on_click=handle_login)

    right_col = ft.Container(
        content=ft.Column([
            ft.Text("Bentornato", size=36, weight=ft.FontWeight.BOLD, color="#0f172a"),
            ft.Text("Inserisci le tue credenziali per accedere", size=16, color="#475569"),
            ft.Container(height=30),
            username_field,
            password_field,
            error_label,
            login_btn,
            ft.Container(height=20),
            ft.Text("© 2024 GlicoCare - Tutti i diritti riservati", size=12, color="#94a3b8")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
        bgcolor="white", expand=3, padding=40
    )

    page.add(ft.Row(controls=[left_col, right_col], expand=True, spacing=0))
    page.update()


def main(page: ft.Page):
    show_login_page(page)


if __name__ == "__main__":
    init_database()
    print(f"Database init: {os.path.abspath(db)}")
    ft.app(target=main)