# Library imports
from flask import Flask, request, url_for, render_template, redirect, flash

# Project imports
from search_form import search_form
from db_operations import get_db_version

# Flask config info
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SECRET_KEY'] = "+_I&Mh+If`KPP23+P{1U"

@app.route("/")
def route_empty_link_to_home():
    return redirect(url_for("search"))

@app.route("/search", methods=["GET", "POST"])
def search():
    form = search_form(request.form)
    if request.method == 'POST' and form.validate():
        # Do things with the form data
        print(form.query_field)
        flash("Thanks for the query")
        return redirect(url_for("hello"))
    return render_template("search.html", form=form)

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", name=name)

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)
