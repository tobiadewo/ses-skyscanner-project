from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import SearchForm, ResultSortSelect
from searchHandler import *
import arrow

# These variables are global so /results and /results_sorted can both access them
formData = {}
currency = ""
quotes = {}

@app.route('/')
@app.route('/index')
def index():
    """Creates a form asking for user input."""
    form = SearchForm()
    return render_template('index.html', form = form)

@app.route('/results', methods = ['POST', 'GET'])
def results():
    """Uses information gathered from index.html's form to request data from the Skyscanner API."""
    global formData, currency, quotes

    # Creates a dropdown box that is used to sort the entries of the table
    sorter = ResultSortSelect()

    # Parses information from index.html's form, then uses search() from searchHandler.py to create a dictionary
    # of quotes, which is passed to results.html
    formData = request.form
    currency = formData["Currency"]
    quotes = search(formData)
    return render_template('results.html', arrow = arrow, currency = currency, quotes = quotes, sorter = sorter)

@app.route('/results/sorted', methods = ['POST', 'GET'])
def results_sorted():
    global currency, quotes

    # Creates a dropdown box that is used to sort the entries of the table
    sorter = ResultSortSelect()

    # Takes the selected option from the box, and uses it and information from /results to created a sorted
    # dictionary of quotes
    sorterData = request.form
    criteria = sorterData["Sorting"]
    quotes = sortResults(quotes, criteria, currency)
    return render_template('results.html', arrow = arrow, currency = currency, quotes = quotes, sorter = sorter)


