"""
Program wide helper functions
"""

import os

PHOTO_EXTENTIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                    ".raw", ".ico", ".tiff"]


def get_file_list(extentions):
    """
    Uses os.walk to go through all the files in the Takeout directory, and
    return a list of the names of files that match the given list of file
    extentions, with their filepath for easy access.
    """

    file_list = []

    for root, dirs, files in os.walk("Takeout/"):
        for filename in files:
            if any((filename.lower().endswith(ext)) for ext in extentions):
                file_list.append(os.path.join(root, filename))

    return file_list
