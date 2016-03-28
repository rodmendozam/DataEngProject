from py2neo import authenticate, Graph
import json
import numpy as np
import cStringIO
import matplotlib.pyplot as plt
import datetime as dt
import calendar

import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO

import json
import numpy as np
import pandas as pd
import datetime

def converter(x):
    return datetime.datetime.fromtimestamp(
        int(x)
    ).strftime('%Y%m%d')

collect_lst = [[820454400, 112], [820454401, 112],[19960103, 223],[19960104, 323],[19960105, 423]]
df = pd.DataFrame(collect_lst, columns=['Date','Comparison_Value'])
df['Date'] = df['Date'].apply(converter)
df['Comparison_Value'] = df['Comparison_Value'].apply(lambda x: 1)
df = df.groupby("Date").sum().reset_index()

print df

# df['Date1'] = df.index
# df = df[['Date1','Comparison_Value']]


# df1 = df[['Date','Comparison_Value']]
# df = df.apply(f, axis=1)

# print df1
# print df





# @app.route('/plot_time/')
# @app.route('/plot_time', methods=['GET'])
# def plot_time():
#     plt.clf()
#     plt.style.use('ggplot')
#     x = np.array([dt.datetime(2013, 9, 28, i, 0) for i in range(24)])
#     y = np.random.randint(100, size=x.shape)
#     plt.plot(x,y)
#     f = cStringIO.StringIO()
#     plt.savefig(f, format='png')
#     # Serve up the data
#     header = {'Content-type': 'image/png'}
#     f.seek(0)
#     data = f.read()
#     return data, 200, header

# @app.route('/plot_heatmap/')
# @app.route('/plot_heatmap', methods=['GET'])
# def plot_heatmap():
#     plt.clf()
#     column_labels = [calendar.month_name[i] for i in range(1,13)]
#     # row_labels = [i+1 for i in range(30)]
#     # row_labels = ['1990','1991','1992','1993', '1994', '1995']
#     row_labels = [1900+i*100 for i in range(10)]
#     data = np.random.rand(len(column_labels),len(row_labels))
#     data = np.around(data, decimals=1)
#     fig, ax = plt.subplots()
#     fig.set_size_inches(18,8)
#     heatmap = ax.pcolor(data, cmap=plt.cm.PuRd)
#
#     # put the major ticks at the middle of each cell
#     ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
#     ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
#
#     # want a more natural, table-like display
#     ax.invert_yaxis()
#     ax.xaxis.tick_top()
#
#     ax.set_xticklabels(row_labels, minor=False)
#     ax.set_yticklabels(column_labels, minor=False)


    # for y in range(data.shape[0]):
    #     for x in range(data.shape[1]):
    #         plt.text(x + 0.5, y + 0.5, '%.1f' % data[y, x],
    #                  horizontalalignment='center',
    #                  verticalalignment='center',
    #                  )

    # plt.colorbar(heatmap)
    # f = cStringIO.StringIO()
    # plt.savefig(f, format='png', transparent=True, bbox_inches='tight', pad_inches=0)
    #
    # # Serve up the data
    # header = {'Content-type': 'image/png'}
    # f.seek(0)
    # data = f.read()
    # return data, 200, header















