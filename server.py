#!flask/bin/python
from flask import Flask, send_from_directory, request, jsonify
from py2neo import authenticate, Graph
import json

app = Flask(__name__, static_url_path='')

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "root")

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

@app.route('/content')
def content():
	result = request.args.get('movie1_rating')
	print result
  	return json.dumps(result)

if __name__ == '__main__':
  app.run(debug=True)