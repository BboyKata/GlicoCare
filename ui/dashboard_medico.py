import flet as ft
from src.user import User


def show_doctor_dashboard(page: ft.Page, user):
    from main import show_login_page
    
    page.controls.clear()
    page.title = "GlicoCare - Medico"
    page.bgcolor = "#F8FAFC"
    page.padding = 0
    
    page.add(ft.Column([
        ft.Text("Area Medico", size=40, weight=ft.FontWeight.BOLD, color="#1e293b"),
        ft.Text("Benvenuto Dottore! Gestisci i tuoi pazienti qui.", size=18, color="#64748b"),
        ft.Container(height=20),
        ft.Button(
            content=ft.Text("Logout", size=16, weight=ft.FontWeight.BOLD, color="white"),
            bgcolor="#ef4444", width=200, height=50,
            on_click=lambda e: show_login_page(e.page)
        )
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    page.update()