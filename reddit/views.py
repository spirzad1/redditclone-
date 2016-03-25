#!venv/bin/python
from flask import request, render_template
from reddit import app, db
from models import *


@app.route('/')
def index():
    return "Reddit is sugoi"
