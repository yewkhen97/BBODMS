from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, BooleanField
from wtforms.validators import DataRequired


class DonationForm(FlaskForm):
    organ_name = StringField("Organ Name: ", validators=[DataRequired()])
    donor = StringField("Donor: ", validators=[DataRequired()])
    age = IntegerField("Donor Age: ", validators=[DataRequired()])
    height = FloatField("Donor Height(cm): ", validators=[DataRequired()])
    weight = FloatField("Donor Weight(kg): ", validators=[DataRequired()])
    blood_type = StringField("Donor Age: ", validators=[DataRequired()])
    hla_group = StringField("HLA Group: ", validators=[DataRequired()])
    previous_hash = StringField("Previous Block Hash: ", validators=[DataRequired()])
    block_index = IntegerField("Block Index", validators=[DataRequired()])
    update_block = BooleanField("Organ Request", validators=[DataRequired()])
    applier_details = StringField("Applier Details", validators=[DataRequired()])
    submit = SubmitField('Submit')