from PyQt5 import QtWidgets
from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5 import QtGui
from Change import Change
import platform
import ctypes
import 资源_rc


directory = []
change = Change()
class myWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton_2.clicked.connect(self.button2Clicked)


    def buttonClicked(self):
        global directory
        directory = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                           "getOpenFileNames", "./",
                                                           "All Files (*);;Text Files (*.txt)")
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        for i in range(len(directory[0])):
            cursor = self.textBrowser.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(str(i+1)+"、 "+directory[0][i])
            cursor.insertText("\n")
            self.textBrowser.setTextCursor(cursor)
            self.textBrowser.ensureCursorVisible()

    def button2Clicked(self):
        self.textBrowser_2.clear()
        QApplication.processEvents()
        if len(directory)==0:
            self.textBrowser_2.setText("未选择文件")
        for i in range(len(directory[0])):
            change.changeOneFile(directory[0][i])
            cursor = self.textBrowser_2.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(str(i+1)+"、 "+directory[0][i]+"转换完成")
            cursor.insertText("\n")
            self.textBrowser_2.setTextCursor(cursor)
            self.textBrowser_2.ensureCursorVisible()
            QApplication.processEvents()


if __name__ == '__main__':
    if platform.system().lower() =='windows':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/pictures/d.png'))
    ui = myWindow()
    ui.show()
    sys.exit(app.exec_())

