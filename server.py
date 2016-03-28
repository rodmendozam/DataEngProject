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
import datetime

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
    print 'The movie title: {0}'.format('m1')
    # print request.args.get('movie_name')
    movie_title = 'Toy Story (1995)'
    # movie_title = 'Jumanji (1995)'
    # movie_title = 'Lord of the Rings: The Return of the King, The (2003)'
    # connection properties and auth
    authenticate("localhost:7474", "neo4j", "dataeng123=")
    graph = Graph("http://localhost:7474/db/data/")
    #query
    cypher = graph.cypher
    results = cypher.execute("MATCH (m:Movie {title:{r1}})<-[e:EDITED]-(u:User) "
                                "RETURN collect([e.` timestamp`,e.` rating`])", r1=movie_title)
    try:
        timestamps = results[0]
        #transform
        def change_to_date_format(x):
            return datetime.datetime.fromtimestamp(
                int(x)
            ).strftime('%Y%m%d')
        df = pd.DataFrame(timestamps[0], columns=['Date','Comparison_Value'])
        df['Date'] = df['Date'].apply(change_to_date_format)
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

















