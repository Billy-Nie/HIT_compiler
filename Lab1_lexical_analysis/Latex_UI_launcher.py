# -*- coding: utf-8 -*-
# @Time    : 2019-04-06 19:28
# @Author  : Billy-Nie
# @FileName: Latex_UI_launcher.py
# @E-mail    ：niechenxiHIT@126.com

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
import UI.Latex_UI as ui
from utils import DigitDFA, CharDFA, StringDFA, CommentDFA, O_H_DFA
from utils import digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA
from Latex import Latex_analyse_main

class MainWindowUIClass(ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def tokenPrint(self, token_l):
        self.tokenBrowser.clear()
        self.tokenBrowser.append("token\t类型\t值\t行号")
        for token in token_l:
            self.tokenBrowser.append(token)

    def characterPrint(self, character_l):
        self.tokenListBrowser.clear()
        self.tokenListBrowser.append("符号表")
        for character in character_l:
            self.tokenListBrowser.append(character)

    def errorPrint(self, error_l):
        self.errorbrowser.clear()
        for error in error_l:
            self.errorbrowser.append(error)

    #slot
    def ReturnPressed(self):
        self.codeDisplay.clear()

        chardfa = None
        commentdfa = None
        digitdfa = None
        o_h_dfa = None
        stringdfa = None
        dfa_l = [False for i in range(5)]
        input_text = self.lineEdit.text()
        if "charDFA".lower() in input_text.lower():
            chardfa = CharDFA(input_text)
            dfa_l[0] = True
        elif "commentDFA".lower() in input_text.lower():
            commentdfa = CommentDFA(input_text)
            dfa_l[1] = True
        elif "DigitDFA".lower() in input_text.lower():
            digitdfa = DigitDFA(input_text)
            dfa_l[2] = True
        elif "O_H_DFA".lower() in input_text.lower():
            o_h_dfa = O_H_DFA(input_text)
            dfa_l[3] = True
        elif "stringDFA".lower() in input_text.lower():
            stringdfa = StringDFA(input_text)
            dfa_l[4] = True
        else:
            file = open(input_text)
            for line in file.readlines():
                if line[-1] == "\n":
                    self.codeDisplay.append(line[:-1])
                else:
                    self.codeDisplay.append(line)
            if False in dfa_l:
                character_table, error_l, token_l = Latex_analyse_main(input_text, digitDFA, charDFA, stringDFA,
                                                                       commentDFA, o_H_DFA)
            else:
                character_table, error_l, token_l = Latex_analyse_main(input_text, digitdfa, chardfa, stringdfa,
                                                                       commentdfa, o_h_dfa)
            self.tokenPrint(token_l)
            self.errorPrint(error_l)
            self.characterPrint(character_table)


    #slot
    def SelectSlot(self):
        # input_text = self.lineEdit.text()
        #
        # character_table, error_l, token_l = Latex_analyse_main(input_text, digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA)
        #
        # self.tokenPrint(token_l)
        # self.errorPrint(error_l)
        # self.characterPrint(character_table)

        changed_code = self.codeDisplay.toPlainText()
        file_path = self.lineEdit.text()

        file = open(file_path, "w+", encoding="gbk")
        file.write(changed_code)
        file.close()

        self.ReturnPressed()








def Latex_UI_launcher_main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

Latex_UI_launcher_main()


