# GlicoCare - Sistema di Monitoraggio Glicemico

Applicazione desktop per la gestione del diabete che permette l'interazione
tra diabetologo e paziente. Il paziente registra glicemia, assunzioni di
farmaci e sintomi; il medico visualizza l'andamento, prescrive terapie e
inserisce annotazioni cliniche.


## Avvio rapido
```bash
pip install -r requirements.txt
python main.py
```


## Con Conda
```bash
conda create -n glicocare python=3.12 -y
conda activate glicocare
pip install -r requirements.txt
python main.py
```


## Dipendenze

- Python 3.12 o superiore
- flet==0.27.1
- Pillow>=10.0.0
- matplotlib>=3.7.0
- pytest>=8.0.0
- pytest-cov>=5.0.0


## Credenziali di test

| Ruolo | Username | Password |
|-------|----------|----------|
| Medico | `dott.ceccato` | `IngegneriaDelSoftware!` |
| Paziente grave | `matteo.balzerani` | `password` |
| Paziente medio | `jessica.devescovi` | `password` |
| Paziente sano | `mattia.mantovani` | `password` |

## Test

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


## Database

SQLite. Creato automaticamente al primo avvio nella cartella del progetto
oppure in `~/.glicocare/` se mancano i permessi di scrittura.
