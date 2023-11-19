light_theme = """
    QWidget {
        background-color: #ffffff;
        color: #000000;
        font-family: "Roboto";
        font-size: 12px;
    }

    QPushButton {
        background-color: #0066cc;
        color: #ffffff;
        border: 1px solid #004080;
        padding: 8px 16px;
        font-size: 14px;
        min-width: 100px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #0052a3;
    }

    QSlider {
        background-color: #ffffff;
    }

    QSlider::handle:horizontal {
        background: #0066cc;
        border: 1px solid #0066cc;
        width: 18px;
        margin: -2px 0;
        border-radius: 4px;
    }

    QLabel {
        font-size: 14px;
    }

    QLineEdit, QCheckBox {
        background-color: #f0f0f0;
        border: 1px solid #cccccc;
        padding: 8px;
        font-size: 14px;
        color: #000000;
        border-radius: 4px;
    }

    QLineEdit:focus, QCheckBox:focus {
        border: 2px solid #004080;
    }

    QMessageBox {
        background-color: #ffffff;
        color: #000000;
    }

    QPalette {
        background-color: #000000;
        color: #000000;
    }
"""

dark_theme = """
    QWidget {
        background-color: #262626;
        color: #f0f0f0;
        font-family: "Roboto";
        font-size: 12px;
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
