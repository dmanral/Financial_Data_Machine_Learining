# This is a super simple machine learning program. Again, I would not use this to
# do any real world stuff except research and practice. I do have a finance degree
# so, please don't use this as a real world trading tool.

import numpy as np
import pandas as pd
# Ignoring warning.
import warnings
from sklearn.exceptions import ConvergenceWarning
import pickle
from collections import Counter
# svm = sort vector machine, cross_validation for nice training samples, neighbors for k nearest.
from sklearn import svm, model_selection as cross_validation, neighbors
# VotingClassifier because we will use more than one and use voting to pick the best.
# RandomForestClassifier is just another calssifier.
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.neural_network import MLPClassifier

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
# Each model we create will be on per company basis, but that model is going to
# take into acount all of the companies in S&P 500.
def process_data_for_labels(ticker):
    hm_days = 7        # How many days in the future we have to make or lose 2%.
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)      # All NaN is being replaced by 0.

    # So, we are going back 30 years, however, that might not be the best thing
    # in this case because when we look at correlation different companies might
    # have changed relatiohships between themselves over time.
    for i in range(1, hm_days+1):   # We want to run through 7 days.
        # XOM_2 = ticker_twodaysfromnow
        # Shifting negatively(-i) to get future data. Future minus current divided by old.
        # New column and we will do it for everyday up to 7 days.
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker])/df[ticker]
    df.fillna(0, inplace=True)
    return tickers, df, hm_days

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02          # 2%
    for col in cols:
        # This indicates buy b/c we are saying the company's price might go up 2% in the next 7 days.
        if col > requirement:
            return 1
        # This indicates sell b/c we are saying the company's price might go down 2% in the next 7 days.
        if col < -requirement:
            return -1
    # This indicates hold b/c it might not change.
    return 0


# The 'target' column will have either a -1, 0, or 1 which represents sell, hold,
# or buy for each row.
def extract_featuresets(ticker):
    tickers, df, hm_days = process_data_for_labels(ticker)
    # df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
    #                                       df['{}_1d'.format(ticker)],
    #                                       df['{}_2d'.format(ticker)],
    #                                       df['{}_3d'.format(ticker)],
    #                                       df['{}_4d'.format(ticker)],
    #                                       df['{}_5d'.format(ticker)],
    #                                       df['{}_6d'.format(ticker)],
    #                                       df['{}_7d'.format(ticker)]
    #                                       ))
    # Eg. 'XOM_target' basically we are adding a new column to the dataframe.
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                          *[df['{}_{}d'.format(ticker, i)]for i in range(1, hm_days+1)]))

    # This will give us the spread between buy, hold, or sell.
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data Spread:', Counter(str_vals))

    # Cleaning up the data.
    df.fillna(0, inplace=True)              # Replace all nas.
    df.replace([np.inf, -np.inf], np.nan)   # Replace infinite changes (price goes from 0 to hacing a price).
    df.dropna(inplace=True)                 # Get rid of nas.

    # Create featuresets and the labels.
    df_vals = df[[ticker for ticker in tickers]].pct_change()   # Just the prices and normalized.
    df_vals = df_vals.replace([np.inf, -np.inf], 0)             # Replace infinite with 0s.
    df_vals.fillna(0, inplace=True)                             # Replace na with 0s just in case(Should have data by now!).

    X = df_vals.values                          # Capital X.
    y = df['{}_target'.format(ticker)].values   # y is what ever the taget is.

    return X, y, df

def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    # Training and testing.
    # 25% of our sample data aka split.
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,
                                                                         y,
                                                                         test_size=0.25)
    # Create a classifier.
    # clf = neighbors.KNeighborsClassifier()
    # Create multiple classifier and use voting.
    # There are other classifiers you can use for machine learning.
    # You can also tweak these algos because they all have parameters you can change
    # to have better performance.
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier()),
                            ('mlp', MLPClassifier())])

    # X is the percent change data for all of the companies.
    # y is the target so, 0, 1, or -1.
    # We are trying to use a classifier that will fit the input data to target we are setting.
    clf.fit(X_train, y_train) # Basically, trainingthe classifiers with our data.
    # If you train and are happy with the confidence, then all you have to do to
    # further predict is pickle it. This way you do not have to train the model again.
    # Pickle out the classifier, then to use it again load the classifier and do clf.predict.
    confidence = clf.score(X_test, y_test)
    print('Accuracy:', confidence)
    predictions = clf.predict(X_test)
    # What are the predictions we are making and are the skewed.
    print('Predicted spread:', Counter(predictions))

    return confidence

do_ml('AAPL')
