import boto3
from urllib.parse import urlparse
from flask import render_template
from flask import Flask, request, jsonify
import flask_cors 
import json
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

from PIL import Image
ACCESS_ID = "AKIAQGGS2CUXIVXVKJO4" #"AKIAQGGS2CUXE3JTWO4S"
ACCESS_KEY = "8xnOcNa914FxVj3iA4K9Qjefpk84cWSvhmRzWVO+"  # "vKNIlIGE1vrV+PZdMb/FtFCXzfjIeFBZv2WR8xd8"
BUCKET_NAME = 'typito'
app = Flask(__name__)
flask_cors.CORS(app, expose_headers='Authorization')

basedir = os.path.abspath(os.path.dirname(__file__))

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Images.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
    
class Images(db.Model):
    
    log_id = db.Column(db.Integer, primary_key= True)
    url = db.Column(db.String(100), unique=True)
    tags = db.Column(db.String(100), unique=True)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __init__(self, url, tags, day, month, year):
        self.url = url
        self.tags = tags
        self.day = day
        self.month = month
        self.year = year
    
class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('log_id', 'url', 'tags', 'day', 'month', 'year')

image_schema = ImagesSchema()

@app.route('/')
def index():
    params = request.args
    try: 
        page = int(params.get('page')) or 1
        perPage = int(params.get('perPage')) or 4
    except TypeError as e:
        page = 1
        perPage = 8
    firstIndex = (page-1)*perPage
    lastIndex = page*perPage
   
  
    urls = [{'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_IMG-20191010-WA0003.jpg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_IMG-20191010-WA0003.jpg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_IMG-20191010-WA0003.jpg',
            'tags': ['tree', 'hills', 'rivers']},{'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}]

    return json.dumps({'result': urls[firstIndex:lastIndex], 'count': len(urls)})

@app.route('/upload', methods=['POST'])
def upload():
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)
    file = request.files['myfile']
    
    filename = 'API_' + file.filename
    print(filename)
    try:
        data = request.files['myfile']
        s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=data)
   
        rek = boto3.client('rekognition', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name='us-east-2')
        response = rek.detect_labels(Image={'S3Object':{'Bucket':'typito','Name': filename}}, MaxLabels=3, MinConfidence = 80)
        lables_list = response.get('Labels')
        tags = [tags.get('Name') for tags in lables_list]
        
        print(tags)
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
       

    except Exception as e:  
        print(e)

    baseUrl = 'https://' + BUCKET_NAME + '.s3.us-east-2.amazonaws.com'
    final_url = "{}{}{}".format(baseUrl,'/',filename)
    print(tags, final_url, day, month, year)
    new_entry = Images(final_url, json.dumps(tags), day, month, year)
    db.create_all()
    db.session.add(new_entry)
    db.session.commit()

    return json.dumps({'status':"Uploaded SuccessFully :)"})


def get_presighned_url(url):

    s3_object_key = urlparse(url).path
    # s3_object_key = s3_object_key.replace('/', "", 1)
    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY
    )

    pre_signed_url = client.generate_presigned_url(
        'get_object', Params={'Bucket': BUCKET_NAME,
                              'Key': s3_object_key}, ExpiresIn=5 * 60)

    return pre_signed_url


if __name__ == '__main__':
    app.run(debug=True)

# API_IMG_20190629_145722.jpg
# API_IMG_20190629_145722.jpg