#!/usr/bin/env python
# -*- coding:utf-8 -*-
from time import perf_counter

from g1879.paths import find_file_or_folder

path = r'D:\tmp\test'
# path = r'H:\2020ldjy'
# keys = ('22', '11')
# keys = ('202001050109002', '202013020103001', '202006010303005')
keys = ('11', '22')
# file_or_folder = 'file'
# file_or_folder = 'folder'
file_or_folder = 'both'
fuzzy = True
find_in_sub = True
# find_in_sub = False
name_or_suffix = 'name'
match_case = False
return_first = False
# return_first = True
each_key = True
# each_key = False
deep_first = False
# deep_first = True

ttt = perf_counter()
ff = find_file_or_folder(
    path,
    keys,
    file_or_folder,
    fuzzy,
    find_in_sub,
    name_or_suffix,
    match_case,
    return_first,
    each_key,
    deep_first
)
print(perf_counter() - ttt)

# print(ff)
if not isinstance(ff, list):
    for i in ff:
        if isinstance(ff, dict):
            print(i)
            if isinstance(ff[i], list):
                for j in ff[i]:
                    print(j)
            else:
                print(ff[i])
            print()

        else:
            print(i)

else:
    print(ff)
