import sys
import re
from pathlib import Path

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, QRegExp
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QMessageBox, QDialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator, QPalette

from common.resources.db.users import User, engine, Session
from common.utils.utils import get_binary, send_mail, SendMailThread, generate_password
from utils.session import session_scope


class ResetPassword(QMainWindow):
    def __init__(self, main_window_pos, parent):
        super().__init__(parent)
        self.main_window_pos = main_window_pos

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry((self.main_window_pos.x() + (self.main_window_pos.x() // 25)),
                         (self.main_window_pos.y() + (self.main_window_pos.y() // 2)), 300, 250)
        self.setWindowTitle('Forgot Password')

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        self.grid = QGridLayout()
        main_widget.setLayout(self.grid)
        self.grid.setSpacing(10)

        self.user_label = QLabel('Username', self)
        self.grid.addWidget(self.user_label, 0, 0, QtCore.Qt.AlignCenter)

        self.user_text_field = QLineEdit(self)
        self.user_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.user_text_field, 0, 1, QtCore.Qt.AlignCenter)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.setDisabled(True)
        self.reset_button.clicked.connect(self.reset)
        self.grid.addWidget(self.reset_button, 1, 0, 1, 2, QtCore.Qt.AlignCenter)

    def clear(self):
        self.user_text_field.clear()

    def validate(self):
        if self.user_text_field.text():
            self.reset_button.setDisabled(False)
        else:
            self.reset_button.setDisabled(True)

    def reset(self):
        self.op_pop_up = QMessageBox(self)
        username = self.user_text_field.text().strip()
        with session_scope(Session) as session:
            user = session.query(User).filter_by(username=username).one_or_none()
            if user is not None:
                random_password = generate_password()
                user.password = random_password
                self.op_pop_up.setIcon(QMessageBox.Information)
                self.op_pop_up.setText('Yay!')
                self.op_pop_up.setInformativeText(f'You will receive an e-mail with a new password.')
                self.send_mail_thread = SendMailThread(user.email, user.username, user.password)
                self.send_mail_thread.message_type = 'reset_password'
                self.send_mail_thread.start()
            else:
                self.op_pop_up.setIcon(QMessageBox.Warning)
                self.op_pop_up.setText('Ohh No!')
                self.op_pop_up.setInformativeText(f'Account with  username {username} does not exist.')

        self.op_pop_up.exec_()
        self.reset_button.setDisabled(True)
