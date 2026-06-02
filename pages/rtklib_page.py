from PySide6.QtWidgets import (

    QWidget,
    QVBoxLayout,
    QHBoxLayout,

    QLabel,

    QPushButton,

    QTextEdit,

    QFrame,

    QLineEdit,

    QComboBox
)

from PySide6.QtGui import QFont

from PySide6.QtCore import Signal

import json

import os

from rtklib_manager import RTKLIBManager


class RTKLIBPage(QWidget):

    log_signal = Signal(str)

    def __init__(self):

        super().__init__()

        self.profiles = {

            "Perfil 1": {

                "ip": "192.168.0.10",

                "base_port": "5017",

                "local_port": "9001",

                "lat": "",

                "lon": "",

                "height": ""

            },

            "Perfil 2": {

                "ip": "",

                "base_port": "",

                "local_port": "9002",

                "lat": "",

                "lon": "",

                "height": ""

            },

            "Perfil 3": {

                "ip": "",

                "base_port": "",

                "local_port": "9003",

                "lat": "",

                "lon": "",

                "height": ""

            }

        }

        self.rtklib = RTKLIBManager(
            log_callback=self.emit_log
        )

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel(
            "RTKLIB STR2STR"
        )

        title.setFont(
            QFont("Segoe UI", 24)
        )

        layout.addWidget(title)

        card = QFrame()

        card_layout = QVBoxLayout()

        # =====================================
        # PERFIL
        # =====================================

        self.profile_combo = QComboBox()

        self.profile_combo.addItems([

            "Perfil 1",
            "Perfil 2",
            "Perfil 3"

        ])

        card_layout.addWidget(

            QLabel("Perfil")
        )

        card_layout.addWidget(

            self.profile_combo
        )

        

        card.setLayout(card_layout)

        # ==========================
        # PERFIL
        # ==========================

        card_layout.addWidget(
            QLabel("Perfil")
        )

        self.profile_combo = QComboBox()

        self.profile_combo.addItems([

            "Perfil 1",
            "Perfil 2",
            "Perfil 3"

        ])

        card_layout.addWidget(
            self.profile_combo
        )

        def load_profile(self, profile_name):

            p = self.profiles[profile_name]

            self.ip_input.setText(
                p["ip"]
            )

            self.base_port_input.setText(
                p["base_port"]
            )

            self.local_port_input.setText(
                p["local_port"]
            )

            self.lat_input.setText(
                p["lat"]
            )

            self.lon_input.setText(
                p["lon"]
            )

            self.height_input.setText(
                p["height"]
            )

        def save_profile(self):

            profile = self.profile_combo.currentText()

            self.profiles[profile] = {

                "ip": self.ip_input.text(),

                "base_port": self.base_port_input.text(),

                "local_port": self.local_port_input.text(),

                "lat": self.lat_input.text(),

                "lon": self.lon_input.text(),

                "height": self.height_input.text()

            }

            with open(
                "profiles.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.profiles,
                    f,
                    indent=4
                )

            self.emit_log(
                f"{profile} guardado correctamente"
            )
        def load_profiles(self):

            if not os.path.exists(
                "profiles.json"
            ):
                return

            with open(
                "profiles.json",
                "r",
                encoding="utf-8"
            ) as f:

                self.profiles = json.load(f)

            self.emit_log(
                "Perfiles cargados"
            )

        # ==========================
        # BASE GNSS
        # ==========================

        card_layout.addWidget(
            QLabel("IP Base GNSS")
        )

        self.ip_input = QLineEdit()

        self.ip_input.setText(
            "192.168.0.10"
        )

        card_layout.addWidget(
            self.ip_input
        )

        card_layout.addWidget(
            QLabel("Puerto Base")
        )

        self.base_port_input = QLineEdit()

        self.base_port_input.setText(
            "5017"
        )

        card_layout.addWidget(
            self.base_port_input
        )

        card_layout.addWidget(
            QLabel("Puerto Local")
        )

        self.local_port_input = QLineEdit()

        self.local_port_input.setText(
            "9001"
        )

        card_layout.addWidget(
            self.local_port_input
        )

        # ==========================
        # RTCM
        # ==========================

        card_layout.addWidget(
            QLabel("Mensajes RTCM")
        )

        self.msg_input = QLineEdit()

        self.msg_input.setText(
            "1005(10),1074(1),1084(1),1094(1),1230(10)"
        )

        self.msg_input.setReadOnly(True)

        card_layout.addWidget(
            self.msg_input
        )

        # ==========================
        # COORDENADAS
        # ==========================

        card_layout.addWidget(
            QLabel("Latitud")
        )

        self.lat_input = QLineEdit()

        self.lat_input.setPlaceholderText(
            "-17.7833"
        )

        card_layout.addWidget(
            self.lat_input
        )

        card_layout.addWidget(
            QLabel("Longitud")
        )

        self.lon_input = QLineEdit()

        self.lon_input.setPlaceholderText(
            "-63.1821"
        )

        card_layout.addWidget(
            self.lon_input
        )

        card_layout.addWidget(
            QLabel("Altura")
        )

        self.height_input = QLineEdit()

        self.height_input.setPlaceholderText(
            "420.000"
        )

        card_layout.addWidget(
            self.height_input
        )

        # ==========================
        # BOTONES
        # ==========================

        self.start_btn = QPushButton(
            "INICIAR STREAM"
        )

        self.stop_btn = QPushButton(
            "DETENER STREAM"
        )

        self.save_btn = QPushButton(
            "GUARDAR PERFIL"
        )   

        self.save_btn.clicked.connect(
            self.save_profile
        )

        card_layout.addWidget(
            self.save_btn
        )

        card_layout.addWidget(
            self.start_btn
        )

        card_layout.addWidget(
            self.stop_btn
        )

        card_layout.addWidget(
            self.save_btn
        )

        layout.addWidget(card)

        # ==========================
        # LOGS
        # ==========================

        self.logs = QTextEdit()

        self.logs.setReadOnly(True)

        layout.addWidget(
            self.logs
        )

        # ==========================
        # EVENTOS
        # ==========================

        self.start_btn.clicked.connect(
            self.start_rtklib
        )

        self.stop_btn.clicked.connect(
            self.stop_rtklib
        )

        self.save_btn.clicked.connect(
            self.save_profile
        )

        self.log_signal.connect(
            self.add_log
        )

        self.load_profiles()

    # ==========================
    # LOGS
    # ==========================

    def add_log(self, text):

        self.logs.append(text)

    def emit_log(self, text):

        self.log_signal.emit(text)

    # ==========================
    # START
    # ==========================

    def start_rtklib(self):

        ip = self.ip_input.text().strip()

        base_port = self.base_port_input.text().strip()

        local_port = self.local_port_input.text().strip()

        messages = self.msg_input.text().strip()

        lat = self.lat_input.text().strip()

        lon = self.lon_input.text().strip()

        height = self.height_input.text().strip()

        input_stream = (

            f"tcpcli://{ip}:{base_port}#rtcm3"
        )

        output_stream = (

            f"tcpsvr://:{local_port}#rtcm3"
        )

        self.emit_log("===================================")

        self.emit_log(
            f"Perfil: {self.profile_combo.currentText()}"
        )

        self.emit_log(
            f"IP Base: {ip}"
        )

        self.emit_log(
            f"Puerto Base: {base_port}"
        )

        self.emit_log(
            f"Puerto Local: {local_port}"
        )

        self.emit_log(
            f"RTCM: {messages}"
        )

        self.emit_log(
            f"LAT: {lat}"
        )

        self.emit_log(
            f"LON: {lon}"
        )

        self.emit_log(
            f"HGT: {height}"
        )

        self.emit_log("===================================")
        
        self.rtklib.start_stream(

            "BASE1",

            input_stream,

            output_stream,

            messages,

            lat,

            lon,

            height
        )

    # ==========================
    # STOP
    # ==========================

    def stop_rtklib(self):

        self.rtklib.stop_stream(
            "BASE1"
        )

        self.emit_log(
            "BASE1 detenido"
        )
        
    def load_profile(self, profile_name):

        if profile_name not in self.profiles:
            return

        p = self.profiles[profile_name]

        self.ip_input.setText(
            p.get("ip", "")
        )

        self.base_port_input.setText(
            p.get("base_port", "")
        )

        self.local_port_input.setText(
            p.get("local_port", "")
        )

        self.lat_input.setText(
            p.get("lat", "")
        )

        self.lon_input.setText(
            p.get("lon", "")
        )

        self.height_input.setText(
            p.get("height", "")
        )