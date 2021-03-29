import sys

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, QRegExp, Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QMessageBox, QToolBar, QAction, QToolButton, QScrollArea, QVBoxLayout
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator, QPalette, QPixmap, QImage, QColor

from common.utils.utils import get_path, random_thought, ClickableLabel, circle_crop
from utils.session import session_scope
from common.resources.db.users import User, engine, Session

from screens.profile import Profile
from screens.about import About
from screens.search import Search


class Home(QWidget):
    def __init__(self, cur_user):
        super().__init__()
        self.cur_user = cur_user
        self.init_UI()

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(760, 300, 360, 480)
        self.setWindowTitle(f'Welcome to TV Tracker {self.cur_user.username}')

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)

        self.home_label = ClickableLabel('home', 'resources/icons/home.png')
        # self.home_label.setPixmap(QPixmap.fromImage(QImage(get_path('resources/icons/home.png'))).scaled(100,100,Qt.KeepAspectRatio))
        self.home_label.setToolTip('Home')
        self.home_label.clicked.connect(self.open_window)
        self.grid.addWidget(self.home_label, 0, 0, Qt.AlignCenter)

        self.search_label = ClickableLabel('search', 'resources/icons/tv.png')
        # self.search_label.setPixmap(QPixmap.fromImage(QImage(get_path('resources/icons/tv.png'))).scaled(100,100,Qt.KeepAspectRatio))
        self.search_label.setToolTip('Search')
        self.search_label.clicked.connect(self.open_window)
        self.grid.addWidget(self.search_label, 1, 0, Qt.AlignCenter)

        self.profile_label = ClickableLabel('profile', self.cur_user.pic)
        # self.profile_label.setPixmap(QPixmap.fromImage((QImage.fromData(self.cur_user.pic))).scaled(100,100,Qt.KeepAspectRatio))
        self.profile_label.setToolTip('Profile')
        self.profile_label.clicked.connect(self.open_window)
        self.grid.addWidget(self.profile_label, 2, 0, Qt.AlignCenter)

        self.about_label = ClickableLabel('about', 'resources/icons/about.png')
        # self.about_label.setPixmap(QPixmap.fromImage((QImage(get_path('resources/icons/about.png')))).scaled(100,100,Qt.KeepAspectRatio))
        self.about_label.setToolTip('About')
        self.about_label.clicked.connect(self.open_window)
        self.grid.addWidget(self.about_label, 3, 0, Qt.AlignCenter)

        self.quit_label = ClickableLabel('quit', 'resources/icons/exit.png')
        # self.quit_label.setPixmap(QPixmap.fromImage((QImage(get_path('resources/icons/about.png')))).scaled(100,100,Qt.KeepAspectRatio))
        self.quit_label.setToolTip('Quit!')
        self.quit_label.clicked.connect(self.close)
        self.grid.addWidget(self.quit_label, 4, 0, Qt.AlignCenter)

        self.profile = Profile(self.pos(), self.cur_user)
        self.about = About(self.pos())
        self.search = Search(self.pos(), self.cur_user)

    # self.show()

    def open_window(self):
        option = self.sender().objectName()
        if option == 'profile':
            sub_window = self.profile
            self.profile.clear()
        elif option == 'about':
            sub_window = self.about
            quote, author = random_thought()
            self.about.quote_label.setText(f'{author} said "{quote}"')
        elif option == 'search':
            sub_window = self.search
        elif option == 'home':
            sub_window = self.home

        sub_window.setWindowModality(Qt.ApplicationModal)
        sub_window.show()
