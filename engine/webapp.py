import os
import sys
cwd = os.getcwd()
sys.path.insert(0, cwd)
from response import app as application
