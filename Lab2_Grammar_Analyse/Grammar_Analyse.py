# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 08:21
# @Author  : Billy-Nie
# @FileName: Grammar_Analyse.py
# @E-mail    ：niechenxiHIT@126.com

from Production import Production
from copy import deepcopy


class Grammar_Analyser:
    # 产生式集,终结符集,非终结符集,FIRST集,FOLLOW集
    __productions = []
    __terminals = []
    __nonterminals = []
    __firsts = {}
    __follows = {}

    def __init__(self):
        # 从文件中读取产生式
        self.readProductions()
        self.setNonTerminals()
        self.setTerminals()

        #self.outputNonterminals()
        #self.outputTerminals()
        #
        self.getFirst()
        #self.outputFirst()
        self.getFollow()
        #self.outputFollow()
        self.getSelect()
        #self.outputSelect()
        #
        self.create_AnalyseTable()

    def get_terminals(self):
        return deepcopy(self.__terminals)

    #遍历输出Select集
    def outputSelect(self):
        for i in range(len(self.__productions)):
            print("{0} -> ".format(self.__productions[i].return_left()), end="")
            for j in range(len(self.__productions[i].return_right())):
                print("{0} ".format(self.__productions[i].return_right()[j]), end="")

            print("\t\t" + str(self.__productions[i].select))

    #遍历输出first集
    def outputFirst(self):
        for i in self.__firsts.keys():
            print("{0} -> {1}".format(i, self.__firsts[i]))

    #遍历输出follow集
    def outputFollow(self):
        for i in self.__follows.keys():
            print("{0} -> {1}".format(i, self.__follows[i]))

    #遍历production集
    def outputProduction(self):
        for i in range(len(self.__productions)):
            print("{0} -> ".format(self.__productions[i].return_left()), end="")
            for j in range(len(self.__productions[i].return_right())):
                print("{0} ".format(self.__productions[i].return_right()[j]), end="")
            print()

    #遍历非终结符集
    def outputNonterminals(self):
        for i in range(len(self.__nonterminals)):
            print(self.__nonterminals[i])

    #遍历终结符集
    def outputTerminals(self):
        for i in range(len(self.__terminals)):
            print(self.__terminals[i])

    #从文件中读取产生式
    def readProductions(self):
        try:
            file = open("file/grammar.txt")
            for line in file.readlines():
                if line[-1] == "\n":
                    line = line[:-1]
                left = line.split("->")[0].strip()
                right = line.split("->")[1].strip()
                production = Production(left, right.split(" "))
                self.__productions.append(production)
            file.close()
        except Exception:
            print("打开文件时出错")

    #获取非终结符集
    def setNonTerminals(self):
        try:
            file = open("file/grammar.txt")
            for line in file.readlines():
                if line[-1] == "\n":
                    line = line[:-1]
                left = line.split("->")[0].strip()
                if left in self.__nonterminals:
                    continue
                else:
                    self.__nonterminals.append(left)
            file.close()
        except IOError:
            print("打开文件时发生错误")

    #获取终结符集
    def setTerminals(self):
        try:
            file = open("file/grammar.txt")
            for line in file.readlines():
                if line[-1] == "\n":
                    line = line[:-1]
                right = line.split("->")[1].strip()
                for i in right.split(" "):
                    if i in self.__nonterminals or i == "$":
                        continue
                    else:
                        self.__terminals.append(i)
            file.close()
        except IOError:
            print("打开文件时发生错误")

    #判断是否产生空字符$
    def isCanBeNull(self, symbol):
        for i in self.__productions:
            left = i.return_left()
            if left == symbol:
                right = i.return_right()
                if right[0] == "$":
                    return True
        return False

    #获取First集
    def getFirst(self):

        #为所有的非终结符定义一个空的list
        for i in range(len(self.__nonterminals)):
            self.__firsts[self.__nonterminals[i]] = []

        #如果X是一个终结符, 那么first(X) = {X}
        for i in self.__terminals:
            self.__firsts[i] = [i]

        self.__firsts["$"] = ["$"]

        while(True):
            previous_firsts = deepcopy(self.__firsts)

            #遍历每一个产生式
            for i in self.__productions:
                left = i.return_left()
                rights = i.return_right()

                #对于右侧的每一个元素
                for right in rights:
                    if right != "$":
                        for j in self.__firsts[right]:
                            if j in self.__firsts[left]:
                                continue
                            else:
                                self.__firsts[left].append(j)


                    else:
                        if "$" not in self.__firsts[left]:
                            self.__firsts[left].append("$")

                    if self.isCanBeNull(right):
                        continue
                    else:
                        break

            if previous_firsts == self.__firsts:
                 break

    #求一个序列的first集
    def getListFirst(self, list):
        if list != []:
            result = deepcopy(self.__firsts[list[0]])
            for l in range(len(list)):
                if "$" not in self.__firsts[list[l]]:
                    return result
                else:
                    if l != len(list) - 1:
                        for j in self.__firsts[list[l + 1]]:
                            if j not in self.__firsts[list[l]]:
                                result.append(j)
            return result
        else:
            return []



    #获取Follow集
    def getFollow(self):
        #初始化每一个非终结符的terminal集合
        for i in self.__nonterminals:
            self.__follows[i] = []

        #使用#代替ppt算法中的$
        self.__follows[self.__nonterminals[0]].append("#")

        while(True):
            previous_follows = deepcopy(self.__follows)

            #遍历每一个产生式
            for production in self.__productions:
                left = production.return_left()
                rights = production.return_right()

                for right_index in range(len(rights)):
                    right = rights[right_index]
                    #follow集和终结符无关
                    if right in self.__terminals or right == "$":
                        continue
                    #求这个right之后的rights的first集
                    first_after_this_right = self.getListFirst(rights[right_index + 1:])
                    if first_after_this_right != []:
                        #这个right之后的first集中除$外, 都是follow{right}中的部分
                        for i in first_after_this_right:
                            if i not in self.__follows[right] and i != "$":
                                self.__follows[right].append(i)

                    #如果这个是产生式右边的最后一个或者这个right后面的产生式里面有$, 那么Follow{left}中的内容一定会出现在follow{right}中
                    if (right_index == len(rights) - 1) or ("$" in first_after_this_right):
                        for i in self.__follows[left]:
                            if i not in self.__follows[right]:
                                self.__follows[right].append(i)

            if previous_follows == self.__follows:
                break

    #获取select集
    def getSelect(self):
        for production in self.__productions:
            left = production.return_left()
            rights = production.return_right()

            rights_first = self.getListFirst(rights)

            if "$" not in rights_first:
                production.select = deepcopy(rights_first)
            else:
                select = deepcopy(rights_first)
                select.remove("$")
                for i in self.__follows[left]:
                    if i not in select:
                        select.append(i)
                production.select = deepcopy(select)


    #获取分析表
    def create_AnalyseTable(self):
        file_path = "file/Analyse_table.txt"
        file = open(file_path, "w")
        temp = []
        for production in self.__productions:
            line = ""
            left = production.return_left()
            rights = production.return_right()

            line = line + left
            line = line + "#"

            for select_list_item in production.select:
                line = line + str(select_list_item)
                temp.append(line)
                line = line + " ->"

                for right in rights:
                    line = line + " " + str(right)
                line += "\n"
                file.write(line)
                line = ""
                line = line + left
                line = line + "#"

        for production in self.__productions:
            left = production.return_left()
            for follow in self.__follows[left]:
                line2 = ""
                line2 = line2 + left + "#" + follow
                if line2 not in temp:
                    line2 = line2 + "->" + " synch\n"
                    file.write(line2)


        file.close()

