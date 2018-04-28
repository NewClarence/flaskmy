#!env/bin/python

import os
from flask_script import Manager
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

manager.run()
