from flask_wtf import FlaskForm
from wtforms import SubmitField


class NewGame(FlaskForm):
    submit = SubmitField('New Game')


class FlipBoard(FlaskForm):
    submit = SubmitField('Flip Board')
