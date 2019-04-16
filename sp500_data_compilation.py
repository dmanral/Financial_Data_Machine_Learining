import pickle
import pandas as pd
# Combining the individual data into one csv. We are just going to use the
# adjusted close, but there are different datas avaible such as:
# date, high, low, close, volume, and Adj close.

def compile_data():
    # We are getting the latest updated ticker symbols.
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    # Creating our data frame.
    main_df = pd.DataFrame()        # Start with an empty data frame.
    for count, ticker in enumerate(tickers):    # Enumerate lets us count things. Count tells us where we are.
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)  # Rename Adj Close to the ticker symbol.
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)    # Remove columns we are not using.

        # Each of these data frames are now just is just the Adj Close price called by their ticker.
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')     # 'How' makes sure we dont lose data.

        # This is just to see whats going on and you can remove it.
        if count % 10 == 0:
            print(count)        # Counts tickers by 10 and tells us where we are.

    print(main_df.head())       # Just gives us the first 5, you can remove this as well.
    main_df.to_csv('sp500_joined_closes.csv')

# This will create a new csv file with just the Adj closes.
# Date will be row header and ticker symbol will be column header.
# NaN(Not a number) means there is no data available for that date.
compile_data()
