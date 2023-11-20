from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
)

from about import AboutSillyPasswords
from password_generator import PasswordGeneratorLogic

class PasswordGeneratorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.create_widgets()
        self.setup_layout()
        self.set_window_properties()

        self.logic = PasswordGeneratorLogic(self)

    def create_widgets(self):
        self.password_label = QLabel('Password:')
        self.password_output = QLineEdit()
        self.password_output.setEchoMode(QLineEdit.EchoMode.Normal)
        self.length_label = QLabel('Password Length:')
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(PasswordGeneratorLogic.MIN_PASSWORD_LENGTH, PasswordGeneratorLogic.MAX_PASSWORD_LENGTH)
        self.length_slider.setValue(PasswordGeneratorLogic.DEFAULT_PASSWORD_LENGTH)
        self.length_display = QLabel(f"{PasswordGeneratorLogic.DEFAULT_PASSWORD_LENGTH}")
        self.generate_button = QPushButton('Generate', toolTip='Generate a password.')
        self.copy_button = QPushButton('Copy', toolTip='Copy the generated password to the clipboard.')
        self.uppercase_checkbox = QCheckBox('ABC', toolTip='Include uppercase letters in the password.')
        self.uppercase_checkbox.setChecked(True)
        self.lowercase_checkbox = QCheckBox('abc', toolTip='Include lowercase letters in the password.')
        self.lowercase_checkbox.setChecked(True)
        self.numbers_checkbox = QCheckBox('123', toolTip='Include numbers in the password.')
        self.numbers_checkbox.setChecked(True)
        self.symbols_checkbox = QCheckBox('$#%', toolTip='Include symbols in the password.')
        self.symbols_checkbox.setChecked(True)

        menubar = self.menuBar()

        about_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.setStatusTip('Help')
        about_action.triggered.connect(self.show_about_dialog)

        about_menu.addAction(about_action)

    def show_about_dialog(self):
        if not self.logic.about_dialog:
            self.logic.about_dialog = AboutSillyPasswords()

        self.logic.about_dialog.show()

    def setup_layout(self):
        central_widget = QWidget(self)

        layout = QVBoxLayout(central_widget)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.length_label, 0, 0)
        grid_layout.addWidget(self.length_slider, 0, 1)
        grid_layout.addWidget(self.length_display, 0, 2)
        layout.addLayout(grid_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.copy_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_output)

        char_sets_layout = QFormLayout()
        char_sets_group_box = QGroupBox('Characters used:')
        char_sets_group_layout = QVBoxLayout(char_sets_group_box)
        char_sets_group_layout.addWidget(self.uppercase_checkbox)
        char_sets_group_layout.addWidget(self.lowercase_checkbox)
        char_sets_group_layout.addWidget(self.numbers_checkbox)
        char_sets_group_layout.addWidget(self.symbols_checkbox)
        char_sets_layout.addRow(char_sets_group_box)
        layout.addLayout(char_sets_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        layout.setSpacing(10)

    def set_window_properties(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('SillyPasswords')
        icon_path = 'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet('Dark Mode')
