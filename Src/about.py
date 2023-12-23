from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtGui import QDesktopServices, QIcon, QMovie
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
)

from themes import dark_theme

class About(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Help')
        self.setGeometry(400, 200, 300, 200)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)

        layout = QVBoxLayout(central_widget)

        self.logo_label = QLabel(self)
        self.logo_movie = QMovie('Assets/Raubtier.gif')
        self.logo_movie.setScaledSize(QSize(126, 162))
        self.logo_label.setMovie(self.logo_movie)
        self.logo_movie.start()
        layout.addWidget(self.logo_label)

        self.name_version_label = QLabel('SillyPasswords v1.0.6 Stable (x64)', self)
        layout.addWidget(self.name_version_label)

        self.license_label = QLabel('GPL-3.0 License', self)
        layout.addWidget(self.license_label)

        self.description_label = QLabel('Free And Open Source', self)
        layout.addWidget(self.description_label)

        self.repo_button = QPushButton('GitHub Repository', self)
        self.repo_button.clicked.connect(self.open_repo)
        layout.addWidget(self.repo_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet(dark_theme)

        icon_path = 'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))

    def open_repo(self):
        QDesktopServices.openUrl(QUrl('https://github.com/VermeilChan/SillyPasswords'))
