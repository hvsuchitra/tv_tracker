import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGridLayout, QLineEdit, QLabel, QMenu, \
    QSpacerItem, QSizePolicy
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QFont

os.chdir(sys.path[0])
sys.path.append('../')

from screens.sign_up import SignUp
from screens.reset_password import ResetPassword
from screens.home_page import Home
from common.resources.db.users import User, Session
from common.utils.utils import get_path, ClickableLabel
from utils.session import session_scope

get_path('cache', False).mkdir(exist_ok=True, parents=True)


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.sign_up_sub_window = SignUp(self.pos(), self)
        self.reset_password_sub_window = ResetPassword(self.pos(), self)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(760, 300, 360, 480)
        self.setWindowTitle('TV Tracker')

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)
        self.setStyleSheet('background-color:#76D7C4')
        self.grid.setAlignment(QtCore.Qt.AlignCenter)

        self.welcome_label = QLabel('TV Tracker', self)
        self.welcome_label.setStyleSheet('color:#E3088D;font-family:Apple Chancery;font-size:25px')
        self.welcome_label.setAlignment(0 | QtCore.Qt.AlignCenter)  # you can "or" flags to get both
        self.grid.addWidget(self.welcome_label, 0, 0, 1, 2)

        blank = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid.addItem(blank)

        self.user_label = QLabel('Username', self)
        self.grid.addWidget(self.user_label, 2, 0, QtCore.Qt.AlignCenter)

        self.password_label = QLabel('Password', self)
        self.grid.addWidget(self.password_label, 3, 0, QtCore.Qt.AlignCenter)

        blank = QSpacerItem(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.grid.addItem(blank, 0, 2, 1, 1)

        self.sign_up_button = QPushButton('Sign Up', self)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.grid.addWidget(self.sign_up_button, 5, 0, QtCore.Qt.AlignCenter)

        self.login_button = QPushButton('Login', self)
        self.grid.addWidget(self.login_button, 5, 1, QtCore.Qt.AlignCenter)
        self.login_button.clicked.connect(self.authenticate)

        self.user_text_field = QLineEdit(self)
        self.user_text_field.returnPressed.connect(self.authenticate)
        self.grid.addWidget(self.user_text_field, 2, 1, QtCore.Qt.AlignCenter)

        self.password_text_field = QLineEdit(self)
        self.password_text_field.setEchoMode(QLineEdit.Password)
        self.password_text_field.returnPressed.connect(self.authenticate)
        self.grid.addWidget(self.password_text_field, 3, 1, QtCore.Qt.AlignCenter)

        self.auth_label = QLabel(self)
        self.grid.addWidget(self.auth_label, 4, 0, 1, 2, QtCore.Qt.AlignCenter)

        blank = QSpacerItem(5, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid.addItem(blank)

        self.forgot_password_label = ClickableLabel('reset_password')
        self.forgot_password_label.setText('Forgot Password?')
        self.forgot_password_label.clicked.connect(self.reset)
        self.grid.addWidget(self.forgot_password_label, 6, 0, 1, 2, QtCore.Qt.AlignCenter)

        menu = QMenu()
        menu.addAction('Exit')
        self.show()

    def authenticate(self):
        with session_scope(Session) as session:
            user = session.query(User).filter_by(username=self.user_text_field.text().strip()).one_or_none()
            if user is not None and user.password == self.password_text_field.text().strip():
                # self.auth_label.setPixmap(QPixmap.fromImage((QImage.fromData(user.pic))))
                self.close()
                self.home = Home(user)
                self.home.show()
            else:
                self.auth_label.setStyleSheet('color:red')
                self.auth_label.setText('Username and Password doesn\'t match')

    def sign_up(self):
        self.sign_up_sub_window.setWindowModality(Qt.ApplicationModal)
        self.sign_up_sub_window.clear()
        self.sign_up_sub_window.show()

    def reset(self):
        self.reset_password_sub_window.setWindowModality(Qt.ApplicationModal)
        self.reset_password_sub_window.clear()
        self.reset_password_sub_window.show()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_path('resources/icons/app.ico')))
    ex = Login()
    app.exec_()


if __name__ == '__main__':
    main()
