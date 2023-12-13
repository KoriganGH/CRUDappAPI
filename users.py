import requests
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QSizePolicy, QAbstractItemView, QPushButton, QLabel, \
    QHBoxLayout, QTableWidget, QLineEdit, QFormLayout, QWidget


class UserTab(QWidget):
    user_added = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(['ID', 'Username', 'Email'])

        self.refresh_users()

        self.layout.addRow("Username:", self.name_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow(QLabel())
        self.layout.addRow("Users:", self.users_table)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_users)

        self.update_button = QPushButton("Update User")
        self.update_button.clicked.connect(self.update_user)

        self.delete_button = QPushButton("Delete User")
        self.delete_button.clicked.connect(self.delete_user)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addRow(button_layout)
        self.setLayout(self.layout)

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.users_table.setSizePolicy(size_policy)
        self.users_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.users_table.itemClicked.connect(self.select_user)

    def select_user(self, item):
        row = item.row()
        self.name_input.setText(self.users_table.item(row, 1).text())
        self.email_input.setText(self.users_table.item(row, 2).text())

    def update_user(self):
        selected_row = self.users_table.currentRow()

        if selected_row >= 0:
            user_id = int(self.users_table.item(selected_row, 0).text())
            name = self.name_input.text()
            email = self.email_input.text()

            if not name or not email:
                return

            data = {'name': name, 'email': email}
            response = requests.put(f"http://127.0.0.1:8000/api/users/{user_id}/", data=data)

            if response.status_code == 200:
                self.refresh_users()
                self.name_input.clear()
                self.email_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Please select a user to update.")

    def delete_user(self):
        selected_row = self.users_table.currentRow()

        if selected_row >= 0:
            user_id = int(self.users_table.item(selected_row, 0).text())
            response = requests.delete(f"http://127.0.0.1:8000/api/users/{user_id}/")

            if response.status_code == 204:
                self.refresh_users()
                self.name_input.clear()
                self.email_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")

    def refresh_users(self):
        response = requests.get("http://127.0.0.1:8000/api/users/")
        users = response.json()

        self.users_table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['name']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['email']))

    def add_user(self):
        name = self.name_input.text()
        email = self.email_input.text()

        if not name or not email:
            return

        data = {'name': name, 'email': email}
        response = requests.post("http://127.0.0.1:8000/api/users/", data=data)

        if response.status_code == 201:
            self.refresh_users()
            self.name_input.clear()
            self.email_input.clear()
            self.user_added.emit()