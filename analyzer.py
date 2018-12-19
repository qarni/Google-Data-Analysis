"""
Fatima Qarni - Google Photos Analyzer
"""

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# # Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate

# Keep a list of all the jpg and jsons separately
jpg_list = []
json_list = []


for root, dirs, files in os.walk("photos/"):
    for filename in files:
        if filename.endswith(".JPG"):
            jpg_list.append(os.path.join(root, filename))
        elif filename.endswith(".json"):
            json_list.append(os.path.join(root, filename))

print(jpg_list)
print(json_list)

# TODO: Make this into a for each loop after everything works - do for each picture
filename = jpg_list[0]

# Loads the image into memory
# TODO: I guess that would mean that I should only put one photo in memory at a
# time...? (just open/close i guess?)
with io.open(filename, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)

# TODO: once the response is complete, print all the json info to the present
# json file - append it
print(response)

# labels = response.label_annotations
# print('Labels:')
# for label in labels:
#     print(label.description)
