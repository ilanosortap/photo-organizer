import os
from flask import Flask
import requests
from flask import request,render_template
import json
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import base64
from datetime import datetime

client = MongoClient()
db = client.stockImage
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def get_tags(path):
    api_key = 'acc_dba37e986089381'
    api_secret = '2de7869e3e57eb42edf4dc2f982a9a86'
    image_path = path

    res = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')})

    js = json.loads(res.text)
    tags = []
    for k in js['result']['tags']:
        if k['confidence'] > 40.0:
            tags.append(k['tag']['en'])
    return tags

@app.route("/")
def main():

    return render_template("myview.html",image_names=db.images.distinct('image'))

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')  #folder path
    if not os.path.isdir(target):
            os.mkdir(target)     # create folder if not exits
    image_db_table = db.images  # database table name
    if request.method == 'POST':
        for upload in request.files.getlist("upload"): #multiple image handel
            filename = secure_filename(upload.filename)
            destination = "".join([target, filename])
            upload.save(destination)
            tags = get_tags(destination)
            with open(destination, "rb") as image:
                image_string = base64.b64encode(image.read())
            now = datetime.now()
            date = now.date()
            image_db_table.insert({'image': image_string.decode('utf-8'), 'tags': tags,'date': date})   #insert into database mongo db
            os.remove(destination)

        return render_template("myview.html",image_names=db.images.distinct('image'))

@app.route('/search',methods=['POST'])
def search():
    image_db_table = db.images
    tag_to_search = request.form['Search']
    print(tag_to_search)
    date_to_search = request.form['date']
    print(date_to_search)
    if tag_to_search == "" and date_to_search == "":
        return render_template("myview.html", image_names=db.images.distinct('image'))
    elif tag_to_search == "":
        images = image_db_table.find({"date":date_to_search})
        return render_template("myview.html", image_names=images.distinct('image'))

    elif date_to_search == "":
        images = image_db_table.find( {"tags": tag_to_search})
        return render_template("myview.html", image_names=images.distinct('image'))
    else:
        images = image_db_table.find({"tags": tag_to_search,"date":date_to_search})
        return render_template("myview.html",image_names=images.distinct('image'))

if __name__ == '__main__':
    app.run()

