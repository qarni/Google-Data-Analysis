"""
Fatima Qarni - Google Photos Analyzer
"""

import io
import os
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


def get_images_list():
    for root, dirs, files in os.walk("photos/"):
        for filename in files:
            if filename.endswith(".JPG"):
                jpg_list.append(os.path.join(root, filename))

    # print(jpg_list)
    return jpg_list


def run_google_vision(filename):
    """Gets label detection for the given filename"""

    # Loads the image into memory
    # TODO: I guess that would mean that I should only put one photo in memory at a
    # time...? (just open/close i guess?)
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    # print(response)

    update_json_with_label_detection(filename, response)


def update_json_with_label_detection(filename, response):

    label_dicts = []
    response = response.label_annotations

    for label in response:
        dict =  { 'mid': label.mid, 'description': label.description, 'score':
                label.score, 'topicality': label.topicality }
        label_dicts.append(dict)

    label_dicts = {'label_annotations': label_dicts}

    # append this json to the original file
    filename = filename + ".json"
    with open(filename) as read:
        orig = json.load(read)

    orig.update(label_dicts)

    with open(filename, "w") as append:
        json.dump(orig, append, indent=2)


if __name__ == "__main__":

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Keep a list of all the jpgs
    jpg_list = []
    jpg_list = get_images_list()

    # TODO: Make this into a for each loop after everything works - do for each picture
    # The name of the image file to annotate
    filename = jpg_list[0]

    run_google_vision(filename)

