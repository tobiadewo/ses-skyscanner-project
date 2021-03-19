import requests
import sqlite3
import os

# "RAPIDAPI_KEY" is stored on Heroku as an environmental variable for security reasons
headers = {
    'x-rapidapi-key': os.environ["RAPIDAPI_KEY"],
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }


def makeDatabase():
    """Accesses skyscanner.db, and initializes all entries in the 'countries' and 'currencies' tables based on the Skyscanner API."""
    
    #Opens a connection to skyscanner.db and creates a cursor
    connection = sqlite3.connect("skyscanner.db")
    c = connection.cursor()

    # Makes the 'countries' table using results from getCountries()
    countries = getCountries()
    for country in countries:
        code, name = country["Code"], country["Name"]
        # Checks if the country already exists in the table
        if code not in [row[0] for row in c.execute("SELECT Code FROM countries")]:
            # If it doesn't, insert it
            c.execute("INSERT INTO countries VALUES (?,?)", (code, name))
        else:
            # If it does, update its values
            c.execute("UPDATE countries SET Name = ? WHERE Code = ?", (name, code))

    # Makes the 'currencies' table using results from getCurrencies()
    currencies = getCurrencies()
    for currency in currencies:
        attributes = tuple(currency.values())
        # Checks if the currency already exists in the table
        if attributes[0] not in [row[0] for row in c.execute("SELECT Code FROM currencies")]:
            # If it doesn't, insert it
            c.execute("INSERT INTO currencies VALUES (?,?,?,?,?,?,?,?)", attributes)
        else:
            # If it does, update its values
            fields = tuple(currency.keys())
            # Updates each key of the currency dict
            for r in range(len(fields)):
                c.execute("UPDATE currencies SET {} = ? WHERE Code = ?".format(fields[r]), (attributes[r], attributes[0]))

    # Saves and exits skyscanner.db
    connection.commit()
    connection.close()

def getCountries():
    """
    Returns a list of all countries supported by the Skyscanner API.
    
            Returns:
                    countries (list): A list of all countries supported by the Skyscanner API
    
    """
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/reference/v1.0/{}"
    countries = requests.request("GET", url.format("countries/en-US"), headers = headers).json()['Countries']

    return countries

def getCurrencies():
    """
    Returns a list of all currencies supported by the Skyscanner API.
    
            Returns:
                    currencies (list): A list of all currencies supported by the Skyscanner API
    
    """
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/reference/v1.0/{}"
    currencies = requests.request("GET", url.format("currencies"), headers = headers).json()['Currencies']

    return currencies

def getPlaces(place):
    """
    Checks the Skyscanner API for all destinations associated with a place.
            
            Parameters:
                    place (str): The place 

            Returns:
                    countries (list): A list of all destinations associated with 'place'
    
    """
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/US/USD/en-US/"
    querystring = {"query": place}

    return requests.request("GET", url, headers = headers, params = querystring).json()['Places']

def getCurrencyData(currency):
    """
    Searches skyscanner.db for information about a given currency.
    
            Parameters:
                    currency (str): The currency about which information is gathered

            Returns:
                    currencyData (dict): Information about 'currency' in dictionary form
    
    """

    #Opens a connection to skyscanner.db and creates a cursor
    connection = sqlite3.connect("skyscanner.db")
    c = connection.cursor()

    # Retrieves the entries of the 'currencies' table corresponding to the given currency, makes them into a list,
    # and closes skyscanner.db
    values = list([row for row in c.execute("SELECT * FROM currencies WHERE Code = ?", (currency.upper(), ))][0])
    keys = [description[0] for description in c.description]
    connection.close()

    # Creates a dictionary with the headers of the 'currencies' table as keys, and the entries corresponding
    # to the given currency as values
    currencyData = dict(zip(keys, values))
    return currencyData

def formatCurrency(currency, amount):
    """
    Formats a number into a string based on a specified currency's data
    
            Parameters:
                    currency (str): The currency that dictates how 'amount' is formatted
                    amount (float): An amount of money

            Returns:
                    display (str): The formatted amount of money
    
    """

    # Uses getCurrencyData() to retrieve a dictionary of information about the currency
    currencyData = getCurrencyData(currency)

    # Creates a string to be formatted using the str.format() method by specifying the amount of 
    # decimal places to which the number must be set
    # The thousands separator is set to "_" because the method has very limited options for what
    # that can be set to
    display = ("{:_." + str(currencyData["DecimalDigits"]) + "f}").format(amount)
    display = display.replace(".", currencyData["DecimalSeparator"])
    display = display.replace("_", currencyData["ThousandsSeparator"])

    # Checks if the symbol shoud be on the left or right of the amount, and also if one or zero spaces 
    # should be between the symbol and amount
    if currencyData["SymbolOnLeft"]:
        # If so, adds the symbol, the correct number of spaces and the partially formatted string in that order
        display = currencyData["Symbol"] + (" " * currencyData["SpaceBetweenAmountAndSymbol"]) + display
    else:
        # If not, adds the partially formatted string, the correct number of spaces and the symbol in that order
        display = display + (" " * currencyData["SpaceBetweenAmountAndSymbol"]) + currencyData["Symbol"]

    return display

def revertCurrency(display, currency):
    """
    Changes a string created by formatCurrency() back into a number.
    
            Parameters:
                    display (str): The formatted amount of money 
                    currency (str): The currency 'display' is in
                    
            Returns:
                    amount (float): The amount of money as a number
    
    """    
 
    # Uses getCurrencyData() to retrieve a dictionary of information about the currency
    currencyData = getCurrencyData(currency)

    # Replaces symbol and thousands-separator with empty strings, and then changes decimal-separator to a decimal point
    display = display.replace(currencyData["Symbol"], "")
    display = display.replace(currencyData["ThousandsSeparator"], "")
    display = display.replace(currencyData["DecimalSeparator"], ".")
    
    # Turns the string into a float
    # The space created by "SpaceBetweenAmountAndSymbol" can stay because float() strips the string before conversion
    amount = float(display)
    return amount