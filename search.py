import json, requests

from elasticsearch import Elasticsearch

import helper

def upload_json():
    """
    Removes previous json files from elastic search
    Gets list of all current jsons and uploads them to elastic search
    """

    es = Elasticsearch()
    res = requests.get('http://localhost:9200')

    json_list = helper.get_file_list([".json"])

    # remove previous json files in case there's been an update to them for some
    # reason... this would probably only really happen in testing circumstances
    es.indices.delete(index='photo_jsons')

    # upload all current json files
    for curr_json in json_list:
        f = open(curr_json)
        docket_content = f.read()
        es.index(index='photo_jsons', ignore=400, doc_type='photo', id=curr_json, body=json.loads(docket_content))


def search():
    """
    Allows a search for one search term and displays the number of search
    results, as well as a list of all files which contain the search term
    """

    es = Elasticsearch()

    search_term = input("Enter search term: ")
    res = es.search(index='photo_jsons', q=search_term)

    # lists all files that contain the search term
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s" % (doc['_id']))
