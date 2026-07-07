![Logo GlicoCare](img/glicocare.png)

# LEGGERE QUESTO FILE PRIMA DI ESEGUIRE IL CODICE

Applicazione desktop per la gestione del diabete che permette l'interazione tra diabetologo e paziente. Il paziente registra glicemia, assunzioni di farmaci e sintomi; il medico visualizza l'andamento, prescrive terapie e inserisce annotazioni cliniche.


> **Autori:** Il progetto è stato realizzato da Matteo Balzerani, Jessica Devescovi e Mattia Mantovani per il progetto di Ingegneria del Software, CdL Bioinformatica L-31.

## Codice sorgente
Il progetto è stato sviluppato attraverso la tecnologia di versioning di Github. Qui allegata nel file `.zip` è fornita una versione stabile e testata, presente nella directory `CodiceSorgente` di questo archivio.

## Esecuzione
Per poter eseguire e testare *Glicocare*, vi sono i seguenti modi elencati:

1. **Esecuzione del codice compilato in eseguibile:** attraverso le *Github Actions* abbiamo creato la build automatica delle versioni pubblicate per i sistemi operativi `Windows` e `Linux`. Sono allegati i due eseguibili nella directory `FileEseguibili` di questo archivio. 
> Eventualmente per eseguirlo è necessario estrarre il file .zip del sistema operativo corrispondente ed unicamente cliccare sul file eseguibile contenuto all'interno.

2. **Compilazione ed esecuzione del codice sorgente:** è possibile accedere alla cartella allegata del codice sorgente `~/Glicocare/` e compilare ed eseguire `~/Glicocare/main.py`. Per poter compilare ed eseguire è necessario rispettare le seguenti istruzioni e requirements. È necessario svolgere queste operazioni da `terminale (bash/cmd)`.

### Dipendenze
- Python 3.12 o superiore (include *sqlite*)
- flet==0.27.1
- Pillow>=10.0.0
- matplotlib>=3.7.0
- pytest>=8.0.0
- pytest-cov>=5.0.0

<sup style="display: inline-block;">**ATTENZIONE:** Non è possibile seguire i passaggi successivi se non si ha prima installato Python 3.12 (*e pip installer incluso in Python*)</sup>

### Avvio rapido
**Attenzione:** per poter eseguire il codice e' necessario entrare nella cartella corretta dove e' presente `main.py`, quindi eventualmente eseguendo il comando `cd Glicocare`.

```bash
pip install -r requirements.txt
python main.py
```

### Con Conda
```bash
conda create -n glicocare python=3.12 -y
conda activate glicocare
pip install -r requirements.txt
python main.py
```

### Credenziali di test
Per poter testare le funzionalità del software abbiamo creato delle utenze *ad hoc*, come segue:

| Ruolo | Username | Password |
|-------|----------|----------|
| Medico | `dott.ceccato` | `IngegneriaDelSoftware!` |
| Paziente grave | `matteo.balzerani` | `password` |
| Paziente medio | `jessica.devescovi` | `password` |
| Paziente sano | `mattia.mantovani` | `password` |

## Database

Progettato in SQLite. Creato automaticamente e popolato al primo avvio nella cartella del progetto oppure in `~/.glicocare/` se mancano i permessi di scrittura. Ogni possibilità di conflitto nella creazione e nell'esecuzione del DB dovrebbe essere stata risolta, ma eventualmente contattare gli studenti in caso di problemi.

## Testing
Per i test sulle varie classi è necessario eseguire il seguente comando da terminale
```bash
python -m pytest tests/ --cov=src -v
```

91 test, copertura del 76%.

| Modulo | Istruzioni | Copertura | Test |
|--------|------------|-----------|------|
| `src/user.py` | 48 | 100% | 14 |
| `src/medico.py` | 171 | 90% | 23 |
| `src/paziente.py` | 358 | 85% | 33 |
| `src/graph_utils.py` | 92 | 0% | 0 (solo UI) |
| **Totale** | **669** | **76%** | **91** |


## Struttura del progetto

```
GlicoCare/
├── main.py                   Entry point
├── requirements.txt           Dipendenze
├── src/
│   ├── user.py                Autenticazione
│   ├── medico.py              Gestione medico
│   ├── paziente.py            Gestione paziente
│   └── graph_utils.py         Grafici glicemici
├── ui/
│   ├── dashboard_medico.py    Dashboard medico
│   ├── dashboard_paziente.py  Dashboard paziente
│   ├── dettaglio_paziente.py  Scheda paziente
│   ├── registrazione.py       Rilevazioni glicemiche
│   ├── assunzioni.py          Assunzioni farmaci
│   ├── sintomi.py             Segnalazioni
│   └── log_page.py            Log operazioni
├── database/
│   ├── schema.sql             Schema database
│   └── popola_test.sql        Dati di test
├── img/
│   └── glicocare.png          Logo
└── tests/
    ├── conftest.py            Fixture condivise
    ├── test_user.py           14 test
    ├── test_medico.py         23 test
    ├── test_paziente.py       33 test
    └── test_gravita.py        18 test
```


