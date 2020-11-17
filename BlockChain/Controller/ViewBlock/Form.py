from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField


class BlockForm(FlaskForm):
    index = StringField('Block Index', validators=[DataRequired()])
