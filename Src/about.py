from platform import system, version, release, architecture

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QDialog,
    QLabel,
)

class About(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("About")

        layout = QVBoxLayout()

        top_left_layout = QHBoxLayout()

        icon_label = QLabel()
        pixmap = QPixmap("Assets/Raubtier.png")
        icon_label.setPixmap(pixmap)
        top_left_layout.addWidget(icon_label)

        metadata_layout = QVBoxLayout()
        metadata_layout.addWidget(QLabel("SillyPasswords (64-bit)"))
        metadata_layout.addWidget(QLabel("GPL-3.0 License"))

        github_link_label = QLabel('<a href="https://github.com/VermeilChan/SillyPasswords">GitHub Repository</a>')
        github_link_label.setOpenExternalLinks(True)
        metadata_layout.addWidget(github_link_label)

        top_left_layout.addLayout(metadata_layout)
        layout.addLayout(top_left_layout)

        build_info_box = QGroupBox("Build Information")
        build_info_layout = QVBoxLayout()

        build_info_layout.addWidget(QLabel("Version: 1.0.7 (X)"))
        build_info_layout.addWidget(QLabel("Pyinstaller: 6.3.0"))
        build_info_layout.addWidget(QLabel("PyQt6: 6.6.1"))
        build_info_layout.addWidget(QLabel("Build date: Jan 3 2024"))

        os_info_box = QGroupBox("Operating System")
        os_info_layout = QVBoxLayout()

        os_name = system()
        os_version = version()
        os_release = release()
        os_architecture = architecture()[0]

        os_info_layout.addWidget(QLabel(f"OS: {os_name} {os_release} ({os_architecture})"))
        os_info_layout.addWidget(QLabel(f"Version: {os_version}"))

        os_info_box.setLayout(os_info_layout)
        layout.addWidget(os_info_box)

        icon_path = 'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))

        build_info_box.setLayout(build_info_layout)
        layout.addWidget(build_info_box)

        self.setLayout(layout)
