from flask import Flask, render_template, request
import requests

app = Flask(__name__)
apikey = ''
imgurl = "https://image.tmdb.org/t/p/original"
# Variables needed for TMDb, initialising Flask application and necessary imports

@app.route('/')
def index():
	url = f"https://api.themoviedb.org/3/movie/popular?api_key={apikey}"
	r = requests.get(url, headers={"Accept":"application/json"}).json()
	# Finds url and directory where data for TMDb api

	popular = []
	for x in range(6):
		popular.append({\
	    'title' : r['results'][x]['title'],\
	    'overview' : r['results'][x]['overview'],\
	    'rating' : r['results'][x]['vote_average'],\
	    'poster_path' : r['results'][x]['poster_path'],\
	    'id' : r['results'][x]['id']})
	listlen = len(popular)
	# Limtiting to only 6 movies databases and collecting all necessary data
	# by defining an empty list and appending 6 sets of the data into it, 1 for each movie
	
	return render_template('popular.html', popular=popular, imgurl=imgurl, listlen=listlen)
	# Linking data to html with Jinja
	# Defines the variables Jinja uses in html and what it is defined to be in python

@app.route('/nowplaying')
def nowplaying():
	url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={apikey}"
	r = requests.get(url, headers={"Accept":"application/json"}).json()

	nowplaying = []
	for x in range(6):
		nowplaying.append({\
		'title' : r['results'][x]['title'],\
	    'overview' : r['results'][x]['overview'],\
	    'rating' : r['results'][x]['vote_average'],\
	    'poster_path' : r['results'][x]['poster_path'],\
	    'id' : r['results'][x]['id']})
	listlen = len(nowplaying)

	return render_template('nowplaying.html', nowplaying=nowplaying, imgurl=imgurl, listlen=listlen)
	# identical as above

@app.route('/popular')
def popular():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={apikey}"
    r = requests.get(url, headers={"Accept":"application/json"}).json()

    popular = []
    for x in range(6):
    	popular.append({\
        'title' : r['results'][x]['title'],\
        'overview' : r['results'][x]['overview'],\
        'rating' : r['results'][x]['vote_average'],\
        'poster_path' : r['results'][x]['poster_path'],\
        'id' : r['results'][x]['id']})
    listlen = len(popular)

    return render_template('popular.html', popular=popular, imgurl=imgurl, listlen=listlen)
    # identical as above

@app.route('/upcoming')
def upcoming():
    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={apikey}"
    r = requests.get(url, headers={"Accept":"application/json"}).json()

    upcoming = []
    for x in range(6):
    	upcoming.append({\
        'title' : r['results'][x]['title'],\
        'overview' : r['results'][x]['overview'],\
        'rating' : r['results'][x]['vote_average'],\
        'poster_path' : r['results'][x]['poster_path'],\
        'id' : r['results'][x]['id']})
    listlen = len(upcoming)

    return render_template('upcoming.html', upcoming=upcoming, imgurl=imgurl, listlen=listlen)
    # identical as above

@app.route('/toprated')
def toprated():
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={apikey}"
    r = requests.get(url, headers={"Accept":"application/json"}).json()

    toprated = []
    for x in range(6):
    	toprated.append({\
        'title' : r['results'][x]['title'],\
        'overview' : r['results'][x]['overview'],\
        'rating' : r['results'][x]['vote_average'],\
        'poster_path' : r['results'][x]['poster_path'],\
        'id' : r['results'][x]['id']})
    listlen = len(toprated)

    return render_template('toprated.html', toprated=toprated, imgurl=imgurl, listlen=listlen)
    # identical as above

@app.route('/movies/<id>')
def movie(id):
	url = f"https://api.themoviedb.org/3/movie/{id}?api_key={apikey}"
	recommendations = f"https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={apikey}"
	credits = f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={apikey}"
    
	maindata = requests.get(url, headers={"Accept":"application/json"}).json() # Movie information
	recdata = requests.get(recommendations, headers={"Accept":"application/json"}).json() # recommended data
	creddata = requests.get(credits, headers={"Accept":"application/json"}).json() # credits data
	# Finding urls and directories where data for TMDb api
	
	data = {
    	'rating' : maindata['vote_average'],
    	'title' : maindata['original_title'],
    	'poster' : maindata['poster_path'],
    	'backdrop' : maindata['backdrop_path'],
    	'date' : maindata['release_date'],
    	'runtime' : maindata['runtime'],
    	'revenue' : maindata['revenue'],
    	'overview' : maindata['overview'],
    	'trailer' : maindata['overview']}
    # Collecting all necessary information for the movie

	rate = data['rating']
	if rate <= 2:
	    rating = "Rotten"
	if rate > 2 and rate <= 4:
	    rating = "Lousy"
	if rate > 4 and rate <= 6:
	    rating = "Mediocre"
	if rate > 6 and rate <= 8:
	    rating = "Good"
	if rate > 8 and rate <= 9:
	    rating = "Great"
	if rate > 9:
	    rating = "Superb"
	# Assigning captions corresponding to movie rating as per criteria
	# Sets conditions of what rating range each caption is  

	credits = []
	for x in range(6):
		credits.append({\
	    'character' : creddata['cast'][x]['character'],\
	    'name' : creddata['cast'][x]['name']})
	listlength = len(credits)
	# Finds first 6 cast mentioned and necessary data for the particular movie

	url = f'https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={apikey}&language=en-US&page=1'
	recommendation = []
	for x in range(6):
		try:
			recommendation.append({\
		    'poster_path' : recdata['results'][x]['poster_path'],\
		    'id' : recdata['results'][x]['id']})
		except IndexError as e:
			print(f"{IndexError}: {e}")
		# Adds an exception if movie cannot be reached, doesn't break the site and prints it to the output log 
	listlen = len(recommendation)
	# Limits to 6 movies being recommended to the user to display

	return render_template('movies.html', data=data, imgurl=imgurl, rating=rating, recommendation=recommendation, credits=credits, listlen=listlen, listlength=listlength) 

@app.route('/search')
def search():
	data = request.args.get('search')

	url = f"https://api.themoviedb.org/3/search/movie?api_key={apikey}&query={data}&page=1"
	# defines user terms and injects into url for searching

	try:

		response = requests.get(url, headers={"Accept":"application/json"}).json()

		for x in range(len(response['results'])):
			if response['results'][x]['poster_path'] == None:
			 response['results'][x]['poster_path'] = 'no_image_available.png'
		# Looks for poster, if cannot be found, text is displayed

		data = []
		for x in range(18):
			data.append({\
		    'title' : response['results'][x]['title'],\
		    'overview' : response['results'][x]['overview'],\
		    'rating' : response['results'][x]['vote_average'],\
		    'poster_path' : response['results'][x]['poster_path'],\
		    'id' : response['results'][x]['id']})
		listlen = len(data)
		# finds all necessary data for each movie

	except IndexError:
		data=[]
		listlen=0
	# Exception if no results are found, displays empty page instead of error

	return render_template("search.html", data=data, imgurl=imgurl, listlen=listlen)
	# Linking python data to html via Jinja

if __name__ == '__main__':
    app.run(debug=True)
    #End Flask contents, runs the web application