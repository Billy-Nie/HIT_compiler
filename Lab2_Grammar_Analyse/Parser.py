# -*- coding: utf-8 -*-
# @Time    : 2019-04-20 15:18
# @Author  : Billy-Nie
# @FileName: Parser.py
# @E-mail    ：niechenxiHIT@126.com

from Stack import Stack
from string import digits
from latex_analyse.Latex import Latex_analyse_main
from Grammar_Analyse import Grammar_Analyser
from treelib import Node, Tree

def generate_parser_tree(tree_input_path):
    def find_parent(node_name, tmp2):
        for i in range(len(rights_l) - 1, -1, -1): #倒着找
            for j in range(tmp2, -1, -1):
                if node_name + str(j) in rights_l[i]:
                    return node_name+str(j)
        return None

    remove_digits = str.maketrans('', '', digits)

    parser_tree = Tree()
    file = open(tree_input_path)
    left_l = []
    rights_l = []
    tmp = 0 # 只是为了让每一个的标识符不一样
    for line in file.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        left = line.split("->")[0]
        left_l.append(left)

        left_parent_node = find_parent(left, tmp - 1)
        rights = line.split("->")[1]
        new_rights = []
        for right in rights.split(" "):
            if right != "":
                new_rights.append(right + str(tmp))
                tmp += 1
        #print(new_rights)
        rights_l.append(new_rights)
        if left_parent_node == None:
            parser_tree.create_node(left, "root")
            for i in range(len(new_rights)):
                parser_tree.create_node(new_rights[i].translate(remove_digits), new_rights[i], parent="root")
            #parser_tree.show()
        else:
            for i in range(len(new_rights)):
                parser_tree.create_node(new_rights[i].translate(remove_digits), new_rights[i], parent=left_parent_node)
    parser_tree.show()
    file.close()



def LL_1_Analyse(input_list, analyse_table_path, grammar_Analyse, line_number_l):
    tree_input_file = open("file/tree_input.txt", "w")
    error_l = [] #存储打印出来的错误信息
    production_l = [] #存储打印出来的产生式
    input_list.append("#") #添上标记为输入尾巴的井号
    stack = Stack()
    #初始符号压入栈
    stack.push("@") #为了避免混淆, 初始符号从ppt里面的$改为了这里的@
    file = open(analyse_table_path, "r")
    line = file.readline()
    hash_key_index = line.index("#")
    stack.push(line[:hash_key_index])
    file.close()

    X = stack.top()
    ip = 0

    def search_analyse_table(stack_top,ip):
        file = open(analyse_table_path, "r")
        for line in file.readlines():
            if stack_top + "#" + input_list[ip] == line[0:line.index("-")].strip():
                return (True, line)
        file.close()
        return (False, None)

    while(X != "@"):
        if X == input_list[ip]:
            stack.pop()
            ip += 1
        #栈顶终结符和输入符号不匹配, 弹出栈顶的终结符
        #TODO: 打印错误信息和行号
        elif X in grammar_Analyse.get_terminals():
            print(str(line_number_l[ip]) + ":栈顶终结符和输入符号不匹配, 弹出栈顶终结符" + stack.top())
            error_l.append(str(line_number_l[ip]) + ":栈顶终结符和输入符号不匹配, 弹出栈顶终结符" + stack.top())
            stack.pop()

        else:
            search_result, line = search_analyse_table(X, ip)
            #TODO: ;没有GUI
            if search_result:
                if line[-1] == "\n":
                    line = line[:-1]
                if "synch" not in line:
                    arrow_index = line.index("-")
                    hash_key = line.index("#")
                    line = line[:hash_key] + line[arrow_index:]
                    print(line)
                    tree_input_file.write(line + "\n")
                    production_l.append(line)
                    stack.pop()
                    line_right = line[line.index(">") + 1 :].strip()
                    rights = line_right.split(" ")
                    if rights[0] != "$":
                        for i in range(len(rights) - 1, -1, -1):
                            stack.push(rights[i])
                else:
                    #TODO: 打印错误信息和行号
                    #M<A,a>是synch, 弹出栈顶的非终结符A并继续
                    print(str(line_number_l[ip]) + ":弹出栈顶终结符" + stack.top())
                    error_l.append(str(line_number_l[ip]) + ":弹出栈顶终结符" + stack.top())
                    stack.pop()
            else:
                #M<A,a>是空, 表示检测到错误, 忽略输入符号a
                #TODO: 没有GUI
                print(str(line_number_l[ip]) + ": 忽略" + input_list[ip])
                error_l.append(str(line_number_l[ip]) + ": 忽略" + input_list[ip])
                ip += 1
        X = stack.top()
    return error_l, production_l




if __name__ == "__main__":
    _,_,token = Latex_analyse_main("file/test")
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
    # print(line_number_l)
    # print(token_l)
    grammar_analyser = Grammar_Analyser()
    error_l, production_l = LL_1_Analyse(token_l, "file/Analyse_table.txt", grammar_analyser, line_number_l)


generate_parser_tree("file/tree_input.txt")