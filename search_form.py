from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('Search Query', validators=[DataRequired()], id="search_autocomplete")
    ir_model = RadioField('Model type', choices=[('bool', 'Boolean Model'),('vsm', 'Vector Space Model')], default='bool')
    corpus = RadioField('Corpus selection', choices=[('courses', 'uOttawa Course List'),('reuters', 'Reuters Articles')], default='courses')
    submit = SubmitField('Zearjch!')