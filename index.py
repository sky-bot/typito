
from urllib.parse import urlparse
from flask import render_template
from flask import Flask, request 
import boto3
ACCESS_ID = "AKIAQGGS2CUXE3JTWO4S"
ACCESS_KEY = "vKNIlIGE1vrV+PZdMb/FtFCXzfjIeFBZv2WR8xd8"
BUCKET_NAME = 'typito'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)

    s3.Bucket(BUCKET_NAME).put_object(Key='API_a_python_filev10.jpeg', Body=request.files['myfile'])
    baseUrl = 'https://' + BUCKET_NAME + '.s3.us-east-2.amazonaws.com'

    final_url = baseUrl + '/API_a_python_filev10.jpeg'

    accessible_url = get_presighned_url(final_url)

    return '<h3>File saved to S3 It saves to {}=========={}</h3>'.format(accessible_url, final_url)


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
