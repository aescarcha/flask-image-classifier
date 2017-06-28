from flask import Flask
from flask import render_template
from flask import request, send_from_directory, jsonify
from flask import g

import sqlite3

# import common.loader as loader
from os import listdir
from os.path import isfile, join

DATABASE = 'db/imageClassifier.db'
DB_SCHEMA = 'db/schema.sql'

app = Flask(__name__)
app.config['imageFolder'] = 'images'
app.config['labels'] = ['smoker', 'non smoker', 'teapot']

@app.route('/')
def index():
    files = get_images()

    return render_template('imagelist.html', images=files, config = app.config )


@app.route('/images', methods=['POST'])
def save_images():
    data = request.get_json()
    result = get_or_create(data)
    print "final"
    print result
    return jsonify(result)

@app.route('/static/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


def get_images():
    imageFolder = app.config['imageFolder']
    files = [f for f in listdir(imageFolder) if (isfile(join(imageFolder, f)) and ".jpg" in f)]
    return files


def get_or_create( data ):
    print data
    existing = get_by_name( data["name"] )
    if existing:
        return existing

    create(data)
    return get_by_name( data["name"] )


def get_by_name( name ):
    return query_db('select * from images WHERE name = ?', [name], True)


def create(data):
    data["path"] = app.config['imageFolder'] + '/' + data["name"]
    conn = get_db()
    conn.cursor().execute("INSERT  INTO images (name, path) VALUES(?, ?)", [data["name"], data["path"]])
    conn.commit()


def make_dicts(cursor, row):
    print "Make dicstsss"
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    print args
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(DB_SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#Call init database on startup
init_db()
