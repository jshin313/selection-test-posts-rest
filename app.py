# Based off of https://impythonist.wordpress.com/2015/07/12/build-an-api-under-30-lines-of-code-with-python-and-flask/
# since I didn't know too much about Flask

#!/usr/bin/python3

from ingester import ingest

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from pathlib import Path



# Convert xml file to sqlite database if it doesn't exist
if not Path("./posts.db").is_file():
    ingest()


e = create_engine('sqlite:///posts.db')

app = Flask(__name__)
api = Api(app)

class Posts(Resource):
	def get(self):
		args = request.args
		print(args)

		conn = e.connect()
		
		# Default behavior is returned based on creation date
		if len(args) == 0:
			query = conn.execute("""SELECT * FROM posts ORDER BY datetime(CreationDate) DESC """)
		# Returns results sorted by view count
		elif args.get('byViewCount') == 'true':
			query = conn.execute("""SELECT * FROM posts ORDER BY ViewCount ASC """)
		# Returns results sorted by score
		elif args.get('byScore') == 'true':
			query = conn.execute("""SELECT * FROM posts ORDER BY Score ASC """)
		elif args.get('search') is not None:
			searchQuery = args['search']
			# https://stackoverflow.com/a/59440990
			query = conn.execute("""SELECT * FROM posts WHERE (body LIKE '%'||?||'%' OR title LIKE '%'||?||'%')""", (searchQuery, searchQuery))
		elif args.get('searchTitle') is not None:
			searchQuery = args['searchTitle']
			query = conn.execute("""SELECT * FROM posts WHERE title LIKE '%'||?||'%'""", (searchQuery, ))
		elif args.get('searchBody') is not None:
			searchQuery = args['searchBody']
			query = conn.execute("""SELECT * FROM posts WHERE body LIKE '%'||?||'%'""", (searchQuery, ))

		# Return formatted as json cause why not? Most REST APIs I've seen use JSON
		result = {'results': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result

api.add_resource(Posts, '/posts')

if __name__ == '__main__':
    app.run()
