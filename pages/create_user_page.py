from PySide6.QtWidgets import (

    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QCheckBox,
    QDateEdit,
    QMessageBox,
    QFrame,
    QSizePolicy,
    QGridLayout
)

from PySide6.QtCore import Qt, QDate

from PySide6.QtGui import QFont

from database import create_user


class CreateUserPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet("""

            QWidget {

                background-color: #0b1220;

                color: white;

                font-family: Segoe UI;
            }

            QFrame {

                background-color: #172033;

                border-radius: 22px;

                border: 1px solid #22304a;
            }

            QLabel {

                color: #f8fafc;

                font-size: 14px;

                font-weight: 600;
            }

            QLineEdit {

                background-color: #243041;

                border: 2px solid #334155;

                border-radius: 14px;

                padding: 16px;

                color: white;

                font-size: 15px;
            }

            QLineEdit:focus {

                border: 2px solid #2563eb;
            }

            QCheckBox {

                color: white;

                font-size: 15px;

                spacing: 10px;
            }

            QDateEdit {

                background-color: #243041;

                border: 2px solid #334155;

                border-radius: 14px;

                padding: 16px;

                color: white;

                font-size: 15px;
            }

            QDateEdit:focus {

                border: 2px solid #2563eb;
            }

            QPushButton {

                background-color: #16a34a;

                border: none;

                border-radius: 16px;

                padding: 18px;

                color: white;

                font-size: 16px;

                font-weight: bold;
            }

            QPushButton:hover {

                background-color: #15803d;
            }

        """)

        # =========================
        # MAIN LAYOUT
        # =========================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        main_layout.setSpacing(20)

        self.setLayout(main_layout)

        # =========================
        # HEADER
        # =========================

        header = QLabel(
            "Crear Nuevo Usuario"
        )

        header.setFont(
            QFont("Segoe UI", 28)
        )

        header.setStyleSheet("""

            font-weight: 800;

            color: white;

            padding-bottom: 10px;
        """)

        main_layout.addWidget(header)

        subtitle = QLabel(
            "Registra nuevos clientes y asigna mountpoints de acceso NTRIP."
        )

        subtitle.setStyleSheet("""

            color: #94a3b8;

            font-size: 15px;

            padding-bottom: 10px;
        """)

        main_layout.addWidget(subtitle)

        # =========================
        # CARD
        # =========================

        card = QFrame()

        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            35,
            35,
            35,
            35
        )

        card_layout.setSpacing(28)

        card.setLayout(card_layout)

        # =========================
        # GRID FORM
        # =========================

        form_grid = QGridLayout()

        form_grid.setHorizontalSpacing(20)

        form_grid.setVerticalSpacing(20)

        # USERNAME

        username_label = QLabel(
            "Usuario"
        )

        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText(
            "Ingrese usuario"
        )

        self.username_input.setMinimumHeight(58)

        # PASSWORD

        password_label = QLabel(
            "Contraseña"
        )

        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Ingrese contraseña"
        )

        self.password_input.setMinimumHeight(58)

        # FULLNAME

        fullname_label = QLabel(
            "Nombre Completo"
        )

        self.fullname_input = QLineEdit()

        self.fullname_input.setPlaceholderText(
            "Nombre completo del cliente"
        )

        self.fullname_input.setMinimumHeight(58)

        # PHONE

        phone_label = QLabel(
            "Teléfono"
        )

        self.phone_input = QLineEdit()

        self.phone_input.setPlaceholderText(
            "Número de contacto"
        )

        self.phone_input.setMinimumHeight(58)

        # GRID POSITIONS

        form_grid.addWidget(username_label, 0, 0)

        form_grid.addWidget(password_label, 0, 1)

        form_grid.addWidget(self.username_input, 1, 0)

        form_grid.addWidget(self.password_input, 1, 1)

        form_grid.addWidget(fullname_label, 2, 0)

        form_grid.addWidget(phone_label, 2, 1)

        form_grid.addWidget(self.fullname_input, 3, 0)

        form_grid.addWidget(self.phone_input, 3, 1)

        card_layout.addLayout(form_grid)

        # =========================
        # MOUNTPOINTS
        # =========================

        mount_title = QLabel(
            "Mountpoints Disponibles"
        )

        mount_title.setFont(
            QFont("Segoe UI", 16)
        )

        mount_title.setStyleSheet("""

            font-weight: bold;

            color: white;
        """)

        card_layout.addWidget(
            mount_title
        )

        mount_frame = QFrame()

        mount_frame.setStyleSheet("""

            QFrame {

                background-color: #101827;

                border-radius: 16px;

                border: 1px solid #1e293b;
            }
        """)

        mount_layout = QHBoxLayout()

        mount_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        mount_layout.setSpacing(40)

        mount_frame.setLayout(
            mount_layout
        )

        self.mp1 = QCheckBox(
            "GSI_IGM2024"
        )

        self.mp2 = QCheckBox(
            "GSI_IGM2010"
        )

        self.mp3 = QCheckBox(
            "GSI_INRA"
        )

        mount_layout.addWidget(self.mp1)

        mount_layout.addWidget(self.mp2)

        mount_layout.addWidget(self.mp3)

        mount_layout.addStretch()

        card_layout.addWidget(
            mount_frame
        )

        # =========================
        # DATE
        # =========================

        date_label = QLabel(
            "Fecha de Expiración"
        )

        date_label.setFont(
            QFont("Segoe UI", 16)
        )

        date_label.setStyleSheet("""

            font-weight: bold;

            color: white;
        """)

        card_layout.addWidget(
            date_label
        )

        self.expire_date = QDateEdit()

        self.expire_date.setCalendarPopup(
            True
        )

        self.expire_date.setDate(
            QDate.currentDate()
        )

        self.expire_date.setMinimumHeight(60)

        card_layout.addWidget(
            self.expire_date
        )

        # =========================
        # BUTTON
        # =========================

        self.save_button = QPushButton(
            "Crear Usuario"
        )

        self.save_button.setMinimumHeight(
            62
        )

        self.save_button.clicked.connect(
            self.save_user
        )

        card_layout.addWidget(
            self.save_button
        )

        main_layout.addWidget(card)

    # =========================
    # SAVE USER
    # =========================

    def save_user(self):

        username = self.username_input.text().strip()

        password = self.password_input.text().strip()

        fullname = self.fullname_input.text().strip()

        phone = self.phone_input.text().strip()

        if not username or not password:

            QMessageBox.warning(

                self,

                "Error",

                "Completa usuario y contraseña"
            )

            return

        mountpoints = []

        if self.mp1.isChecked():

            mountpoints.append(
                "GSI_IGM2024"
            )

        if self.mp2.isChecked():

            mountpoints.append(
                "GSI_IGM2010"
            )

        if self.mp3.isChecked():

            mountpoints.append(
                "GSI_INRA"
            )

        mountpoints = ",".join(
            mountpoints
        )

        expire_date = self.expire_date.date()

        expire_date = expire_date.toString(
            "yyyy-MM-dd"
        )

        try:

            create_user(

                username,

                password,

                mountpoints,

                expire_date,

                fullname,

                phone
            )

            QMessageBox.information(

                self,

                "Correcto",

                "Usuario creado correctamente"
            )

            # LIMPIAR FORMULARIO

            self.username_input.clear()

            self.password_input.clear()

            self.fullname_input.clear()

            self.phone_input.clear()

            self.mp1.setChecked(False)

            self.mp2.setChecked(False)

            self.mp3.setChecked(False)

            self.expire_date.setDate(
                QDate.currentDate()
            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Error",

                str(e)
            )