from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

from themes import dark_theme

class AboutSillyPasswords(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Help')
        self.setGeometry(400, 200, 300, 200)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)

        layout = QVBoxLayout(central_widget)

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('Assets/Raubtier.png')
        self.logo_label.setPixmap(self.logo_pixmap)
        layout.addWidget(self.logo_label)

        self.name_version_label = QLabel('SillyPasswords v1.0.4 (x64)', self)
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
        self.logo_label.setStyleSheet(dark_theme)
        self.name_version_label.setStyleSheet(dark_theme)
        self.license_label.setStyleSheet(dark_theme)
        self.description_label.setStyleSheet(dark_theme)
        self.repo_button.setStyleSheet(dark_theme)

        icon_path = 'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))

    def open_repo(self):
        QDesktopServices.openUrl(QUrl('https://github.com/VermeilChan/SillyPasswords'))
