# Google Pensieve: a Google Data Analysis Tool
#### Fatima Qarni

The average user stores huge amounts of data on Google and other cloud storage sites. Users are often not aware of the quantity of data that is stored over the years, and not careful about the type of information they store. An account breach could potentially lead to sensitive information to be leaked... which could be problematic.

Going through all of a user’s Google data online manually would be incredibly slow, and Google accounts offer many service, so there could be many years worth of data to sift through. How can all of this data be searched through efficiently? How can potentially sensitive data be flagged and shown to a user, so the user can be more aware of the data that they have, and should possibly be more careful with?

This project has two parts: an analyzer script and a visualization/GUI.

The analyzer program will look at all photos, emails, and text documents from Google Takeout (honestly, this will work for any mailbox/photos/documents - I guess they don't neccessarily have to be from Google, but that is the intended use case). An interesting expansion may be to add other social media data to the visualizations.

- The photos will be analyzed using Google Vision and the new data will be appended to each photo's json metadata file.
- The mailbox file for Gmail is analyzed; all emails are downloaded as text files and all attachments are downloaded and saved.
- Metadata files for each type of data (photos from both Photos/Drive and emails, so far) will then be uploaded to Elasticsearch, along with the other text based documents. 
- After this, search will be available (powered by Elasticsearch) to search for anything in these newly updated json files.
- All data that has a date will be saved in csv files with just a filename/minimal data

The visualization will show graphs of the data available from the analyzation.

This is an example visualization from my Google data:

![image](https://user-images.githubusercontent.com/17552078/80857451-f291cf80-8c17-11ea-8ad2-bcf08fd889ba.png)
![image](https://user-images.githubusercontent.com/17552078/80857457-ffaebe80-8c17-11ea-8b81-84b633e6a698.png)

This is how stuff works if you're curious:
![image](https://user-images.githubusercontent.com/17552078/80857475-1d7c2380-8c18-11ea-99cd-38a765b34168.png)


### Things to get ready before use:

1. Make sure you have python 3 installed.

1. Get your Google Takeout data downloaded from here: [Google Takeout](https://takeout.google.com/settings/takeout)

#### Install Elastic Search:

1. Make sure you have java installed - at least Java8, and JDK 1.8 is
   recommended as of writing this readme

1. Install elastic search: [Elastic Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html)

1. Install elastic search for python:
`pip elasticsearch` (or) `pip3 elasticsearch`

#### Set up Google Vision:

1. Set up google application creditials for Google Vision

1. Once complete, download credentials file and run this command:
`export GOOGLE_APPLICATION_CREDENTIALS=[path_to_file]`

#### Install any other libraries used that you may not have installed....

### To run the analyzer program:

1. Move your entire `Takeout` directory which you downloaded to the same level
   as this program. If it split up the directory into several parts, move them
   all into a new folder named `Takeout`

1. Run elastic search on terminal with `elasticsearch`

1. In a separate terminal pane, run program with the command:
`python3 analyzer.py`


### To run the visualization/GUI program:

1. After running the analyzer program, open the `analyzer` folder in a terminal pane and run the command: `python3 app.py`

1. This will launch the app on local host, so it can be viewed at the given address/port printed in terminal. On my computer that is: `http://127.0.0.1:8050/`

