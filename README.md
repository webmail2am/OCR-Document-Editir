# Document Editor

A Windows desktop application for editing the text inside PDFs and images
(JPG, JPEG, PNG, BMP, TIFF) while keeping the original layout.

It detects text with OCR (or reads the real text of digital PDFs) and turns
each line or field into an editable text box. When you change a box, the
original text is removed and the background is rebuilt underneath it. The new
text is then drawn in a matching font, size, colour and position.

**Everything runs on your computer.** No document, image, OCR text or other
data is ever uploaded, and no cloud service or account is needed. Internet
access is only needed once, during installation (Python packages, and
optionally the PaddleOCR model download).

---

## 1. Quick start (run from source)

1. Install **Python 3.12** (64-bit) from python.org. Tick "Add python.exe to
   PATH" in the installer.
2. Install **Tesseract OCR** (see section 2). This is required for Sinhala and
   Tamil, and is the fallback engine for English.
3. Open a Command Prompt in this folder and run:

   ```bat
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

   You can also pass files to open straight away:
   `python main.py invoice.pdf scan.jpg`.

If you only want Tesseract and not PaddleOCR (a much smaller install), install
just the core packages:

```bat
pip install PySide6 PyMuPDF opencv-python-headless Pillow numpy pytesseract
```

---

## 2. OCR setup (offline)

The editor looks for its OCR engines, in this order, in:

1. an `ocr\` folder next to `DocumentEditor.exe` (or next to `main.py` when
   running from source);
2. `%LOCALAPPDATA%\DocumentEditor\ocr\`;
3. a normal Tesseract installation (`C:\Program Files\Tesseract-OCR\`, or
   `tesseract` on the PATH).

To set the location yourself, open **OCR Settings** (toolbar button, or
**OCR → OCR settings**). Enter the Tesseract folder, for example
`C:\Program Files\Tesseract-OCR`. If your language files are somewhere else,
also enter the language-files folder. Press **Test these settings** to see
which program, language folder and languages will be used, then **Save**. The
setting is remembered.

### Tesseract (English, Sinhala, Tamil and combinations)

1. Download the Windows installer from the UB Mannheim build
   (https://github.com/UB-Mannheim/tesseract/wiki). During installation, under
   "Additional language data", tick **Sinhala** and **Tamil**.
2. To make the app portable, copy the installed folder into the project:

   ```
   ocr\
     tesseract\        <- the whole C:\Program Files\Tesseract-OCR folder
       tesseract.exe
       *.dll
     tessdata\         <- language files
       eng.traineddata
       sin.traineddata
       tam.traineddata
       osd.traineddata (used for automatic page orientation)
   ```

   `ocr\tessdata` takes priority over `ocr\tesseract\tessdata`, so you can add
   languages there. For better accuracy, use the `tessdata_best` files from
   https://github.com/tesseract-ocr/tessdata_best.

### PaddleOCR (more accurate English, optional)

PaddleOCR is installed by `requirements.txt`. It downloads its models the first
time it runs, so do that **once**, on a computer with internet access:

```bat
.venv\Scripts\activate
python tools\download_paddle_models.py
```

This copies the models into `ocr\paddle\`. From then on PaddleOCR runs fully
offline, and `build_exe.bat` ships the models next to the exe.

### Which engine is used

**OCR → OCR settings** has three choices:

- **Automatic** (the default): PaddleOCR for English when it is installed,
  otherwise Tesseract. Sinhala, Tamil and any combination always use
  Tesseract.
- **Tesseract** only.
- **PaddleOCR** only, for languages it supports.

### Adding more languages

Languages are listed in `LANGUAGE_OPTIONS` in `core/ocr_engine.py`. To add one,
drop its `xxx.traineddata` into `ocr\tessdata`. Every Tesseract language found
there also appears automatically in the OCR language list.

---

## 3. Building DocumentEditor.exe

On Windows, in this folder:

```bat
build_exe.bat
```

The script creates `.venv`, installs the requirements, runs PyInstaller with
`DocumentEditor.spec`, and copies the `ocr\` folder and this README next to the
program.

| Build | Command | Result |
|---|---|---|
| Folder (recommended) | `build_exe.bat` | `dist\DocumentEditor\DocumentEditor.exe` |
| Single file | `build_exe.bat onefile` | `dist\DocumentEditor.exe` (plus `dist\ocr\`) |

- The **folder build** is the recommended one. It starts faster and includes
  PaddleOCR. To install on another PC, copy the whole
  `dist\DocumentEditor` folder and run `DocumentEditor.exe`. Python is not
  needed there.
- The **single-file build** leaves out PaddleOCR, which is too large to unpack
  on every start, and uses Tesseract. Keep the `ocr` folder next to the exe.

If the build fails, the messages above `BUILD FAILED` name the package or step
that failed.

---

## 4. Using the editor

### Opening documents

- **File → Open** (Ctrl+O), drag files onto the window, or **Ctrl+V** to paste
  a screenshot or a copied file. When the document already has pages, a drop
  asks whether to add the files or open them as a new document.
- For images, the app asks for the page size: **Original**, **A4**, **A5**,
  **Letter**, or **Custom** (mm). The image is never stretched, only scaled to
  fit and centred.
- Text detection starts automatically in **Automatic** mode. The status bar
  shows the language and mode; change them in the toolbar or the **OCR** menu.

### Editing text

| Action | How |
|---|---|
| Edit | Double-click a box (or select it and press F2 / Enter). Type, then **Enter** to apply or **Esc** to cancel. Shift+Enter adds a new line. |
| Move | Drag the box, or use arrow keys (Shift = bigger steps). |
| Resize | Drag one of the 8 handles of a selected box. |
| Style | Properties panel on the right: font, size, bold, italic, underline, colour, alignment, letter spacing, rotation, wrap, exact X/Y/W/H in mm. |
| Delete | Delete key. The original text is removed and the background rebuilt. |
| Restore | Properties panel → **Restore original**. |
| Add text | **Add Text** tool (Ctrl+T), then click on the page. |
| Manual field | **Draw Field** tool (Ctrl+Shift+F): drag a rectangle around text that was missed. It is recognised and becomes a box. |
| Erase an area | **Erase Area** tool: drag a rectangle to remove anything, such as a stamp or a stray mark. |
| Find / replace | Ctrl+F, or Ctrl+H. Covers every page; **Replace all** can be undone in one step. |
| Undo / redo | Ctrl+Z / Ctrl+Y. Every change can be undone: text, style, moves, OCR, page operations. |

When new text is too long for its box, the editor asks what to do: **reduce the
font size**, **expand the box**, **wrap onto more lines**, or **keep it as is**.
You can make the choice permanent per box in the Properties panel ("Fit").

Toggle the outline of every detected box with **View → Show text boxes**
(Ctrl+B).

### Pages

The **Pages** panel on the left shows thumbnails:

- Drag a thumbnail to reorder.
- Right-click to duplicate, delete, rotate, export or print the selected pages.
- **Document** menu: add a blank page, page size (A4 / A5 / original / custom),
  rotate 0/90/180/270, straighten (deskew), and detect orientation.

### Saving, exporting and printing

- **Ctrl+S** saves a `.dedit` project. This is a single file containing the
  original files and every edit, and it can be reopened and edited later.
- **Ctrl+E** exports a PDF of all, the current, or the selected pages:
  - Digital PDF pages keep their vector content and real text.
  - Scanned pages keep the original image, with only the changed areas
    patched.
  - Edited text is real, selectable and searchable text.
- **Ctrl+P** opens the print dialog: printer, copies, page range, paper size,
  orientation, and scale (**Original size** by default, or fit to page). It
  prints at 300 dpi or more. "Save as PDF file" prints to a PDF instead.
- **Quality** (View menu): Draft, Normal, **High** (the default) or Very High.
  This sets the on-screen rendering and OCR resolution. Printing is always at
  least 300 dpi.

### Keyboard shortcuts

| Keys | Action | Keys | Action |
|---|---|---|---|
| Ctrl+O | Open | Ctrl+F / Ctrl+H | Find / Replace |
| Ctrl+V | Paste image | Ctrl+R / Ctrl+Shift+R | Detect text on page / all pages |
| Ctrl+S | Save project | Ctrl+T | Add text tool |
| Ctrl+E | Export PDF | Ctrl+Shift+F | Draw field tool |
| Ctrl+P | Print | Ctrl+B | Show text boxes |
| Ctrl+Z / Ctrl+Y | Undo / Redo | Ctrl+0 / 1 / 2 | Fit page / 100% / fit width |
| F2 | Edit selected | Ctrl+wheel | Zoom |
| Delete | Delete selected | Ctrl+[ / Ctrl+] | Rotate page |
| Space+drag, middle button | Pan | Ctrl+PgUp/PgDn | Previous / next page |

---

## 5. How it works

### Layers

Each page is held as layers:

1. the untouched original (the PDF page, or the image);
2. erased areas, where the background is rebuilt;
3. the text boxes.

Unchanged text is never redrawn, so it stays pixel-identical to the original.
Only boxes you change, move or delete get their old text removed and new text
drawn.

### Coordinates

All positions are stored in PDF points of the unrotated page, never in screen
pixels. Zoom, quality, page rotation and paper size therefore never move the
text.

### Digital PDFs

The existing text objects are used directly, with their real font, size and
colour. Edited text is removed with PyMuPDF redaction, which removes only the
text and keeps the lines, images and other vector content. Images inside a
digital PDF (for example a stamp) are OCR'd too.

### Scans and images

The OCR text is grouped into fields:

- A gap or a table ruling line splits a line into separate fields.
- Ruling lines are removed before OCR, so table cells are read cleanly.

Size, font family, boldness, italics, colour and alignment are measured from
the ink. The background under edited text is rebuilt from the surrounding
paper:

- Flat paper is filled with matching grain.
- Anything else is inpainted.
- Table lines that cross the area are kept.

Logos and other graphics are left alone unless you erase them.

### Rendering

The same drawing routine draws text on screen, on the printer, and into the
exported PDF, so all three match.

### Threads

OCR, loading, rendering, exporting and printing run in background threads
with a progress dialog. Errors show a message instead of closing the
application.

### Project layout

```
document_editor/
  main.py                    start-up, crash dialog
  app/                       user interface (PySide6)
    main_window.py           menus, toolbar, all user actions
    document_viewer.py       zoomable page view and tools
    text_editor.py           editable text boxes (inline editing, handles)
    properties_panel.py      right-hand properties panel
    thumbnails.py            page thumbnails
    dialogs.py               print, export, find/replace, page size, fit, OCR settings
    commands.py              undo/redo commands
    workers.py               background threads + progress
  core/                      document engine (no UI)
    pdf_engine.py            PDF reading, text extraction, redaction
    image_engine.py          image loading, page sizes, deskew, orientation
    ocr_engine.py            Tesseract and PaddleOCR back-ends
    text_detection.py        OCR lines -> editable fields, font estimation
    background_reconstruction.py
    text_render.py           shared text drawing and fitting
    export_manager.py        PDF export
    print_manager.py         printing
    project_manager.py       .dedit save/load
    document_model.py        document state, rendering, caches
  models/                    Page, TextObject, Document data classes
  tests/                     sample documents and automated tests
  tools/                     icon and PaddleOCR model helpers
  build_exe.bat, DocumentEditor.spec
```

---

## 6. Tests

```bat
.venv\Scripts\activate
python tests\generate_test_documents.py
python -m pytest -q tests
```

`generate_test_documents.py` creates 10 sample documents in
`tests\test_documents\`:

- scanned A4 and A5 invoices;
- a digital invoice PDF;
- a 3-page PDF (digital, scanned, and mixed);
- a JPG photo;
- Sinhala, Tamil, and mixed English/Sinhala pages;
- a table;
- a rotated, skewed scan.

The tests check:

- OCR positions on each sample;
- the invoice edit from the specification (ABC → XYZ COMPANY,
  INV-12345 → INV-99999, 25,000.00 → 30,000.00) with the layout unchanged;
- page sizes, export, rotation, and the print size and position at 300 dpi;
- project save and load;
- damaged files;
- a GUI run-through: open, double-click edit, Esc, drag, undo/redo,
  properties, add text, find/replace across pages, page operations, project,
  print-to-PDF, clipboard paste, and error messages.

The tests need Tesseract with `eng`, `sin` and `tam`.

---

## 7. Known limitations

- **What was tested and where.** The application was developed and tested on
  Linux with the same Python 3.12 / PySide6 / PyMuPDF / Tesseract 5 stack,
  using the automated tests above. The following were **not** run there:
  - building and running the Windows `.exe`;
  - a real Windows printer (printing was verified through Qt's PDF printer);
  - PaddleOCR (the test machine could not download its models).

  Tesseract was used for all OCR tests. Please run `build_exe.bat` and a test
  print on your PC.
- **Font matching is approximate.** The font family is chosen from the fonts
  installed on the PC by measuring letter shapes. Size, bold and italic are
  usually right; an unusual or decorative typeface is replaced with the
  closest common font. You can always pick another in the Properties panel.
- **Background rebuild.** This is very good on plain paper, coloured fills
  and table cells. On photos, gradients or heavy patterns behind text, the
  rebuilt area can look slightly smoothed. Use "Erase method" in the
  Properties panel to try *inpaint* or *fill*.
- **OCR accuracy depends on the scan.** Low resolution, blur or handwriting
  reduce accuracy. For Sinhala and Tamil, Tesseract sometimes misreads
  conjuncts (for example ශ්‍රී read as ශී). Check the text and correct it in
  the box. `tessdata_best` models are more accurate.
- **Digital PDFs.**
  - Rotated or curved text objects are edited as straight boxes.
  - Form fields are not edited as form fields.
  - Exporting rewrites the page content, so links, comments and other
    annotations on the original page are not carried into the exported PDF.
  - Fonts embedded as subsets cannot be reused for new letters, so edited
    text uses the closest installed font.
- **Very large documents** (hundreds of pages) work, but OCR of every page
  takes a while. Use "Detect text (page)" when you only need one page.
- The sample PNG test images are large (about 14 MB each) because they
  simulate scanner noise.
