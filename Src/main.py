import sys

from PyQt6.QtWidgets import QApplication

from gui import PasswordGeneratorUI

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    generator_instance = PasswordGeneratorUI()
    generator_instance.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
