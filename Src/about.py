from PyQt6.QtCore import QSize
from PyQt6.QtGui import QMovie, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QGroupBox,
    QDialog,
    QLabel,
)

from themes import dark_theme

class About(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle(f"About")

        layout = QVBoxLayout()

        top_left_layout = QHBoxLayout()

        icon_label = QLabel()
        movie = QMovie(f"Assets/Raubtier.gif")
        movie.setScaledSize(QSize(84, 108))
        icon_label.setMovie(movie)
        movie.start()
        top_left_layout.addWidget(icon_label)

        metadata_layout = QVBoxLayout()
        metadata_layout.addWidget(QLabel(f"SillyPasswords (64-bit)"))
        metadata_layout.addWidget(QLabel(f"GPL-3.0 License"))
        
        github_link_label = QLabel('<a href="https://github.com/VermeilChan/SillyPasswords">GitHub Repository</a>')
        github_link_label.setOpenExternalLinks(True)
        metadata_layout.addWidget(github_link_label)

        top_left_layout.addLayout(metadata_layout)
        layout.addLayout(top_left_layout)

        build_info_box = QGroupBox(f"Build Information")
        build_info_layout = QVBoxLayout()

        build_info_layout.addWidget(QLabel(f"Version: 1.0.6 (X)"))
        build_info_layout.addWidget(QLabel(f"Pyinstaller: 6.3.0"))
        build_info_layout.addWidget(QLabel(f"PyQt6: 6.6.1"))
        build_info_layout.addWidget(QLabel(f"Build date: Dec 24 2023"))

        self.setStyleSheet(dark_theme)
        icon_path = f'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))

        build_info_box.setLayout(build_info_layout)
        layout.addWidget(build_info_box)

        about_dialog.setLayout(layout)
        about_dialog.exec()
