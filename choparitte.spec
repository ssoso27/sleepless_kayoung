# -*- mode: python ; coding: utf-8 -*0

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
options = parser.parse_args()

_debug = options.debug

block_cipher = None

added_files = [ ('./hamham.ico', '.') ]
a = Analysis(['start.py'],
    pathex=['C:\\Users\\sohi8\\Documents\\workspace\\sleepless_kayoung'],
    binaries=[],
    datas=added_files,
    hiddenimports=[''],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Choparitte',
    debug=_debug,
    console=_debug,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    uac_admin=True,
    icon='./hamham.ico'
)
