from wtforms import Form, StringField, validators

class search_form(Form):
    """Form for client searching
    
    Will add advanced search options later
    """
    query_field = StringField("Enter your search...", [validators.InputRequired()])
    #TODO add advanced search options