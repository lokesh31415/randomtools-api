from flask import Flask, jsonify
from helpers.compress import compress_pdf

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1> Welcome To RandomTools <h1>"


@app.route('/compress/<string:name>')
def compress(name: str):
    if name == 'pdf':
        pass
        # compress_pdf('file')
    return {"status": "uploaded successfully, compressing {}".format(name)}


app.run(port=4200)