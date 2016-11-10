import os
import sys


root = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, root)

from app_factory import create_app
application = create_app('DEV')
