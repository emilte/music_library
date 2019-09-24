import http.client
import json
import requests

sess = requests.Session()
scopes = 'playlist-modify-public user-read-private user-read-email'

redirect_uri = 'https://google.com/'
redirect_uri = 'http://localhost:8000/account/spotify/callback/'

show_dialog = 'true'

url = 'https://accounts.spotify.com/authorize'
url += '?response_type=code'
url += '&client_id=' + '6b34a08ef909414181faaedf68ec4304'
url += '&scope=' + scopes
url += '&redirect_uri=' + redirect_uri
url += '&show_dialog=' + show_dialog

print(url)

r = sess.get(url)
print(r.status_code, r.reason)
print(r.request)
print(r.text)


# h = {
#     'csrfmiddlewaretoken': csrf,
#     'tittel': 'hh',
#     'artist': 'fgfg',
#     'bpm': '60',
#     'spotify_URL': 'hh',
#     'spotify_URI': 'hh',
#     'tags': 'hh',
# }


# r = sess.post('https://swingkurs.herokuapp.com/songs/add/', data=h)
#
# print(r.status_code, r.reason)
# print(r.request.body)

# conn = http.client.HTTPSConnection("swingkurs.herokuapp.com")
#
# conn.request(method='GET', url='/songs/add/')
# r = conn.getresponse()
# data = r.read()
# print(data)
#
# h = {
#     'csrfmiddlewaretoken': 'nUHLddrSbVBRAFnuuGXto6oMEWcgQPjPmeaMtDUxFbTqJTl4AI7yZqV2u5jUnnP0',
#     'tittel': 'hh',
#     'artist': 'fgfg',
#     'bpm': '60',
#     'spotify_URL': 'hh',
#     'spotify_URI': 'hh',
#     'tags': 'hh',
# }
#
# conn.request(method='POST', url='/songs/add/', body=json.dumps(h))
# r = conn.getresponse()
# data = r.read()
#
# print(r.status, r.reason)
# #print(data)
