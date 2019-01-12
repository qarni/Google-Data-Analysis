"""
Manages all of initial google vision labeling:
- basic label detection
- safe search
- text detection
- appends/updates to original json
"""

import io
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

import helper

# Instantiates a client
CLIENT = vision.ImageAnnotatorClient()


def start_labeling():
    """Gets all the photos and processes them"""

    # Keep a list of all the photos
    photo_list = helper.get_file_list(helper.PHOTO_EXTENTIONS)

    # print a progress bar so we know how many pictures have been processed:
    print("\nTotal pictures to be processed: " + str(len(photo_list)))
    print("[ ", end="", flush=True)

    for filename in photo_list:
        # The name of the image file to annotate
        run_google_vision(filename)
        print(".", end=" ", flush=True)

    print("]\n")
    print("Finished processing!")


def append_to_json(filename, new_json):
    """ append this json to the original file
        if the json file already has a section with the same name, it will just
        be overwritten (useful in test cases)"""

    # if a photo does not have a json file, then create a json for it
    # this may be the case for google drive photos
    if any((filename.lower().endswith(ext)) for ext in helper.PHOTO_EXTENTIONS):
        new_file_data = {
            'title': filename,
            'modificationTime': {
                'timestamp': 'N/A',
                'formatted': 'N/A'
                },
            'geoData': {
                'latitude': 0.0,
                'longitude': 0.0,
                'altitude': 0.0,
                'latitudeSpan': 0.0,
                'longitudeSpan': 0.0
                },
            'geoDataExif': {
                'latitude': 0.0,
                'longitude': 0.0,
                'altitude': 0.0,
                'latitudeSpan': 0.0,
                'longitudeSpan': 0.0
                },
            'photoTakenTime': {
                'timestamp': 'N/A',
                'formatted': 'N/A'
                }
            }
    else:
        new_file_data = {}

    filename = filename + ".json"

    try:
        with open(filename) as read:
            orig = json.load(read)
    except FileNotFoundError:
        orig = new_file_data

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

    response = CLIENT.label_detection(image=image)
    annotations = response.label_annotations
    update_json_with_label_detection(filename, annotations)


def run_safe_search(image, filename):
    """Performs safe search on image file"""

    response = CLIENT.safe_search_detection(image=image)
    annotations = response.safe_search_annotation
    update_json_with_safe_search(filename, annotations)


def run_document_text_detection(image, filename):
    """Performs text detection on image file"""

    response = CLIENT.document_text_detection(image=image)
    annotations = response.full_text_annotation
    update_json_with_document_text_detection(filename, annotations)


def update_json_with_label_detection(filename, annotations):
    """Converts all label annotations and appends to json """

    label_dicts = []

    for label in annotations:
        lab = {'mid': label.mid, 'description': label.description, 'score':
               label.score, 'topicality': label.topicality}
        label_dicts.append(lab)

    label_dicts = {'label_annotations': label_dicts}

    append_to_json(filename, label_dicts)


def update_json_with_safe_search(filename, annotations):
    """Converts safe search annotations and appends to json"""

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
    """Converts all document text annotations and appends to json"""

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
