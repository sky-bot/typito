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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from sqlalchemy import inspect
import os
basedir = os.path.abspath(os.path.dirname(__file__))


ACCESS_ID = "AKIAQGGS2CUXIVXVKJO4" #"AKIAQGGS2CUXE3JTWO4S"
ACCESS_KEY = "8xnOcNa914FxVj3iA4K9Qjefpk84cWSvhmRzWVO+"  # "vKNIlIGE1vrV+PZdMb/FtFCXzfjIeFBZv2WR8xd8"
BUCKET_NAME = 'typito'
app = Flask(__name__)
flask_cors.CORS(app, expose_headers='Authorization')

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Images.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


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

    urls2 = []
    all_images = Images.query.order_by(Images.log_id.desc()).limit(30).all()
    for image in all_images:
        temp = row2dict(image)
        temp['tags'] = json.loads(temp.get('tags') or ["No data Available"])
        urls2.append(temp)
    
    urls = [{'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_IMG-20191010-WA0003.jpg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_IMG-20191010-WA0003.jpg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_IMG-20191010-WA0003.jpg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}, {'url': 'https://typito.s3.us-east-2.amazonaws.com/API_photo-1441974231531-c6227db76b6e.jpeg',
            'tags': ['tree', 'hills', 'rivers']}]

    
    


    lastIndex = min(page * perPage, len(urls2))
    return json.dumps({'result': urls2[firstIndex:lastIndex], 'count': len(urls2)})


def row2dict(row):
    d = dict()
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


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
        response = rek.detect_labels(Image={'S3Object': {'Bucket': 'typito', 'Name': filename}},
                                     MaxLabels=3, MinConfidence=80)
        lables_list = response.get('Labels')
        tags = [tags.get('Name') for tags in lables_list]

    except Exception as e:  
        print(e)  # to be replaced by logger
        tags = ["No detail Available"]

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    baseUrl = 'https://' + BUCKET_NAME + '.s3.us-east-2.amazonaws.com'
    final_url = "{}{}{}".format(baseUrl, '/', filename)

    new_entry = Images(final_url, json.dumps(tags), day, month, year)

    db.session.add(new_entry)
    db.session.commit()

    return json.dumps({'status': "Uploaded SuccessFully :)"})


def get_presighned_url(url):

    s3_object_key = urlparse(url).path
    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY
    )

    pre_signed_url = client.generate_presigned_url(
        'get_object', Params={'Bucket': BUCKET_NAME,
                              'Key': s3_object_key}, ExpiresIn=5 * 60)

    return pre_signed_url


@app.route('/search')
def search():
    params = request.args
    search_key = "*%2434"

    search_key = params.get('search')
    date = params.get('date')
    day = None
    month = None
    year = None

    if date:
        day = date.split('-')[0]
        month = date.split('-')[1]
        year = date.split('-')[2]

    query = "Select * from Images"
    looking_for = "%{}%".format(search_key)

    constaints_clause = "where"

    if search_key:
        query = "{} {} {} '{}' ".format(query, constaints_clause, "tags like", looking_for)

    if day and '*' not in month:
        day_clause = "day = {}".format(day)
        if constaints_clause in query:
            query = "{} {} {}".format(query, "and", day_clause)
        else:
           
            query = "{} {} {}".format(query, constaints_clause, day_clause)
           
    if month and '*' not in month:
        month_clause = "month = {}".format(month)
        if constaints_clause in query:
            query = "{} {} {}".format(query, "and", day_clause)
        else:
            query = "{} {} {}".format(query, constaints_clause, month_clause)

    if year and '*' not in month:
        year_clause = "year = {}".format(year)
        if constaints_clause in query:
            query = "{} {} {}".format(query, "and", day_clause)
        else:
            query = "{} {} {}".format(query, constaints_clause, year_clause)
    query = "{} {}".format(query, "order by log_id desc")
    urls2 = []
    with engine.connect() as con:
        rs = con.execute(query)
        for row in rs:
            urls2.append(row_to_dict(row))
            
    return json.dumps({'result': urls2, 'count': len(urls2)})


def row_to_dict(row):
    urls_dict = dict()
    inspector = inspect(engine)
    columns_list_of_dict = inspector.get_columns('Images')
    column = [col.get('name') for col in columns_list_of_dict]

    for col in column:
        urls_dict[col] = str(getattr(row, col))

    urls_dict['tags'] = json.loads(urls_dict.get('tags')) if urls_dict.get('tags') else "No Data Available"
    return urls_dict


if __name__ == '__main__':
    app.run(debug=True)
