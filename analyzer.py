"""
Fatima Qarni - Google Photos Analyzer
"""

import labeling
import search

if __name__ == "__main__":

    print("\nGoogle Photos Analyzer\n")

    label = input("Have you updated your Google Takeout files for analysis? (y/n) ")
    if label is "y":
        print("Okiedokes. Time to reanalyze.")
        labeling.start_labeling()
        search.upload_json()
    else:
        print("Okay. Will continue with prior data.")

    # start search loop if input is y
    cont_search = input("Would you like to search for any terms? (y/n) ")

    while cont_search is "y":

        search_term = input("Enter search term: ")
        res = search.search(search_term)

        # lists all files that contain the search term
        print("%d documents found" % res['hits']['total'])
        for doc in res['hits']['hits']:
            print("%s" % (doc['_id']))

        cont_search = input("Would you like to search for any more terms? (y/n) ")

    print("Goodbye!")
