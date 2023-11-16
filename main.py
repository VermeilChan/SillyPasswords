import sys
import secrets
import string

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QCheckBox,
    QGridLayout,
    QMessageBox,
    QHBoxLayout,
    QGroupBox,
)


class PasswordGenerator(QWidget):
    MIN_PASSWORD_LENGTH = 1
    MAX_PASSWORD_LENGTH = 512
    DEFAULT_PASSWORD_LENGTH = 16
    PASSWORD_CHARS = string.ascii_letters + string.digits + string.punctuation

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.create_widgets()
        self.setup_layout()
        self.connect_signals()
        self.set_window_properties()

    def create_widgets(self):
        self.password_label = QLabel('Password:')
        self.password_output = QLineEdit()
        self.password_output.setEchoMode(QLineEdit.EchoMode.Normal)
        self.length_label = QLabel('Length:')
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(self.MIN_PASSWORD_LENGTH, self.MAX_PASSWORD_LENGTH)
        self.length_slider.setValue(self.DEFAULT_PASSWORD_LENGTH)
        self.length_display = QLabel(str(self.DEFAULT_PASSWORD_LENGTH))
        self.generate_button = QPushButton('Generate', toolTip='Generate a password.')
        self.copy_button = QPushButton('Copy', toolTip='Copy the generated password to the clipboard.')
        self.strength_label = QLabel('Strength: ')
        self.uppercase_checkbox = QCheckBox('ABC', toolTip='Include uppercase letters in the password.')
        self.uppercase_checkbox.setChecked(True)
        self.lowercase_checkbox = QCheckBox('abc', toolTip='Include lowercase letters in the password.')
        self.lowercase_checkbox.setChecked(True)
        self.numbers_checkbox = QCheckBox('123', toolTip='Include numbers in the password.')
        self.numbers_checkbox.setChecked(True)
        self.symbols_checkbox = QCheckBox('&#%', toolTip='Include symbols in the password.')
        self.symbols_checkbox.setChecked(True)

    def setup_layout(self):
        layout = QVBoxLayout(self)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.length_label, 0, 0)
        grid_layout.addWidget(self.length_slider, 0, 1)
        grid_layout.addWidget(self.length_display, 0, 2)
        layout.addLayout(grid_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_output)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.strength_label)

        char_sets_layout = QHBoxLayout()
        char_sets_group_box = QGroupBox('Characters used:')
        char_sets_group_layout = QVBoxLayout(char_sets_group_box)
        char_sets_group_layout.addWidget(self.uppercase_checkbox)
        char_sets_group_layout.addWidget(self.lowercase_checkbox)
        char_sets_group_layout.addWidget(self.numbers_checkbox)
        char_sets_group_layout.addWidget(self.symbols_checkbox)
        char_sets_layout.addWidget(char_sets_group_box)
        layout.addLayout(char_sets_layout)

        layout.setSpacing(10)

    def connect_signals(self):
        self.generate_button.clicked.connect(self.generate_password)
        self.length_slider.valueChanged.connect(self.update_password_and_length_display)
        self.copy_button.clicked.connect(self.copy_password)
        self.uppercase_checkbox.stateChanged.connect(self.generate_password)
        self.lowercase_checkbox.stateChanged.connect(self.generate_password)
        self.numbers_checkbox.stateChanged.connect(self.generate_password)
        self.symbols_checkbox.stateChanged.connect(self.generate_password)

    def set_window_properties(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('SillyPasswords')
        icon_path = 'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))
        font = QFont("Space Grotesk", 16)
        self.setFont(font)

        stylesheet = """
            QWidget {
                background-color: #262626;
                color: #f0f0f0;
            }

            QPushButton {
                background-color: #6706e0;
                color: #ffffff;
                border: 1px solid #4d04a6;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 100px;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #4a049f;
            }

            QSlider {
                background-color: #262626;
            }

            QSlider::handle:horizontal {
                background: #6706e0;
                border: 1px solid #6706e0;
                width: 18px;
                margin: -2px 0;
                border-radius: 4px;
            }

            QLabel {
                font-size: 14px;
            }

            QLineEdit, QCheckBox {
                background-color: #333333;
                border: 1px solid #444444;
                padding: 8px;
                font-size: 14px;
                color: #f0f0f0;
                border-radius: 4px;
            }

            QLineEdit:focus, QCheckBox:focus {
                border: 2px solid #4d04a6;
            }

            QMessageBox {
                background-color: #262626;
                color: #f0f0f0;
            }
        """

        self.setStyleSheet(stylesheet)
        self.show()

    def update_password_and_length_display(self):
        self.generate_password(update_length_display=True)

    def generate_password(self, update_length_display=True):
        length = self.length_slider.value()

        selected_chars = ''
        if self.uppercase_checkbox.isChecked():
            selected_chars += string.ascii_uppercase
        if self.lowercase_checkbox.isChecked():
            selected_chars += string.ascii_lowercase
        if self.numbers_checkbox.isChecked():
            selected_chars += string.digits
        if self.symbols_checkbox.isChecked():
            selected_chars += string.punctuation

        if not selected_chars:
            self.show_info_popup('Please select at least one character set.')
            return

        selected_chars = ''.join(secrets.SystemRandom().sample(selected_chars, min(length, len(selected_chars))))
        password = ''.join(secrets.SystemRandom().sample(selected_chars, min(length, len(selected_chars))))
        self.password_output.setText(password)

        if update_length_display:
            self.length_display.setText(str(length))

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_output.text())
        self.show_info_popup('Password copied to clipboard.')

    def show_info_popup(self, message):
        info_popup = QMessageBox(self)
        info_popup.setIcon(QMessageBox.Icon.Information)
        info_popup.setText(message)
        info_popup.setWindowTitle('SillyPasswords')
        info_popup.exec()



def main():
    app = QApplication(sys.argv)
    global generator_instance
    generator_instance = PasswordGenerator()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
