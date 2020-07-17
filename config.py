import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    TEMPLATES_AUTO_RELOAD = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
