from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, QRegExp, Qt, QSize, QTimeLine
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QMessageBox, QDialog, QScrollArea, QFrame, QVBoxLayout, QStackedWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator, QPalette, QPixmap, QImage, QBrush, QPainter


class Episode(QMainWindow):
    def __init__(self):
        # def __init__(self,main_window_pos,cur_user):
        super().__init__()
        # self.id_=id_
        # self.cur_user=cur_user
        # self.main_window_pos=main_window_pos

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(760, 300, 1000, 1000)
        # self.setGeometry(self.main_window_pos.x(),(self.main_window_pos.y()+(self.main_window_pos.y()//6)),360, 480)
        self.setWindowTitle(f'{1}')  # recieve show name or use api to get that

        self.search_widget = QWidget()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setAlignment(Qt.AlignTop)

        self.show()


app = QApplication([])
ex = Episode()
app.exec_()
