from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('Search Query', validators=[DataRequired()])
    ir_model = RadioField('Model type', choices=[('bool', 'Boolean Model'),('vsm', 'Vector Space Model')], default='bool')
    submit = SubmitField('Zearjch!')