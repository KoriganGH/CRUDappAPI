import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QStyleFactory
from qdarkstyle import load_stylesheet_pyqt5
from posts import PostTab
from users import UserTab


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()

        user_tab = UserTab()
        post_tab = PostTab()

        user_tab.user_added.connect(post_tab.refresh_authors)

        self.tabs.addTab(user_tab, "Users")
        self.tabs.addTab(post_tab, "Posts")

        self.setCentralWidget(self.tabs)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Desktop app for API test')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyleSheet(load_stylesheet_pyqt5())
    #app.setStyle(QStyleFactory.create('Fusion'))
    main_app = MainApp()
    sys.exit(app.exec_())
