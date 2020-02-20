import os
from flask import Flask, flash
import requests
from flask import request,render_template
import json
from pymongo import MongoClient,DESCENDING,ASCENDING
from werkzeug.utils import secure_filename
import base64
from datetime import datetime,date
from PIL import Image
from flask_toastr import Toastr



client = MongoClient("mongodb://sonali:typito1@ds239692.mlab.com:39692/heroku_bp7xlj7c", retryWrites=False)
db = client.heroku_bp7xlj7c
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
toastr = Toastr(app)
app.secret_key = "super secret key"

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

    return render_template("myview.html",image_names=db.images.find().sort("date",DESCENDING).distinct('image')[:31])

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')  #folder path
    if not os.path.isdir(target):
            os.mkdir(target)     # create folder if not exits
    image_db_table = db.images  # database table name
    if request.method == 'POST':
        if not request.files.getlist("upload"):
            flash("select some images to upload")
        for upload in request.files.getlist("upload"): #multiple image handel
            filename = secure_filename(upload.filename)
            destination = "".join([target, filename])
            try:
                upload.save(destination)
            except:
                flash("select some images to upload")
            tags = get_tags(destination)
            foo = Image.open(destination)
            foo = foo.resize((240,240),Image.ANTIALIAS)
            os.remove(destination)
            foo.save(destination)
            try:
                with open(destination,"rb") as image:
                    image_string = base64.b64encode(image.read())
            except:
                flash("Images havent been selected to upload or the selected file is not an image")

            today = datetime.today().strftime("%d-%m-%Y")
            image_db_table.insert({'image': image_string.decode('utf-8'), 'tags': tags,'date': today})   #insert into database mongo db
            os.remove(destination)

        return render_template("myview.html",image_names=db.images.find().sort("date",DESCENDING).distinct('image')[:31])

@app.route('/search',methods=['POST'])
def search():
    #tags:cats,dogs date:some from:date to date
    image_db_table = db.images
    try:
        features_to_search = request.form['Search'].split()
    except:
        flash("search query not in write format. Should be in key-value pairs, for eg: tags:dog from:19-02-2020 to:19-02-2020")
    dict = {}

    for feature in features_to_search:
        try:
            key,value = feature.split(":")
            dict[key] = value
        except:
            flash("search query not in write format. Should be in key-value pairs, for eg: tags:dog from:19-02-2020 to:19-02-2020")

    print(dict)

    if not dict:
        return render_template("myview.html", image_names=db.images.find().sort("date",DESCENDING).distinct('image')[:31])
    if "from" in dict:
        images = image_db_table.find({"tags":dict["tags"],"date":{"$gte":dict["from"],"$lt":dict["to"]}}).sort("date",DESCENDING)
        return render_template("myview.html", image_names=images.distinct('image')[:31])
    if "date" in dict:
        d,m,y = dict["date"].split("-")
        image_list = []
        if d == "*":
            for i in range(31,0,-1):
                if len(str(i))==1:
                    new_date = "0"+str(i)+"-"+m+"-"+y
                else:
                    new_date = str(i) + "-" + m + "-" + y
                images = image_db_table.find({"tags":dict["tags"],"date":new_date}).sort("date",DESCENDING).distinct('image')
                if images:
                    image_list.extend(images)
        elif m == "*":
            for i in range(12,0,-1):
                if len(str(i))==1:
                    new_date = d+"-"+"0"+str(i)+"-"+y
                else:
                    new_date = d + "-" + str(i) + "-" + y
                images = image_db_table.find({"tags": dict["tags"], "date": new_date}).sort("date",DESCENDING).distinct('image')
                if images:
                    image_list.extend(images)
        elif y=="*":
            for i in range(date.today().isocalendar()[0],1969,-1):
                new_date = d + "-" + m + "-" + str(i)
                images = image_db_table.find({"tags": dict["tags"], "date": new_date}).sort("date",DESCENDING).distinct('image')
                if images:
                    image_list.extend(images)
        else:
            image_list = image_db_table.find({"tags":dict["tags"],"date":dict["date"]}).sort("date",DESCENDING).distinct('image')
        print(image_list)
        return render_template("myview.html", image_names=image_list[:31])

    images = image_db_table.find({"tags": dict["tags"]}).sort("date",DESCENDING)
    return render_template("myview.html",image_names=images.distinct('image')[:31])

if __name__ == '__main__':
    app.debug = True
    app.run()
    toastr.init_app(app)

