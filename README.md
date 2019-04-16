# Financial Data and Machine Learining
Collecting data and using it for different things in python.

## Part 1: (sp500_data_collection.py and sp500_data_collection_2.py) ##
  - We start by scrubbing the S&P 500 Wikipedia page to get the ticker symbols for the companies that are in S&P 500.
  - We then use pickling to searilize the ticker symbols. (sp500tickers.pickle and sp500tickers_sectors.pickle)
  - We then use the pickle file to collect data from Yahoo Finance. *(This takes a while depending on the date range picked and individual 
  internet speed.!!)*
  - Collecting data from Yahoo finance will create a directory called 'stock_dfs' in which there are csv files for all 
  the individual S&P 500 companies.
  - All of the companies' files are organized as follows:
  
        - First Column: Dates
        
        - Second Column: High
        
        - Third Column: Low
        
        - Fourth Column: Open
        
        - Fifth Column: Close
        
        - Sixth Column: Volume
        
        - Seventh Column: Adjusted Close

## Part 2: (sp500_data_compilation.py and sp500_data_visualization.py) ##
  - All of the data we have collected so far are in individual csv files, therefore, we need to find a way to compile them.
  - For the sake of this project I will be using just the Adjusted Close, therefore, when compiling the data we can dump the other 
  columns.
  -The compiled data is saved in a csv file and is organized as follows:
  
        - Row header: Date
        
        - Column Header: Ticker Symbol
        
        - In-between: Adjusted closing prices for that date for the individual tickers.
       
## Part 3: (sp500_data_ml.py) ##
    - This is where we can finally use our data and use the machine learning framework provided by python.
    - This is just the tip of the ice berg when it comes to machine learning. It was my first exposure to it.
    - We are hoping that the algorithms will be able to map the relationships of existing price changes to the future price changes for
    a company.
    - The output when running this file is as follows:
    
        - Data Spread : Counter({'1':#, '-1':#, '0':#})
        
        - Accuracy: 0.#
        
        - Predicted Spread: Counter({'1':#, '-1':#, '0':#})
     
 ## Source: ##
   - I basically followed the tutorial that can be found [here](https://pythonprogramming.net/getting-stock-prices-python-programming-for-finance/).
 
 ## Notes ##
   - You can actually copy and paste all of the codes in the files provided and create one long file to run.
   - Since, I did this to learn it was just more helpful for myself to seperate the files.
   - I also have a lot of comments in each of the files because writing those helped me understand it better.
   - Thank you [sentdex](https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ) for great tutorials on youtube.
