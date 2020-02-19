# import requests
# import json
# api_key = 'acc_dba37e986089381'
# api_secret = '2de7869e3e57eb42edf4dc2f982a9a86'
# image_path = '/Users/sonalipatro/Downloads/WhatsApp Image 2019-03-01 at 12.57.00.jpeg'
#
# response = requests.post(
#     'https://api.imagga.com/v2/tags',
#     auth=(api_key, api_secret),
#     files={'image': open(image_path, 'rb')})
# print(response.json())
#
# js = json.loads(response.text)
#
# for k in js['result']['tags']:
#     if k['confidence'] > 70.0:
#         print(k['tag']['en'])

from PIL import Image
import cloudsight



im = Image.open('/Users/sonalipatro/Downloads/5EA7397F-3C0F-4F1E-864F-A11A37D3E4B3_1_201_a.jpeg')

im.thumbnail((600,600))
im.save('cloudsight.jpg')

auth = cloudsight.SimpleAuth('CloudSight [19ee8d00fb9859ee1c9c12d3fa66977f]')
api = cloudsight.API(auth)
with open('cloudsight.jpg', 'rb') as f:
    response = api.image_request(f, 'cloudsight.jpg',  {'image_request[locale]': 'en-US',})

status = api.wait(response['token'], timeout=30)
print(status)
