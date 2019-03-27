"""
Program wide helper functions
"""

import os

PHOTO_EXTENTIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                    ".raw", ".ico", ".tif", ".tiff"]

TEXT_EXTENSIONS = [".doc", ".docx", ".odt", ".rtf", ".tex", "wks",
                   ".wps", ".wpd", ".txt"]

PHOTO_FOLDER_LIST = ["Takeout/Google Photos",
                     "Takeout/Drive", "Takeout/mail_attachments"]

TEXT_FOLDER_LIST = ["Takeout/Drive", "Takeout/mail_attachments"]


def get_file_list(extentions, folder_names):
    """
    Uses os.walk to go through all the files in the Takeout directory, and
    return a list of the names of files that match the given list of file
    extentions, with their filepath for easy access.
    Can include which folders to search through
    """

    file_list = []

    for folder in folder_names:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if any((filename.lower().endswith(ext)) for ext in extentions):
                    file_list.append(os.path.join(root, filename))

    return file_list
