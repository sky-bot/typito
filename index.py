
from urllib.parse import urlparse
from flask import render_template
from flask import Flask, request 
import boto3
import util
from PIL import Image
ACCESS_ID = "AKIAQGGS2CUXIVXVKJO4" #"AKIAQGGS2CUXE3JTWO4S"
ACCESS_KEY = "8xnOcNa914FxVj3iA4K9Qjefpk84cWSvhmRzWVO+"  # "vKNIlIGE1vrV+PZdMb/FtFCXzfjIeFBZv2WR8xd8"
BUCKET_NAME = 'typito'
app = Flask(__name__)


@app.route('/')
def index():
    urls = ['https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg', 
    'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    # 'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg',
    'https://typito.s3.us-east-2.amazonaws.com/API_a_python_file20.jpeg'
    ]

    return render_template('index.html', urls=urls)

@app.route('/upload', methods=['POST'])
def upload():
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)
    
    s3.Bucket(BUCKET_NAME).put_object(Key='API_a_python_file20.jpeg', Body=request.files['myfile'])

    rek = boto3.client('rekognition', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY, region_name='us-west-2')
    response = rek.detect_labels(Image={'S3Object':{'Bucket':'typito','Name':'API_a_python_filev13.jpeg'}}, MaxLabels=10)
    # with open(request.files['myfile'], 'rb') as f:
    # image_bytes = request.files['myfile'].read()
    # image_bytes = util.resize_image( request.files['myfile'], (300, 300))
    # tag_responce = rek.detect_labels(Image = {'Bytes': image_bytes})

    baseUrl = 'https://' + BUCKET_NAME + '.s3.us-east-2.amazonaws.com'

    final_url = baseUrl + '/API_a_python_filev20.jpeg'

    return '<h3>File saved to S3, tags = {}</h3>'.format(response)


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




# https://typito.s3.us-east-2.amazonaws.com/API/a_python_filev9.jpeg
# {
#     "Version": "2012-10-17",
#     "Id": "Policy1488494182833",
#     "Statement": [
#         {
#             "Sid": "Stmt1488493308547",
#             "Effect": "Allow",
#             "Principal": "*",
#             "Action": [
#                 "s3:ListBucket",
#                 "s3:ListBucketVersions",
#                 "s3:GetBucketLocation",
#                 "s3:Get*",
#                 "s3:Put*"
#             ],
#             "Resource": [
#                 "arn:aws:s3:::typito",
#                 "arn:aws:s3:::typito/*"
#             ]
#         }
#     ]
# }