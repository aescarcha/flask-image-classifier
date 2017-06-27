from flask import Flask
from flask import render_template
from flask import request, send_from_directory
# import common.loader as loader
from os import listdir
from os.path import isfile, join

app = Flask(__name__)
app.config['imageFolder'] = 'images'
app.config['labels'] = ['smoker', 'non smoker', 'teapot']

@app.route('/')
def index():
    dir = app.config['imageFolder']
    files = [f for f in listdir(dir) if (isfile(join(dir, f)) and ".jpg" in f )]

    return render_template('imagelist.html', images=files, config = app.config )


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)