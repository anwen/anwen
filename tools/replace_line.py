#!/usr/bin/env python
#-*- coding=utf-8 -*-

import sys
import os


def replace_linesep(file_name):
    if type(file_name) != str:
        raise ValueError
    new_lines = []

    #以读模式打开文件
    try:
        fobj_original = open(file_name, 'r')
    except IOError:
        print('Cannot read file %s!' % file_name)
        return False
    #逐行读取原始脚本
    print('Reading file %s' % file_name)
    line = fobj_original.readline()
    while line:
        if line[-2:] == '\r\n':
            new_lines.append(line[:-2] + '\n')
        else:
            new_lines.append(line)
        line = fobj_original.readline()
    fobj_original.close()

    #以写模式打开文件
    try:
        fobj_new = open(file_name, 'w')
    except IOError:
        print('Cannot write file %s!' % file_name)
        return False
    #逐行写入新脚本
    print('Writing file %s' % file_name)
    for new_line in new_lines:
        fobj_new.write(new_line)
    fobj_new.close()
    return True


def main():
    args = sys.argv
    if len(args) < 2:
        print('Please enter the file names as parameters follow this script.')
        os._exit(0)
    else:
        file_names = args[1:]
        for file_name in file_names:
            if replace_linesep(file_name):
                print('Replace for %s successfully！' % file_name)
            else:
                print('Replace for %s failed！' % file_name)
    os._exit(1)

if __name__ == '__main__':
    main()
