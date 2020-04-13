from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, FieldList, FormField

class RelevanceForm(FlaskForm):
    relevant = BooleanField("Is this relevant to your search?", validators=None)

class RelevancesForm(FlaskForm):
    """ A form for 0 or more relevance fields"""
    relevances = FieldList(FormField(RelevanceForm))
    submit = SubmitField('Confirm Selection')