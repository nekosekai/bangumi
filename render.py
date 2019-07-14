# coding:utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import qtawesome
import crawler


class Bangumi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.Magnet = Magnet()
        self.setUi()

    def setUi(self):
        self.setFixedSize(700, 400)
        self.bangumi_widget = QtWidgets.QWidget()
        self.bangumi_layout = QtWidgets.QGridLayout()
        self.bangumi_widget.setLayout(self.bangumi_layout)

        self.bangumi_information_widget = QtWidgets.QWidget()
        self.bangumi_information_widget.setObjectName('bangumi_information_widget')
        self.bangumi_information_layout = QtWidgets.QGridLayout()
        self.bangumi_information_widget.setLayout(self.bangumi_information_layout)
        self.bangumi_operating_widget = QtWidgets.QWidget()
        self.bangumi_operating_widget.setObjectName('bangumi_operating_widget')
        self.bangumi_operating_layout = QtWidgets.QGridLayout()
        self.bangumi_operating_widget.setLayout(self.bangumi_operating_layout)
        self.bangumi_layout.addWidget(self.bangumi_information_widget, 0, 0, 10, 9)
        self.bangumi_layout.addWidget(self.bangumi_operating_widget, 0, 9, 10, 1)

        self.search_bar_widget = QtWidgets.QWidget()
        self.search_bar_layout = QtWidgets.QGridLayout()
        self.search_bar_widget.setLayout(self.search_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + 'Search  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("輸入動漫名稱檢索")
        self.search_input.setFixedSize(300,15)
        self.search_button = QtWidgets.QPushButton("檢索")
        self.search_button.setFixedSize(200, 15)
        self.search_button.clicked.connect(self.searchBangumi)
        self.search_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.search_bar_layout.addWidget(self.search_input, 0, 1, 1, 5)
        self.search_bar_layout.addWidget(self.search_button, 0, 5, 1, 3)
        self.search_bar_layout.setSpacing(0)
        self.bangumi_information_layout.addWidget(self.search_bar_widget, 0, 0, 1, 9)

        self.crawler_result_widget = QtWidgets.QWidget()
        self.crawler_result_layout = QtWidgets.QGridLayout()
        self.information_talbe = QtWidgets.QTableWidget()
        self.information_talbe.setRowCount(0)
        self.information_talbe.setColumnCount(2)
        self.information_talbe.horizontalHeader().resizeSection(0, 560)
        self.information_talbe.setColumnHidden(1, True)
        self.information_talbe.verticalHeader().setHidden(True)
        self.information_talbe.horizontalHeader().setHidden(True)
        self.information_talbe.verticalScrollBar().setHidden(True)
        self.information_talbe.setShowGrid(False)
        self.renderInfomationTable("")
        self.crawler_result_layout.addWidget(self.information_talbe,0,0,9,9)
        self.crawler_result_widget.setLayout(self.crawler_result_layout)
        self.bangumi_information_layout.addWidget(self.crawler_result_widget, 1, 0, 9, 9)

        self.minimize_button = QtWidgets.QPushButton("")
        self.minimize_button.setFixedSize(15, 15)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.close_button = QtWidgets.QPushButton("")
        self.close_button.setFixedSize(15, 15)
        self.close_button.clicked.connect(self.close)
        self.bangumi_operating_layout.addWidget(self.minimize_button, 0, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.bangumi_operating_layout.addWidget(self.close_button, 0, 2, 1, 1, alignment=QtCore.Qt.AlignTop)


        self.magnet_button = QtWidgets.QPushButton("磁力链")
        self.magnet_button.setObjectName('magnet_button')
        self.magnet_button.setFixedSize(45, 15)
        self.magnet_button.clicked.connect(self.showMagnet)
        self.bangumi_operating_layout.addWidget(self.magnet_button, 1, 0, 1, 2, alignment=QtCore.Qt.AlignTop)

        self.setCentralWidget(self.bangumi_widget)
        self.setWindowOpacity(0.8)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.bangumi_layout.setSpacing(0)


        self.bangumi_information_widget.setStyleSheet('''
                QWidget{
                    color:#232C51;
                    background:white;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                }
            ''')

        self.bangumi_operating_widget.setStyleSheet('''
                QWidget#bangumi_operating_widget{
                    color:#232C51;
                    background:white;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-right:1px solid white;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
                }
            ''')

        self.magnet_button.setStyleSheet('''
               QPushButton{
                    border:none;
                    color:black;
               }
                QPushButton:hover{
                    font-weight:600;
                }
            ''')

        self.minimize_button.setStyleSheet('''
                     QPushButton{
                         background:#6DDF6D;
                         border-radius:5px;
                     }
                     QPushButton:hover{
                         background:green;
                     }
                 ''')

        self.close_button.setStyleSheet('''
                       QPushButton{
                           background:#F76677;
                           border-radius:5px;
                       }
                       QPushButton:hover{
                           background:red;
                       }
                 ''')


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def renderInfomationTable(self,searchName):
        infomationTable = self.information_talbe
        infomationTable.setRowCount(0)
        crawlerResult = crawler.generateUrl(searchName)
        if crawlerResult:
            bangumiList = crawlerResult[0]
            magnetList = crawlerResult[1]
            for index in range(len(bangumiList)):
                bangumiName = bangumiList[index]
                magnet = magnetList[index]
                rowCurrent = infomationTable.rowCount()
                infomationTable.setRowCount(rowCurrent + 1)
                infomationTable.setRowHeight(rowCurrent, 20)
                bangumiItem = QtWidgets.QTableWidgetItem()
                bangumiItem.setText(bangumiName)
                infomationTable.setItem(rowCurrent, 0, bangumiItem)
                magnetItem = QtWidgets.QTableWidgetItem()
                magnetItem.setText(magnet)
                infomationTable.setItem(rowCurrent, 1, magnetItem)

    def searchBangumi(self):
        bangumiName = self.search_input.text()
        self.renderInfomationTable(bangumiName)

    def showMagnet(self):
        infomationTable = self.information_talbe
        rows = infomationTable.rowCount()
        magnetInfo=""
        for index in range(rows):
            magnetInfo = magnetInfo+infomationTable.item(index, 1).text()+"\n"
        self.Magnet.setMagnetInfo(magnetInfo)
        self.Magnet.show()


class Magnet(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUi()

    def setUi(self):
        self.setFixedSize(400, 400)
        self.magnet_widget = QtWidgets.QWidget()
        self.magnet_layout = QtWidgets.QGridLayout()
        self.magnet_widget.setLayout(self.magnet_layout)

        self.magnet_information_widget = QtWidgets.QWidget()
        self.magnet_information_widget.setObjectName('magnet_information_widget')
        self.magnet_information_layout = QtWidgets.QGridLayout()
        self.magnet_information_widget.setLayout(self.magnet_information_layout)
        self.magnet_operating_widget = QtWidgets.QWidget()
        self.magnet_operating_widget.setObjectName('magnet_operating_widget')
        self.magnet_operating_layout = QtWidgets.QGridLayout()
        self.magnet_operating_widget.setLayout(self.magnet_operating_layout)
        self.magnet_layout.addWidget(self.magnet_information_widget, 0, 0, 10, 9)
        self.magnet_layout.addWidget(self.magnet_operating_widget, 0, 9, 10, 1)

        self.magnet_info=QtWidgets.QTextEdit()
        self.magnet_info.setObjectName('magnet_info')
        self.magnet_info.verticalScrollBar().setHidden(True)
        self.magnet_information_layout.addWidget(self.magnet_info)

        self.close_button = QtWidgets.QPushButton("")
        self.close_button.setFixedSize(15, 15)
        self.close_button.clicked.connect(self.close)
        self.magnet_operating_layout.addWidget(self.close_button, 0, 2, 1, 1, alignment=QtCore.Qt.AlignTop)

        self.setCentralWidget(self.magnet_widget)
        self.setWindowOpacity(0.8)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.magnet_layout.setSpacing(0)


        self.magnet_information_widget.setStyleSheet('''
                QWidget{
                    color:#232C51;
                    background:white;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                }
            ''')

        self.magnet_operating_widget.setStyleSheet('''
                QWidget#magnet_operating_widget{
                    color:#232C51;
                    background:white;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-right:1px solid white;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
                }
            ''')

        self.close_button.setStyleSheet('''
                        QPushButton{
                            background:#F76677;
                            border-radius:5px;
                        }
                        QPushButton:hover{
                            background:red;
                        }
                  ''')

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def setMagnetInfo(self,magnet):
        self.magnet_info.setText(magnet)



def main():
    app = QtWidgets.QApplication(sys.argv)
    bangumi = Bangumi()
    bangumi.show()
    sys.exit(app.exec_())
