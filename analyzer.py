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

    # Loads the image into memory
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    run_label_detection(image, filename)
    run_safe_search(image, filename)

def run_label_detection(image, filename):
    """Performs label detection on the image file"""
    response = client.label_detection(image=image)
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


def run_safe_search(image, filename):
    response = client.safe_search_detection(image=image)
    update_json_with_safe_search(filename, response)

def update_json_with_safe_search(filename, response):

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY',
            'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

    safe = response.safe_search_annotation

    safe_annot = {'adult': likelihood_name[safe.adult], 'spoof':
            likelihood_name[safe.spoof], 'medical':
            likelihood_name[safe.medical], 'violence':
            likelihood_name[safe.violence], 'racy': likelihood_name[safe.racy]}
    safe_annot = {'safe_search_annotation': safe_annot}

    filename = filename + ".json"
    with open(filename) as read:
        orig = json.load(read)

    orig.update(safe_annot)

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

