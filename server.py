#!flask/bin/python
from flask import Flask, send_from_directory, request, jsonify, render_template, make_response, Response
from py2neo import authenticate, Graph
import json
import numpy as np
import cStringIO
import matplotlib.pyplot as plt
import datetime as dt
import calendar
import pandas as pd
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO
from datetime import datetime

app = Flask(__name__, static_url_path='')

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "dataeng123=")

# connect to authenticated graph database
graph = Graph("http://localhost:7474/db/data/")

@app.route('/')
def index():
  return app.send_static_file('interface.html')

@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
  return send_from_directory('static/css', path)


# API calls
@app.route('/temporal_distance')
def distance2():
  return "Do something with temporal distance"

@app.route('/centrality')
def centrality():
  return "Maybe some centrality metric"

@app.route('/structure')
def structure():
	result = request.args.get('movie1')
	print result
  	return json.dumps(result)


@app.route('/content/')
def content():
    return app.send_static_file('heatmap.html')


@app.route('/timestamps_ratings/')
@app.route('/timestamps_ratings', methods=['GET'])
def heatmap_movie():
    def timestamp_to_date(x):
        return datetime.utcfromtimestamp(
            int(x)
        ).strftime('%Y%m%d')
    def date_to_timestamp(year, month, day):
        s = "{0}/{1}/{2}".format(day,month,year)
        return calendar.timegm(datetime.strptime(s, "%d/%m/%Y").timetuple())
    if request.method == 'GET':
        movie_title = request.args.get('movie_title')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        if movie_title is not None or date_from is not None or date_to is not None:
            timestamp_date_from = date_to_timestamp(date_from[:4], date_from[4:6], date_from[6:8])
            timestamp_date_to = date_to_timestamp(date_to[:4], date_to[4:6], date_to[6:8])
            print 'timestamp_date_from: ', timestamp_date_from
            print 'timestamp_date_to: ', timestamp_date_to
            print 'The title is {0}'.format(movie_title)
            print 'The date_from is {0}'.format(date_from)
            print 'The date_to is {0}'.format(date_to)
        else:
            print 'Missing some parameters'
            movie_title = 'Toy Story (1995)'
            timestamp_date_from = 822873600 # 1996 Jan to 1996 Dec
            timestamp_date_to = 851990400 #1454045658
    else:
        movie_title = 'Toy Story (1995)'
        timestamp_date_from = 822873600 # 1996 Jan to 1996 Dec
        timestamp_date_to = 851990400 #1454045658



    #connection to graph
    authenticate("localhost:7474", "neo4j", "dataeng123=")
    graph = Graph("http://localhost:7474/db/data/")
    #query
    cypher = graph.cypher
    results = cypher.execute("MATCH (m:Movie {title:{r1}})<-[e:EDITED]-(u:User) "
                             "WHERE e.` timestamp` > {t1} AND e.` timestamp` < {t2} "
                             "RETURN collect([e.` timestamp`,e.` rating`])", r1=movie_title,
                                t1= int(timestamp_date_from), t2= int(timestamp_date_to))
    #Participation of user per day
    try:
        timestamps = results[0]
        #transform

        df = pd.DataFrame(timestamps[0], columns=['Date','Comparison_Value'])
        df['Date'] = df['Date'].apply(timestamp_to_date)
        df['Comparison_Value'] = df['Comparison_Value'].apply(lambda x: 1)
        df = df.groupby("Date").sum().reset_index()
        output = StringIO.StringIO()
        return df.to_json()
    except:
        return jsonify(results=[])


@app.route('/some_dataframe.json')
def output_dataframe_csv():
    # collect_lst = [[19960101, 112],[19960102, 112],[19960103, 223],[19960104, 323],[19960105, 423]]
    def converter(x):
        return datetime.datetime.fromtimestamp(
            int(x)
        ).strftime('%Y%m%d')
    collect_lst = [[820454400, 112], [820454401, 112],[857347200, 223],[857347201, 323],[857347203, 423]]
    df = pd.DataFrame(collect_lst, columns=['Date','Comparison_Value'])
    df['Date'] = df['Date'].apply(converter)
    df['Comparison_Value'] = df['Comparison_Value'].apply(lambda x: 1)
    df = df.groupby("Date").sum().reset_index()
    output = StringIO.StringIO()
    df.to_csv(output)
    return df.to_json()
    # return Response(output.getvalue(), mimetype="text/csv")


if __name__ == '__main__':
  app.run(debug=True)

















