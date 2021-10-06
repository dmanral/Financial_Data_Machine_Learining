# This is if you wanted both the ticker and the sector.
# The sector could be helpful for analysis between sector related stocks.
# These help get list from wiki.
import bs4 as bs        # Beautiful soup for web scraping.
import pickle           # Searilizes any python object. Aka pickling/saves data in an efficient manner.
import requests
# These help with getting data from yahoo.
import datetime as dt
import os               # Create new directories.
import pandas as pd
import pandas_datareader.data as web

# Getting all the ticker symbols for S&P 500 companies from Wikipedia.
# This will save the S&P 500 list so we dont have to go to Wikipedia everytime we run this program.
# It will create a pickle file called sp500tickers.pickle which has all of the
# S&P 500 companies' ticker symbols.
# I would probably try and run this once every year as the company line up
# changes from year to year.
def save_sp500_tickers_sectors():
    # Get S&P 500 list source code from Wikipedia.
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # Beautiful soup object. response.text = text of source code.
    soup = bs.BeautifulSoup(response.text, "lxml")
    # Table data or find a specific table we need by class because there are other tables on the page.
    table = soup.find('table', {'class':'wikitable sortable'})
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # Difference between sp500_datacollection_2.py and sp500_datacollection.py
    # Empty ticker and sector dictionary.
    tickers_sector = {}
    for row in table.findAll('tr')[1:]:     # We dont need the first row because it is column titles.
        key = row.findAll('td')[1].text     # The symbols are in the 2nd row. (first_row = 0, second_row = 1, ..., etc.)
        value = row.findAll('td')[3].text   # Sector as value.
        tickers_sector[key] = value         # Adding the key and value to dictionary.
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    # Saving the data gathered for future use as sp500tickers.pickle.
    with open("sp500tickers_sectors.pickle", "wb") as f:    # Opening pickle so we can write in it.
        pickle.dump(tickers_sector, f)                     # Adding the tickers list to f aka pickle file.

    return tickers_sector

# save_sp500_tickers_sectors()                  # This will create the pickle file.

#Check to see if it created.
# pickle_in = open("sp500tickers_sectors.pickle", "rb")
# example_dct = pickle.load(pickle_in)
# print(example_dct['AAPL'])


# Now that we have all the companies we need to find data of we can collect the data we need.
def get_data_from_yahoo(reload_sp500=False):    # Since we are not calling previous function.
    if not reload_sp500:
        tickers_sectors = save_sp500_tickers_sectors()          # We will call it here if we need to.
    else:
        with open("sp500tickers_sectors.pickle", "rb") as f:    # We are reading the file since it already has symbols in it.
            tickers_sectors = pickle.load(f)

    # Take all the stock data and store them into their own directories in a csv file.
    # We want to do this because it takes way too long to do it everytime because of the size of the data.
    if not os.path.exists('stock_dfs'):  # Checking to see if stock_dfs directory exists.
        os.makedirs('stock_dfs')        # If it doesnt exist, then make it.

    # We are setting the data length.
    start = dt.datetime(2009, 1, 1)
    end = dt.datetime.today()

    for ticker in tickers_sectors:  # Traversing all the keys which are the tickers.
        print(ticker)           # This is just to make sure it is working. You can comment this out.
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            # Had to replace just ticker with ticker.replace('.','-') because of tickers with '.' in them.
            df = web.DataReader(ticker.replace('.','-'), 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}!'.format(ticker))

get_data_from_yahoo()
