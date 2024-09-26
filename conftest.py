import sys
import os

# Add the "scripts" directory to sys.path so that "scripts.downloader" can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))