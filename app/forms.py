from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """A form that takes a user's queries about quotes. All fields excpet InboundDate are required."""
    Currency = StringField("Currency", validators = [DataRequired()])
    Origin = StringField("Origin", validators = [DataRequired()])
    Destination = StringField("Destination", validators = [DataRequired()])
    OutboundDate = StringField("Outbound Date", validators = [DataRequired()])
    InboundDate = StringField("Inbound Date")
    Submission = SubmitField("Search!")

class ResultSortSelect(FlaskForm):
    """A dropdown box that allows a user to choose how to sort a table of quotes."""
    choices = [
                    ("PriceLowToHigh", "Minimum Price (cheapest to most expensive)"), 
                    ("PriceHighToLow", "Minimum Price (most expensive to cheapest)"), 
                    ("DepartureDate", "Outbound Date"),
                    ("ReturnDate", "Inbound Date")        
    ]
    Sorting = SelectField("Sort by:", choices = choices)
    Submission = SubmitField("Sort!")


