from flask import Flask

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.create_jinja_environment()

from app import routes
