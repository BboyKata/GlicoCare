# GlicoCare.spec
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database/schema.sql', 'database'),
        ('database/popola_test.sql', 'database'),
        ('img/*', 'img'),
    ],
    hiddenimports=['matplotlib', 'flet', 'PIL'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='GlicoCare',
    debug=False,
    strip=False,
    upx=True,
    console=False,        # Nessuna finestra terminale
    icon='img/glicocare.png'  # Icona dell'app (opzionale)
)