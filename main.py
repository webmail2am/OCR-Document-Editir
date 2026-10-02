"""Document Editor - edit text in PDFs and images while keeping their layout.

Run:  python main.py [file.pdf | image | project.dedit ...]
"""
from __future__ import annotations

import os
import sys
import traceback

# make "app", "core" and "models" importable when started from anywhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _excepthook(exc_type, exc, tb):
    """Show unexpected errors instead of closing the application."""
    details = "".join(traceback.format_exception(exc_type, exc, tb))
    sys.stderr.write(details)
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        if QApplication.instance() is not None:
            box = QMessageBox(QMessageBox.Critical, "Unexpected error",
                              f"An unexpected error occurred:\n\n{exc}\n\nYour document is still open; "
                              "save your work as a project if possible.")
            box.setDetailedText(details)
            box.exec()
    except Exception:
        pass


def main() -> int:
    # Windows: crisp rendering on high-DPI screens and a proper taskbar icon
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("DocumentEditor.App")
        except Exception:
            pass
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QGuiApplication, QIcon
    from PySide6.QtWidgets import QApplication

    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName("Document Editor")
    app.setOrganizationName("DocumentEditor")
    app.setStyle("Fusion")
    icon_path = os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))),
                             "resources", "app_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    sys.excepthook = _excepthook

    from app.main_window import MainWindow
    win = MainWindow()
    win.show()
    files = [a for a in sys.argv[1:] if os.path.isfile(a)]
    if files:
        win.open_files(files)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
