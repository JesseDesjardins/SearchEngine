# Library imports
from flask import Flask, request, url_for, render_template, redirect, flash, jsonify
import requests
import json

# Project imports
from search_form import SearchForm
from db_operations import get_db_version, retrieve_courses_documents, retrieve_reuters_documents
from boolean_retrieval import execute_boolean_query
from query_processing import process_boolean_query
from process_and_load import process_and_load_courses

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
        query = json.dumps({"ir_model":form.ir_model.data, "corpus":form.corpus.data, "query":form.query.data})
        if form.ir_model.data == 'bool':
            model_type = "Boolean Model"
        elif form.ir_model.data == 'vsm':
            model_type = "Vector Space Model"
        else:
            model_type = ''
        if form.corpus.data == 'courses':
            corpus_selection = 'uOttawa Course List'
        elif form.corpus.data == 'reuters':
            corpus_selection = 'Reuters Articles'
        else:
            corpus_selection = ''
        flash('{0} search through the {1} corpus on query: {2}'.format(model_type, corpus_selection, form.query.data))
        return redirect(url_for('results', query=query))
    return render_template("home.html", title='Zearjch', form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    docs = []
    query_json = request.args['query']
    query = json.loads(query_json)
    if query['ir_model'] == 'bool':
        collection = None
        if query['corpus'] == 'courses':
            collection = "courses"
        elif query['corpus'] == 'reuters':
            collection = "reuters"
        doc_ids = execute_boolean_query(process_boolean_query(query['query']), collection)
    elif query['ir_model'] == 'vsm':
        doc_ids = [] # TODO implement VSM
    if doc_ids == []:
        docs = []
        doc_count = 0
    else:
        print(doc_ids)
        if query['corpus'] == 'courses':
            docs = retrieve_courses_documents(doc_ids)
        elif query['corpus'] == 'reuters':
            docs = retrieve_reuters_documents(doc_ids)
        doc_count = len(doc_ids)
    if docs == None:
        docs = []
    return render_template('results.html', title='Zearjch', docs=docs, doc_count=doc_count)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """ Autocomplete functionality based off of: https://stackoverflow.com/questions/34704997/jquery-autocomplete-in-flask """
    with open('bigram_language_model.json') as bigram_language_model:
        autocomplete_bigrams = json.load(bigram_language_model)

    search = request.args.get('q').strip().lower()
    term_to_search = search.split()[-1].strip() # checks the last word in the query

    if term_to_search not in autocomplete_bigrams: # If term is not in the bigrams list then offer no autocompletion
        return jsonify(matching_results=[])

    autocomplete_options = autocomplete_bigrams[term_to_search] # Otherwise pull up all relevant bigrams

    sorted_autocomplete_options = sorted(autocomplete_options.items(), key=lambda kv: kv[1], reverse=True) # Sort the relevant bigrams

    sorted_autocomplete_options = sorted_autocomplete_options[:(10 if len(sorted_autocomplete_options) > 10 else len(sorted_autocomplete_options) - 1)] # Show up to 10 terms
    
    autocomplete_display = [f"{search} {key}" for key, _ in sorted_autocomplete_options] # Display the last queried word followed by all selected bigrams options

    return jsonify(matching_results=autocomplete_display)