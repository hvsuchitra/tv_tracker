import sys
import re
from pathlib import Path

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, QRegExp
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QMessageBox, QDialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator, QPalette, QImage, QPixmap

from common.resources.db.users import User, engine, Session
from common.utils.utils import get_binary, send_mail, SendMailThread
from utils.session import session_scope


class SignUp(QMainWindow):
    def __init__(self, main_window_pos, parent):
        super().__init__(parent)
        self.main_window_pos = main_window_pos

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry((self.main_window_pos.x() + (self.main_window_pos.x() // 25)),
                         (self.main_window_pos.y() + (self.main_window_pos.y() // 2)), 300, 250)
        self.setWindowTitle('Sign Up for TV Tracker')

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        self.grid = QGridLayout()
        main_widget.setLayout(self.grid)
        self.grid.setSpacing(10)

        self.user_label = QLabel('Username', self)
        self.grid.addWidget(self.user_label, 0, 0, QtCore.Qt.AlignCenter)

        self.password_label = QLabel('Password', self)
        self.grid.addWidget(self.password_label, 1, 0, QtCore.Qt.AlignCenter)

        self.confirm_password_label = QLabel('Confirm Password', self)
        self.grid.addWidget(self.confirm_password_label, 2, 0, QtCore.Qt.AlignCenter)

        self.email_label = QLabel('Email', self)
        self.grid.addWidget(self.email_label, 3, 0, QtCore.Qt.AlignCenter)

        self.user_text_field = QLineEdit(self)
        self.user_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.user_text_field, 0, 1, QtCore.Qt.AlignCenter)

        self.password_text_field = QLineEdit(self)
        self.password_text_field.setObjectName('password')
        self.password_text_field.setEchoMode(QLineEdit.Password)
        self.password_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.password_text_field, 1, 1, QtCore.Qt.AlignCenter)

        self.confirm_password_text_field = QLineEdit(self)
        self.confirm_password_text_field.setObjectName('confrim_password')
        self.confirm_password_text_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.confirm_password_text_field, 2, 1, QtCore.Qt.AlignCenter)

        self.email_text_field = QLineEdit(self)
        self.email_text_field.setObjectName('email')
        self.email_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.email_text_field, 3, 1, QtCore.Qt.AlignCenter)

        self.browse_label = QLabel('Optional Profile Pic', self)
        self.grid.addWidget(self.browse_label, 4, 0, QtCore.Qt.AlignCenter)
        # self.browse_label.setAlignment(QtCore.Qt.AlignCenter)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse)
        self.grid.addWidget(self.browse_button, 4, 1)

        self.valid_password_label = QLabel('Password Strength', self)
        self.valid_password_label.setStyleSheet('color:red')
        self.grid.addWidget(self.valid_password_label, 5, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.match_password_label = QLabel('Passwords Match', self)
        self.match_password_label.setStyleSheet('color:red')
        self.grid.addWidget(self.match_password_label, 6, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.valid_email_label = QLabel('Valid Email', self)
        self.valid_email_label.setStyleSheet('color:red')
        self.grid.addWidget(self.valid_email_label, 7, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.create_button = QPushButton('Create', self)
        self.create_button.setDisabled(True)
        self.create_button.clicked.connect(self.sign_up)
        self.grid.addWidget(self.create_button, 8, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.inputs = (
        self.user_text_field, self.password_text_field, self.confirm_password_text_field, self.email_text_field)

    def validate(self):
        sender = self.sender().objectName()

        if sender == 'password':
            match = re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", self.sender().text())
            self.valid_password_label.setStyleSheet(f'color:{"green" if match else "red"}')

        elif sender == 'confrim_password':
            self.match_password_label.setStyleSheet(
                f'color:{"green" if self.sender().text() == self.password_text_field.text() else "red"}')

        elif sender == 'email':
            match = re.search(r"^.+@[^\.].*\.[a-z]{2,}$", self.sender().text())
            self.valid_email_label.setStyleSheet(f'color:{"green" if match else "red"}')

        allow = list(filter(lambda x: x.palette().color(QPalette.WindowText).name() == '#008000',
                            (self.valid_password_label, self.match_password_label, self.valid_email_label)))
        self.create_button.setDisabled(False if len(allow) == 3 and self.user_text_field.text() else True)

    def clear(self):
        for field in self.inputs:
            field.clear()
        self.create_button.setDisabled(True)
        self.valid_password_label.setStyleSheet('color:red')
        self.match_password_label.setStyleSheet('color:red')
        self.valid_email_label.setStyleSheet('color:red')
        self.pic_dir = None

    def browse(self):
        self.pic_dir = \
        QFileDialog.getOpenFileName(self, "Select Profile Picture", '.', 'Image Files (*.jpg *.jpeg *.png)')[0]

    def sign_up(self):
        user = dict(zip(('username', 'password', 'email'), (map(lambda x: x.text().strip(), (
        self.user_text_field, self.password_text_field, self.email_text_field)))))
        self.op_pop_up = QMessageBox(self)
        with session_scope(Session) as session:
            if session.query(User).filter_by(username=user['username']).one_or_none() is None:
                if session.query(User).filter_by(email=user['email']).one_or_none() is None:
                    if self.pic_dir is not None and self.pic_dir:
                        user['pic'] = get_binary(self.pic_dir)
                    new_user = User(**user)
                    session.add(new_user)
                    self.op_pop_up.setIcon(QMessageBox.Information)
                    self.op_pop_up.setText('Yay!')
                    self.op_pop_up.setInformativeText(f'Account with username {user["username"]} successfully created')
                    self.send_mail_thread = SendMailThread(user['email'], user['username'], user['password'])
                    self.send_mail_thread.message_type = 'account_creation'
                    self.send_mail_thread.start()
                else:
                    self.op_pop_up.setIcon(QMessageBox.Warning)
                    self.op_pop_up.setText('Ohh No!')
                    self.op_pop_up.setInformativeText(f'Account with email {user["email"]} already exists.')
            else:
                self.op_pop_up.setIcon(QMessageBox.Warning)
                self.op_pop_up.setText('Ohh No!')
                self.op_pop_up.setInformativeText(f'Account with username {user["username"]} already exists.')

        self.create_button.setDisabled(True)
        self.op_pop_up.exec_()
