import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# The Patient Register

@bp.route('/register', methods=('GET', 'POST'))
def register():
    pass

#The Patient Sign In page

@bp.route('/login')
def login():
    pass