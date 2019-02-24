"""
Program wide helper functions
"""

import os
import imaplib
import poplib
import mailbox
import email

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

def process_mbox():
    """
    TODO: EVERYTHING
    Process mbox file
    1. Download all the attachments, and then they can be processed just like the other files are
    2. Download the emails themselves as text files, and then they can be processed like other files too
    """

    mb = mailbox.mbox("Takeout/Mail/All mail Including Spam and Trash.mbox")

    print("okay now i will try email \n\n\n\n\n")

    get_all_attachments(mb)

def get_all_attachments(mb):
    # source: stackoverflow.com/questions/18497397/how-to-get-csv-attachment-from-email-and-save-it

    attach_folder = "Takeout/mail_attachments/"
    if not os.path.exists(attach_folder):
        os.makedirs(attach_folder)

    for message in mb:
        for part in message.walk():
            if not message.is_multipart():
                continue
            if message.get('Content-Disposition'):
                continue

            #if there's a filename then there is an attachment
            file_name = part.get_filename()
            if file_name:
                dest = attach_folder + file_name
                file = open(dest, 'wb')
                file.write(part.get_payload(decode=True))
                file.close()
            