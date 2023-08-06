#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pathlib import Path

from openpyxl import load_workbook
from time import perf_counter
import re
from g1879.paths import get_usable_path, make_valid_name
from g1879.xlsx import split_sheet

e = r"C:\Users\g1879\Desktop\111\tmp\aa (1).xlsx"
e = r"C:\Users\g1879\Desktop\111\tmp\bb.xlsx"
t1 = r'C:\Users\g1879\Desktop\111\tmp\新建文件夹'
t2 = r'C:\Users\g1879\Desktop\111\tmp\新建文件夹 (2)'
# wb = load_workbook(e)
# ws = wb.active
#
# n = perf_counter()
# split_sheet(ws, 'h', t1)
# s1 = perf_counter() - n
#
#
# print(s1)
# x=Path(e).parent
# print(type(x))
# x=get_usable_path(e)
# print(x)
# r = re.search(r' \((\d+)\)$', t2)
# print(r.group(1))


# a='gsfdg.ghfg.56'
# r = re.search(r'(.*)(\.[^.]+$)', a)
# print(r.group(1))


x=make_valid_name(('啊'*211)+'b.ff')
print(x)