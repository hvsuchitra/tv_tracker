import sys

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, QRegExp, Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QMessageBox, QToolBar, QAction, QToolButton, QScrollArea
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator, QPalette, QPixmap, QImage

from common.utils.utils import get_path
from utils.session import session_scope
from common.resources.db.users import User, engine, Session


class Home(QMainWindow):
    def __init__(self, cur_user):
        super().__init__()
        self.cur_user = cur_user
        self.home = QGridLayout()
        self.search = QGridLayout()
        self.profile = QGridLayout()
        self.grid = QGridLayout()

        self.options_bar = QToolBar()
        self.options_bar.setIconSize(QSize(75, 75))
        self.options_bar.setMovable(False)

        self.home_tool_button = QToolButton(self)
        # self.home_tool_button.setCheckable(True)
        self.home_tool_button.setIcon(QIcon(get_path('resources/icons/home.png')))
        self.home_tool_button.setToolTip('Home')
        self.home_tool_button.setObjectName('home')
        self.home_tool_button.clicked.connect(self.show_grid)
        self.options_bar.addWidget(self.home_tool_button)

        self.search_tool_button = QToolButton(self)
        # self.search_tool_button.setCheckable(True)
        self.search_tool_button.setIcon(QIcon(get_path('resources/icons/tv.png')))
        self.search_tool_button.setToolTip('Explore')
        self.search_tool_button.setObjectName('search')
        self.search_tool_button.clicked.connect(self.show_grid)
        self.options_bar.addWidget(self.search_tool_button)

        self.profile_tool_button = QToolButton(self)
        # self.profile_tool_button.setCheckable(True)
        self.profile_tool_button.setIcon(QIcon(QPixmap.fromImage((QImage.fromData(self.cur_user.pic)))))
        self.profile_tool_button.setToolTip('Profile')
        self.profile_tool_button.setObjectName('profile')
        self.profile_tool_button.clicked.connect(self.show_grid)
        self.options_bar.addWidget(self.profile_tool_button)

        label = QLabel('Home', self)
        self.grid.addWidget(label, 0, 0, 1, 5)
        self.home.setObjectName('home')
        label = QLabel('Search', self)
        self.search.addWidget(label, 0, 0, 1, 5)
        self.search.setObjectName('search')
        label = QLabel('Profile', self)
        self.profile.addWidget(label, 0, 0, 1, 5)
        self.profile.setObjectName('profile')

        self.addToolBar(Qt.LeftToolBarArea, self.options_bar)
        self.show()

    def show_grid(self):
        print(self.sender().objectName())
        if self.sender().objectName() == 'home':
            self.setCentralWidget(self.home)

        elif self.sender().objectName() == 'search':
            self.home.setVisible(0)
            self.search.setVisible(1)
            self.profile.setVisible(0)
        elif self.sender().objectName() == 'profile':
            self.home.setVisible(0)
            self.search.setVisible(0)
            self.profile.setVisible(1)
