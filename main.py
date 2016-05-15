import tweepy
import re
from bottle import route, request, run
import json

def auth():
	consumer_key = ''
	consumer_secret = ''
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

	return auth


def find_id(url):
	url = url.replace("https://twitter.com/", "").split("/")

	return url[2]


def status(api, url):
	print("Url du Tweet " + url)
	id = find_id(url)
	print("id du Tweet : " + id)
	status = api.get_status(id).text
	print("Tweet : " + status)
	return status


def search(api, tweet):
	r = status(api, tweet)
	url = re.sub('https([A-Za-z0-9:\/\/\.]*)', '', r)
	print("Tweet sans les liens : " + url)
	print("")

	#search = api.search(q = url, count = 200)
	search = tweepy.Cursor(api.search, q = url).items(50000)

	return search

@route('/')
def home():
	return '''
		<h1>Plagiat Twitter</h1>
		<p>Une solution simple pour voir si un tweet est/ a été plagié.</p>
		<form action="/" method="post">
			Lien du tweet <input name="tweet" type="text" required/>
			<input value="Search" type="submit" />
		</form>
	'''

@route('/', method='post')
def twitter():
	tweet = request.forms.get('tweet')

	api = tweepy.API(auth())

	recherche = search(api, tweet)
	dico = {}
	
	for s in recherche:
		if 'rt @' not in s.text.lower():
			dico[s.id] = "http://twitter.com/" + s.user.screen_name + "/status/" + str(s.id) 
	return json.dumps(dico)
			#return s.user.screen_name + " -> http://twitter.com/" + s.user.screen_name + "/status/" + str(s.id)


if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)