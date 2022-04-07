import os
import json
import time
import threading

from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import pymongo

from genetic_architecture import GeneticAlgorithm

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/data', methods=['POST'])
def data():
    mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
    mongo_db = mongoClient['ml_app']
    collection = mongo_db['process_status']

    email = request.form['emailId'] if 'emailId' in request.form else 'manpreetignite@gmail.com'
    resp_data = collection.find_one({'email': email}, {'_id': 0}) or {}
    if not resp_data:
        threaded_function(email)
        resp_data = {'email': email, 'status': 'processing'}

    # Save csv file
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']), exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{int(time.time())}_{filename}"))

    return resp_data


def threaded_function(email):
    g = GeneticAlgorithm(userEmailId=email)
    threading.Thread(target=g.train).start()


if __name__ == '__main__':
    app.run()
