from PySide6.QtWidgets import (

    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QCheckBox,
    QDateEdit,
    QMessageBox,
    QFrame
)

from PySide6.QtCore import Qt, QDate

from PySide6.QtGui import (
    QFont,
    QIcon
)

from utils import resource_path
from database import update_user
from database import delete_user


class EditUserDialog(QDialog):

    def __init__(self, user_data):

        super().__init__()

        self.user_data = user_data

        self.setWindowTitle(
            f"Editar Usuario: {user_data['username']}"
        )

        self.setWindowIcon(
            QIcon(
                resource_path(
                    "assets/icon.ico"
                )
            )
        )

        self.resize(820, 650)

        self.setStyleSheet("""

            QDialog {

                background-color: #0b1220;
            }

            QFrame {

                background-color: #172033;

                border-radius: 18px;

                border: 1px solid #22304a;
            }

            QLabel {

                color: #e2e8f0;

                font-size: 14px;

                font-weight: 600;
            }

            QLineEdit {

                background-color: #243041;

                border: 2px solid #334155;

                border-radius: 12px;

                padding: 12px;

                color: #f8fafc;

                font-size: 14px;
            }

            QLineEdit:focus {

                border: 2px solid #22c55e;
            }

            QLineEdit:disabled {

                background-color: #1e293b;

                color: #94a3b8;
            }

            QCheckBox {

                color: #e2e8f0;

                font-size: 14px;

                spacing: 10px;
            }

            QDateEdit {

                background-color: #243041;

                border: 2px solid #334155;

                border-radius: 12px;

                padding: 12px;

                color: white;

                font-size: 14px;
            }

            QPushButton {

                border: none;

                border-radius: 14px;

                padding: 14px;

                font-size: 14px;

                font-weight: bold;

                color: white;
            }

        """)

        # =========================
        # MAIN LAYOUT
        # =========================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        main_layout.setSpacing(18)

        self.setLayout(main_layout)

        # =========================
        # TITLE
        # =========================

        title = QLabel(
            f"⚙ Editar Usuario: {user_data['username']}"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont("Segoe UI", 22)
        )

        title.setStyleSheet("""

            color: white;

            font-weight: bold;

            padding-bottom: 8px;
        """)

        main_layout.addWidget(title)

        # =========================
        # ACCOUNT CARD
        # =========================

        account_card = QFrame()

        account_layout = QVBoxLayout()

        account_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        account_layout.setSpacing(15)

        account_card.setLayout(
            account_layout
        )

        section_title = QLabel(
            "👤 Datos del Cliente"
        )

        section_title.setStyleSheet("""

            font-size: 18px;

            font-weight: bold;

            color: white;
        """)

        account_layout.addWidget(
            section_title
        )

        # =========================
        # ROW 1
        # =========================

        row1 = QHBoxLayout()

        row1.setSpacing(15)

        # USERNAME

        user_box = QVBoxLayout()

        user_label = QLabel(
            "Usuario"
        )

        self.username_input = QLineEdit()

        self.username_input.setText(
            user_data["username"]
        )

        self.username_input.setDisabled(
            True
        )

        user_box.addWidget(
            user_label
        )

        user_box.addWidget(
            self.username_input
        )

        # PASSWORD

        pass_box = QVBoxLayout()

        pass_label = QLabel(
            "Contraseña"
        )

        self.password_input = QLineEdit()

        self.password_input.setText(
            user_data["password"]
        )

        pass_box.addWidget(
            pass_label
        )

        pass_box.addWidget(
            self.password_input
        )

        row1.addLayout(
            user_box
        )

        row1.addLayout(
            pass_box
        )

        account_layout.addLayout(
            row1
        )

        # =========================
        # ROW 2
        # =========================

        row2 = QHBoxLayout()

        row2.setSpacing(15)

        # FULLNAME

        fullname_box = QVBoxLayout()

        fullname_label = QLabel(
            "Nombre Completo"
        )

        self.fullname_input = QLineEdit()

        self.fullname_input.setText(
            user_data["fullname"]
        )

        fullname_box.addWidget(
            fullname_label
        )

        fullname_box.addWidget(
            self.fullname_input
        )

        # PHONE

        phone_box = QVBoxLayout()

        phone_label = QLabel(
            "Teléfono / Celular"
        )

        self.phone_input = QLineEdit()

        self.phone_input.setText(
            user_data["phone"]
        )

        phone_box.addWidget(
            phone_label
        )

        phone_box.addWidget(
            self.phone_input
        )

        row2.addLayout(
            fullname_box
        )

        row2.addLayout(
            phone_box
        )

        account_layout.addLayout(
            row2
        )

        main_layout.addWidget(
            account_card
        )

        # =========================
        # MOUNTPOINT CARD
        # =========================

        mount_card = QFrame()

        mount_layout = QVBoxLayout()

        mount_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        mount_layout.setSpacing(15)

        mount_card.setLayout(
            mount_layout
        )

        mount_title = QLabel(
            "🛰 Configuración de Mountpoints"
        )

        mount_title.setStyleSheet("""

            font-size: 18px;

            font-weight: bold;

            color: white;
        """)

        mount_layout.addWidget(
            mount_title
        )

        checks_layout = QHBoxLayout()

        self.mp1 = QCheckBox(
            "GSI_IGM2024"
        )

        self.mp2 = QCheckBox(
            "GSI_IGM2010"
        )

        self.mp3 = QCheckBox(
            "GSI_INRA"
        )

        mounts = user_data["mountpoints"]

        if "GSI_IGM2024" in mounts:

            self.mp1.setChecked(True)

        if "GSI_IGM2010" in mounts:

            self.mp2.setChecked(True)

        if "GSI_INRA" in mounts:

            self.mp3.setChecked(True)

        checks_layout.addWidget(self.mp1)

        checks_layout.addWidget(self.mp2)

        checks_layout.addWidget(self.mp3)

        mount_layout.addLayout(
            checks_layout
        )

        main_layout.addWidget(
            mount_card
        )

        # =========================
        # STATUS CARD
        # =========================

        status_card = QFrame()

        status_layout = QHBoxLayout()

        status_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        status_layout.setSpacing(20)

        status_card.setLayout(
            status_layout
        )

        # ACTIVE

        active_box = QVBoxLayout()

        active_label = QLabel(
            "Estado Usuario"
        )

        active_label.setStyleSheet("""

            font-size: 16px;

            font-weight: bold;

            color: white;
        """)

        self.active_check = QCheckBox(
            "Usuario Activo"
        )

        self.active_check.setChecked(
            user_data["active"]
        )

        active_box.addWidget(
            active_label
        )

        active_box.addWidget(
            self.active_check
        )

        # DATE

        date_box = QVBoxLayout()

        date_label = QLabel(
            "Fecha de Expiración"
        )

        date_label.setStyleSheet("""

            font-size: 16px;

            font-weight: bold;

            color: white;
        """)

        self.expire_date = QDateEdit()

        self.expire_date.setCalendarPopup(
            True
        )

        db_date = str(
            user_data["expire_date"]
        )

        qdate = QDate.fromString(
            db_date,
            "yyyy-MM-dd"
        )

        self.expire_date.setDate(
            qdate
        )

        date_box.addWidget(
            date_label
        )

        date_box.addWidget(
            self.expire_date
        )

        status_layout.addLayout(
            active_box
        )

        status_layout.addLayout(
            date_box
        )

        main_layout.addWidget(
            status_card
        )

        # =========================
        # BUTTONS
        # =========================

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch()

        self.save_button = QPushButton(
            "Guardar Cambios"
        )

        self.save_button.setMinimumWidth(
            180
        )

        self.save_button.setStyleSheet("""

            QPushButton {

                background-color: #16a34a;
            }

            QPushButton:hover {

                background-color: #15803d;
            }
        """)

        self.delete_button = QPushButton(
            "Eliminar Usuario"
        )

        self.delete_button.setMinimumWidth(
            180
        )

        self.delete_button.setStyleSheet("""

            QPushButton {

                background-color: #dc2626;
            }

            QPushButton:hover {

                background-color: #b91c1c;
            }
        """)

        buttons_layout.addWidget(
            self.save_button
        )

        buttons_layout.addWidget(
            self.delete_button
        )

        main_layout.addLayout(
            buttons_layout
        )

        # =========================
        # EVENTS
        # =========================

        self.save_button.clicked.connect(
            self.save_user
        )

        self.delete_button.clicked.connect(
            self.remove_user
        )

    # =========================
    # SAVE USER
    # =========================

    def save_user(self):

        username = self.username_input.text()

        password = self.password_input.text()

        fullname = self.fullname_input.text()

        phone = self.phone_input.text()

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

        active = self.active_check.isChecked()

        expire_date = self.expire_date.date()

        expire_date = expire_date.toString(
            "yyyy-MM-dd"
        )

        update_user(

            username,

            password,

            fullname,

            phone,

            mountpoints,

            active,

            expire_date
        )

        QMessageBox.information(

            self,

            "Guardado",

            "Usuario actualizado correctamente"
        )

        self.accept()

    # =========================
    # DELETE USER
    # =========================

    def remove_user(self):

        username = self.username_input.text()

        confirm = QMessageBox.question(

            self,

            "Eliminar",

            f"Eliminar usuario {username}?"
        )

        if confirm == QMessageBox.Yes:

            delete_user(username)

            QMessageBox.information(

                self,

                "Eliminado",

                "Usuario eliminado"
            )

            self.accept()