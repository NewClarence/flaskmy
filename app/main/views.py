from flask import render_template
from . import main
from .forms import Login_Form


@main.route('/')
def index():
    form=Login_Form()
    return render_template('auth/login.html',form=form)
