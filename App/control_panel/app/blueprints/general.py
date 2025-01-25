from flask import Blueprint, render_template

bp_general = Blueprint('general', __name__)


@bp_general.route('/')
def index():
    return render_template('index.html')
