import requests
from skyscannerDB import *
import arrow

def search(form):
    """
    Searches for quotes matching a user's input using the Skyscanner API.

            Parameters:
                    form (ImmutableMultiDict): An ImmutableMultiDict containing a user's input

            Returns:
                    newQuotes (list): A list made up of dictionaries, each of which represents a quote
    """
    # 'values' is made up of currency, place of origin, destination, outbound date and inbound date in that order
    values = [form[key] for key in ["Currency", "Origin", "Destination", "OutboundDate", "InboundDate"]] 

    # Creates a url based on the contents of 'values'
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0"\
    + "/US/{}/en-US/{}/{}/{}".format(*values[0:-1])

    # Checks if the URL is valid 
    try:
        # URL is valid; the contents of the request are split into three lists containing quotes, airlines 
        # and origins/destinations respectively
        if values[-1]:
            theJSON = requests.request("GET", url + "/" + values[-1], headers = headers).json()
        else:    
            theJSON = requests.request("GET", url, headers = headers, params = {"inboundpartialdate": values[-1]}).json()
        quotes = theJSON['Quotes']
        carriers = theJSON['Carriers']
        places = theJSON['Places']
    except KeyError:
         # URL is invalid; returns an empty list, which will stop the app from returning data later
        return []

    newQuotes = []
    # Creates a new quote dictionary for each quote retrieved from the request
    for quote in quotes:
        legs = ["OutboundLeg"]
        # Checks if the user asked for one-way flights or not
        if "InboundLeg" in quote.keys():
            legs.append("InboundLeg")
        
        newQuote = {}
        newQuote["QuoteId"] = quote["QuoteId"]

        # Uses formatCurrency() to display prices in a human-readable format
        newQuote["MinPrice"] = formatCurrency(values[0], quote["MinPrice"]) 
        newQuote["Direct"] = quote["Direct"]
        
        for leg in legs:
            newQuote[leg] = {"Carriers": [], "Origin": "", "Destination": "", "DepartureDate": ""}
            # Matches the CarrierId of a carrier to the CarrierIds in one of the legs of a quote
            for carrier in carriers:
                if carrier["CarrierId"] in quote[leg]["CarrierIds"]:
                    newQuote[leg]["Carriers"].append(carrier['Name'])
            # Matches the PlaceId of a place to the OriginId and DestinationId of one of the legs of a quote
            for place in places:
                if place['PlaceId'] == quote[leg]['OriginId']:
                    newQuote[leg]['Origin'] = place['Name']
                elif place['PlaceId'] == quote[leg]['DestinationId']:
                    newQuote[leg]['Destination'] = place['Name']
            newQuote[leg]["DepartureDate"] = quote[leg]["DepartureDate"]

        newQuote["QuoteDateTime"] = quote["QuoteDateTime"]

        # Adds new quote to the list of new quotes after construction is complete
        newQuotes.append(newQuote)

    return newQuotes


def sortResults(results, criteria, currency):
    """
    Sorts a list of quotes according to a user's selected criteria.
    
            Parameters:
                    results (list): A list of quotes passed by search()
                    criteria (str): The criteria by which 'results' is sorted
                    currency (str): The code of the currency in which the prices in 'results' are displayed

            Returns:
                    results (list): The sorted version of 'results'
    """
    if criteria == "PriceLowToHigh":
        # Uses revertCurrency() to change formatted strings of money back into numbers, so they can be used to sort quotes
        results = sorted(results, key = lambda item: revertCurrency(item['MinPrice'], currency))
    elif criteria == "PriceHighToLow":
        results = sorted(results, key = lambda item: revertCurrency(item['MinPrice'], currency), reverse = True)
    elif criteria == "DepartureDate":
        results = sorted(results, key = lambda item: item['OutboundLeg']['DepartureDate'])
    elif criteria == "ReturnDate":
        # Checks if a ReturnDate exists, as this determines whether or not the flight is one-way
        try:
            results = sorted(results, key = lambda item: item['InboundLeg']['DepartureDate'])
        except:
            results = results
    
    return results
        