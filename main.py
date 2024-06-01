import sys
import os
import hashlib
from PyQt5 import QtWidgets, QtGui, uic, QtCore


def calculate_checksum(filename):
    """Calculates the SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


class LoadingWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Semi-transparent background

        # Dynamically load the loading icon
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "icon.png")
        self.movie = QtGui.QMovie(icon_path)
        self.movie.setScaledSize(QtCore.QSize(128, 128))

        self.label = QtWidgets.QLabel(self)
        self.label.setMovie(self.movie)
        self.movie.start()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, loading_window):
        super().__init__()
        self.loading_window = loading_window

        # Dynamically load the UI and icons
        if getattr(sys, "frozen", False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "assets", "main.ui")
        window_icon_path = os.path.join(base_dir, "assets", "medium.png")  # For window icon
        tray_icon_path = os.path.join(base_dir, "assets", "medium.png")  # For tray icon

        uic.loadUi(ui_path, self)
        self.setWindowTitle("RedstoneLauncher")
        self.setWindowIcon(QtGui.QIcon(window_icon_path))

        # System Tray Icon
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(tray_icon_path))
        self.tray_icon.setVisible(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Create the menu for the system tray icon
        self.tray_menu = QtWidgets.QMenu()
        self.show_action = self.tray_menu.addAction("Show")
        self.show_action.triggered.connect(self.show)
        self.quit_action = self.tray_menu.addAction("Quit")
        self.quit_action.triggered.connect(app.quit)
        self.tray_icon.setContextMenu(self.tray_menu)

        # Signal to close the loading window after the main window is shown
        self.loadFinished.connect(self.loading_window.close)

    def showEvent(self, event):
        """This is called when the main window is shown."""
        self.loadFinished.emit()  # Emit the signal immediately

    loadFinished = QtCore.pyqtSignal()


if __name__ == "__main__":
    # ... (checksum verification logic as before)

    app = QtWidgets.QApplication(sys.argv)
    loading_window = LoadingWindow()
    loading_window.show()

    window = MainWindow(loading_window)
    window.show()

    sys.exit(app.exec_())
