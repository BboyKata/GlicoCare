#!/usr/bin/env python
import inspect
import importlib
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

# Importa il tuo modulo main
import main

def clean_docstring(docstring):
    """Pulisce i caratteri speciali per il PDF"""
    if not docstring:
        return "Nessuna descrizione disponibile."
    return docstring.replace('\n', ' ').replace('\r', '')

def generate_pdf(output_file="GlicoCare_Documentation_Finale.pdf"):
    # Crea il documento
    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    style_func = ParagraphStyle(
        'CustomFunction',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        textColor='#003366'
    )
    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        fontName='Helvetica'
    )
    
    story = []
    story.append(Paragraph("GlicoCare - Documentazione Tecnica", style_title))
    story.append(Paragraph("Generato il: " + str(__import__('datetime').datetime.now().strftime("%d/%m/%Y %H:%M")), style_normal))
    story.append(Spacer(1, 15))

    # Trova tutte le funzioni nel modulo main
    functions = [func for func in dir(main) if callable(getattr(main, func)) and not func.startswith("_")]
    
    for func_name in functions:
        func = getattr(main, func_name)
        try:
            # Intestazione funzione
            story.append(Paragraph(f"{func_name}", style_func))
            
            # Docstring
            docstring = inspect.getdoc(func)
            cleaned_doc = clean_docstring(docstring)
            story.append(Paragraph(cleaned_doc, style_normal))
            
            # Parametri (Args) e Return
            sig = inspect.signature(func)
            story.append(Paragraph(f"<b>Firma:</b> {func_name}{sig}", style_normal))
            
            # Cerca Args e Returns nella docstring
            if "Args:" in docstring or "Returns:" in docstring or "Raises:" in docstring:
                story.append(Paragraph("<b>Dettagli parametri:</b>", style_normal))
                lines = docstring.split('\n')
                for line in lines:
                    if "Args:" in line or "Returns:" in line or "Raises:" in line:
                        story.append(Paragraph(line, style_normal))
                    elif "    " in line and not line.strip().startswith(" "):
                        story.append(Paragraph(line, style_normal))
                        
        except Exception as e:
            story.append(Paragraph(f"Errore nel processare {func_name}: {str(e)}", style_normal))
        
        story.append(Spacer(1, 10))
    
    # Costruisci il PDF
    story.append(Paragraph("--- Fine Documentazione ---", style_normal))
    doc.build(story)
    print(f"PDF Generato con successo: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_pdf()