# -*- coding: utf-8 -*-
# @Time    : 2019-04-19 20:29
# @Author  : Billy-Nie
# @FileName: Production.py
# @E-mail    ：niechenxiHIT@126.com

class Production:
    #初始化select集
    select = []

    def __init__(self, left, right):
        self.__left = left
        self.__right = right

    def return_left(self):
        return self.__left

    def return_right(self):
        return self.__right
