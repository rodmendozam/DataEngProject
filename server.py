#!flask/bin/python
from flask import Flask, send_from_directory, request, jsonify
from py2neo import authenticate, cypher, neo4j, Graph
from py2neo.packages.httpstream import http
import json

app = Flask(__name__, static_url_path='')
http.socket_timeout = 9999

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "givemegraphs")
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
	result = []
	input1 = request.args.get('movie1')
	input2 = request.args.get('movie2')

	# add CASE
	query = "MATCH (from:Movie {movieId:{movie1}}), (to:Movie {movieId:{movie2}}) , path = (from)-[r:RATED*0..2]-(to) RETURN r AS relations LIMIT 100"	
	for record in graph.cypher.execute(query, parameters={"movie1": int(input1), "movie2": int(input2)}):
		array = []
		for x in range(0, len(record.relations)):
			array.append(record.relations[x].properties['timestamp'])
		result.append(array)
	print result
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

@app.route('/content')
def content():
	result = request.args.get('movie1_rating')
	print result
  	return result.timestamp

if __name__ == '__main__':
  app.run(debug=True)