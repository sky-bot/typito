# from flask import Flask, jsonify
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return jsonify({"abount":"Hello World!"})

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request 
import boto3
ACCESS_ID = "AKIAQGGS2CUXE3JTWO4S"
ACCESS_KEY="vKNIlIGE1vrV+PZdMb/FtFCXzfjIeFBZv2WR8xd8"
app = Flask(__name__)

@app.route('/')
def index():
    return '''<form method=POST enctype=multipart/form-data action="upload">
    <input type=file name=myfile>
    <input type=submit>
    </form>'''

@app.route('/upload', methods=['POST'])
def upload():
    s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

    s3.Bucket('typito').put_object(Key='API/a_python_filev2.py', Body=request.files['myfile'])

    return '<h1>File saved to S3</h1>'

if __name__ == '__main__':
    app.run(debug=True)