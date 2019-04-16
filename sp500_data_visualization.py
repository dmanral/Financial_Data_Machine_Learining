# This is a simple example of correlation. I wouldn't use this for actual anything.
# When you have the correlation values note that the correlation range
# is between +1 and -1. The closer to 0 the more neutral it is and, the closer
# to 1 the more correlated or positively correlated it is to the other company.
# Obviously, the close to -1 the more negatively correlate.
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    # Here is a test to see if we can access data.
    # df['AAPL'].plot()
    # plt.show()

    # This will create correlation table of our data frame.
    df_corr = df.corr()

    # Visualizing correlated data.
    data = df_corr.values           # The numpy array of columns and rows or inner data.
    fig = plt.figure()              # This is our figure.
    ax = fig.add_subplot(1,1,1)     # Define our axis. It means 1 x 1 and plot number 1.

    # Building a heatmap because there is no predetermined heatmap.
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)   # Red is negative. Yellow is neutral. Green is positive.
    fig.colorbar(heatmap)                           # Gives us a legend of the colors.

    ax.set_xticks(np.arange(data.shape[0]) +0.5, minor=False)   # (x) arranging ticks at every half mark.
    ax.set_yticks(np.arange(data.shape[1]) +0.5, minor=False)   # (y) arranging ticks at every half mark.
    ax.invert_yaxis()   # y-axis will be on side without random gap on side.
    ax.xaxis.tick_top() # x-axis will be on top.

    # These are the same because we are checking correlation between stocks.
    column_labels = df_corr.columns     # Stock symbols
    row_labels = df_corr.index          # Stock symbols

    ax.set_xticklabels(column_labels)   # x-axis row_labels
    ax.set_yticklabels(row_labels)      # y-axis labels

    plt.xticks(rotation=90)             # By default x-lables are horizontal, but we want verticle so its not squished.
    heatmap.set_clim(-1,1)              # Limit of the colors. -1 is the min and 1 is the max.
    plt.tight_layout()                  # Might clean it up a little.
    plt.show()

visualize_data()
