import requests
import json

api_key = 'acc_dba37e986089381'
api_secret = '2de7869e3e57eb42edf4dc2f982a9a86'
image_path = "/Users/sonalipatro/Downloads/test.jpeg"

res = requests.post(
    'https://api.imagga.com/v2/tags',
    auth=(api_key, api_secret),
    files={'image': open(image_path, 'rb')})

print(res.text)
js = json.loads(res.text)

tags = []
if "result" not in js:
    print("hello")
for k in js['result']['tags']:
    if k['confidence'] > 40.0:
        tags.append(k['tag']['en'])
print(tags)