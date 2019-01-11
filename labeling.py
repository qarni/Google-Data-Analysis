"""
Manages all of initial google vision labeling:
- basic label detection
- safe search
- text detection
- appends/updates to original json
"""

import os
import io
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()


def get_images_list():
    """Uses os.walk to go through all the photos in the photos directory, and
    save a list of their names with their filepath for easy access.
    The json files are ignored. """

    jpgs = []

    for root, dirs, files in os.walk("photos/"):
        for filename in files:
            if filename.endswith(".JPG"):
                jpgs.append(os.path.join(root, filename))

    return jpgs


def start_labeling():

    # Keep a list of all the jpgs
    jpg_list = get_images_list()

    # print a progress bar so we know how many pictures have been processed:
    print("Total pictures to be processed: " + str(len(jpg_list)))
    print("[ ", end="", flush=True)

    for filename in jpg_list:
        # The name of the image file to annotate
        # print(filename)
        run_google_vision(filename)
        print(".", end=" ", flush=True)

    print("]\n")
    print("Finished processing!")


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


def run_google_vision(filename):
    """Opens image as a google vision image type"""

    # Loads the image into memory
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    run_label_detection(image, filename)
    run_safe_search(image, filename)
    run_document_text_detection(image, filename)

def run_label_detection(image, filename):
    """Performs label detection on the image file"""

    response = client.label_detection(image=image)
    annotations = response.label_annotations
    update_json_with_label_detection(filename, annotations)


def run_safe_search(image, filename):
    """Performs safe search on image file"""

    response = client.safe_search_detection(image=image)
    annotations = response.safe_search_annotation
    update_json_with_safe_search(filename, annotations)


def run_document_text_detection(image, filename):
    """Performs text detection on image file"""

    response = client.document_text_detection(image=image)
    annotations = response.full_text_annotation
    update_json_with_document_text_detection(filename, annotations)


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

def update_json_with_document_text_detection(filename, annotations):

    doc_annot = []

    for page in annotations.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])

                    word_dict = {'word': word_text, 'confidence': word.confidence}
                    doc_annot.append(word_dict)

    doc_annot = {'document_text_annotation': doc_annot}

    append_to_json(filename, doc_annot)
