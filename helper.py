"""
Program wide helper functions
"""

import os
import mailbox
import email

PHOTO_EXTENTIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                    ".raw", ".ico", ".tif", ".tiff"]

TEXT_EXTENSIONS = [".doc", ".docx", ".odt", ".rtf", ".tex", "wks", 
                   ".wps", ".wpd", ".txt"]


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
    Process mbox file
    Download all the attachments, and saves them in Takeout/mail_attachments/
    TODO: Download the emails themselves as text files, and then they can be processed like other files too
    """

    mb = mailbox.mbox("Takeout/Mail/All mail Including Spam and Trash.mbox")
    get_all_attachments(mb)
    get_all_emails(mb)

def get_all_attachments(mb):
    """
    Downloads all attachments
    source: stackoverflow.com/questions/18497397/how-to-get-csv-attachment-from-email-and-save-it
    """

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

def get_all_emails(mb):
    """
    Downloads all emails and saves as txt files?

    TODO: this just gets the subject it only sometimes gets the body of the email - WIP
    """

    mail_folder = "Takeout/mail_text/"
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)
    
    for message in mb:

        dest = mail_folder + " " + message['subject'] + ".txt"

        try:
            with open(dest, 'w') as file:
                file.write("Subject: " + message['subject'] + "\nText:\n" + str(message.get_payload(decode=True)))
                file.close()
        except Exception:
            pass