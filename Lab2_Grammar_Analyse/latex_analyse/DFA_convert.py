# -*- coding: utf-8 -*-
# @Time    : 2019-04-03 22:26
# @Author  : Billy-Nie
# @FileName: DFA_convert.py
# @E-mail    ：niechenxiHIT@126.com

class DFA_converter:
    #将输入的DFA转换表路径转换为DFA
    def __init__(self, filePath):
        '''
        :param filePath: DFA转换表的文件路径, 该文件必须以\t分隔
        '''
        self.__filePath = filePath

    def convert(self):
        file = open(self.__filePath, "r", encoding="gbk")
        lines = file.readlines()
        DFA = []
        final_state = []
        for line in lines:
            if "#接受状态:" in line:
                final_state = line[6:-1].split("\t")
            if line[0] == '#' or line[0] == '\t':
                continue
            line = line.replace('\t', '')
            line = line.replace('\n', '')
            DFA.append(line[1:])
        return DFA, final_state