# -*- coding: utf-8 -*-
# @Time    : 2019-04-05 14:35
# @Author  : Billy-Nie
# @FileName: Latex.py
# @E-mail    ：niechenxiHIT@126.com

from utils import DigitDFA, CharDFA, StringDFA, CommentDFA, O_H_DFA
from utils import digitDFA_path, charDFA_path, stringDFA_path, commentDFA_path, O_H_DFA_path
from utils import isAlpha, isOp, isDigit, isChar, isString
from utils import isPlusSame, isPlusEqu, isPlusOp
from utils import boundary, operator, keywords

character_table = [] # 符号表

def token_recognition(token, digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number):
    #关键字和标识符
    if isAlpha(token[0]):
        if token in keywords:
            print(token + "\t<关键字\t" + token + ">\t" + str(line_number))
        else:
            if token not in character_table:
                character_table.append(token)
                print(token + "\t<标识符\t" + token + ">\t" + str(line_number))

    if isOp(token[0]):
        print(token + "\t<运算符\t" + token + ">\t" + str(line_number))

    if isDigit(token[0]):
        digitDFA_result, isfloat = digitDFA.in_digitDFA(token)
        if digitDFA_result:
            if isfloat:
                print(token + "\t<浮点型常量\t" + token + ">\t" + str(line_number))
            else:
                print(token + "\t<整形常量\t" + token + ">\t" + str(line_number))

        o_H_DFA_result, error_message, is_octal = o_H_DFA.in_O_H_DFA(token)
        if o_H_DFA_result:
            if is_octal:
                print(token + "\t<八进制常量\t" + token+ ">\t" + str(line_number))
            else:
                print(token + "\t<十六进制常量\t" + token + ">\t" + str(line_number))

        if not digitDFA_result and not o_H_DFA_result:
            print("错误:在" + str(line_number) + "行, 试图将" + token + "解析为数字型常量发生错误!")

    if isChar(token[0]):
        charDFA_result, error_message = charDFA.in_charDFA(token)

        if charDFA_result:
            print(token + "\t<字符型常量\t" + token + ">\t" + str(line_number))
        else:
            print("错误:在" + str(line_number) + "行, 试图将" + token + "解析为字符型常量发生错误!" )

    if isString(token[0]):
        stringDFA_result, error_message = stringDFA.in_stringDFA(token)

        if stringDFA_result:
            print(token + "\t<字符串常量\t" + token + ">\t" + str(line_number))
        else:
            print("错误:在" + str(line_number) + "行, 试图将" + token + "解析为字符串常量发生错误!")



if __name__ == "__main__":
    ######################
    #       DFA          #
    ######################
    digitDFA = DigitDFA(digitDFA_path)
    charDFA = CharDFA(charDFA_path)
    stringDFA = StringDFA(stringDFA_path)
    commentDFA = CommentDFA(commentDFA_path)
    o_H_DFA = O_H_DFA(O_H_DFA_path)

    #######################
    #      文件操作        #
    #######################

    file = open("test_file/test_file.txt", "r", encoding="gbk")
    line_number = 0
    while True:
        line = file.readline()
        if not line:
            break
        line_number += 1
        program_line = line

        #处理跨行注释
        iscomment = False
        if len(line)>=2 and line[0] == "/" and line[1] == "*" :
            iscomment = True
            if line[-3] != "*" and line[-2] != "/":
                while line and (len(line) < 2 or (line[-3] != "*" and line[-2] != "/")):
                    line = file.readline()
                    program_line = program_line + line
        elif len(line) >= 2 and line[0] == "/" and line[1] == "/":
            iscomment = True
        elif  len(line)>=4 and line[0] == "/":
            iscomment = True

        if iscomment:
            if "nbx" in program_line:
                h = 1
            if program_line[1] != "/":
                comment_true, error_message = commentDFA.in_commentDFA(program_line[:-1]) #跨行注释, 需要删掉最后一行最后面的换行符
            else:
                comment_true, error_message = commentDFA.in_commentDFA(program_line) #单行注释, 最后的换行符是结束的标志, 不能删除
            if comment_true:
                print(program_line.replace("\n", "") + "\t<注释\t"+ program_line.replace("\n", "") + ">\t" + str(line_number))

            if not comment_true:
                print("错误:在" + str(line_number) + "行, 试图将" + program_line.replace("\n", "") + "解析为注释发生错误!")
        else:
            token = ""
            i = 0
            while( i < len(line)):
                if line[i] not in boundary and line[i] not in operator and line[i] != " ":
                    token += line[i]
                else:
                    if token != "":
                        # 不加这一个判断科学计数法里面那个e会被切分成10.23e和-和10三个部分qwq
                        if isPlusOp(line[i -1]) and isDigit(line[i - 2]):
                            token = token + line[i]
                            i += 1
                            while (isDigit(line[i])):
                                token = token + line[i]
                                i += 1
                        token_recognition(token, digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number)
                        token = ""
                    if line[i] != " ":
                        if isPlusSame(line[i]):
                            if (i+1) < len(line) and line[i+1] == line[i]:
                                token_recognition(line[i] * 2, digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number)
                                i += 1
                            else:
                                token_recognition(line[i], digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number)
                        elif isPlusEqu(line[i]):
                            if (i + 1) < len(line) and line[i+1] == "=":
                                token_recognition(line[i] + "=", digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number)
                                i += 1
                            else:
                                token_recognition(line[i], digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number)
                        else:
                            token_recognition(line[i], digitDFA, charDFA, stringDFA, commentDFA, o_H_DFA, line_number)
                i += 1
