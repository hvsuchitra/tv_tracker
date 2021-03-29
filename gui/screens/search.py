import sys
import re
from pathlib import Path

from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal, QRegExp, Qt, QSize, QTimeLine
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QGroupBox, QHBoxLayout, QGridLayout, \
    QFileDialog, QMainWindow, QLineEdit, QLabel, QTableView, QTabWidget, QRadioButton, QFrame, QSystemTrayIcon, QStyle, \
    QMenu, QSpacerItem, QSizePolicy, QMessageBox, QDialog, QScrollArea, QFrame, QVBoxLayout, QStackedWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator, QPalette, QPixmap, QImage, QBrush, QPainter

sys.path.append('../../')

from common.utils.api_utils import search_show, get_image, resource_base_url

from common.utils.utils import get_path, get_binary, make_dark, StackedWidget


class GetImageThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, img_url, stack, show_frame, widget):
        super().__init__()
        self.img_url = img_url
        self.stack = stack
        self.show_frame = show_frame
        self.widget = widget

    def run(self):
        print('running')
        img = get_image(self.img_url)

        pallete = QPalette()
        label = QLabel(self.widget)

        label.setPixmap(QPixmap.fromImage((QImage.fromData(img)).scaled(680 / 2, 1000 / 2, Qt.KeepAspectRatio)))
        self.stack.addWidget(label)

        self.widget.setAutoFillBackground(True)
        pallete.setBrush(QPalette.Background, QBrush(
            QPixmap.fromImage(make_dark(QImage.fromData(img), 160)).scaled(680 / 2, 1000 / 2, Qt.KeepAspectRatio)))
        self.show_frame.setPalette(pallete)


class Search(QMainWindow):
    def __init__(self, main_window_pos, cur_user):
        super().__init__()
        self.cur_user = cur_user
        self.stack_widgets = []
        self.main_window_pos = main_window_pos

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(self.main_window_pos.x(), (self.main_window_pos.y() + (self.main_window_pos.y() // 6)), 360,
                         480)
        self.setWindowTitle('Search')

        self.search_widget = QWidget()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setAlignment(Qt.AlignTop)

        self.search_text_field = QLineEdit(self)
        self.search_text_field.setPlaceholderText('Enter the name of a TV show you want to track')
        self.search_text_field.returnPressed.connect(self.display)

        self.grid.addWidget(self.search_text_field, 0, 0, 1, 3)

        self.search_widget.setLayout(self.grid)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.search_widget)
        self.setCentralWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        self.search_text_field.setText('the mick')

    # self.showFullScreen()
    # self.show()

    def display(self):
        self.setGeometry(180, 25, 1068, 1088)
        for show_frame in self.stack_widgets:
            self.grid.removeWidget(show_frame)
            show_frame.setParent(None)
        self.stack_widgets = []

        row = 0
        col = -1
        for pos_idx, show in enumerate(search_show(self.search_text_field.text().strip())):

            stack = StackedWidget(str(show['id']))

            show_frame = QFrame(self)
            show_frame.setFrameShape(QFrame.StyledPanel)
            show_frame.setFixedSize(680 // 2, 1000 // 2)
            self.stack_widgets.append(stack)

            stack.addWidget(show_frame)

            v_box = QVBoxLayout()

            ####
            scroll_area = QScrollArea()
            scroll_area.setWidget(show_frame)
            # scroll_area.setWidgetResizable(True)
            ###
            # get_image_thread=GetImageThread(show['image'],stack,show_frame,self)
            # get_image_thread.start()

            # show['image']=get_image_thread.img
            show['image'] = get_image(show['image'])  # this is an expensive line

            for key, val in show.items():
                if key == 'image':
                    pallete = QPalette()
                    label = QLabel(self)

                    label.setPixmap(QPixmap.fromImage(
                        (QImage.fromData(show['image'])).scaled(680 / 2, 1000 / 2, Qt.KeepAspectRatio)))
                    stack.addWidget(label)

                    self.setAutoFillBackground(True)
                    pallete.setBrush(QPalette.Background, QBrush(
                        QPixmap.fromImage(make_dark(QImage.fromData(val), 160)).scaled(680 / 2, 1000 / 2,
                                                                                       Qt.KeepAspectRatio)))
                    show_frame.setPalette(pallete)

                # t.setPixmap(QPixmap.fromImage((QImage.fromData(val))).scaled(680/2,1000/2,Qt.KeepAspectRatio))

                if key == 'id':
                    ...
                # add to database?

                else:
                    val_label = QLabel(self)
                    if key == 'seriesName':
                        val_label.setStyleSheet('font-family:Apple Chancery;font-size:30px;color:#f07192')
                        val_label.setText(val)
                    elif key == 'status':
                        if val == 'Ended':
                            val_label.setStyleSheet('font-size:15px;color:#e63749')
                        elif val == 'Continuing':
                            val_label.setStyleSheet('font-size:15px;color:#6dfc93')
                        else:
                            val_label.setStyleSheet('font-size:15px;color:#48f0ad')
                        val_label.setText(f'Status : {val}')
                    elif key == 'overview':
                        if val != 'Not Available' and len(val) > 500:
                            val = val[:500] + '...'
                        val_label.setStyleSheet('font-size:15px;color:white')
                        val_label.setText(val)
                    else:
                        if key == 'network':
                            val_label.setText(f'Network : {val}')
                        elif key == 'firstAired':
                            val_label.setText(f'First Aired : {val}')
                        val_label.setStyleSheet('font-size:15px;color:white')

                    val_label.setWordWrap(True)
                    val_label.setAlignment(Qt.AlignCenter)
                    v_box.addWidget(val_label)

            show_frame.setLayout(v_box)
            stack.addWidget(show_frame)

            row, col = (row + 1, 0) if not pos_idx % 3 else (row, col + 1)

            # stack.installEventFilter(self)

            stack.clicked.connect(lambda: print(self.sender().objectName()))

            self.grid.addWidget(stack, row, col, 1, 1, Qt.AlignCenter)
