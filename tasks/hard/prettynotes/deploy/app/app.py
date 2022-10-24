import os

import redis
from flask import Flask, g, session, render_template, redirect, request, flash, abort
from config import configure
from db import DB, Note
from uuid import uuid4

app = Flask(__name__)

app = configure(app)


def get_redis():
    return redis.Redis(app.config['REDIS_HOST'], app.config['REDIS_PORT'], db=0)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DB(get_redis())
    return db


@app.get('/')
def index_page():
    return render_template('index.html')


@app.get('/register')
def register_page():
    user = session.get('user', None)
    if user:
        return redirect('/notes')
    return render_template('register.html', user=user)


@app.post('/register')
def register_handle():
    user = session.get('user', None)
    if user:
        return redirect('/notes')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == '' or password == '':
        flash('Empty login or password', category='error')
        return render_template('register.html', user=user), 418
    db = get_db()
    if db.user_exists(username):
        flash('User already exists.')
        return render_template('register.html', user=user), 418
    db.save_user(username, password)
    session['user'] = username
    return redirect('/notes')


@app.get('/login')
def login_page():
    user = session.get('user', None)
    if user:
        return redirect('/notes')
    return render_template('login.html', user=user)


@app.post('/login')
def login_handle():
    user = session.get('user', None)
    if user:
        return redirect('/notes')

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == '' or password == '':
        flash('Empty login or password', category='error')
        return render_template('login.html', user=user), 418

    print(username, password)
    if get_db().validate_user_credentials(username, password):
        session['user'] = username
        return redirect('/notes')

    flash("User not found.")
    return render_template('login.html', user=user), 418


@app.get('/notes')
def notes():
    user = session.get('user', None)
    if not user:
        return "Authentication required", 401

    styles = ('light', 'dark')
    user_notes = get_db().get_user_notes(user)
    return render_template('notes.html', user=user, notes=user_notes, styles=styles)


@app.post('/notes')
def note_create():
    user = session.get('user', None)
    if not user:
        return "Authentication required", 401

    name = request.form.get('name', '')
    content = request.form.get('content', '')

    n = Note(name=name, content=content, author=user, id=str(uuid4()))

    get_db().save_note(user, n)
    flash('Note was saved successfully.')

    return redirect('/notes')


class NotePresenter:
    def __init__(self, note: Note):
        self.note = note

    def paragraphs(self):
        return '\n'.join(['<p>' + x + '</p>' for x in self.note.content.split('\n')])

    @property
    def html(self):
        return '''
        <div class="center">
            <h3>'{note.name}' by {note.author}</h3>
            {content}
        </div>
    '''.format(note=self.note, content=self.paragraphs())


@app.get('/note/<note_id>')
def get_note(note_id):
    note = get_db().get_note(note_id)
    if note is None:
        return "No such note", 404

    styling = request.args.get('styling', '')
    body_t = '''<body class="''' + styling + '''">
    {np.html}
    </body>
    '''
    np = NotePresenter(note)
    body = body_t.format(note=note, np=np)
    return render_template('note.html', body=body, title=note)

@app.get('/logout')
def logout_handle():
    session.clear()
    return redirect('/')


@app.before_first_request
def init_app():
    db = get_db()
    db.save_user('admin', os.getenv('ADMIN_PASSWORD', ''))
    db.save_note('admin', Note(id=str(uuid4()), name='flag', content=os.getenv('FLAG', 'test'), author='admin'))
