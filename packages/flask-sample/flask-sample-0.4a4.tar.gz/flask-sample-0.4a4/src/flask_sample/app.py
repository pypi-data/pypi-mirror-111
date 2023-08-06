#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from flask import Flask
from flask import render_template
from flask import __version__
import os

APP_NAME = 'sample flask app'

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

app = Flask(__name__, static_folder=STATIC_DIR)


@app.route('/')
def home():
    return render_template('index.html', flask_ver=__version__)


if __name__ == '__main__':
    app.run()
