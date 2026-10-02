# -*- mode: python ; coding: utf-8 -*-
# PyInstaller configuration for Document Editor.
#
#   pyinstaller DocumentEditor.spec                -> dist\DocumentEditor\DocumentEditor.exe (folder build)
#   set DEDIT_ONEFILE=1 & pyinstaller DocumentEditor.spec  -> dist\DocumentEditor.exe (single file)
#
# OCR engines/models are NOT packed into the exe: build_exe.bat copies the
# "ocr" folder (Tesseract + language data + PaddleOCR models) next to the exe,
# where the application looks for them at run time.
import os
import importlib.util
from PyInstaller.utils.hooks import collect_all, collect_submodules

ONEFILE = os.environ.get("DEDIT_ONEFILE") == "1"
WITH_PADDLE = os.environ.get("DEDIT_NO_PADDLE") != "1" and importlib.util.find_spec("paddleocr") is not None

datas = [("resources", "resources")]
binaries = []
hiddenimports = ["pytesseract", "PySide6.QtPrintSupport"]
excludes = ["tkinter", "matplotlib", "PyQt5", "PyQt6", "IPython", "jupyter"]

for pkg in ("pymupdf", "cv2"):
    d, b, h = collect_all(pkg)
    datas += d; binaries += b; hiddenimports += h

if WITH_PADDLE:
    for pkg in ("paddleocr", "paddlex", "paddle", "pyclipper", "shapely", "skimage", "imgaug", "lmdb"):
        if importlib.util.find_spec(pkg) is None:
            continue
        d, b, h = collect_all(pkg)
        datas += d; binaries += b; hiddenimports += h
else:
    excludes += ["paddle", "paddleocr", "paddlex"]

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + collect_submodules("app") + collect_submodules("core") + collect_submodules("models"),
    excludes=excludes,
    noarchive=False,
)
pyz = PYZ(a.pure)
icon = "resources/app_icon.ico" if os.path.exists("resources/app_icon.ico") else None

if ONEFILE:
    exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name="DocumentEditor", console=False,
              icon=icon, upx=False, runtime_tmpdir=None)
else:
    exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="DocumentEditor", console=False,
              icon=icon, upx=False)
    coll = COLLECT(exe, a.binaries, a.datas, name="DocumentEditor", upx=False)
