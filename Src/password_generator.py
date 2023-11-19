import string
import secrets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox

from themes import light_theme, dark_theme

class CheckboxState:
    CHECKED = Qt.CheckState.Checked
    UNCHECKED = Qt.CheckState.Unchecked

class PasswordGeneratorLogic:
    DEFAULT_PASSWORD_LENGTH = 24
    MIN_PASSWORD_LENGTH = 1
    MAX_PASSWORD_LENGTH = 512
    PASSWORD_CHARS = string.ascii_letters + string.digits + string.punctuation

    def __init__(self, ui):
        self.ui = ui
        self.ui.generate_button.clicked.connect(self.generate_password)
        self.ui.length_slider.valueChanged.connect(self.update_password_and_length_display)
        self.ui.copy_button.clicked.connect(self.copy_password)
        self.ui.uppercase_checkbox.stateChanged.connect(self.generate_password)
        self.ui.lowercase_checkbox.stateChanged.connect(self.generate_password)
        self.ui.numbers_checkbox.stateChanged.connect(self.generate_password)
        self.ui.symbols_checkbox.stateChanged.connect(self.generate_password)
        self.ui.theme_menu_toggle.triggered.connect(self.toggle_theme)

        self.ui.setStyleSheet(light_theme)
        self.ui.theme_menu_toggle.setText('Light Mode')

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
            self.show_info_popup('Please select at least one character set.')
            return

        random_bytes = secrets.token_bytes(length)
        password = ''.join(selected_chars[i % len(selected_chars)] for i in random_bytes)

        self.ui.password_output.setText(password)

        if update_length_display:
            self.ui.length_display.setText(f"{length}")

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.password_output.text())
        self.show_info_popup('Password copied to clipboard.')

    def show_info_popup(self, message):
        with QMessageBox(self.ui) as info_popup:
            info_popup.setIcon(QMessageBox.Icon.Information)
            info_popup.setText(message)
            info_popup.setWindowTitle('SillyPasswords')

    def toggle_theme(self):
        current_stylesheet = self.ui.styleSheet()

        if current_stylesheet == dark_theme:
            self.ui.setStyleSheet(light_theme)
            self.ui.theme_menu_toggle.setText('Dark Mode')
        else:
            self.ui.setStyleSheet(dark_theme)
            self.ui.theme_menu_toggle.setText('Light Mode')


        if self.about_dialog:
            self.about_dialog.update_theme()