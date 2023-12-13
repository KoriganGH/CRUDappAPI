import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView, QSizePolicy, QPushButton, QHBoxLayout, \
    QLabel, QTableWidget, QComboBox, QTextEdit, QFormLayout, QLineEdit, QWidget


class PostTab(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QFormLayout()

        self.title_input = QLineEdit()
        self.content_input = QTextEdit()
        self.content_input.setMaximumHeight(100)

        self.author_combo = QComboBox()
        self.refresh_authors()

        self.posts_table = QTableWidget()
        self.posts_table.setColumnCount(4)
        self.posts_table.setHorizontalHeaderLabels(['ID', 'Title', 'Content', 'Author ID'])

        self.refresh_posts()

        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Content:", self.content_input)
        self.layout.addRow("Author:", self.author_combo)
        self.layout.addRow(QLabel())
        self.layout.addRow("Posts:", self.posts_table)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Post")
        self.add_button.clicked.connect(self.add_post)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_posts)

        self.update_button = QPushButton("Update Post")
        self.update_button.clicked.connect(self.update_post)

        self.delete_button = QPushButton("Delete Post")
        self.delete_button.clicked.connect(self.delete_post)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addRow(button_layout)

        self.setLayout(self.layout)

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.posts_table.setSizePolicy(size_policy)
        self.posts_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.posts_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.posts_table.itemClicked.connect(self.select_post)
    def select_post(self, item):
        row = item.row()
        self.title_input.setText(self.posts_table.item(row, 1).text())
        self.content_input.setPlainText(self.posts_table.item(row, 2).text())

        author_id = int(self.posts_table.item(row, 3).text())

        author_index = self.author_combo.findData(author_id, Qt.UserRole)

        if author_index >= 0:
            self.author_combo.setCurrentIndex(author_index)

    def update_post(self):
        selected_row = self.posts_table.currentRow()

        if selected_row >= 0:
            post_id = int(self.posts_table.item(selected_row, 0).text())
            title = self.title_input.text()
            content = self.content_input.toPlainText()

            if not title or not content:
                return

            selected_author_id = int(self.author_combo.currentText().split(": ")[1].split(")")[0])

            data = {'title': title, 'content': content, 'author': selected_author_id}
            response = requests.put(f"http://127.0.0.1:8000/api/posts/{post_id}/", data=data)

            if response.status_code == 200:
                self.refresh_posts()
                self.title_input.clear()
                self.content_input.clear()
                self.author_combo.setCurrentIndex(-1)
        else:
            QMessageBox.warning(self, "Warning", "Please select a post to update.")

    def delete_post(self):
        selected_row = self.posts_table.currentRow()

        if selected_row >= 0:
            post_id = int(self.posts_table.item(selected_row, 0).text())
            response = requests.delete(f"http://127.0.0.1:8000/api/posts/{post_id}/")

            if response.status_code == 204:
                self.refresh_posts()
                self.title_input.clear()
                self.content_input.clear()
                self.author_combo.setCurrentIndex(-1)
        else:
            QMessageBox.warning(self, "Warning", "Please select a post to delete.")

    def refresh_authors(self):
        response = requests.get("http://127.0.0.1:8000/api/users/")
        users = response.json()

        self.author_combo.clear()
        self.author_combo.addItem("Select Author")

        for user in users:
            item_text = f"{user['name']} (ID: {user['id']})"
            self.author_combo.addItem(item_text, userData=user['id'])

        self.author_combo.setCurrentIndex(-1)

    def refresh_posts(self):
        response = requests.get("http://127.0.0.1:8000/api/posts/")
        posts = response.json()

        self.posts_table.setRowCount(len(posts))

        for row, post in enumerate(posts):
            self.posts_table.setItem(row, 0, QTableWidgetItem(str(post['id'])))
            self.posts_table.setItem(row, 1, QTableWidgetItem(post['title']))
            self.posts_table.setItem(row, 2, QTableWidgetItem(post['content']))
            self.posts_table.setItem(row, 3, QTableWidgetItem(str(post['author'])))

    def add_post(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()

        if not title or not content:
            return

        selected_author_id = int(self.author_combo.currentText().split(": ")[1].split(")")[0])

        data = {'title': title, 'content': content, 'author': selected_author_id}
        response = requests.post("http://127.0.0.1:8000/api/posts/", data=data)

        if response.status_code == 201:
            self.refresh_posts()
            self.title_input.clear()
            self.content_input.clear()
            self.author_combo.setCurrentIndex(-1)