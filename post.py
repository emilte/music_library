import http.client
import json
import requests

sess = requests.Session()
r = sess.get('https://swingkurs.herokuapp.com/songs/add')
print(r.status_code, r.reason)
print(r.cookies['csrftoken'])
csrf = r.cookies['csrftoken']

h = {
    'csrfmiddlewaretoken': csrf,
    'tittel': 'hh',
    'artist': 'fgfg',
    'bpm': '60',
    'spotify_URL': 'hh',
    'spotify_URI': 'hh',
    'tags': 'hh',
}


r = sess.post('https://swingkurs.herokuapp.com/songs/add/', data=h)

print(r.status_code, r.reason)
print(r.request.body)

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
