import os
from pathlib import Path
import shutil
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_folder(flag=''):
    print(Path().absolute())
    _list = []
    try:
        with open(Path(Path().absolute()).joinpath('folder.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                one = str(line).replace('\n', '')
                if one != '':
                    _list.append(one)
        _list.sort()
        if flag == '':
            _gen2(_list)  # all folder
        else:
            _gen(_list)  # expect folder
        print('create_folder() is OK')
    except Exception as e:
        print('create_folder() ERROR \n')
        print(e)

def _gen2(_list):
    length = len(_list)
    for i in range(0, length):
        a = str(_list[i])
        Path(Path(Path().absolute()).joinpath(a)).mkdir(exist_ok=True)
def _gen(_list):
    length = len(_list)
    for i in range(0, length):
        for j in range(i+1, length):
            a = str(_list[i])
            b = str(_list[j])
            if len(a) == len(b):
                Path(Path(Path().absolute()).joinpath(a)).mkdir(exist_ok=True)
                if length == j+1:
                    Path(Path(Path().absolute()).joinpath(b)).mkdir(exist_ok=True)
            else:
                if a in b:
                    break
                else:
                    Path(Path(Path().absolute()).joinpath(a)).mkdir(exist_ok=True)


if __name__ == '__main__':
    create_folder(1)