#!D:\1学习资料\人工智能\Flask_AI\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.3.1','console_scripts','pyi-makespec'
__requires__ = 'PyInstaller==3.3.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('PyInstaller==3.3.1', 'console_scripts', 'pyi-makespec')()
    )
