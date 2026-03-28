# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_dynamic_libs, copy_metadata

project_root = Path.cwd()
tkinterdnd2_datas = collect_data_files('tkinterdnd2')
tkinterdnd2_binaries = collect_dynamic_libs('tkinterdnd2')
rembg_datas = collect_data_files('rembg')
onnxruntime_datas = collect_data_files('onnxruntime')
onnxruntime_binaries = collect_dynamic_libs('onnxruntime')

# copy_metadata bundles the dist-info directory so importlib.metadata.version()
# works at runtime for packages that call it (pymatting, rembg, onnxruntime).
metadata_datas = (
    copy_metadata('pymatting')
    + copy_metadata('rembg')
    + copy_metadata('onnxruntime')
    + copy_metadata('numpy')
    + copy_metadata('scipy')
    + copy_metadata('scikit-image')
    + copy_metadata('Pillow')
    + copy_metadata('pooch')
)

# collect_all captures binaries (.pyd/.dll), data files AND hidden imports —
# needed for scipy and skimage whose Cython extensions are missed by collect_data_files alone.
scipy_datas, scipy_binaries, scipy_hiddenimports  = collect_all('scipy')
skimage_datas, skimage_binaries, skimage_hiddenimports = collect_all('skimage')

a = Analysis(
    [str(project_root / 'main.py')],
    pathex=[str(project_root)],
    binaries=tkinterdnd2_binaries + onnxruntime_binaries + scipy_binaries + skimage_binaries,
    datas=(
        tkinterdnd2_datas
        + rembg_datas
        + onnxruntime_datas
        + scipy_datas
        + skimage_datas
        + metadata_datas
        + [(str(project_root / 'assets'), 'assets')]
    ),
    hiddenimports=[
        'customtkinter',
        'tkinterdnd2',
        'rembg',
        'rembg.sessions',
        'rembg.sessions.u2net',
        'rembg.sessions.u2netp',
        'rembg.sessions.u2net_human_seg',
        'rembg.sessions.silueta',
        'onnxruntime',
        'onnxruntime.capi',
        'onnxruntime.capi.onnxruntime_inference_collection',
        'onnxruntime.capi._pybind_state',
        'pooch',
    ] + scipy_hiddenimports + skimage_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

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