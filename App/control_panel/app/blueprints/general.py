from flask import Blueprint, render_template

bp_general = Blueprint('general', __name__)


@bp_general.route('/')
def index():
    return render_template('index.html')


@bp_general.route('/a')
def index2():
    return render_template('index2.html')
