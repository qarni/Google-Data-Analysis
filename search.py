"""
Everything that has to do with elastic search
"""

import json
import requests
import time

from elasticsearch import Elasticsearch

import helper

es = Elasticsearch()


def upload_json(all_search_data, all_youtube_data):
    """
    Removes previous json files from elastic search
    Gets list of all current jsons and uploads them to elastic search
    """

    res = requests.get('http://localhost:9200')

    # remove previous json files in case there's been an update to them for some
    # reason... this would probably only really happen in testing circumstances
    
    try:
        es.indices.delete(index='photo_jsons')
        es.indices.delete(index='text_jsons')
        es.indices.delete(index='search_jsons')
        es.indices.delete(index='youtube_jsons')
    except Exception:
        pass
    

    # upload all current json files
    index_photos()
    index_text_files()
    index_search(all_search_data)
    index_youtube(all_youtube_data)


def index_photos():
    """
    upload photo jsons
    """
    json_list = helper.get_file_list([".json"], helper.PHOTO_FOLDER_LIST)

    for curr_json in json_list:
        json_file = open(curr_json)
        docket_content = json_file.read()
        es.index(index='photo_jsons', ignore=400, doc_type='photo',
                 id=curr_json, body=json.loads(docket_content))


def index_text_files():
    """
    Process all other attachments - add them to the list of documents to process
    TODO: add PDF files....not sure how to do that... might have to be with google vision?
    """

    text_list = helper.get_file_list(
        helper.TEXT_EXTENSIONS, helper.TEXT_FOLDER_LIST)

    for curr_text in text_list:
        try:
            text_file = open(curr_text)
            file_content = text_file.read()
            docket_content = {'filename': curr_text, 'doc_text': file_content}
            es.index(index='text_jsons', ignore=400, doc_type='text',
                     id=curr_text, body=json.dumps(docket_content))
        except Exception:
            pass

def index_search(search_list):
    for data in search_list:
        try:
            docket_content = {'filename': data['content'], 'doc_text': data}
            es.index(index='search_jsons', ignore=400, doc_type='html',
                     id=data['content'], body=json.dumps(docket_content))
        except Exception:
            pass

def index_youtube(youtube_list):
    for data in youtube_list:
        try:
            docket_content = {'filename': data['content'], 'doc_text': data}
            es.index(index='youtube_jsons', ignore=400, doc_type='html',
                     id=data['content'], body=json.dumps(docket_content))
        except Exception:
            pass


def search(search_term):
    """
    Allows search for one search term and displays the number of search
    results, as well as a list of all files which contain the search term
    Returns list of results
    """

    page = es.search(index=['photo_jsons', 'text_jsons', 'search_jsons', 'youtube_jsons'],
                     q=search_term, scroll='2m', size=1000)
    return getAllResults(page)


def riskSearch(risk_list):
    """
    Bulk searches for a list of risk terms
    TODO: make this list more expansive
    TODO: make it so that it must match a term exactly... currently it is only matching on one in a multi-word term
    """

    #risk_list = ["password", "bank", "SSN", "VERY_LIKELY"]
    # I can't search with the colons/quotes... see if there's anything i can do about that
    others = ["\"adult\": \"VERY_LIKELY\"", "\"adult\": \"LIKELY\"",
              "\"racy\": \"VERY_LIKELY\"", "\"racy\": \"LIKELY\""]

    page = es.search(index=['photo_jsons', 'text_jsons', 'search_jsons', 'youtube_jsons'],
                     q=risk_list, scroll='2m', size=1000)
    return getAllResults(page)


def getAllResults(page):
    """
    allows getting more than 1000 results
    source: https://gist.github.com/drorata/146ce50807d16fd4a6aa
    """
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    res = []

    if scroll_size == 0:
        for doc in page['hits']['hits']:
            res.append("%s" % (doc['_id']))
        return res

    # Start scrolling
    while (scroll_size > 0):
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])

        for doc in page['hits']['hits']:
            res.append("%s" % (doc['_id']))

        # Update the scroll ID
        sid = page['_scroll_id']
        page = es.scroll(scroll_id=sid, scroll='2m')

    return res
