from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired


class DonationForm(FlaskForm):
    organ_name = StringField("Organ Name: ", validators=[DataRequired()])
    donor = StringField("Donor: ", validators=[DataRequired()])
    age = IntegerField("Donor Age: ", validators=[DataRequired()])
    height = FloatField("Donor Height(cm): ", validators=[DataRequired()])
    weight = FloatField("Donor Weight(kg): ", validators=[DataRequired()])
    blood_type = SelectField("Donor Age: ",choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],
                             validators=[DataRequired()])
    hla_group = SelectField("HLA Group: ", choices=[('HLA-A', 'HLA-A'), ('HLA-B', 'HLA-B'), ('HLA-C', 'HLA-C'),
                                                ('HLA-E', 'HLA-E'), ('HLA-F', 'HLA-F'), ('HLA-G', 'HLA-G'),
                                                ('HLA-DMA1', 'HLA-DMA1'), ('HLA-DMB1', 'HLA-DMB1'),
                                                ('HLA-DQA1', 'HLA-DQA1'), ('HLA-DQB1', 'HLA-DQB1'),
                                                ('HLA-DRA1', 'HLA-DRA1'), ('HLA-DRB1', 'HLA-DRB1'),
                                                ('HLA-DRB3', 'HLA-DRB3'), ('HLA-DRB4', 'HLA-DRB4'),
                                                ('HLA-DRB5', 'HLA-DRB5'), ('HLA-DPA1', 'HLA-DPA1'),
                                                ('HLA-DPB1', 'HLA-DPB1'), ('other', 'other')],
                            validators=[DataRequired()])
    other_hla_group = StringField("Other HLA Group: ")
    submit = SubmitField('Submit')


class approvalForm(FlaskForm):
    selection = [('Rejected', 'Reject'), ('Approved', 'Approve'), ('Pending', 'Pending')]
    approval_status = SelectField('Approval', choices=selection)
    submit = SubmitField("Confirm")