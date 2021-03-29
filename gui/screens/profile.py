import re

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QVBoxLayout, QMessageBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage, QPalette

from common.resources.db.users import User, engine, Session
from common.utils.utils import get_binary, get_path, send_mail, SendMailThread
from utils.session import session_scope


class Profile(QMainWindow):
    def __init__(self, main_window_pos, cur_user):
        super().__init__()
        self.main_window_pos = main_window_pos
        self.cur_user = cur_user
        self.pic_dir = self.cur_user.pic
        self.init_UI()

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(self.main_window_pos.x(), (self.main_window_pos.y() + (self.main_window_pos.y() // 2)), 300,
                         250)
        self.setWindowTitle('Profile Settings')

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        self.grid = QGridLayout()
        main_widget.setLayout(self.grid)
        self.grid.setSpacing(10)

        self.user_label = QLabel('Username', self)
        self.grid.addWidget(self.user_label, 0, 0, QtCore.Qt.AlignCenter)

        self.user_text_label = QLabel(self)
        self.user_text_label.setText(self.cur_user.username)
        self.grid.addWidget(self.user_text_label, 0, 1, QtCore.Qt.AlignCenter)

        self.email_label = QLabel('Email', self)
        self.grid.addWidget(self.email_label, 1, 0, QtCore.Qt.AlignCenter)

        self.email_text_label = QLabel(self)
        self.email_text_label.setText(self.cur_user.email)
        self.grid.addWidget(self.email_text_label, 1, 1, QtCore.Qt.AlignCenter)

        self.type_label = QLabel('Type', self)
        self.grid.addWidget(self.type_label, 2, 0, QtCore.Qt.AlignCenter)

        self.type_text_label = QLabel(self)
        self.type_text_label.setText(self.cur_user.role)
        self.grid.addWidget(self.type_text_label, 2, 1, QtCore.Qt.AlignCenter)

        self.old_password_label = QLabel('Old Password', self)
        self.grid.addWidget(self.old_password_label, 3, 0, QtCore.Qt.AlignCenter)

        self.new_password_label = QLabel('New Password', self)
        self.grid.addWidget(self.new_password_label, 4, 0, QtCore.Qt.AlignCenter)

        self.confirm_password_label = QLabel('Confirm New Password', self)
        self.grid.addWidget(self.confirm_password_label, 5, 0, QtCore.Qt.AlignCenter)

        self.old_password_text_field = QLineEdit(self)
        self.old_password_text_field.setObjectName('old_password')
        self.old_password_text_field.setEchoMode(QLineEdit.Password)
        self.old_password_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.old_password_text_field, 3, 1, QtCore.Qt.AlignCenter)

        self.new_password_text_field = QLineEdit(self)
        self.new_password_text_field.setObjectName('password')
        self.new_password_text_field.setEchoMode(QLineEdit.Password)
        self.new_password_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.new_password_text_field, 4, 1, QtCore.Qt.AlignCenter)

        self.confirm_password_text_field = QLineEdit(self)
        self.confirm_password_text_field.setObjectName('confrim_password')
        self.confirm_password_text_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_text_field.textEdited.connect(self.validate)
        self.grid.addWidget(self.confirm_password_text_field, 5, 1, QtCore.Qt.AlignCenter)

        self.browse_button = QPushButton('Change Profile Pic', self)
        self.browse_button.clicked.connect(self.browse)
        self.grid.addWidget(self.browse_button, 8, 0)

        self.remove_pic_button = QPushButton('Remove Profile Pic', self)
        self.remove_pic_button.clicked.connect(self.remove)
        self.grid.addWidget(self.remove_pic_button, 8, 1)

        self.valid_password_label = QLabel('Password Strength', self)
        self.valid_password_label.setStyleSheet('color:red')
        self.grid.addWidget(self.valid_password_label, 6, 0, QtCore.Qt.AlignCenter)

        self.match_password_label = QLabel('Passwords Match', self)
        self.match_password_label.setStyleSheet('color:red')
        self.grid.addWidget(self.match_password_label, 6, 1, QtCore.Qt.AlignCenter)

        self.change_password_button = QPushButton('Change Password', self)
        self.change_password_button.setDisabled(True)
        self.change_password_button.clicked.connect(lambda x: self.update('password'))
        self.grid.addWidget(self.change_password_button, 7, 0, 1, 2, QtCore.Qt.AlignCenter)

        self.inputs = (self.old_password_text_field, self.confirm_password_text_field, self.new_password_text_field)

    def clear(self):
        for field in self.inputs:
            field.clear()

    def browse(self):
        self.pic_dir = \
            QFileDialog.getOpenFileName(self, "Select Profile Picture", '.', 'Image Files (*.jpg *.jpeg *.png)')[0]
        # self.pic_dir=get_binary(self.pic_dir) if self.pic_dir else self.cur_user.pic
        if self.pic_dir:
            self.pic_dir = get_binary(self.pic_dir)
            self.update('image')
        else:
            self.pic_dir = self.cur_user.pic

    def remove(self):
        self.pic_dir = get_binary(get_path('resources/icons/default_av.png'))
        self.update('image')

    def validate(self):
        sender = self.sender().objectName()

        if sender == 'password':
            match = re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", self.sender().text())
            self.valid_password_label.setStyleSheet(f'color:{"green" if match else "red"}')

        elif sender == 'confrim_password':
            self.match_password_label.setStyleSheet(
                f'color:{"green" if self.sender().text() == self.new_password_text_field.text() else "red"}')

        allow = list(filter(lambda x: x.palette().color(QPalette.WindowText).name() == '#008000',
                            (self.valid_password_label, self.match_password_label)))
        self.change_password_button.setDisabled(False if len(
            allow) == 2 and self.old_password_text_field.text().strip() == self.cur_user.password else True)

    def update(self, from_):
        # picture changed only on restart, find a way
        self.op_pop_up = QMessageBox(self)
        with session_scope(Session) as session:
            existing_user = session.query(User).filter_by(username=self.user_text_label.text()).one_or_none()
            if from_ == 'image':
                existing_user.pic = self.pic_dir
            elif from_ == 'password':
                existing_user.password = self.new_password_text_field.text()
                self.send_mail_thread = SendMailThread(existing_user.email, existing_user.username,
                                                       existing_user.password)
                self.send_mail_thread.message_type = 'password_change'
                self.send_mail_thread.start()

        self.cur_user = existing_user
        self.op_pop_up.setIcon(QMessageBox.Information)
        self.op_pop_up.setText('Yay!')
        self.op_pop_up.setInformativeText(f'Account details successfully updated')
        self.op_pop_up.exec_()
