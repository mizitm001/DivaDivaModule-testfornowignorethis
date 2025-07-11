# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['divadivamodule.py'],
    pathex=[],
    binaries=[],
    datas=[('modules_data.csv', '.'), ('images', 'images')],
    # --- IMPORTANT: ADD THIS LINE ---
    hiddenimports=['PIL._tkinter_finder'],
    # --------------------------------
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='divadivamodule',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='your_icon.ico', # Uncomment if you have an icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='divadivamodule',
)
