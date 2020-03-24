import os
from flask import Flask, flash, redirect
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

image_list = list(db.images.find())
#.strftime("%d-%m-%Y")
# for i in image_list:
#     i["date"] = datetime.strptime(i["date"], "%d-%m-%Y")

for item in image_list:
    db.images.update_one({"_id" : item["_id"] }, {"$set" : {"n_date" :datetime.strptime(item["date"], "%d-%m-%Y")}})