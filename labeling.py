"""
Manages all of initial google vision labeling:
- basic label detection
- safe search
- text detection
- appends/updates to original json

Also calls for email processing
"""

import io
import json
import os

import multiprocessing
from multiprocessing.pool import ThreadPool

from queue import Queue
from datetime import datetime

# from pyPDF2 import PdfFileReader
# Imports the Google Cloud client library

from google.cloud import vision
from google.cloud.vision import types

import helper
import html_parse
import mailbox_processing
import data_manipulation
import search

# Instantiates a client
CLIENT = vision.ImageAnnotatorClient()

# Makes a queue for the threads
photoDataQueue = Queue()


def start_labeling():
    """Gets all the emails and photos and processes them"""

    if not os.path.exists("graph_data/"):
        os.makedirs("graph_data/")

    # process searches, visits, youtube
    all_search_data = html_parse.parse_search()
    all_youtube_data = html_parse.parse_youtube()

    # get all info from gmail processed
    mailbox_processing.process_mbox()

    # Gets all the photos and processes them
    process_photos()

    # TODO THIS DOES NOT WORK CURRENTLY - find a library to process pdfs
    # only process a file of max 2000 pages
    # hopefully this will stop any textbooks from being processed as well
    # Get a list of all the pdfs
    # pdf_list = helper.get_file_list('.pdf', helper.TEXT_FOLDER_LIST)

    search.upload_json(all_search_data, all_youtube_data)


def process_photos():
     # Keep a list of all the photos
    photo_list = helper.get_file_list(
        helper.PHOTO_EXTENTIONS, helper.PHOTO_FOLDER_LIST)

    # print a progress bar so we know how many pictures have been processed:
    print("\nTotal pictures to be processed: " + str(len(photo_list)))
    print("[ ", end="", flush=True)

    pool = ThreadPool()
    pool.map(run_google_vision, photo_list)

    print("]\n")
    print("Finished processing!")

    data_manipulation.createDateCSV(
        photoDataQueue, "graph_data/photo_data.csv")


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
        new_file_data = {'title': filename}

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

    try:
        # Loads the image into memory
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        run_label_detection(image, filename)
        run_safe_search(image, filename)
        run_document_text_detection(image, filename)

        printToQueue(filename)

    except Exception:
        print("mm something went wrong with runnig..")
        pass

    print(".", end=" ", flush=True)


def printToQueue(filename):
    """writes available data to queue for future use"""

    json_filename = filename + ".json"

    try:
        with open(json_filename) as read:
            orig = json.load(read)
            # TODO: check to make sure this is the right time variable to use rather than one of the others
            # TODO: check to make sure this format for the time is ok... otherwise maybe change?
            date = orig['photoTakenTime']['formatted']
            # date is spliced to only include date, not time
            date = ",".join(date.split(",", 2)[:2])

            # if the data is available, then add it to the photo dates json
            # otherwise - do not add to file (but it can still be found from elasticsearch)
            if date != 'N/A' and date != '':
                # currently need: date, filename TODO: add more things here later
                # TODO: Google drive pics/etc don't have dates... can that be fixed?

                datetimeobject = datetime.strptime(date, '%b %d, %Y')
                date = datetimeobject.strftime('%Y-%m-%d')

                new_json_entry = {
                    'date': date,
                    'filename': filename
                }
                photoDataQueue.put(new_json_entry)

    except Exception:
        print("something is wrong with the queueing")
        return


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
                    word_text = ''.join(
                        [symbol.text for symbol in word.symbols])

                    word_dict = {'word': word_text,
                                 'confidence': word.confidence}
                    doc_annot.append(word_dict)

    doc_annot = {'document_text_annotation': doc_annot}

    append_to_json(filename, doc_annot)
