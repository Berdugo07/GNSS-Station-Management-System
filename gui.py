import sys
import socket
import json
import threading

from PySide6.QtWidgets import (

    QApplication,
    QWidget,
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QListWidget,
    QListWidgetItem,
    QHeaderView,
    QStackedWidget
)

from PySide6.QtCore import Qt, QTimer

from PySide6.QtGui import QFont, QColor, QIcon

from PySide6.QtGui import QPixmap

import qtawesome as qta

from utils import resource_path

from pages.rtklib_page import RTKLIBPage


from pages.users_page import UsersPage

from pages.create_user_page import CreateUserPage

from database import *

from server import start_server


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowIcon(
            QIcon(
                resource_path(
                    "assets/icon.ico"
                )
            )
        )

        self.server_process = None

        self.setWindowTitle(
            "GSI NTRIP CASTER"
        )

        self.resize(1700, 950)

        self.setStyleSheet("""

            QWidget {

                background-color: #0b1220;

                color: #f8fafc;

                font-size: 14px;

                font-family: Segoe UI;
            }

            QFrame {

                background-color: #172033;

                border-radius: 18px;
            }

            QPushButton {

                border: none;

                border-radius: 14px;

                padding: 16px;

                font-size: 16px;

                font-weight: bold;

                color: white;
            }

            QPushButton:hover {

                background-color: #334155;
            }

            QListWidget {

                border: none;

                background: transparent;

                outline: 0;
            }

            QListWidget::item {

                padding: 16px;

                margin-top: 5px;

                border-radius: 12px;
            }

            QListWidget::item:selected {

                background-color: #2563eb;
            }

            QTableWidget {

                background-color: #172033;

                border: none;

                border-radius: 14px;

                gridline-color: #243041;

                alternate-background-color: #1d2940;

                selection-background-color: #1d4ed8;

                selection-color: white;
            }

            QTableWidget::item {

                padding: 14px;
            }

            QTableWidget::item:selected {

                background-color: #2563eb;

                color: white;
            }

            QHeaderView::section {

                background-color: #243041;

                color: white;

                border: none;

                padding: 14px;

                font-size: 15px;

                font-weight: bold;
            }

        """)

        # =========================
        # MAIN LAYOUT
        # =========================

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        main_layout.setSpacing(15)

        self.setLayout(main_layout)

        # =========================
        # SIDEBAR
        # =========================

        sidebar = QFrame()

        sidebar.setFixedWidth(260)

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        sidebar_layout.setSpacing(15)

        sidebar.setLayout(sidebar_layout)

        logo = QLabel()

        pixmap = QPixmap(
            resource_path(
                "assets/logo.png"
            )
        )

        logo.setPixmap(
            pixmap.scaled(
                180,
                180,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        logo.setAlignment(
            Qt.AlignCenter
        )

        sidebar_layout.addWidget(
            logo
        )

        logo_title = QLabel(
            "GEOSPATIAL INDUSTRY"
        )

        logo_title.setAlignment(
            Qt.AlignCenter
        )

        logo_title.setFont(
            QFont("Segoe UI", 22)
        )

        logo_title.setStyleSheet("""

            font-weight: bold;

            color: white;
        """)

        sidebar_layout.addWidget(
            logo_title
        )

        version = QLabel(
            "v1.0 JSON EDITION"
        )

        version.setAlignment(
            Qt.AlignCenter
        )

        version.setStyleSheet("""

            color: #64748b;

            font-size: 11px;
        """)

        sidebar_layout.addWidget(
            version
        )

        self.menu = QListWidget()

        items = [

            ("Dashboard", "fa5s.tachometer-alt"),

            ("Usuarios", "fa5s.users-cog"),

            ("Crear Usuario", "fa5s.user-plus"),

            ("RTKLIB", "fa5s.satellite")
        ]

        for text, icon in items:

            item = QListWidgetItem(

                qta.icon(icon, color='white'),

                text
            )

            self.menu.addItem(item)

        self.menu.setCurrentRow(0)

        self.menu.itemClicked.connect(
            self.menu_action
        )

        sidebar_layout.addWidget(
            self.menu
        )

        sidebar_layout.addStretch()

        # =========================
        # PAGES
        # =========================

        self.pages = QStackedWidget()

        # =========================
        # DASHBOARD PAGE
        # =========================

        dashboard_page = QWidget()

        content = QVBoxLayout()

        content.setSpacing(18)

        dashboard_page.setLayout(content)

        panel_title = QLabel(
            "PANEL DE ADMINISTRACIÓN"
        )

        panel_title.setMinimumHeight(90)

        panel_title.setFont(
            QFont("Segoe UI", 42)
        )

        panel_title.setStyleSheet("""

            color: white;

            font-weight: 900;

            letter-spacing: 2px;

            padding-top: 10px;

            padding-bottom: 20px;
        """)

        content.addWidget(
            panel_title
        )

        # =========================
        # TOP BUTTONS
        # =========================

        top_cards = QHBoxLayout()

        top_cards.setSpacing(15)

        self.start_button = QPushButton(
            "▶ Iniciar NTRIP"
        )

        self.start_button.setMinimumHeight(70)

        self.start_button.setStyleSheet("""

            QPushButton {

                background-color: #16a34a;
            }

            QPushButton:hover {

                background-color: #15803d;
            }
        """)

        self.stop_button = QPushButton(
            "■ Detener NTRIP"
        )

        self.stop_button.setMinimumHeight(70)

        self.stop_button.setStyleSheet("""

            QPushButton {

                background-color: #dc2626;
            }

            QPushButton:hover {

                background-color: #b91c1c;
            }
        """)

        self.status_card = QFrame()

        self.status_card.setMinimumHeight(70)

        status_layout = QHBoxLayout()

        status_layout.setContentsMargins(
            20,
            10,
            20,
            10
        )

        self.status_card.setLayout(
            status_layout
        )

        self.status_label = QLabel(
            "🔴 Servidor NTRIP OFFLINE"
        )

        self.status_label.setFont(
            QFont("Segoe UI", 14)
        )

        self.status_label.setStyleSheet("""

            color: white;

            font-weight: bold;
        """)

        status_layout.addWidget(
            self.status_label
        )

        top_cards.addWidget(
            self.start_button
        )

        top_cards.addWidget(
            self.stop_button
        )

        top_cards.addWidget(
            self.status_card
        )

        content.addLayout(
            top_cards
        )

        # =========================
        # ONLINE USERS
        # =========================

        online_card = QFrame()

        online_layout = QVBoxLayout()

        online_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        online_card.setLayout(
            online_layout
        )

        online_title = QLabel(
            "Usuarios Online"
        )

        online_title.setFont(
            QFont("Segoe UI", 17)
        )

        online_title.setStyleSheet("""

            color: white;

            font-weight: bold;

            padding-bottom: 10px;
        """)

        online_layout.addWidget(
            online_title
        )

        self.online_table = QTableWidget()

        self.online_table.setAlternatingRowColors(True)

        self.online_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.online_table.verticalHeader().setVisible(False)

        self.online_table.setColumnCount(4)

        self.online_table.setHorizontalHeaderLabels([

            "Usuario",
            "IP",
            "Mountpoint",
            "Conectado"
        ])

        self.online_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.online_table.setMinimumHeight(250)

        online_layout.addWidget(
            self.online_table
        )

        content.addWidget(
            online_card
        )

        # =========================
        # LAST USERS
        # =========================

        last_card = QFrame()

        last_layout = QVBoxLayout()

        last_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        last_card.setLayout(
            last_layout
        )

        last_title = QLabel(
            "Últimos Usuarios Registrados"
        )

        last_title.setFont(
            QFont("Segoe UI", 17)
        )

        last_title.setStyleSheet("""

            color: white;

            font-weight: bold;

            padding-bottom: 10px;
        """)

        last_layout.addWidget(
            last_title
        )

        self.last_users_table = QTableWidget()

        self.last_users_table.setAlternatingRowColors(True)

        self.last_users_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.last_users_table.verticalHeader().setVisible(False)

        self.last_users_table.setColumnCount(6)

        self.last_users_table.setHorizontalHeaderLabels([

            "Usuario",
            "Nombre Completo",
            "Teléfono",
            "Mountpoints",
            "Expira",
            "Estado"
        ])

        self.last_users_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.last_users_table.setMinimumHeight(250)

        last_layout.addWidget(
            self.last_users_table
        )

        content.addWidget(
            last_card
        )

        # =========================
        # OTHER PAGES
        # =========================

        self.users_page = UsersPage()

        self.create_user_page = CreateUserPage()

        self.rtklib_page = RTKLIBPage()

        # =========================
        # ADD PAGES
        # =========================

        self.pages.addWidget(
            dashboard_page
        )

        self.pages.addWidget(
            self.users_page
        )

        self.pages.addWidget(
            self.create_user_page
        )

        self.pages.addWidget(
            self.rtklib_page
        )

        # =========================
        # ADD TO MAIN
        # =========================

        main_layout.addWidget(
            sidebar
        )

        main_layout.addWidget(
            self.pages,
            1
        )

        # =========================
        # EVENTS
        # =========================

        self.start_button.clicked.connect(
            self.start_server
        )

        self.stop_button.clicked.connect(
            self.stop_server
        )

        self.load_last_users()

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.load_online_users
        )

        self.timer.start(3000)

    # =========================
    # LOAD LAST USERS
    # =========================

    def load_last_users(self):

        users = get_last_users(5)

        self.last_users_table.setRowCount(
            len(users)
        )

        for row, user in enumerate(users):

            username = str(user[0])

            fullname = str(user[1])

            phone = str(user[2])

            mountpoints = str(user[3])

            expire = str(user[4])

            active = user[5]

            status = "ACTIVO" if active else "INACTIVO"

            values = [

                username,
                fullname,
                phone,
                mountpoints,
                expire,
                status
            ]

            for col, value in enumerate(values):

                item = QTableWidgetItem(
                    value
                )

                item.setForeground(
                    QColor("#ffffff")
                )

                self.last_users_table.setItem(
                    row,
                    col,
                    item
                )

    # =========================
    # LOAD ONLINE USERS
    # =========================

    def load_online_users(self):

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(1)

            sock.connect(
                ("127.0.0.1", 9090)
            )

            data = sock.recv(65535)

            sock.close()

            users = json.loads(
                data.decode()
            )

            self.online_table.setRowCount(
                len(users)
            )

            for row, user in enumerate(users):

                values = [

                    user["username"],
                    user["ip"],
                    user["mountpoint"],
                    user["connected_at"]
                ]

                for col, value in enumerate(values):

                    item = QTableWidgetItem(
                        str(value)
                    )

                    item.setForeground(
                        QColor("#ffffff")
                    )

                    self.online_table.setItem(
                        row,
                        col,
                        item
                    )

        except:

            self.online_table.setRowCount(0)

    # =========================
    # START SERVER
    # =========================

    def start_server(self):

        if self.server_process is None:

            self.server_process = threading.Thread(

                target=start_server,

                daemon=True
            )

            self.server_process.start()

            self.status_label.setText(

                "🟢 Servidor NTRIP TRANSMITIENDO"
            )
    # =========================
    # STOP SERVER
    # =========================
    def stop_server(self):

        self.status_label.setText(

            "🔴 Servidor NTRIP OFFLINE"
        )

        self.server_process = None

    # =========================
    # CLOSE EVENT
    # =========================

    def closeEvent(self, event):

       event.accept()


    # =========================
    # MENU ACTION
    # =========================

    def menu_action(self, item):

        text = item.text()

        if text == "Dashboard":

            self.load_last_users()

            self.pages.setCurrentIndex(0)

        elif text == "Usuarios":

            self.users_page.load_users()

            self.pages.setCurrentIndex(1)

        elif text == "Crear Usuario":

            self.pages.setCurrentIndex(2)
        
        elif text == "RTKLIB":

            self.pages.setCurrentIndex(3)
    


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())