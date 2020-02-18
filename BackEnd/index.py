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
from datetime import datetime, date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from sqlalchemy import inspect
import os
import _thread, threading
from sqlalchemy.sql import func
basedir = os.path.abspath(os.path.dirname(__file__))


ACCESS_ID = "AKIAQGGS2CUXIVXVKJO4"
ACCESS_KEY = "8xnOcNa914FxVj3iA4K9Qjefpk84cWSvhmRzWVO+"
BUCKET_NAME = 'typito'
THREAD = [] 
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
    tags = db.Column(db.String(100))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    desc = db.Column(db.String(100))

    def __init__(self, url, tags, day, month, year, date, desc):
        self.url = url
        self.tags = tags
        self.day = day
        self.month = month
        self.year = year
        self.date = date
        self.desc = desc


class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('log_id', 'url', 'tags', 'day', 'month', 'year', "date", "desc")

image_schema = ImagesSchema()

@app.route('/')
def index():
    params = request.args
    try: 
        page = int(params.get('page')) or 1
        perPage = int(params.get('perPage')) or 8
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
    files = request.files.get('myfile')
   
    desc = request.values.get('desc')

    filename = 'API_' + files.filename
    
    try:
        data = files
        s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=data)
   
        rek = boto3.client('rekognition', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name='us-east-2')
        response = rek.detect_labels(Image={'S3Object': {'Bucket': 'typito', 'Name': filename}},
                                     MaxLabels=3, MinConfidence=80)
        lables_list = response.get('Labels')
        tags = [tags.get('Name') for tags in lables_list]

    except Exception as e:  
        tags = ["No detail Available"]
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    today = datetime.now().replace(microsecond=0)
    
    baseUrl = 'https://' + BUCKET_NAME + '.s3.us-east-2.amazonaws.com'
    final_url = "{}{}{}".format(baseUrl, '/', filename)
    
    t = threading.Thread(target=db_entry, args=(final_url, tags, day, month, year, today, desc))
    THREAD.append(t)
    t.start()
    t.join()

    return json.dumps({'status': "{} Uploaded SuccessFully :)".format(files.filename)})


def db_entry(final_url, tags, day, month, year, today, desc):
    new_entry = Images(final_url, json.dumps(tags), day, month, year, today, desc)
    db.session.add(new_entry)
    db.session.commit()


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

def give_constraints_vals(constaints_name, search_key):
    first_index_tags = search_key.find(constaints_name) + len(constaints_name)
    last_index_tags = search_key[first_index_tags:].find(" ") + first_index_tags
    if last_index_tags < first_index_tags:
        last_index_tags = len(search_key)+1
    return search_key[first_index_tags:last_index_tags]


@app.route('/search')
def search():
    params = request.args

    search_key = params.get('search')
    query = "Select * from Images"
    where_clause = "where"
    new_tag_clause=""
    if "tag:" in search_key:
        all_tags = give_constraints_vals("tag:", search_key)
        tags = all_tags.split(',')
        tags_query_list= list()
        for tag in tags:
            tags_query_list.append( "tags LIKE '%{}%'".format(tag))
        
        new_tag_clause = " or ".join(tags_query_list)

        tags_with_or = "|".join(tags)    

        query = "{} {} {}".format(query, where_clause, new_tag_clause)

    if "date" in search_key:
        date_val = give_constraints_vals("date:", search_key)
        day = date_val.split('-')[0]
        month = date_val.split('-')[1]
        year = date_val.split('-')[2]

        if '*' not in day:
            day_clause = "day = {}".format(day)
            if where_clause in query:
                query = "{} {} {}".format(query, "and", day_clause)
            else:
                query = "{} {} {}".format(query, where_clause, day_clause)
           
        if '*' not in month:
            month_clause = "month = {}".format(month)
            if where_clause in query:
                query = "{} {} {}".format(query, "and", day_clause)
            else:
                query = "{} {} {}".format(query, where_clause, month_clause)

        if '*' not in year:
            year_clause = "year = {}".format(year)
            if where_clause in query:
                query = "{} {} {}".format(query, "and", day_clause)
            else:
                query = "{} {} {}".format(query, where_clause, year_clause)


    from_date = '2020-01-01'
    now = datetime.now()
    to_date = '{}-{}-{}'.format(now.year, now.month, now.day)
    
    if 'from' in search_key:
        from_date = give_constraints_vals('from:', search_key)
        formatted_date = from_date.split("-")

        _year = formatted_date[2]
        _month = formatted_date[1]
        _day = formatted_date[0]
        from_date = "{}-{}-{}".format(_year, _month, _day)
    
    from_date_clause = "DATE(date) >= '{}'".format(from_date)

    if 'to' in search_key:
        to_date = give_constraints_vals("to:", search_key)
        formatted_date = to_date.split("-")
        _year = formatted_date[2]
        _month = formatted_date[1]
        _day = formatted_date[0]
        to_date = "{}-{}-{}".format(_year, _month, _day)


    to_date_clause = "DATE(date) <= '{}'".format(to_date)

    if where_clause in query:
        query = "{} {} {} {} {}".format(query, "and", from_date_clause, "and", to_date_clause)
    else:
        query = "{} {} {} {} {}".format(query, where_clause, from_date_clause, "and", to_date_clause)

    query = "{} {}".format(query, "order by log_id desc")
    urls2 = []
    try:
        with engine.connect() as con:
            rs = con.execute(query)
            for row in rs:
                urls2.append(row_to_dict(row))
    except Exception as e:
        print(e)
        urls2 = []
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
    app.run(debug=True, processes=4, threaded=False)