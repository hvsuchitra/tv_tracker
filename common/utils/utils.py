import smtplib


def get_binary(src_file):
    with open(src_file, 'rb') as f:
        return f.read()


def send_mail(to, username, password, message_type='account_creation'):
    server = 'smtp.mail.me.com'
    port = 587
    email = 'mailid'
    _password = 'password'

    if message_type == 'account_creation':
        message = f'''Subject: Welcome to TV Tracker
From: TV Tracker Dev<{email}>
To: {to}

Thank You for registering. Your username is {username} and password is {password}.

Have a nice day 0:)'''
    elif message_type == 'password_change':
        message = f'''Subject: TV Track Password Change
From: TV Tracker Dev<{email}>
To: {to}

The password to your TV Tracker account {username} was changed to {password}.

If you have not made this change, reply to this email to deactivate your account.

Have a nice day 0:)'''

    elif message_type == 'reset_password':
        message = f'''Subject: TV Track Password Change
From: TV Tracker Dev<{email}>
To: {to}

The password to your TV Tracker account {username} was reset to {password}.

Use this password the next time to login.

Have a nice day 0:)'''

    with smtplib.SMTP(server, port) as server:
        server.starttls()
        server.login(email, _password)
        server.sendmail(from_addr=email, to_addrs=to, msg=message)


from pathlib import Path


def get_path(path, to_str=True):
    app_root = Path('../common').resolve()
    return f'{app_root / path}' if to_str else app_root / path


from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPainter, QBrush, QColor


def make_trans(image, opaque_factor):
    temp = QImage(image.size(), QImage.Format_ARGB32)
    temp.fill(QtCore.Qt.transparent)

    painter = QPainter(temp)
    painter.setOpacity(opaque_factor)
    painter.drawImage(QtCore.QRect(0, 0, image.width(), image.height()), image)

    return temp


def make_dark(image, dark_factor):
    painter = QPainter(image)
    brush = QBrush(QColor(0, 0, 0, dark_factor))
    painter.setBrush(brush)
    painter.drawRect(0, 0, image.width(), image.height())
    return image


from random import choice
from json import load


def random_thought():
    with open(get_path('resources/misc/quotes.json')) as file_obj:
        random_quote = choice(load(file_obj))
        return random_quote['text'], random_quote['author']


from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from secrets import choice as secret_choice
from random import shuffle, randint


def generate_password():
    characters = [ascii_lowercase, ascii_uppercase, digits, punctuation]

    shuffle(characters)

    random_password = [*map(secret_choice, characters)]
    random_password.extend(secret_choice(secret_choice(characters)) for _ in range(randint(4, 12)))

    shuffle(random_password)

    return ''.join(random_password)


from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class ClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, name=None, src=None):
        super().__init__()
        self.setObjectName(name)
        if name is not None and src is not None:
            if name != 'profile':
                self.setPixmap(QPixmap.fromImage(QImage(get_path(src))).scaled(100, 100, Qt.KeepAspectRatio))
            else:
                self.setPixmap(circle_crop(src).scaled(100, 100, Qt.KeepAspectRatio))

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


class SendMailThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, to, username, password):
        super().__init__()
        self.to = to
        self.username = username
        self.password = password

    def run(self):
        send_mail(self.to, self.username, self.password, self.message_type)


from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QImage, QPainter, QPixmap, QWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


def circle_crop(image):
    size = 100

    image = QImage.fromData(image)
    image.convertToFormat(QImage.Format_ARGB32)

    imgsize = min(image.width(), image.height())
    rect = QRect((image.width() - imgsize) / 2, (image.height() - imgsize) / 2, imgsize, imgsize)
    image = image.copy(rect)

    out_img = QImage(image.size(), QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    brush = QBrush(image)
    painter = QPainter(out_img)
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()

    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    # pm.setDevicePixelRatio(pr)
    # size*=pr
    # pm=pm.scaled(size,size,Qt.KeepAspectRatio,Qt.SmoothTransformation)

    return pm


from PyQt5.QtCore import QTimeLine
from PyQt5.QtWidgets import QCalendarWidget, QGridLayout, QStackedWidget, QTextEdit


class FaderWidget(QWidget):
    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)
        self.pixmap_opacity = 1.0
        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.update()


class StackedWidget(QStackedWidget):
    clicked = pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        self.setEnabled(True)
        self.setObjectName(name)

    def setCurrentIndex(self, index):
        if self.currentIndex() != index:
            self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        super().setCurrentIndex(index)

    def enterEvent(self, event):
        self.setCurrentIndex(1)

    def leaveEvent(self, event):
        self.setCurrentIndex(0)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit(self.objectName())
