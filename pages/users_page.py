from PySide6.QtWidgets import (

    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QLineEdit
)

from PySide6.QtGui import QColor, QFont

from PySide6.QtCore import Qt

from database import *

from dialogs.edit_user import EditUserDialog


class UsersPage(QWidget):

    def __init__(self):

        super().__init__()

        self.all_users = []


        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.setLayout(layout)


        card = QFrame()

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        card.setLayout(
            card_layout
        )


        title = QLabel(
            "Gestión de Usuarios"
        )

        title.setFont(
            QFont("Segoe UI", 18)
        )

        title.setStyleSheet("""

            color: white;

            font-weight: bold;

            padding-bottom: 10px;
        """)

        card_layout.addWidget(
            title
        )


        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Buscar usuario, nombre o teléfono..."
        )

        self.search_input.setMinimumHeight(45)

        self.search_input.setStyleSheet("""

            QLineEdit {

                background-color: #243041;

                border: 2px solid #334155;

                border-radius: 12px;

                padding-left: 15px;

                color: white;

                font-size: 14px;
            }

            QLineEdit:focus {

                border: 2px solid #2563eb;
            }

        """)

        card_layout.addWidget(
            self.search_input
        )

        self.table = QTableWidget()

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setShowGrid(False)

        self.table.setFocusPolicy(Qt.NoFocus)

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([

            "Usuario",
            "Nombre Completo",
            "Teléfono",
            "Mountpoints",
            "Expira",
            "Estado"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setMinimumHeight(700)

        self.table.setStyleSheet("""

            QTableWidget {

                background-color: #172033;

                border: none;

                border-radius: 14px;

                gridline-color: transparent;

                alternate-background-color: #1d2940;

                selection-background-color: #2563eb;

                selection-color: white;

                outline: 0;
            }

            QTableWidget::item {

                padding: 14px;

                border: none;
            }

            QTableWidget::item:selected {

                background-color: #2563eb;

                color: white;

                border: none;
            }

            QTableCornerButton::section {

                background-color: #172033;

                border: none;
            }

            QHeaderView::section {

                background-color: #243041;

                color: white;

                border: none;

                padding: 14px;

                font-size: 14px;

                font-weight: bold;
            }

        """)

        card_layout.addWidget(
            self.table
        )

        layout.addWidget(
            card
        )


        self.table.doubleClicked.connect(
            self.open_user
        )

        self.search_input.textChanged.connect(
            self.filter_users
        )


        self.load_users()


    def load_users(self):

        self.all_users = get_users()

        self.populate_table(
            self.all_users
        )


    def populate_table(self, users):

        self.table.setRowCount(
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
                    str(value)
                )

                item.setForeground(
                    QColor("#ffffff")
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    col,
                    item
                )

    def filter_users(self):

        text = self.search_input.text().lower()

        filtered = []

        for user in self.all_users:

            username = str(user[0]).lower()

            fullname = str(user[1]).lower()

            if text in username or text in fullname:

                filtered.append(user)

        self.populate_table(
            filtered
        )


    def open_user(self):

        row = self.table.currentRow()

        username = self.table.item(
            row,
            0
        ).text()

        user = get_user(username)

        if not user:
            return

        dialog = EditUserDialog(
            user
        )

        dialog.exec()

        self.load_users()