import os
import mailbox
import email
from email import header
from bs4 import BeautifulSoup
import chardet

def process_mbox():
    """
    Process mbox file
    Download all the attachments, and saves them in Takeout/mail_attachments/
    Download the emails themselves as text files, and then they can be processed like other files too
    """

    #mb = mailbox.mbox("Takeout/Mail/All mail Including Spam and Trash.mbox")
    #get_all_attachments(mb)
    #get_all_emails(mb)

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
    source: https://stackoverflow.com/questions/26567843/reading-the-mail-content-of-an-mbox-file-using-python-mailbox

    Gets info and body
    TODO: use JSON instead of txt
    """

    mail_folder = "Takeout/mail_text/"
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)
    
    for message in mb:
        try:
            subject = str(header.make_header(header.decode_header(message['subject'])))
        except Exception:
            subject = ""
        dest = mail_folder + subject + ".txt"

        content = get_email_body(message)

        try:
            with open(dest, 'w+') as file:
                file.write("Date: " + message['Date'] + "\nMailbox:" + message['X-Gmail-Labels'] + "\nFrom: " + message['From'] + 
                    "\nTo: " + message['To'] + "\nSubject: " + subject + "\nText:\n" + str(content))
                file.close()
        except Exception:         # not sure why there is an exception sometimes?
            pass
        
def get_email_body(message):
    """
    https://pythontips.com/2013/09/29/the-python-yield-keyword-explained/

    https://stackoverflow.com/questions/26567843/reading-the-mail-content-of-an-mbox-file-using-python-mailbox
    """

    body = ''

    def decode_wrapper(m):
        charset = m.get_content_charset('utf-8')
        try:
            return m.get_payload(decode = True).decode(charset)
        except UnicodeDecodeError:
            try:
                charset = chardet.detect(m)['encoding']
                return m.get_payload(decode = True).decode(charset)
            except Exception:
                return ""
        except Exception:
                return ""


    def get_content(m):
        if m.get_content_type() == 'html':
            return BeautifulSoup(decode_wrapper(m), features="html.parser").text
        elif m.get_content_type() == 'text/html':
            return BeautifulSoup(decode_wrapper(m), features="html.parser").text  
        elif m.get_content_type() == 'text/plain':
            return decode_wrapper(m)
        elif m.get_content_type() == 'text':
            return decode_wrapper(m)
        elif m.get_content_type() == 'plain':
            return decode_wrapper(m)

    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    content = get_content(subpart)
                    if content is not None:
                        body += '\n' + content
            else:
                content = get_content(part)
                if content is not None:
                    body += '\n' + content
    else:
        content = get_content(message)
        if content is not None:
            body = content

    return body