import sys
import string
import secrets

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QAction, QPixmap, QDesktopServices
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
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
    QFormLayout,
)

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

        self.ui.setStyleSheet(dark_theme)
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
        info_popup = QMessageBox(self.ui)
        info_popup.setIcon(QMessageBox.Icon.Information)
        info_popup.setText(message)
        info_popup.setWindowTitle('SillyPasswords')
        info_popup.exec()

    def toggle_theme(self):
        current_stylesheet = self.ui.styleSheet()

        if current_stylesheet == light_theme:
            self.ui.setStyleSheet(dark_theme)
            self.ui.theme_menu_toggle.setText('Light Mode')
        else:
            self.ui.setStyleSheet(light_theme)
            self.ui.theme_menu_toggle.setText('Dark Mode')

        if self.about_dialog:
            self.about_dialog.update_theme()


class AboutSillyPasswords(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('About SillyPasswords')
        self.setGeometry(400, 200, 300, 200)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)

        layout = QVBoxLayout(central_widget)

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('Assets/Raubtier.png')
        self.logo_label.setPixmap(self.logo_pixmap)
        layout.addWidget(self.logo_label)

        self.name_version_label = QLabel('SillyPasswords v1.0.3 (x64)', self)
        layout.addWidget(self.name_version_label)

        self.license_label = QLabel('GPL-3.0 License', self)
        layout.addWidget(self.license_label)

        self.description_label = QLabel('Free And Open Source Forever!', self)
        layout.addWidget(self.description_label)

        self.repo_button = QPushButton('GitHub Repository', self)
        self.repo_button.clicked.connect(self.open_repo)
        layout.addWidget(self.repo_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet(dark_theme)

    def open_repo(self):
        QDesktopServices.openUrl(QUrl('https://github.com/VermeilChan/SillyPasswords'))

    def update_theme(self):
        current_stylesheet = self.styleSheet()

        if current_stylesheet == light_theme:
            self.setStyleSheet(dark_theme)
            self.logo_label.setStyleSheet(dark_theme)
            self.name_version_label.setStyleSheet(dark_theme)
            self.license_label.setStyleSheet(dark_theme)
            self.description_label.setStyleSheet(dark_theme)
            self.repo_button.setStyleSheet(dark_theme)
        else:
            self.setStyleSheet(light_theme)
            self.logo_label.setStyleSheet(light_theme)
            self.name_version_label.setStyleSheet(light_theme)
            self.license_label.setStyleSheet(light_theme)
            self.description_label.setStyleSheet(light_theme)
            self.repo_button.setStyleSheet(light_theme)


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

        theme_menu = menubar.addMenu('Appearance')

        self.theme_menu_toggle = QAction('Dark Mode', self)
        self.theme_menu_toggle.setStatusTip('Toggle between dark and light modes.')
        theme_menu.addAction(self.theme_menu_toggle)

        about_menu = menubar.addMenu('About SillyPasswords')

        about_action = QAction('About', self)
        about_action.setStatusTip('About SillyPasswords')
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


def main():
    app = QApplication(sys.argv)
    generator_instance = PasswordGeneratorUI()
    generator_instance.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
