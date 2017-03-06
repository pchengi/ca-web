import sys
import logging
import os
from flask import Flask
where=os.path.dirname(__file__)
sys.path.insert(0,where)
app = Flask(__name__)
from caops import app as application
