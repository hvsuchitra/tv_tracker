from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QVBoxLayout
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage

from common.utils.utils import get_binary, get_path


class About(QMainWindow):
    def __init__(self, main_window_pos):
        super().__init__()
        self.main_window_pos = main_window_pos

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(self.main_window_pos.x(), self.main_window_pos.y(), 360, 600)
        # self.setGeometry(760, 300, 360, 600)
        self.setWindowTitle('About')

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        self.grid = QGridLayout()
        main_widget.setLayout(self.grid)
        self.grid.setSpacing(10)

        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(
            QPixmap.fromImage(QImage.fromData(get_binary(get_path('resources/icons/app.ico')))).scaled(200, 200,
                                                                                                       Qt.KeepAspectRatio))
        self.grid.addWidget(self.logo_label, 0, 0, Qt.AlignCenter)

        self.name_label = QLabel('TV Tracker', self)
        self.name_label.setStyleSheet('color:#E3088D;font-family:Apple Chancery;font-size:25px')
        self.grid.addWidget(self.name_label, 2, 0, Qt.AlignCenter)

        self.copyright_label = QLabel('\u00A9' + 'TV Tracker 2020', self)
        self.grid.addWidget(self.copyright_label, 3, 0, Qt.AlignCenter)

        self.feedback_label = QLabel('For Queries (Bugs / Features) undefined_mail@example.com', self)
        # self.feedback_label.setWordWrap(True)
        # self.feedback_label.setFixedWidth(250)
        self.grid.addWidget(self.feedback_label, 4, 0, Qt.AlignCenter)

        self.author_label = QLabel('Me Me Me', self)
        # self.author_label.setWordWrap(True)
        # self.author_label.setFixedWidth(250)
        self.grid.addWidget(self.author_label, 5, 0, Qt.AlignCenter)

        self.quote_label = QLabel(self)
        self.quote_label.setWordWrap(True)
        # self.quote_label.setFixedWidth(250)
        self.grid.addWidget(self.quote_label, 6, 0, Qt.AlignCenter)
