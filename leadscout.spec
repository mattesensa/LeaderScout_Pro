# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

datas = [
    ('templates', 'templates'),
    ('static', 'static')
]

hiddenimports = [
    'jinja2',
    'bs4',
    'requests',
    'urllib3',
    'flask',
    'werkzeug',
    'json',
    'concurrent.futures'
]

a = Analysis(
    ['desktop_launcher.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LeadScoutPRO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# For macOS App Bundle (if built on macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='LeadScoutPRO.app',
        icon=None,
        bundle_identifier='com.leadscout.pro'
    )
