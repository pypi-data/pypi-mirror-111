#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# @Author    : g1879
# @date      : 2021/6/03
# @email     : g1879@qq.com
# @File      : files.py
"""
文件、文件夹处理常用方法
"""
import shutil
import winreg
from pathlib import Path
from typing import Union, List


def find_file_or_folder(path: Union[Path, str],
                        keys: Union[str, list, tuple, set],
                        file_or_folder: str = 'file',
                        fuzzy: bool = True,
                        find_in_sub: bool = True,
                        name_or_suffix: str = 'name',
                        match_case: bool = False,
                        return_one: bool = True,
                        each_key: bool = True,
                        deep_first: bool = False) -> Union[Path, List[Path], dict]:
    """根据关键字查找文件或文件夹，返回Path对象或其组成的列表或字典
    :param path: 在这个文件夹路径下查找
    :param keys: 关键字，可输入多个
    :param file_or_folder: 查找文件还是文件夹，可传入 'file' 'folder' 'both'
    :param fuzzy: 是否模糊匹配
    :param find_in_sub: 是否进入子文件夹查找
    :param name_or_suffix: 在文件名还是后缀名中匹配，可传入 'name' 'suffix' 'full'
    :param match_case: 是否区分大小写
    :param return_one: 只返回第一个结果还是返回全部结果
    :param each_key: 是否分开返回每个key的结果
    :param deep_first: 是否深度优先搜索
    :return: Path对象或其组成的列表或字典
    """
    # -------------- 处理关键字 --------------
    if isinstance(keys, str):
        keys = (keys,)

    if name_or_suffix == 'suffix':
        keys = map(lambda x: x if x.startswith('.') else f'.{x}', keys)

    if not match_case:
        keys = map(lambda x: x.lower(), keys)

    keys = set(keys)

    # -------------- 执行查找操作 --------------
    results = {x: None for x in keys} if each_key else []

    folders = []
    for item in Path(path).iterdir():
        # 判断模式是否和当前类型一致，不一致则跳过该文件（夹）
        if ((file_or_folder == 'both')
                or (file_or_folder == 'file' and item.is_file())
                or (file_or_folder == 'folder' and item.is_dir())):
            # 准备待匹配的部分
            if name_or_suffix == 'name':
                find_str = item.stem
            elif name_or_suffix == 'suffix':
                find_str = item.suffix
            elif name_or_suffix == 'full':
                find_str = item.name
            else:
                raise ValueError("name_or_suffix参数只能传入'name', 'suffix', 'full'")

            # 若不区分大小写，全部转为小写
            if not match_case:
                find_str = find_str.lower()

            # 对关键字进行匹配
            is_it = None
            item_keys = []
            for key in tuple(keys):
                if (fuzzy and key in find_str) or (not fuzzy and find_str == key):
                    is_it = True
                    item_keys.append(key)

                    if return_one:
                        keys.remove(key)

                    if not each_key:
                        break

            # 若匹配成功，即该文件（夹）为结果（之一）
            if is_it:
                # 用字典返回每个key的结果
                if each_key:
                    for k in item_keys:
                        # 如果只要第一个结果，且该key值已经有结果，就跳到下一个
                        if return_one and results.get(k, None):
                            continue

                        if results.get(k, None) is None:
                            results[k] = item if return_one else [item]
                        else:
                            results[k].append(item)

                # 用列表或Path对象返回全部结果
                else:
                    if return_one:
                        return item
                    else:
                        results.append(item)

        # -------------- 如果是文件夹，调用自己，进入下层 --------------
        if item.is_dir() and find_in_sub and keys:
            # 广度优先，记录文件夹，等下再处理
            if not deep_first:
                folders.append(item)

            # 深度优先，遇到文件夹即时进入查找
            else:
                sub_results = find_file_or_folder(item, keys, file_or_folder, fuzzy, find_in_sub, name_or_suffix,
                                                  match_case, return_one, each_key, deep_first)
                results = _merge_results(results, sub_results, each_key, return_one)

    # 广度优先，上面判断完文件，再逐个进入该层文件夹查找
    if not deep_first:
        for item in folders:
            sub_results = find_file_or_folder(item, keys, file_or_folder, fuzzy, find_in_sub, name_or_suffix,
                                              match_case, return_one, each_key, deep_first)
            results = _merge_results(results, sub_results, each_key, return_one)

    return results


def _merge_results(par_results: Union[dict, list],
                   sub_results: Union[dict, list, Path],
                   each_key: bool,
                   return_one: bool) -> Union[dict, list, Path]:
    """合并查找结果
    :param par_results: 父级查找结果
    :param sub_results: 子文件夹查找结果
    :param each_key: 是否分开返回每个key的结果
    :param return_one: 只返回第一个结果还是返回全部结果
    :return: 合并后的结果
    """
    # 用字典返回每个关键字结果
    if each_key and any(sub_results.values()):
        # 将父字典和子字典的结果合并
        for k in tuple(x for x in sub_results if sub_results[x]):
            if par_results.get(k, None) is None:
                par_results[k] = sub_results[k] if return_one else [sub_results[k]]
            else:
                par_results[k].extend(sub_results[k])

    # 用列表或Path对象返回查找结果
    elif not each_key and sub_results:
        if return_one:
            return sub_results
        else:
            par_results.extend(sub_results)

    return par_results


def clean_folder(path: str, ignore: Union[str, list, tuple] = None) -> None:
    """清空一个文件夹，除了ignore里的文件和文件夹
    :param path: 要清空的文件夹路径
    :param ignore: 忽略列表或文件（夹）全名
    :return: None
    """
    if isinstance(ignore, str):
        ignore = (ignore,)
    for f in Path(path).iterdir():
        if not ignore or f.name not in ignore:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f, True)


def get_valid_name(path: Union[str, Path], name: str) -> str:
    """检查文件或文件夹是否重名，并返回可以使用的名称
    :param path: 文件夹路径
    :param name: 要检查的名称
    :return: 可用的文件名
    """
    while (file_Path := Path(path).joinpath(name)).exists():
        ext_name = file_Path.suffix
        base_name = file_Path.stem
        num = base_name.split(' ')[-1]
        if num[0] == '(' and num[-1] == ')' and num[1:-1].isdigit():
            num = int(num[1:-1])
            name = f'{base_name.replace(f"({num})", "", -1)}({num + 1}){ext_name}'
        else:
            name = f'{base_name} (1){ext_name}'
    return name


def get_desktop() -> str:
    """获取桌面路径"""
    return winreg.QueryValueEx(
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'),
        "Desktop")[0]
