"""
Fatima Qarni - Google Photos Analyzer
"""

import initial_labeling
import search

if __name__ == "__main__":

    print("\nGoogle Photos Analyzer\n")

    labeling = input("Have you updated your Google Takeout photos for analysis? (y/n) ")
    if labeling is "y":
        print("Okiedokes. Time to reanalyze.")
        initial_labeling.start_labeling()
        search.upload_json()
    else:
        print("Okay. Will continue with prior data.")

    # start search loop if input is y
    cont_search = input("Would you like to search for any terms? (y/n) ")

    while cont_search is "y":

        search.search()

        cont_search = input("Would you like to search for any more terms? (y/n) ")

    print("Goodbye!")

