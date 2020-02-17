# Library imports
from flask import Flask, request, url_for, render_template, redirect, flash
import requests
import json

# Project imports
from search_form import SearchForm
from db_operations import get_db_version, retrieve_courses_documents
from boolean_retrieval import execute_boolean_query
from query_processing import process_query

# Flask config info
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SECRET_KEY'] = "+_I&Mh+If`KPP23+P{1U"

# Flask functionality inspired by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    model_type = ''
    if form.validate_on_submit():
        query = json.dumps({"ir_model":form.ir_model.data, "query":form.query.data})
        if form.ir_model.data == 'bool':
            model_type = "Boolean Model"
        elif form.ir_model.data == 'vsm':
            model_type = "Vector Space Model"
        else:
            model_type = ''
            
        flash('{0} search on query: {1}'.format(model_type, form.query.data))
        return redirect(url_for('results', query=query))
    return render_template("home.html", title='Zearjch', form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    query_json = request.args['query']
    query = json.loads(query_json)
    if query['ir_model'] == 'bool':
        doc_ids = execute_boolean_query(process_query(query['query']))
    elif query['ir_model'] == 'vsm':
        doc_ids = [] # TODO implement VSM
    if doc_ids == []:
        docs = []
        doc_count = 0
    else:
        docs = retrieve_courses_documents(doc_ids)
        doc_count = len(doc_ids)
    if docs == None:
        docs = []
    return render_template('results.html', title='Zearjch', docs=docs, doc_count=doc_count)
