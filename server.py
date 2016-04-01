#!flask/bin/python
from flask import Flask, send_from_directory, request, jsonify
from py2neo import authenticate, cypher, neo4j, Graph
from py2neo.packages.httpstream import http
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
http.socket_timeout = 9999

# set up authentication parameters
# authenticate("localhost:7474", "neo4j", "givemegraphs")
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

@app.route('/static/data/<path:path>')
def send_json(path):
	return send_from_directory('static/data', path)

# API calls
@app.route('/temporal_distance')
def distance2():
	result = []
	input1 = request.args.get('movie1')
	input2 = request.args.get('movie2')

	# add CASE
	query = "MATCH (m:Movie),(n:Movie), p = shortestPath((m)-[r:RATED*..8]-(n)) WHERE ((m.movieId < 3999 AND m.movieId > 3973 AND n.movieId < 3999 AND n.movieId > 3973) OR (m.movieId < 4036 AND m.movieId > 4013 AND n.movieId < 4036 AND n.movieId > 4013)) AND m.movieId <> n.movieId  RETURN round((r[1]).timestamp/(3600*24*30.4167))*(3600*24*30.4167) AS time, count(p) AS count ORDER BY time"	
	for record in graph.cypher.execute(query):
		result.append([record.time, record.count])
	
	return json.dumps(result)
	
@app.route('/reachability')
def reachability():
	result = []
	input1 = request.args.get('movie1')
	input2 = request.args.get('movie2')
	count = 2
	queries = [#"MATCH (from:Movie {movieId:{movie1}}), (to:Movie {movieId:{movie2}}) , path = (from)-[r:RATED*0..2]-(to) RETURN r AS relations LIMIT 200",
				"MATCH (from:Movie {movieId:{movie1}}), (to:Movie {movieId:{movie2}}) , path = (from)-[r:RATED*3..4]-(to) RETURN r AS relations LIMIT 200",
				"MATCH (from:Movie {movieId:{movie1}}), (to:Movie {movieId:{movie2}}) , path = (from)-[r:RATED*5..6]-(to) RETURN r AS relations LIMIT 200",
				"MATCH (from:Movie {movieId:{movie1}}), (to:Movie {movieId:{movie2}}) , path = (from)-[r:RATED*7..8]-(to) RETURN r AS relations LIMIT 200"]

	# add CASE
	for query in queries:
		for record in graph.cypher.execute(query, parameters={"movie1": int(input1), "movie2": int(input2)}):
			array = []
			array.append(count)
			for x in range(0, len(record.relations)):
				array.append(record.relations[x].properties['timestamp'])
			result.append(array)
		print result[0]
		count = count +2
	return json.dumps(result)

@app.route('/centrality')
def centrality():
	result = []
	result1 = []
	result2 = [] 
	input1 = request.args.get('movie1')	
	input2 = request.args.get('movie2')
	query = "MATCH (m:Movie {movieId: {movie}})<-[r:RATED]-(u:User) RETURN round(r.timestamp/(3600*24*30.4167))*(3600*24*30.4167) AS time, count(*) AS count ORDER BY time"
	for record in graph.cypher.execute(query, parameters={"movie": int(input1)}):
		result1.append([record.time, record.count])
	for record in graph.cypher.execute(query, parameters={"movie": int(input2)}):
		result2.append([record.time, record.count])
	result.append(result1)
	result.append(result2)
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

















