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
        self.password_strength_calculator = PasswordStrengthCalculator()

    def init_ui(self):
        self.create_widgets()
        self.setup_layout()
        self.connect_signals()
        self.set_window_properties()

    def create_widgets(self):
        self.password_label = QLabel('Password:')
        self.password_output = QLineEdit()
        self.password_output.setEchoMode(QLineEdit.EchoMode.Password)
        self.length_label = QLabel('Length:')
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(self.MIN_PASSWORD_LENGTH, self.MAX_PASSWORD_LENGTH)
        self.length_slider.setValue(self.DEFAULT_PASSWORD_LENGTH)
        self.length_display = QLabel(str(self.DEFAULT_PASSWORD_LENGTH))
        self.generate_button = QPushButton('Generate', toolTip='Generate a password.')
        self.show_password_checkbox = QCheckBox('Show Password', toolTip='Show the generated password in plain text.')
        self.show_password_checkbox.setVisible(False)
        self.copy_button = QPushButton('Copy', toolTip='Copy the generated password to the clipboard.')
        self.strength_label = QLabel('Strength: ')
        self.uppercase_checkbox = QCheckBox('ABC', toolTip='Include uppercase letters in the password.')
        self.lowercase_checkbox = QCheckBox('abc', toolTip='Include lowercase letters in the password.')
        self.numbers_checkbox = QCheckBox('123', toolTip='Include numbers in the password.')
        self.symbols_checkbox = QCheckBox('&#%', toolTip='Include symbols in the password.')

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
        layout.addWidget(self.show_password_checkbox)
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
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        self.copy_button.clicked.connect(self.copy_password)
        self.uppercase_checkbox.stateChanged.connect(self.generate_password)
        self.lowercase_checkbox.stateChanged.connect(self.generate_password)
        self.numbers_checkbox.stateChanged.connect(self.generate_password)
        self.symbols_checkbox.stateChanged.connect(self.generate_password)
        self.info_popup_shown = False

    def set_window_properties(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('SillyPasswords')
        icon_path = 'Assets/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))
        font = QFont("Space Grotesk", 12)
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

        if not (
            self.uppercase_checkbox.isChecked()
            or self.lowercase_checkbox.isChecked()
            or self.numbers_checkbox.isChecked()
            or self.symbols_checkbox.isChecked()
        ):
            self.uppercase_checkbox.setChecked(True)

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

        selected_chars = ''.join(secrets.SystemRandom().sample(selected_chars, len(selected_chars)))
        password = secrets.token_urlsafe(length)
        self.password_output.setText(password)

        if update_length_display:
            self.length_display.setText(str(length))

        strength = self.password_strength_calculator.calculate_password_strength(password)
        self.password_strength_calculator.update_strength_label(strength)

        if length < 16 and not self.info_popup_shown:
            self.show_info_popup('its good to make your passwords at least 16 characters long or more.')
            self.info_popup_shown = True

        self.show_password_checkbox.setChecked(True)
        self.show_password_checkbox.setVisible(True)
        self.toggle_password_visibility()

    def toggle_password_visibility(self):
        echo_mode = QLineEdit.EchoMode.Normal if self.show_password_checkbox.isChecked() else QLineEdit.EchoMode.Password
        self.password_output.setEchoMode(echo_mode)

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


class PasswordStrengthCalculator:
    def calculate_password_strength(self, password):
        weights = {
            'lowercase': 0.2,
            'uppercase': 0.5,
            'digit': 0.3,
            'symbol': 0.7,
            'length': 1.0,
            'charset_bonus': 0.4,
        }

        lowercase_strength = any(char in string.ascii_lowercase for char in password)
        uppercase_strength = any(char in string.ascii_uppercase for char in password)
        digit_strength = any(char in string.digits for char in password)
        symbol_strength = any(char in string.punctuation for char in password)
        length_strength = len(password) / len(string.printable)

        total_strength = (
            weights['lowercase'] * lowercase_strength +
            weights['uppercase'] * uppercase_strength +
            weights['digit'] * digit_strength +
            weights['symbol'] * symbol_strength +
            weights['length'] * length_strength
        ) / 5.0

        char_sets_count = sum([lowercase_strength, uppercase_strength, digit_strength, symbol_strength])
        charset_bonus = weights['charset_bonus'] * (char_sets_count / 4.0)
        total_strength += charset_bonus

        return total_strength

    def update_strength_label(self, strength):
        strength_percentage = int(strength * 100)

        color_stops = [100, 75, 50, 25, 10]
        colors = ['#00FF00', '#FFFF00', '#FFA500', '#FF0000', '#8B4513']

        if strength_percentage > 100:
            interpolated_color = colors[0]
        else:
            color_index = next((i for i, stop in enumerate(color_stops) if strength_percentage >= stop), len(color_stops) - 1)
            lower_stop = color_stops[color_index - 1]
            upper_stop = color_stops[color_index]
            lower_color = colors[color_index - 1]
            upper_color = colors[color_index]
            interpolation_factor = (strength_percentage - lower_stop) / (upper_stop - lower_stop)

            def interpolate_color(c1, c2, factor):
                return tuple(int((1 - factor) * c1[i] + factor * c2[i]) for i in range(3))

            interpolated_color = '#%02x%02x%02x' % interpolate_color(
                tuple(int(lower_color[i:i + 2], 16) for i in (1, 3, 5)),
                tuple(int(upper_color[i:i + 2], 16) for i in (1, 3, 5)),
                interpolation_factor
            )

        strength_text = f'<font color="{interpolated_color}">Strength:</font> {strength_percentage}% (Basic Calculation, Its Really Bad 💀)'
        generator_instance.strength_label.setText(strength_text)
        generator_instance.strength_label.setObjectName("password_strength_label")


def main():
    app = QApplication(sys.argv)
    global generator_instance
    generator_instance = PasswordGenerator()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
