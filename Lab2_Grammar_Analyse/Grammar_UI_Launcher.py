# -*- coding: utf-8 -*-
# @Time    : 2019-04-20 23:39
# @Author  : Billy-Nie
# @FileName: Grammar_UI_Launcher.py
# @E-mail    ：niechenxiHIT@126.com

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from latex_analyse.Latex import Latex_analyse_main
from Grammar_Analyse import Grammar_Analyser
from Parser import LL_1_Analyse
from Latex_UI import Ui_MainWindow

class MainWindowUIClass(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def tokenPrint(self, productions):
        self.tokenBrowser.clear()
        self.tokenBrowser.append("产生式")
        for production in productions:
            self.tokenBrowser.append(production)

    def errorPrint(self, error_l):
        self.errorbrowser.clear()
        for error in error_l:
            self.errorbrowser.append(error)

    # slot
    def ReturnPressed(self):
        self.codeDisplay.clear()
        input_text = self.lineEdit.text()
        file = open(input_text)
        for line in file.readlines():
            if line[-1] == "\n":
                self.codeDisplay.append(line[:-1])
            else:
                self.codeDisplay.append(line)
        _, _, token = Latex_analyse_main(input_text)
        token_l = []
        line_number_l = []

        for i in token:
            tmp = i.split("\t")[1]
            if tmp == "IDN":
                token_l.append("IDN")
            elif tmp == "FLOAT":
                token_l.append("FLOAT")
            elif tmp == "INT10":
                token_l.append("INT10")
            elif tmp == "INT8":
                token_l.append("INT8")
            elif tmp == "INT16":
                token_l.append("INT16")
            elif tmp == "STR":
                token_l.append("STR")
            elif tmp == "CHAR":
                token_l.append("CHAR")
            else:
                token_l.append(i.split("\t")[0])

            line_number_l.append(i.split("\t")[-1])

        grammar_analyser = Grammar_Analyser()
        error_l, production_l = LL_1_Analyse(token_l, "file/Analyse_table.txt", grammar_analyser, line_number_l)
        self.tokenPrint(production_l)
        self.errorPrint(error_l)

    #slot
    def SelectSlot(self):

        changed_code = self.codeDisplay.toPlainText()
        file_path = self.lineEdit.text()

        file = open(file_path, "w+", encoding="gbk")
        file.write(changed_code)
        file.close()

        self.ReturnPressed()

# def Latex_UI_launcher_main():
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = MainWindowUIClass()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())