import re, os
import shutil
from pathlib import Path
import zipfile
import ntpath
#
# def file_copy(file_path, file_name, file_tmp, copy_to_path, rename=None):
#
#     tmpf = os.path.join(file_path, file_tmp)
#     tmpf = tmpf.replace('\\', '/')
#
#     if rename:
#         path_list = file_name.split('.')
#         file_name = path_list[0] + '_report.' + path_list[1]
#         tmpt = os.path.join(copy_to_path, file_name)
#     else:
#         tmpt = os.path.join(copy_to_path, file_name)
#         tmpt = tmpt.replace('\\', '/')
#
#     if not os.path.exists(tmpt):
#         shutil.copy(tmpf, tmpt)
#         return file_name
#     num = 1
#     if re.findall('\((\d+)\)', file_name):
#         num = re.findall('\((\d+)\)', file_name)
#         new_num = int(num[0]) + 1
#         file_name = file_name.replace(num[0], str(new_num))
#         return file_copy(file_path, file_name, file_tmp, copy_to_path)
#     path_list = file_name.split('.')
#
#     if rename:
#         if '_report' in path_list[0]:
#             file_name = path_list[0] + f'({num}).' + path_list[1]
#         else:
#             file_name = path_list[0] + '_report' + f'({num}).' + path_list[1]
#     else:
#         file_name = path_list[0] + f'({num}).' + path_list[1]
#
#     return file_copy(file_path, file_name, file_tmp, copy_to_path)

def file_unzip(file_name: str, dir_name):
    try:
        name = ntpath.basename(file_name)
        new = os.path.splitext(name)[0]
        dir_name = os.path.join(dir_name, new)
        file = zipfile.ZipFile(file_name)
        file.extractall(dir_name)
        file.close()
        # 递归修复编码
        # __rename(dir_name)
    except:
        print(f'{file_name} unzip fail')

def __rename(pwd: str, file_name=''):
    path = f'{pwd}/{file_name}'
    if os.path.isdir(path):
        for i in os.scandir(path):
            __rename(pwd, i.name)
    newname = file_name.encode('cp437').decode('gbk')
    os.rename(path, f'{pwd}/{newname}')

def file_del(filepath):
    del_list = os.listdir(filepath)

    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def file_zip_path(input_path, output_path, ignore=[]):
    outdir = os.path.dirname(output_path)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    f = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)

    filepathlists = []
    filenamelists = []
    _dfs_zip_file(input_path, filepathlists, filenamelists, ignore)

    for file in filepathlists:
        file = file.replace('\\', '/')
        input_path = input_path.replace('\\', '/')
        f.write(file, file.replace(input_path, ''))
    f.close()
    return output_path

def _dfs_zip_file(input_path, resultpath, resultfile, ignore=[]):
    files = os.listdir(input_path)

    for file in files:
        filepath = os.path.join(input_path, file)

        if os.path.isdir(filepath):
            _dfs_zip_file(filepath, resultpath, resultfile, ignore)
        else:
            count = 0
            for one in ignore:
                if one in file:
                    count += 1
            if count == len(ignore):
                resultpath.append(filepath)
                resultfile.append(file)

def _dfs_current_folder(input_path, resultpath, resultfile, ignore=[]):
    files = os.listdir(input_path)

    for file in files:
        filepath = os.path.join(input_path, file)
        if os.path.isdir(filepath):
            continue
        else:
            count = 0
            for one in ignore:
                if one in file:
                    count += 1
            if count == len(ignore):
                resultpath.append(filepath)
                resultfile.append(file)

def current_folder_file_copy(input_path, copy_to_path, ignore=[], rename=None):

    filepathlists = []
    filenamelists = []
    _dfs_current_folder(input_path, filepathlists, filenamelists, ignore)
    s = ''
    for file in filepathlists:
        dirs_f = os.path.dirname(file)
        dirs_t = dirs_f.replace(input_path, copy_to_path)
        os.makedirs(dirs_t, exist_ok=True)

        name = ntpath.basename(file)
        name_tmp = ntpath.basename(file)
        f = file_copy(dirs_f, name, name_tmp, dirs_t, rename)
        if s == '':
            s = s + f
        else:
            s = s + ',' + f
    return s


def copy_current_folder_file(from_path, copy_to_path, ignore=[], rename=None):

    L = []
    # filenamelists = []
    # _dfs_current_folder(from_path, filepathlists, filenamelists, ignore)
    # s = ''
    # for file in filepathlists:
    #     dirs_f = os.path.dirname(file)
    #     dirs_t = dirs_f.replace(from_path, copy_to_path)
    #     os.makedirs(dirs_t, exist_ok=True)
    #
    #     name = ntpath.basename(file)
    #     name_tmp = ntpath.basename(file)
    #     f = file_copy(dirs_f, name, name_tmp, dirs_t, rename)
    #     if s == '':
    #         s = s + f
    #     else:
    #         s = s + ',' + f
    # return s
    file = 'C:/Users/kangs/Desktop/desk/macaca-master/macaca-master/新建 DOC 文档.doc'
    print(os.path.dirname(file))
    dirs_f = os.path.dirname(file)
    print(dirs_f.replace(from_path, copy_to_path))
    if Path(from_path).exists():
        for root, dirs, files in os.walk(from_path):
            if root == from_path:
                for file in files:
                    if ignore:
                        for r in ignore:
                            if r in file:
                                L.append(Path(root, file))
                    else:
                        L.append(Path(root, file))
    else:
        print('File not exist.')
    return L











def file_and_folder_copy(input_path, copy_to_path, ignore=[], rename=None):

    filepathlists = []
    filenamelists = []
    _dfs_zip_file(input_path, filepathlists, filenamelists, ignore)
    s = ''
    for file in filepathlists:
        dirs_f = os.path.dirname(file)
        dirs_t = dirs_f.replace(input_path, copy_to_path)
        os.makedirs(dirs_t, exist_ok=True)

        name = ntpath.basename(file)
        name_tmp = ntpath.basename(file)
        f = file_copy(dirs_f, name, name_tmp, dirs_t, rename)
        if s == '':
            s = s + f
        else:
            s = s + ',' + f
    return s






def find_current_folder_files(file_path, f_name='', f_suffix=None):
    """
    find_current_folder_files
    :param filepath: file path or path+file_name
    :param name: file name or part name
    :param ignore: .csv / '' / ...
    :param return: path+file_name list
    """
    pattern = r'(.+)'
    res = re.findall(pattern, str(f_name))
    L = []
    if Path(file_path).exists() and Path(file_path).is_file():
        L.append(Path(file_path))
    elif Path(file_path).exists() and Path(file_path).is_dir():
        for root, dirs, files in os.walk(file_path):
            if root == file_path:
                for file in files:
                    if f_name == '':
                        if f_suffix is None:
                            L.append(Path(root, file))
                        else:
                            if Path(file).suffix == f_suffix.lower():
                                L.append(Path(root, file))
                    else:
                        for r in res:
                            if r in file:
                                if f_suffix is None:
                                    L.append(Path(root, file))
                                else:
                                    if Path(file).suffix == f_suffix.lower():
                                        L.append(Path(root, file))
    else:
        print('File not exist.')
    return L

def __dfs_find_files(L, res, file_path, f_name, f_suffix):
    for file in Path(file_path).glob('*'):
        if file.is_file():
            if f_name == '':
                if f_suffix is None:
                    L.append(Path(file))
                else:
                    if Path(file).suffix == f_suffix.lower():
                        L.append(Path(file))
            else:
                for r in res:
                    if r in file:
                        if f_suffix is None:
                            L.append(Path(file))
                        else:
                            if Path(file).suffix == f_suffix.lower():
                                L.append(Path(file))
        else:
            __dfs_find_files(L, res, file, f_name, f_suffix)
            # L.append(file)


def find_files(file_path, f_name='', f_suffix=None):
    """
    find all files
    :param filepath: file path or path+file_name
    :param name: file name or part name
    :param ignore: .csv / '' / ...
    :param return: path+file_name list
    """
    pattern = r'(.+)'
    res = re.findall(pattern, str(f_name))
    L = []
    if Path(file_path).exists() and Path(file_path).is_file():
        L.append(Path(file_path))
    elif Path(file_path).exists() and Path(file_path).is_dir():
        __dfs_find_files(L, res, file_path, f_name, f_suffix)
    else:
        print('File not exist.')
    return L


def del_current_folder_files(file_path, f_name='', f_suffix=None):
    """
    del_current_folder_files
    :param filepath: file path or path+file_name
    :param name: file name or part name
    :param ignore: .csv / '' / ...
    :param return: path+file_name list
    """
    pattern = r'(.+)'
    res = re.findall(pattern, str(f_name))
    L = []
    if Path(file_path).exists() and Path(file_path).is_file():
        os.remove(Path(file_path))
        L.append(Path(file_path))
    elif Path(file_path).exists() and Path(file_path).is_dir():
        for root, dirs, files in os.walk(file_path):
            if root == file_path:
                for file in files:
                    if f_name == '':
                        if f_suffix is None:
                            os.remove(Path(root, file))
                            L.append(Path(root, file))
                        else:
                            if Path(file).suffix == f_suffix.lower():
                                os.remove(Path(root, file))
                                L.append(Path(root, file))
                    else:
                        for r in res:
                            if r in file:
                                if f_suffix is None:
                                    os.remove(Path(root, file))
                                    L.append(Path(root, file))
                                else:
                                    if Path(file).suffix == f_suffix.lower():
                                        os.remove(Path(root, file))
                                        L.append(Path(root, file))
    else:
        print('File not exist.')
    return L


def __dfs_del_files(L, res, file_path, f_name, f_suffix):
    for file in Path(file_path).glob('*'):
        if file.is_file():
            if f_name == '':
                if f_suffix is None:
                    file.unlink()
                    L.append(Path(file))
                else:
                    if Path(file).suffix == f_suffix.lower():
                        file.unlink()
                        L.append(Path(file))
            else:
                for r in res:
                    if r in file:
                        if f_suffix is None:
                            file.unlink()
                            L.append(Path(file))
                        else:
                            if Path(file).suffix == f_suffix.lower():
                                file.unlink()
                                L.append(Path(file))
        else:
            __dfs_del_files(L, res, file, f_name, f_suffix)
            file.rmdir()
            L.append(file)

def del_files(file_path, f_name='', f_suffix=None):
    """
    delete all files
    :param filepath: file path or path+file_name
    :param name: file name or part name
    :param ignore: .csv / '' / ...
    :param return: path+file_name list
    """
    pattern = r'(.+)'
    res = re.findall(pattern, str(f_name))
    L = []
    if Path(file_path).exists() and Path(file_path).is_file():
        os.remove(Path(file_path))
        L.append(Path(file_path))
    elif Path(file_path).exists() and Path(file_path).is_dir():
        __dfs_del_files(L, res, file_path, f_name, f_suffix)
    else:
        print('File not exist.')
    return L




def file_copy(file_path, file_name, file_tmp, copy_to_path, rename):
    pattert = '\((\d+)\)'
    tmpf = Path(file_path, file_tmp)
    if rename and not re.findall(pattert, file_name):
        file_name = rename + Path(file_name).suffix
    tmpt = Path(copy_to_path, file_name)
    if not tmpt.exists():
        shutil.copy(tmpf, tmpt)
        return file_name
    num = 1
    if re.findall(pattert, file_name):
        num = re.findall(pattert, file_name)
        new_num = str(int(num[0])+1)
        file_name = re.sub(pattert, '('+new_num+')', file_name)
        return file_copy(file_path, file_name, file_tmp, copy_to_path, rename)

    if rename and not re.findall(pattert, file_name):
        file_name = rename +f'({str(num)})'+ str(Path(file_name).suffix)
    else:
        file_name = str(file_name).replace(str(Path(file_name).suffix), '') +f'({str(num)})'+ str(Path(file_name).suffix)
    return file_copy(file_path, file_name, file_tmp, copy_to_path, rename)

def __dfs_find_copy_current_folder(file_path, file_path_list, file_name_list, ignore):
    for file in Path(file_path).iterdir():
        if file.is_file():
            if ignore:
                for one in ignore:
                    if str(one) in str(file):
                        file_path_list.append(file)
                        file_name_list.append(file.name)
            else:

                file_path_list.append(file)
                file_name_list.append(file.name)

def find_copy_current_folder(input_path, copy_to_path, ignore=[], rename=''):
    """
    find_copy_current_folder
    :param input_path: file path dir or path + file_name
    :param copy_to_path: file path dir
    :param ignore: file name(xxx.txt) or part name(xxx.txt--> txt)
    :param ignore: new file name not contains suffix
    :param return: file_name list
    """
    file_path_list = []
    file_name_list = []
    L = []

    if Path(input_path).exists() and Path(input_path).is_file():
        dirs_f = Path(input_path).parent
        dirs_to = Path(copy_to_path)
        Path(copy_to_path).mkdir(exist_ok=True)
        f_name = Path(input_path).name
        f_name_tmp = Path(input_path).name
        f = file_copy(dirs_f, f_name, f_name_tmp, dirs_to, rename)
        L.append(f)
    elif Path(input_path).exists() and Path(input_path).is_dir():
        __dfs_find_copy_current_folder(input_path, file_path_list, file_name_list, ignore)
        if len(file_name_list)!= 1: # multi files do not rename
            rename = ''
        for i in range(0, len(file_path_list)):
            dirs_f = Path(file_path_list[i]).parent
            dirs_to = Path(copy_to_path)
            Path(copy_to_path).mkdir(exist_ok=True)
            f_name = file_name_list[i]
            f_name_tmp = file_name_list[i]
            f = file_copy(dirs_f, f_name, f_name_tmp, dirs_to, rename)
            L.append(f)
    else:
        print(f'File name/path not exist. "{input_path}"')


def __dfs_find_copy_all_folder(file_path, file_path_list, file_name_list, ignore):
    for file in Path(file_path).iterdir():
        if file.is_file():
            if ignore:
                for one in ignore:
                    if str(one) in str(file):
                        file_path_list.append(file)
                        file_name_list.append(file.name)
            else:
                file_path_list.append(file)
                file_name_list.append(file.name)
        else:
            __dfs_find_copy_all_folder(file, file_path_list, file_name_list, ignore)


def find_copy_all_folder(input_path, copy_to_path, ignore=[], rename=''):
    """
    find_copy_all_folder
    :param input_path: file path dir or path + file_name
    :param copy_to_path: file path dir
    :param ignore: file name(xxx.txt) or part name(xxx.txt--> txt)
    :param ignore: new file name not contains suffix
    :param return: file_name list
    """
    file_path_list = []
    file_name_list = []
    L = []

    if Path(input_path).exists() and Path(input_path).is_file():
        dirs_f = Path(input_path).parent
        dirs_to = str(dirs_f).replace(str(Path(input_path).parent), str(Path(copy_to_path)))
        Path(dirs_to).mkdir(exist_ok=True)
        f_name = Path(input_path).name
        f_name_tmp = Path(input_path).name
        f = file_copy(dirs_f, f_name, f_name_tmp, dirs_to, rename)
        L.append(f)
    elif Path(input_path).exists() and Path(input_path).is_dir():
        __dfs_find_copy_all_folder(input_path, file_path_list, file_name_list, ignore)
        if len(file_name_list) != 1: # multi files do not rename
            rename = ''
        for i in range(0, len(file_path_list)):
            dirs_f = Path(file_path_list[i]).parent
            dirs_to = str(dirs_f).replace(str(Path(input_path)), str(Path(copy_to_path)))
            Path(dirs_to).mkdir(exist_ok=True)
            f_name = file_name_list[i]
            f_name_tmp = file_name_list[i]
            f = file_copy(dirs_f, f_name, f_name_tmp, dirs_to, rename)
            L.append(f)
    else:
        print(f'File name/path not exist. "{input_path}"')
    return L


def __dfs_file_zip(file_path, file_path_list, file_name_list, ignore):
    for file in Path(file_path).iterdir():
        if file.is_file():
            if ignore:
                for one in ignore:
                    if str(one) in str(file):
                        file_path_list.append(file)
                        file_name_list.append(file.name)
            else:
                file_path_list.append(file)
                file_name_list.append(file.name)
        else:
            __dfs_file_zip(file, file_path_list, file_name_list, ignore)

def file_zip(input_path, output_path, ignore=[]):
    """
    file_zip
    :param input_path: file path dir or path + file_name
    :param output_path: output path
    :param ignore: file name(xxx.txt) or part name(abcd.txt--> bc)
    """
    file_path_list = []
    file_name_list = []

    if not Path(output_path).is_file():
        Path(input_path).parent.mkdir(exist_ok=True)
    z_file = zipfile.ZipFile(Path(output_path), 'w', zipfile.ZIP_DEFLATED)
    if Path(input_path).exists() and Path(input_path).is_file():
        z_file.write(Path(input_path), Path(input_path).name)
        z_file.close()

    elif Path(input_path).exists() and Path(input_path).is_dir():
        __dfs_file_zip(input_path, file_path_list, file_name_list, ignore)
        for i in range(0, len(file_path_list)):
            z_file.write(Path(file_path_list[i]), str(file_path_list[i]).replace(str(Path(input_path)), ''))
        z_file.close()
    else:
        print(f'File name/path not exist. "{input_path}"')



# def __dnf_file_name_change(file_path):
#
#     pattert = '\((\d+)\)'
#     f_path = Path(file_path).parent
#     f_name = Path(file_path).name
#     f_name_no_suffix = Path(file_path).stem
#     f_name_suffix = Path(file_path).suffix
#     f_flag = False
#     num = 1
#     if not Path(file_path).exists():
#         return file_path
#     else:
#         f_flag = True
#
#     if rename and len(re.findall(pattert, str(file_path))) == 0:
#         file_name = rename + Path(file_path).suffix
#         file_path = Path().joinpath(f_path, f_name)
#         if f_flag:
#             new_name = f_name_no_suffix + f'({str(num)})' + f_name_suffix
#         return __dnf_file_name_change(file_path, rename)
#
#     elif rename and len(re.findall(pattert, str(file_path))) != 0:
#         num = re.findall(pattert, f_name)
#         new_num = str(int(num[0])+1)
#         file_path = Path().joinpath(f_path, rename + f_name_suffix)
#         if f_flag:
#             new_name = re.sub(pattert, '('+new_num+')', f_name_no_suffix)
#             file_path = Path().joinpath(f_path, new_name, f_name_no_suffix)
#         return __dnf_file_name_change(file_path, rename)
#
#     elif not re.findall(pattert, str(file_path)):
#         new_name = f_name_no_suffix + f'({str(num)})' + f_name_suffix
#         file_path = Path().joinpath(f_path, new_name)
#         return __dnf_file_name_change(file_path, rename)
#
#     elif re.findall(pattert, str(file_path)):
#         num = re.findall(pattert, f_name)
#         new_num = str(int(num[0])+1)
#         new_name = re.sub(pattert, '('+new_num+')', f_name_no_suffix)
#         file_path = Path().joinpath(f_path, new_name, f_name_suffix)
#         return __dnf_file_name_change(file_path, rename)
#     else:
#         pass




# def file_name_change(file_path):
#     if Path(file_path).exists() and Path(file_path).is_file():
#         file_path = __dnf_file_name_change(file_path)
#         return file_path
#     else:
#         print(f'File name/path not exist. "{file_path}"')
#         return ''



if __name__ == '__main__':
    path=r'C:\Users\kangs\Desktop\desk\macaca-master\macaca-master\新建文本文档.txt'
    to = r'C:\Users\kangs\Desktop\desk\macaca-master\macaca-master\新建文件夹'
    # print(del_files_and_folder(path))
    # print(del_current_folder_files(path))
    # print(find_files(path))

    pass
