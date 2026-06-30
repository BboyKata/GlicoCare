#!/usr/bin/env python
import os
import sys
import inspect
import importlib.util
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

# --- CONFIGURAZIONE ---
EXCLUDE_DIRS = ['__pycache__', 'docs', '.git', 'venv', 'env', 'glicocare_env']
EXCLUDE_FILES = ['generate_pdf.py', 'generate_full_pdf.py', 'generate_uml_pdf.py']

def clean_docstring(docstring):
    """Pulisce i caratteri speciali per il PDF"""
    if not docstring:
        return "Nessuna descrizione disponibile. (Aggiungi una docstring!)"
    return docstring.replace('\n', ' ').replace('\r', '')

def parse_docstring(docstring):
    """Estrae Args, Returns e Raises da una docstring."""
    result = {'args': [], 'returns': '', 'raises': '', 'description': ''}
    if not docstring:
        return result
    lines = docstring.split('\n')
    current_section = None
    buffer = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Args:") or stripped.startswith("Args"):
            current_section = "args"
            continue
        elif stripped.startswith("Returns:") or stripped.startswith("Returns"):
            current_section = "returns"
            continue
        elif stripped.startswith("Raises:") or stripped.startswith("Raises"):
            current_section = "raises"
            continue
        if current_section is None:
            result['description'] += " " + stripped
            continue
        if stripped.startswith("Args:") or stripped.startswith("Returns:") or stripped.startswith("Raises:"):
            if current_section == "args":
                for arg_line in buffer:
                    import re
                    match = re.search(r'^([a-zA-Z_]\w*)\s*(?:\(([^)]+)\))?\s*:\s*(.*)$', arg_line)
                    if match:
                        result['args'].append({
                            'name': match.group(1),
                            'type': match.group(2) or 'Any',
                            'desc': match.group(3).strip()
                        })
                    else:
                        result['args'].append({'name': arg_line.strip(), 'type': 'Any', 'desc': ''})
            elif current_section == "returns":
                result['returns'] = " ".join(buffer).strip()
            elif current_section == "raises":
                result['raises'] = " ".join(buffer).strip()
            buffer = []
            continue
        buffer.append(stripped)
    if buffer:
        if current_section == "args":
            for arg_line in buffer:
                import re
                match = re.search(r'^([a-zA-Z_]\w*)\s*(?:\(([^)]+)\))?\s*:\s*(.*)$', arg_line)
                if match:
                    result['args'].append({
                        'name': match.group(1),
                        'type': match.group(2) or 'Any',
                        'desc': match.group(3).strip()
                    })
                else:
                    result['args'].append({'name': arg_line.strip(), 'type': 'Any', 'desc': ''})
        elif current_section == "returns":
            result['returns'] = " ".join(buffer).strip()
        elif current_section == "raises":
            result['raises'] = " ".join(buffer).strip()
    return result

def get_python_files(root_dir):
    """Trova tutti i file .py nel progetto, esclusi quelli da saltare."""
    py_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith('.py') and file not in EXCLUDE_FILES and not file.startswith('_'):
                py_files.append(os.path.join(root, file))
    return py_files

def import_module_from_file(file_path):
    """Importa un modulo Python da un percorso file."""
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"⚠️ Impossibile importare {file_path}: {e}")
        return None

def generate_uml_pdf(output_file="GlicoCare_UML_Specs.pdf"):
    # Trova tutti i file Python
    root_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = get_python_files(root_dir)
    print(f"📁 Trovati {len(py_files)} file Python da analizzare per il Class Diagram.")

    # Imposta il documento PDF
    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=28, spaceAfter=30, fontName='Helvetica-Bold')
    style_module = ParagraphStyle('ModuleTitle', parent=styles['Heading2'], fontSize=18, spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold', textColor='#003366')
    style_class = ParagraphStyle('ClassTitle', parent=styles['Heading3'], fontSize=16, spaceBefore=15, spaceAfter=8, fontName='Helvetica-Bold', textColor='#2563eb')
    style_method = ParagraphStyle('MethodTitle', parent=styles['Heading4'], fontSize=13, spaceBefore=8, spaceAfter=3, fontName='Helvetica-Bold', textColor='#1e293b')
    style_attr = ParagraphStyle('AttributeTitle', parent=styles['Heading5'], fontSize=11, spaceBefore=3, spaceAfter=2, fontName='Helvetica', textColor='#475569')
    style_normal = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=11, spaceAfter=4, fontName='Helvetica')
    style_code = ParagraphStyle('CustomCode', parent=styles['Normal'], fontSize=10, fontName='Courier', spaceAfter=3)

    story = []
    story.append(Paragraph("GlicoCare - Specifiche per Class Diagram UML", style_title))
    story.append(Paragraph(f"Generato il: {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_normal))
    story.append(Paragraph("Contiene la definizione completa di Classi, Attributi e Metodi per la progettazione del diagramma (inclusi costruttori e metodi privati).", style_normal))
    story.append(Spacer(1, 20))

    # Analizza ogni file
    for file_path in py_files:
        module = import_module_from_file(file_path)
        if not module:
            continue

        module_name = os.path.basename(file_path)
        story.append(Paragraph(f"📁 Modulo: {module_name}", style_module))
        story.append(Paragraph(f"Percorso: `{os.path.relpath(file_path, root_dir)}`", style_normal))
        story.append(Spacer(1, 5))

        # Trova le classi nel modulo
        classes = []
        for name in dir(module):
            obj = getattr(module, name)
            if name.startswith('_'):
                continue
            if inspect.isclass(obj):
                # Salta le eccezioni base o classi built-in
                if obj.__module__ != module.__name__:
                    continue
                classes.append((name, obj))

        if not classes:
            story.append(Paragraph("Nessuna classe pubblica definita in questo modulo.", style_normal))
            story.append(Spacer(1, 10))
            continue

        classes.sort(key=lambda x: x[0])

        # Analizza ogni classe
        for class_name, cls in classes:
            story.append(Paragraph(f"🏛️ Classe: {class_name}", style_class))
            
            # 1. Descrizione della classe (docstring)
            docstring = inspect.getdoc(cls)
            if docstring:
                story.append(Paragraph(f"<b>Descrizione:</b> {clean_docstring(docstring)}", style_normal))
            else:
                story.append(Paragraph("<b>Descrizione:</b> Nessuna descrizione disponibile.", style_normal))
            
            # 2. Classe base (ereditarietà)
            bases = inspect.getmro(cls)[1:]
            if bases and bases[0] != object:
                base_names = [b.__name__ for b in bases if b != object]
                story.append(Paragraph(f"<b>Estende:</b> {', '.join(base_names)}", style_normal))
            
            # 3. Attributi (cerca nei campi del costruttore e nelle variabili di istanza)
            story.append(Paragraph("🔹 Attributi (Variabili di istanza):", style_attr))
            
            # Analizza la firma del costruttore per trovare gli attributi
            try:
                sig = inspect.signature(cls.__init__)
                params = list(sig.parameters.values())
                # Salta 'self'
                if params and params[0].name == 'self':
                    params = params[1:]
                
                if params:
                    data = [['Nome', 'Tipo suggerito', 'Descrizione']]
                    for param in params:
                        # Cerca di trovare la descrizione nella docstring
                        desc = ""
                        if docstring:
                            import re
                            match = re.search(rf"{param.name}\s*\(([^)]+)\):\s*(.*)", docstring)
                            if match:
                                desc = match.group(2)
                        data.append([param.name, str(param.annotation) if param.annotation != inspect._empty else 'Any', desc])
                    
                    t = Table(data, colWidths=[100, 100, 280])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ]))
                    story.append(t)
                else:
                    story.append(Paragraph("Nessun attributo pubblico rilevato nel costruttore.", style_normal))
            except Exception:
                story.append(Paragraph("Impossibile analizzare gli attributi dal costruttore.", style_normal))
            
            story.append(Spacer(1, 5))

            # 4. Costruttore (__init__)
            story.append(Paragraph("🔸 Costruttore:", style_method))
            try:
                init_method = getattr(cls, '__init__')
                if init_method != object.__init__:
                    sig = inspect.signature(init_method)
                    # Il costruttore è sempre un metodo pubblico (anche se in UML è speciale)
                    story.append(Paragraph(f"<b>+ {class_name}{sig}</b>", style_code))
                    
                    # Docstring del costruttore
                    m_docstring = inspect.getdoc(init_method)
                    if m_docstring:
                        parsed = parse_docstring(m_docstring)
                        if parsed['description']:
                            story.append(Paragraph(f"<b>Descrizione:</b> {clean_docstring(parsed['description'])}", style_normal))
                        if parsed['args']:
                            data = [['Nome', 'Tipo', 'Descrizione']]
                            for arg in parsed['args']:
                                data.append([arg['name'], arg['type'], arg['desc']])
                            t = Table(data, colWidths=[80, 80, 300])
                            t.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, -1), 10),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                            ]))
                            story.append(t)
            except Exception:
                story.append(Paragraph("Impossibile analizzare il costruttore.", style_normal))
            
            story.append(Spacer(1, 5))

            # 5. Metodi (pubblici e privati)
            story.append(Paragraph("🔸 Metodi (UML: + pubblico, - privato):", style_method))
            
            # Raccogliamo TUTTI i metodi (non solo i pubblici)
            all_methods = []
            for name, method in inspect.getmembers(cls, inspect.isfunction):
                # Escludiamo il costruttore perché già trattato separatamente
                if name == '__init__':
                    continue
                all_methods.append((name, method))
            
            if all_methods:
                all_methods.sort(key=lambda x: x[0])
                for method_name, method in all_methods:
                    # Determina il simbolo UML: + per pubblico, - per privato
                    uml_symbol = "+" if not method_name.startswith('_') else "-"
                    story.append(Paragraph(f"📌 {uml_symbol} {method_name}", style_method))
                    
                    # Docstring del metodo
                    m_docstring = inspect.getdoc(method)
                    parsed = parse_docstring(m_docstring)
                    if parsed['description']:
                        story.append(Paragraph(f"<b>Descrizione:</b> {clean_docstring(parsed['description'])}", style_normal))
                    
                    # Firma (se è un metodo pubblico o privato, mostriamola)
                    try:
                        sig = inspect.signature(method)
                        story.append(Paragraph(f"<b>Firma:</b> {method_name}{sig}", style_code))
                    except:
                        pass
                    
                    # Parametri
                    if parsed['args']:
                        data = [['Nome', 'Tipo', 'Descrizione']]
                        for arg in parsed['args']:
                            data.append([arg['name'], arg['type'], arg['desc']])
                        t = Table(data, colWidths=[80, 80, 300])
                        t.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ]))
                        story.append(t)
                    
                    if parsed['returns']:
                        story.append(Paragraph(f"<b>Ritorna:</b> {parsed['returns']}", style_normal))
                    if parsed['raises']:
                        story.append(Paragraph(f"<b>Eccezioni sollevate:</b> {parsed['raises']}", style_normal))
                    
                    story.append(Spacer(1, 5))
            else:
                story.append(Paragraph("Nessun metodo (oltre al costruttore) definito.", style_normal))
            
            story.append(Spacer(1, 10))

    story.append(Spacer(1, 30))
    story.append(Paragraph("--- Fine Specifiche UML ---", style_normal))
    doc.build(story)
    print(f"✅ PDF con Specifiche UML (con costruttori e metodi privati) generato: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_uml_pdf()