"""
Manages all of initial google vision labeling:
- basic label detection
- safe search
- appends/updates to original json
"""

import io
import json

# Imports the Google Cloud client library
from google.cloud.vision import types

def append_to_json(filename, new_json):
    """ append this json to the original file
        if the json file already has a section with the same name, it will just
        be overwritten (useful in test cases)"""

    filename = filename + ".json"
    with open(filename) as read:
        orig = json.load(read)

    orig.update(new_json)

    with open(filename, "w") as append:
        json.dump(orig, append, indent=2)


def run_google_vision(client, filename):
    """Opens image as a google vision image type"""

    # Loads the image into memory
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    run_label_detection(client, image, filename)
    run_safe_search(client, image, filename)

def run_label_detection(client, image, filename):
    """Performs label detection on the image file"""

    response = client.label_detection(image=image)
    annotations = response.label_annotations
    update_json_with_label_detection(filename, annotations)


def run_safe_search(client, image, filename):
    """Performs safe search on image file"""

    response = client.safe_search_detection(image=image)
    annotations = response.safe_search_annotation
    update_json_with_safe_search(filename, annotations)


def update_json_with_label_detection(filename, annotations):
    """Converts all label annotations  """

    label_dicts = []

    for label in annotations:
        lab = {'mid': label.mid, 'description': label.description, 'score':
                label.score, 'topicality': label.topicality}
        label_dicts.append(lab)

    label_dicts = {'label_annotations': label_dicts}

    append_to_json(filename, label_dicts)


def update_json_with_safe_search(filename, annotations):
    """ """

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY',
            'POSSIBLE', 'LIKELY', 'VERY_LIKELY')


    safe_annot = {'adult': likelihood_name[annotations.adult], 'spoof':
            likelihood_name[annotations.spoof], 'medical':
            likelihood_name[annotations.medical], 'violence':
            likelihood_name[annotations.violence], 'racy': likelihood_name[annotations.racy]}
    safe_annot = {'safe_search_annotation': safe_annot}

    append_to_json(filename, safe_annot)