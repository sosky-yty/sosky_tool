# coding:utf-8

import os
import argparse


# 脚本测试通过

# 通过扩展名批量修改同类文件名


def batch_name(dir_name, new_filename, new_ext, old_ext):
    falg = 0
    for filename in os.listdir(dir_name):
        split_file = os.path.splitext(filename)
        file_ext = split_file[1]
        if old_ext == file_ext:
            newname = new_filename + str(falg) + new_ext
            falg = falg + 1
            os.rename(
                os.path.join(dir_name, filename),
                os.path.join(dir_name, newname)
            )


def get_parser():
    description = '本脚本是通过批量修改相同后缀名文件的名称'
    parser = argparse.ArgumentParser(description=description)

    dir_name_help = '修改文件所在的文件路径'
    parser.add_argument('dir_name', metavar='DIR_NAME', type=str, nargs=1, help=dir_name_help)

    new_filename_help = '重命名文件名'
    parser.add_argument('new_filename', metavar='NEW_FILENAME', type=str, nargs=1, help=new_filename_help)

    new_ext_help = '新的文件扩展名'
    parser.add_argument('new_ext', metavar='NEW_EXT', type=str, nargs=1, help=new_ext_help)

    old_ext_help = '旧的文件扩展名'
    parser.add_argument('old_ext', metavar='OLD_EXT', type=str, nargs=1, help=old_ext_help)

    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    dir_name = args['dir_name'][0]

    new_filename = args['new_filename'][0]

    new_ext = args['new_ext'][0]
    if new_ext[0] != '.':
        new_ext = '.' + new_ext

    old_ext = args['old_ext'][0]
    if old_ext[0] != '.':
        old_ext = '.' + old_ext

    batch_name(dir_name, new_filename, new_ext, old_ext)


if __name__ == '__main__':
    main()
