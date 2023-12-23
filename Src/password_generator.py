import string
import secrets

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox

from themes import dark_theme

class CheckboxState:
    CHECKED = Qt.CheckState.Checked
    UNCHECKED = Qt.CheckState.Unchecked

class PasswordGeneratorLogic:
    DEFAULT_PASSWORD_LENGTH = 12
    MIN_PASSWORD_LENGTH = 1
    MAX_PASSWORD_LENGTH = 4096
    PASSWORD_CHARACTERS = string.ascii_letters + string.digits + string.punctuation

    def __init__(self, ui):
        self.ui = ui
        self.ui.generate_button.clicked.connect(self.generate_password)
        self.ui.length_slider.valueChanged.connect(self.update_password_and_length_display)
        self.ui.copy_button.clicked.connect(self.copy_password)
        self.ui.uppercase_checkbox.stateChanged.connect(self.generate_password)
        self.ui.lowercase_checkbox.stateChanged.connect(self.generate_password)
        self.ui.numbers_checkbox.stateChanged.connect(self.generate_password)
        self.ui.symbols_checkbox.stateChanged.connect(self.generate_password)

        self.ui.setStyleSheet(dark_theme)

        self.about_dialog = None

    def update_password_and_length_display(self):
        self.generate_password(update_length_display=True)

    def generate_password(self, update_length_display=True):
        length = self.ui.length_slider.value()

        selected_chars = ''
        for checkbox, char_set in zip(
            [self.ui.uppercase_checkbox, self.ui.lowercase_checkbox, self.ui.numbers_checkbox, self.ui.symbols_checkbox],
            [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]
        ):
            if checkbox.checkState() == CheckboxState.CHECKED:
                selected_chars += char_set

        if not selected_chars:
            self.show_info_popup(f'Please select at least one character set.')
            return

        selected_chars = ''.join(secrets.choice(selected_chars) for _ in range(length))

        self.ui.password_output.setText(selected_chars)

        if update_length_display:
            self.ui.length_display.setText(f"{length}")

    def copy_password(self):
        password = self.ui.password_output.text()
        if not password:
            self.show_info_popup(f'No password generated. Please generate a password first.')
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        self.show_info_popup(f'Password copied to clipboard.')

    def show_info_popup(self, message):
        info_popup = QMessageBox(self.ui)
        info_popup.setIcon(QMessageBox.Icon.Information)
        info_popup.setText(message)
        info_popup.setWindowTitle(f'SillyPasswords')
        info_popup.exec()
