import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv('../.env')


def create_app():
    app = Flask(__name__)
    # set default button style and size, will be overwritten by macro parameters
    app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
    app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

    # set default icon title of table actions
    app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
    app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
    app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
    app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

    app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
    return app
