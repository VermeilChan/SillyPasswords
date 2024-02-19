from sys import argv, exit

from PySide6.QtWidgets import QApplication

from gui import PasswordGeneratorUI

def main():
    app = QApplication(argv)
    app.setStyle('Fusion')
    generator_instance = PasswordGeneratorUI()
    generator_instance.show()
    exit(app.exec())

if __name__ == '__main__':
    main()
