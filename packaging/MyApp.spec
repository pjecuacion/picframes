# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

project_root = Path.cwd()
tkinterdnd2_datas = collect_data_files('tkinterdnd2')
tkinterdnd2_binaries = collect_dynamic_libs('tkinterdnd2')

block_cipher = None

a = Analysis(
    [str(project_root / 'main.py')],
    pathex=[str(project_root)],
    binaries=tkinterdnd2_binaries,
    datas=tkinterdnd2_datas + [(str(project_root / 'assets'), 'assets')],
    hiddenimports=['customtkinter', 'tkinterdnd2'],
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
    a.datas,
    [],
    name='PicFrames',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    icon=str(project_root / 'assets' / 'app_icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PicFrames',
)