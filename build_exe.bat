@echo off
REM ======================================================================
REM  Build DocumentEditor.exe with PyInstaller
REM
REM    build_exe.bat            folder build (recommended, includes PaddleOCR)
REM    build_exe.bat onefile    single DocumentEditor.exe (Tesseract only)
REM
REM  Output:
REM    folder build : dist\DocumentEditor\DocumentEditor.exe
REM    onefile      : dist\DocumentEditor.exe  (+ dist\ocr\ next to it)
REM ======================================================================
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3.12) else (set PY=python)

if not exist .venv (
    echo Creating virtual environment...
    %PY% -m venv .venv || goto :error
)
call .venv\Scripts\activate.bat || goto :error

echo Installing dependencies...
python -m pip install --upgrade pip
if /I "%1"=="onefile" (
    pip install PySide6 PyMuPDF opencv-python-headless Pillow numpy pytesseract pyinstaller || goto :error
    set DEDIT_ONEFILE=1
    set DEDIT_NO_PADDLE=1
) else (
    pip install -r requirements.txt || goto :error
    set DEDIT_ONEFILE=
)

python tools\make_icon.py

echo Building...
pyinstaller --noconfirm --clean DocumentEditor.spec || goto :error

REM Copy the local OCR engines / models next to the executable
if /I "%1"=="onefile" (
    set TARGET=dist
) else (
    set TARGET=dist\DocumentEditor
)
if exist ocr (
    echo Copying OCR data...
    xcopy /E /I /Y ocr "%TARGET%\ocr" >nul
) else (
    echo WARNING: no "ocr" folder found. See README.md "OCR setup" - text detection
    echo          will only work if Tesseract is installed on the target PC.
)
copy /Y README.md "%TARGET%\README.md" >nul

echo.
if /I "%1"=="onefile" (
    echo Done: %CD%\dist\DocumentEditor.exe
) else (
    echo Done: %CD%\dist\DocumentEditor\DocumentEditor.exe
    echo Copy the whole dist\DocumentEditor folder to another PC to run it there.
)
exit /b 0

:error
echo.
echo BUILD FAILED. See the messages above.
exit /b 1
