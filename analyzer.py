"""
Fatima Qarni - Google Photos Analyzer
"""

import os

# Imports the Google Cloud client library
from google.cloud import vision

import initial_labeling


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


if __name__ == "__main__":

    print("\nGoogle Photos Analyzer\n")

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Keep a list of all the jpgs
    jpg_list = get_images_list()

    # print a progress bar so we know how many pictures have been processed:
    print("Total pictures to be processed: " + str(len(jpg_list)))
    print("[ ", end="", flush=True)

    for filename in jpg_list:
        # The name of the image file to annotate
        # print(filename)
        initial_labeling.run_google_vision(client, filename)
        print(".", end=" ", flush=True)

    print("]\n")
    print("Finished processing!")
