"""
Utility per la generazione di grafici con Matplotlib.

Questo modulo fornisce funzioni per creare grafici dell'andamento della glicemia
a partire dai dati di rilevazione del paziente.
"""

import io
import base64
from datetime import datetime


def crea_grafico_glicemia_matplotlib(rilevazioni):
    """
    Genera un grafico a linee dell'andamento della glicemia degli ultimi 30 giorni.

    La funzione filtra le rilevazioni per includere solo gli ultimi 30 giorni
    e le date non future. Il grafico include linee di riferimento per i range
    di normalità (80-130 mg/dL prima dei pasti, max 180 mg/dL dopo i pasti).

    Args:
        rilevazioni (list): Lista di tuple provenienti da `paziente.getRilevazioni()`.
            Ogni tupla deve essere nel formato:
            (giorno (str), ora (str), glicemia (float), primaDopoPasto (str)).

    Returns:
        str | None: Immagine del grafico codificata in base64, pronta per essere
            visualizzata con `ft.Image(src_base64=...)`. Restituisce `None`
            se non ci sono dati validi.

    Raises:
        Exception: Se si verifica un errore durante la creazione del grafico
            (es. matplotlib non installato, dati non validi).
    """
    oggi = datetime.now().date()
    
    dati = []
    for giorno_str, ora_str, glicemia, _ in rilevazioni:
        try:
            data_rilev = datetime.strptime(giorno_str, "%Y-%m-%d").date()
            # VINCOLO: Solo gli ultimi 30 giorni E solo date NON future
            if (oggi - data_rilev).days <= 30 and data_rilev <= oggi:
                dati.append((data_rilev, giorno_str[-5:], glicemia))
        except ValueError:
            continue
    
    if not dati:
        return None

    # Ordina cronologicamente
    dati.sort(key=lambda x: x[0])
    
    indici = list(range(len(dati)))
    valori_y = [d[2] for d in dati]

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(9, 4.5), facecolor='#F8FAFC')
        ax = plt.axes()
        ax.set_facecolor('#FFFFFF')
        
        plt.plot(indici, valori_y, marker='o', color='#2563eb', linestyle='-', 
                 linewidth=2, markersize=6, zorder=5)
        
        plt.title("Andamento Glicemia (Ultimi 30 giorni)", fontsize=14, fontweight='bold', color='#1e293b', y=1.02)
        plt.ylabel("mg/dL", fontsize=12)
        plt.xticks([]) 
        plt.grid(True, linestyle='--', alpha=0.5)
        
        # Aggiunge le linee di riferimento
        plt.axhline(y=80, color='#10b981', linestyle='--', linewidth=1.5, alpha=0.8)
        plt.axhline(y=130, color='#10b981', linestyle='--', linewidth=1.5, alpha=0.8)
        plt.fill_between(indici, 80, 130, alpha=0.08, color='#10b981')
        plt.axhline(y=180, color='#f59e0b', linestyle='--', linewidth=1.5, alpha=0.8)
        
        x_pos = max(indici) if indici else 0
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