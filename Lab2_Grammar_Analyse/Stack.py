# -*- coding: utf-8 -*-
# @Time    : 2019-04-20 16:08
# @Author  : Billy-Nie
# @FileName: Stack.py
# @E-mail    ：niechenxiHIT@126.com

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[-1]

    def size(self):
        return len(self.items)
