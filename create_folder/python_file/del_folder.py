import os
from pathlib import Path
import shutil
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def del_folder():
    try:
        ls = os.listdir(Path(Path().absolute()))
        for i in ls:
            c_path = (Path().absolute()).joinpath(i)
            if Path(c_path).is_dir() and Path(c_path).name !='python_file':
                shutil.rmtree(c_path)
        print('del_folder() is OK')
    except Exception as e:
        print('del_folder() ERROR \n')
        print(e)

if __name__ == '__main__':
    del_folder()