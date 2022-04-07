import os
import json
import time
import threading
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import pymongo

from genetic_architecture import GeneticAlgorithm

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/data', methods=['POST'])
def data():
    mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
    mongo_db = mongoClient['ml_app']
    collection = mongo_db['process_status']

    # Save csv file
    if 'file' in request.files:
        file = request.files['file']
        print(file.filename)
        if file.filename != '':
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file_uploaded_name = os.path.join(app.config['UPLOAD_FOLDER'], f"{int(time.time())}_{filename}")
                file.save(file_uploaded_name)

    email = request.form['emailId'] if 'emailId' in request.form else 'manpreetignite@gmail.com'
    threaded_function(email, file_uploaded_name)
    resp_data = {'email': email, 'status': 'processing'}

    return resp_data


def threaded_function(email,file_uploaded_name):
    #reading data
    data = pd.read_csv(file_uploaded_name, header=None, skiprows=1)
    data = data.sample(frac=1).reset_index(drop=True)

    #train test split
    train, test = train_test_split(data, test_size=0.2)
    train_labels = train.iloc[:, 0]
    test_labels = test.iloc[:, 0]
    del train[0]
    del test[0]

    # normalizing data
    column_maxes = train.max()
    df_max = column_maxes.max()
    train = train / df_max

    # normalizing data
    column_maxes = test.max()
    df_max = column_maxes.max()
    test = test / df_max

    train = np.asarray(train).astype('float32')
    test = np.asarray(test).astype('float32')

    g = GeneticAlgorithm(userEmailId=email, train_data=train, test_data=test, test_labels=test_labels, train_labels=train_labels, inputneuron=request.form['inputNeurons'], outputneuron=request.form['outputNeuron'])
    threading.Thread(target=g.train).start()


@app.after_request
def add_cross_origin_header(response):
    headers = {
        'Access-Control-Allow-Origin': request.headers.get('origin'),
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PATCH",
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Headers': 'Range, Content-Range, Content-Disposition, Content-Type',
        'Access-Control-Expose-Headers': 'Accept-Ranges, Content-Encoding, Content-Length, Content-Range'
    }
    for header, value in headers.items():
        if header not in response.headers:
            response.headers.add(header, value)
    return response

if __name__ == '__main__':
    app.run()

