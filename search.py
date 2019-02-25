"""
Everything that has to do with elastic search
"""

import json
import requests
import time

from elasticsearch import Elasticsearch

import helper

es = Elasticsearch()

def upload_json():
    """
    Removes previous json files from elastic search
    Gets list of all current jsons and uploads them to elastic search
    """

    res = requests.get('http://localhost:9200')

    # remove previous json files in case there's been an update to them for some
    # reason... this would probably only really happen in testing circumstances
    es.indices.delete(index='photo_jsons')
    es.indices.delete(index='text_jsons')

    # upload all current json files
    index_photos()
    index_text_files()

def index_photos():
    """
    upload photo jsons
    TODO: hmm... i guess this would also upload non-photo jsons as well... do i care about that?
    """
    json_list = helper.get_file_list([".json"])

    for curr_json in json_list:
        json_file = open(curr_json)
        docket_content = json_file.read()
        es.index(index='photo_jsons', ignore=400, doc_type='photo', id=curr_json, body=json.loads(docket_content))

def index_text_files():
    """
    Process all other attachments - add them to the list of documents to process
    TODO: add PDF files....not sure how to do that... might have to be with google vision?
    """
    
    text_list = helper.get_file_list(helper.TEXT_EXTENSIONS)
    print(text_list)

    for curr_text in text_list:
        text_file = open(curr_text)
        file_content = text_file.read()
        docket_content = {'filename': curr_text, 'doc_text': file_content}
        es.index(index='text_jsons', ignore=400, doc_type='text', id=curr_text, body=json.dumps(docket_content))

def search(search_term):
    """
    Allows search for one search term and displays the number of search
    results, as well as a list of all files which contain the search term
    Returns list of results
    """

    # print(search_term)
    res = es.search(index=['photo_jsons', 'text_jsons'], q=search_term)
    # print(res)
    return res
