from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class DonationForm(FlaskForm):
    OrganName = StringField("Organ Name", validators=[DataRequired()])
    OrganOwner = StringField("Organ Owner Name", validators=[DataRequired()])
    submit = SubmitField('Submit')




class approvalForm(FlaskForm):
    selection = [('Rejected', 'Reject'), ('Approved', 'Approve'), ('Pending', 'Pending')]
    approval_status = SelectField('Approval', choices=selection)
    submit = SubmitField("Confirm")