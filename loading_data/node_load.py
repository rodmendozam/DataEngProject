from py2neo import Graph, Path, authenticate
import csv
import urllib2

class Movie(object):
    def __init__(self, user_id, movie_id, movie_title, rating, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.rating = rating
        self.timestamp = timestamp
    def to_string(self):
        return 'Movie: ', self.movie_title, 'MovieID', self.movie_id, 'Rating: ', self.rating

url_ratings = 'https://gist.githubusercontent.com/Giraphne/7b9f7f2381ca2b49a178/raw/2a3f041ee3142450636b913b8d5109d1c216c41b/ratings.csv'
url_movies = 'https://gist.githubusercontent.com/Giraphne/b485c7aae9ec1f09f05e/raw/cd7008d4d6fc4db0963a879e7bfb838977a5f435/movies.csv'

response_ratings = urllib2.urlopen(url_ratings)
cr_ratings = csv.reader(response_ratings)

response_movies = urllib2.urlopen(url_movies)
cr_movies = csv.reader(response_movies)

movie_lst = []
movies_dictionary = {}

for row in cr_movies:
    movies_dictionary[row[0]] = row[1]

print movies_dictionary


next(cr_ratings) # skip first line
for row in cr_ratings:
    movie_lst.append(Movie(row[0],row[1], movies_dictionary['1'],row[2],row[3]))
movie_lst.pop(0)



# print movie_lst[0].to_string()


# # set up authentication parameters
# authenticate("localhost:7474", "neo4j", "Rodro123=")
#
# # connect to authenticated graph database
# graph = Graph("http://localhost:7474/db/data/")
#
# # insert
# tx = graph.cypher.begin()
# for name in ["Alice", "Bob", "Carol"]:
#     tx.append("CREATE (person:Person {name:{name}}) RETURN person", name=name)
# alice, bob, carol = [result.one for result in tx.commit()]
#
# # for movie in movie_lst:
# #     tx.append("CREATE (person:Person {name:{name}}) RETURN person", name_movie=movie.)
#
# friends = Path(alice, "KNOWS", bob, "KNOWS", carol)
# graph.create(friends)
#



