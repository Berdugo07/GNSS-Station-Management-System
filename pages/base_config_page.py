from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from PySide6.QtGui import QFont

import json
import os


class BaseConfigPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel(
            "Configuración Base GNSS"
        )

        title.setFont(
            QFont("Segoe UI", 22)
        )

        layout.addWidget(title)

        layout.addWidget(
            QLabel("IP Base")
        )

        self.ip_input = QLineEdit()

        layout.addWidget(
            self.ip_input
        )

        layout.addWidget(
            QLabel("Puerto Base")
        )

        self.base_port_input = QLineEdit()

        layout.addWidget(
            self.base_port_input
        )

        layout.addWidget(
            QLabel("Puerto Local")
        )

        self.local_port_input = QLineEdit()

        layout.addWidget(
            self.local_port_input
        )

        self.save_btn = QPushButton(
            "Guardar Configuración"
        )

        layout.addWidget(
            self.save_btn
        )

        self.save_btn.clicked.connect(
            self.save_config
        )

        self.load_config()

    def save_config(self):

        data = {

            "base_ip":
                self.ip_input.text(),

            "base_port":
                self.base_port_input.text(),

            "local_port":
                self.local_port_input.text()
        }

        with open(
            "base_config.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        QMessageBox.information(
            self,
            "OK",
            "Configuración guardada"
        )

    def load_config(self):

        if not os.path.exists(
            "base_config.json"
        ):
            return

        with open(
            "base_config.json",
            "r"
        ) as f:

            data = json.load(f)

        self.ip_input.setText(
            data.get("base_ip", "")
        )

        self.base_port_input.setText(
            str(
                data.get(
                    "base_port",
                    ""
                )
            )
        )

        self.local_port_input.setText(
            str(
                data.get(
                    "local_port",
                    ""
                )
            )
        )