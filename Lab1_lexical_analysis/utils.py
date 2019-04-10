# -*- coding: utf-8 -*-
# @Time    : 2019-04-03 21:52
# @Author  : Billy-Nie
# @FileName: utils.py
# @E-mail    ：niechenxiHIT@126.com

"""
定义一些在后面的分析中会用到的常数，简单的判断函数什么的
"""

from DFA_convert import DFA_converter

####################
#      常量        #
####################
#运算符
operator = ['+', '-', '*', '=', '<', '>', '&', '|', '~', '^', '!', '(', ')', '[', ']', '{', '}', '%', ';', ',', '#']
#界符
boundary = [',', ';', '[', ']', '(', ')', '{', '}']
#关键字
keywords = [ "auto", "double", "int", "struct", "break", "else", "long", "switch", "case", "enum", "register",
        "typedef", "char", "extern", "return", "union", "const", "float", "short", "unsigned", "continue", "for", "signed", "void",
        "default", "goto", "sizeof", "volatile", "do", "if", "while", "static", "main", "String"]

####################
#    判断函数       #
####################
def isPlusOp(ch):
    #科学计数法中的e和后面的运算符, 数字应该是一个token
    return ch == "e"

def isAlpha(ch):
    """
    判断该小片段是不是标识符或者关键字
    标识符或者关键字只能以a~z或者A~Z或者_开头
    """
    return ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch == '_' )

def isOp(ch):
    '''
    判断该小片段是不是运算符
    '''
    return ch in operator

def isDigit(ch):
    """
    判断是否是数字
    """
    return (ch >= '0' and ch <= '9')

def isKeywords(str):
    """
    判断输入字符串是不是一个合法的关键字
    """
    return str in keywords

def isPlusEqu(ch):
    """
    运算符之后可以加等于
    """
    plusEqu = ['+', '-', '*', '/', '=', '>', '<', '&', '|', '^', '!']
    return ch in plusEqu

def isPlusSame(ch):
    #运算符后可以连一个一模一样的运算符, 例如++, --
    plusSame = ['+', '-', '&', '|', '=', '<', '>']
    return ch in plusSame

def isChar(ch):
    return ch == "'"

def isString(ch):
    return ch == '"'

#####################
#       DFA         #
#####################

digitDFA_path = "DFA/DigitDFA"
charDFA_path = "DFA/charDFA"
stringDFA_path = "DFA/stringDFA"
commentDFA_path = "DFA/commentDFA"
O_H_DFA_path = "DFA/O_H_DFA"


class DigitDFA:
    __digitDFA = None
    __final_state = None
    __digitDFA_path = None


    def __init__(self, digitDFA_path):
        self.__digitDFA_path = digitDFA_path
        self.__digitDFA, self.__final_state = DFA_converter(self.__digitDFA_path).convert()

    def in_digitDFA(self, program_fraction):
        """
        判断输入的程序片段是不是能够被该自动机识别
        :param program_fraction: 该程序片段
        :return: Boolean， True——能够被识别
                           False——不能够被识别
        """
        state = 0 #state表示该自动机的状态
        is_float = False

        for i in range(len(program_fraction)):
            DFA_state = self.__digitDFA[state]
            ch = program_fraction[i]
            if ch == '.' or ch == 'e':
                is_float = True
            if isDigit(ch):
                if "d" in DFA_state:
                    state = DFA_state.index("d")
                else:
                    error_masage = "状态" + str(state) + "不能接受字符" + ch
                    return (False, error_masage)
            elif (ch == 'e' or ch == '.' or ch == '-'):
                if ch in DFA_state:
                    state = DFA_state.index(ch)
                else:
                    error_masage = "状态" + str(state) + "不能接受字符" + ch
                    return (False, error_masage)
            else:
                error_masage = "输入有不合法字符"
                return (False, error_masage) #出现了不合法的字符


        if str(state) in self.__final_state:
            return (True, is_float)
        else:
            error_masage = "自动机停止状态不再最终状态"
            return (False,error_masage)

class CharDFA:
    __charDFA = None
    __final_state = None
    __charDFA_path = None

    def __init__(self, charDFA_path):
        self.__charDFA_path = charDFA_path
        self.__charDFA, self.__final_state = DFA_converter(self.__charDFA_path).convert()

    def in_charDFA(self, program_fraction):
        state = 0

        for i in range(len(program_fraction)):
            ch = program_fraction[i]
            DFA_state = self.__charDFA[state]

            if ch in DFA_state:
                state = DFA_state.index(ch)
            elif "a" in DFA_state:
                state = 2
            else:
                error_masage = "状态" + str(state) + "不能接受字符" + ch
                return (False, error_masage)

        if str(state) in self.__final_state:
            return (True, None)
        else:
            error_masage = "自动机停止状态不再最终状态"
            return (False, error_masage)

class StringDFA:
    __stringDFA = None
    __final_state = None
    __charDFA_path = None

    def __init__(self, stringDFA):
        self.__stringDFA = stringDFA
        self.__stringDFA, self.__final_state = DFA_converter(stringDFA_path).convert()

    def in_stringDFA(self, program_fraction):
        state = 0

        for i in range(len(program_fraction)):
            ch = program_fraction[i]
            DFA_state = self.__stringDFA[state]

            if ch in DFA_state:
                state = DFA_state.index(ch)
            elif "a" in DFA_state and ch != "\"":
                state = 1
            else:
                error_masage = "状态" + str(state) + "不能接受字符" + ch
                return (False, error_masage)

        if str(state) in self.__final_state:
            return (True, None)
        else:
            error_masage = "自动机停止状态不再最终状态"
            return (False, error_masage)

class CommentDFA:
    __commentDFA = None
    __final_state = None
    __commentDFA_path = None

    def __init__(self, commentDFA_path):
        self.__commentDFA_path = commentDFA_path
        self.__commentDFA, self.__final_state = DFA_converter(commentDFA_path).convert()

    def in_commentDFA(self, program_fraction):
        state = 0

        for i in range(len(program_fraction)):
            ch = program_fraction[i]
            DFA_state = self.__commentDFA[state]

            if ch in DFA_state and ch != "c":
                state = DFA_state.index(ch)
            elif "a" in DFA_state and ch not in ["/", "*"]:
                state = DFA_state.index("a")
            elif "b" in DFA_state and ch != "/" and ch != "\n":
                state = DFA_state.index("b")
            elif "c" in DFA_state and ch == "\n":
                state = DFA_state.index("c")
            else:
                error_masage = "状态" + str(state) + "不能接受字符" + ch
                return (False, error_masage)

        if str(state) in self.__final_state:
            return (True, None)
        else:
            error_masage = "自动机停止状态不再最终状态"
            return (False, error_masage)

class O_H_DFA:
    __O_H_DFA = None
    __O_H_DFA_path = None
    __final_state = None

    def __init__(self, O_H_state):
        self.__O_H_DFA_path = O_H_DFA_path
        self.__O_H_DFA, self.__final_state = DFA_converter(O_H_DFA_path).convert()

    def in_O_H_DFA(self, program_fraction):
        state = 0
        is_octal = False

        for i in range(len(program_fraction)):
            ch = program_fraction[i]
            DFA_state = self.__O_H_DFA[state]
            if state == 2:
                is_octal = True

            if ch in DFA_state:
                state = DFA_state.index(ch)
            elif "a" in DFA_state and ch >= "1" and ch <= "7":
                state = DFA_state.index("a")
            elif "b" in DFA_state and ch >= "0" and ch <= "7":
                state = DFA_state.index("b")
            elif "c" in DFA_state and ((ch >= "1" and ch <= "9") or (ch >= "a" and ch <= "f")):
                state = DFA_state.index("c")
            elif "d" in DFA_state and ((ch >= "0" and ch <= "9") or (ch >= "a" and ch <= "f")):
                state = DFA_state.index("d")
            else:
                error_masage = "状态" + str(state) + "不能接受字符" + ch
                return (False, error_masage, is_octal)

        if str(state) in self.__final_state:
            return (True, None ,is_octal)
        else:
            error_masage = "自动机停止状态不再最终状态"
            return (False, error_masage, is_octal)

digitDFA = DigitDFA(digitDFA_path)
charDFA = CharDFA(charDFA_path)
stringDFA = StringDFA(stringDFA_path)
commentDFA = CommentDFA(commentDFA_path)
o_H_DFA = O_H_DFA(O_H_DFA_path)