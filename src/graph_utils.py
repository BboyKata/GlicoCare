# src/graph_utils.py

import io
import base64
from datetime import datetime


def crea_grafico_glicemia_matplotlib(rilevazioni):
    """Vecchia funzione usata da dashboard_paziente.py"""
    oggi = datetime.now().date()
    
    dati = []
    for giorno_str, ora_str, glicemia, _ in rilevazioni:
        try:
            data_rilev = datetime.strptime(giorno_str, "%Y-%m-%d").date()
            if (oggi - data_rilev).days <= 30:
                dati.append((data_rilev, giorno_str[-5:], glicemia))
        except ValueError:
            continue
    
    if not dati:
        return None

    dati.sort(key=lambda x: x[0])
    
    giorni_x = [d[1] for d in dati]
    valori_y = [d[2] for d in dati]

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(9, 4.5), facecolor='#F8FAFC')
        ax = plt.axes()
        ax.set_facecolor('#FFFFFF')
        
        plt.plot(giorni_x, valori_y, marker='o', color='#2563eb', linestyle='-', linewidth=2, markersize=6, zorder=5)
        plt.title("Andamento Glicemia (Ultimi 30 giorni)", fontsize=14, fontweight='bold', color='#1e293b')
        plt.ylabel("mg/dL", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.5)
        
        plt.axhline(y=80, color='#10b981', linestyle='--', linewidth=1.5, alpha=0.8)
        plt.axhline(y=130, color='#10b981', linestyle='--', linewidth=1.5, alpha=0.8)
        plt.fill_between(range(len(giorni_x)), 80, 130, alpha=0.08, color='#10b981')
        plt.axhline(y=180, color='#f59e0b', linestyle='--', linewidth=1.5, alpha=0.8)
        
        x_pos = len(giorni_x) - 1
        plt.text(x_pos, 105, "Prima dei pasti\n(80-130)", color='#10b981', fontsize=9, 
                fontweight='bold', va='center', ha='right',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#10b981', alpha=0.9))
        plt.text(x_pos, 183, "Dopo i pasti\n(max 180)", color='#f59e0b', fontsize=9, 
                fontweight='bold', va='bottom', ha='right',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#f59e0b', alpha=0.9))
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_data
    except Exception as e:
        print(f"Errore grafico: {e}")
        return None


def crea_grafico_glicemia_periodo(rilevazioni, periodo_label="ultimi 30 giorni"):
    """Nuova funzione con titolo dinamico, usata da dettaglio_paziente.py"""
    oggi = datetime.now().date()
    
    dati = []
    for giorno_str, ora_str, glicemia, _ in rilevazioni:
        try:
            data_rilev = datetime.strptime(giorno_str, "%Y-%m-%d").date()
            dati.append((data_rilev, giorno_str[-5:], glicemia))
        except ValueError:
            continue
    
    if not dati:
        return None

    dati.sort(key=lambda x: x[0])
    
    giorni_x = [d[1] for d in dati]
    valori_y = [d[2] for d in dati]

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 5), facecolor='#F8FAFC')
        ax = plt.axes()
        ax.set_facecolor('#FFFFFF')
        
        plt.plot(giorni_x, valori_y, marker='o', color='#2563eb', linestyle='-', linewidth=2, markersize=6, zorder=5)
        plt.title(f"Andamento Glicemia ({periodo_label})", fontsize=16, fontweight='bold', color='#1e293b', pad=15)
        plt.ylabel("mg/dL", fontsize=13)
        plt.xlabel("Data", fontsize=13)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.4)
        
        plt.axhline(y=80, color='#10b981', linestyle='--', linewidth=1.5, alpha=0.8)
        plt.axhline(y=130, color='#10b981', linestyle='--', linewidth=1.5, alpha=0.8)
        plt.fill_between(range(len(giorni_x)), 80, 130, alpha=0.06, color='#10b981')
        plt.axhline(y=180, color='#f59e0b', linestyle='--', linewidth=1.5, alpha=0.8)
        
        x_pos = len(giorni_x) - 1
        if x_pos > 0:
            plt.text(x_pos, 105, "Prima pasti\n(80-130)", color='#10b981', fontsize=9, 
                    fontweight='bold', va='center', ha='right',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#10b981', alpha=0.9))
            plt.text(x_pos, 183, "Dopo pasti\n(max 180)", color='#f59e0b', fontsize=9, 
                    fontweight='bold', va='bottom', ha='right',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#f59e0b', alpha=0.9))
        
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_data
    except Exception as e:
        print(f"Errore grafico: {e}")
        return None