from flask import Flask
import sys
import os
from pathlib import Path
from path_finder import GetScriptDirectory

script_path = GetScriptDirectory()
parent_path = os.path.dirname(script_path)
sys.path.append(parent_path)
# print(' -- script dir:', script_path, ' base: ', parent_path)
# print(sys.path)


app = Flask(__name__)

from views import *


if __name__ == '__main__':
    app.run(debug=True)