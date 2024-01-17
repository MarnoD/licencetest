# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg
from scipy.spatial import distance


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/get_similar', methods=['POST'])
def cosine_similarity():
    data = request.json
    query_vector = data['query_vector']
    vector_text_pairs = data['vectors']

    # Extract embeddings and their corresponding texts
    vectors = [pair['embeddings'] for pair in vector_text_pairs]
    texts = [pair['text'] for pair in vector_text_pairs]

    # Calculate cosine similarity for each vector
    # Return the index of the most similar vector
    most_similar_index = max(range(len(vectors)), key=lambda index: 1 - distance.cosine(query_vector, vectors[index]))

    return jsonify({'most_similar_text': texts[most_similar_index]})

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def extract_vehicle_info(data):
    reg_number_pattern = r'%([A-Z0-9]+)%'
    color_pattern = r'%([a-zA-Z\s/]+)%'
    brand_pattern = r'%([A-Z]+)%'
    series_pattern = r'%([a-zA-Z0-9\s]+)%'

    reg_number_match = re.search(reg_number_pattern, data)
    color_match = re.search(color_pattern, data)
    brand_match = re.search(brand_pattern, data)
    series_match = re.search(series_pattern, data)

    if reg_number_match and color_match and brand_match and series_match:
        registration_number = reg_number_match.group(1)
        color = color_match.group(1)
        brand = brand_match.group(1)
        series = series_match.group(1)

        return {
            'Registration Number': registration_number,
            'Color': color,
            'Brand': brand,
            'Series': series
        }
    else:
        return None

@app.route('/api/extract-vehicle-info', methods=['POST'])
def api_extract_vehicle_info():
    data = request.json.get('data')

    if data:
        result = extract_vehicle_info(data)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Could not extract vehicle information.'}), 400
    else:
        return jsonify({'error': 'No data provided in the request.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
