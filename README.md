# Google Photos Analysis
#### Fatima Qarni

Thus far, this program will look at all photos from Google Takeout (honestly, this will work for any photos - they don't neccessarily have to be from Google, but that is the current intended use case). The photos will be analyzed using Google Vision and the new data will be appended to each photo's json metadata file. After this, search will be available (powered by Elastic Search) to search for anything in these newly updated json files.

### Things to get ready before use:

1. Make sure you have python installed.

1. Get your Google Takeout data downloaded from here: [Google Takeout](https://takeout.google.com/settings/takeout)

#### Install Elastic Search:

1. Make sure you have java installed - at least Java8, and JDK 1.8 is
   recommended as of writing this readme

1. Install elastic search: [Elastic Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html)

1. Install elastic search for python:
`pip elasticsearch`


#### Set up Google Vision:

1. Set up google application creditials for Google Vision

1. Once complete, download credentials file and run this command:
`export GOOGLE_APPLICATION_CREDENTIALS=[path_to_file]`


### To run this program:

1. Move your entire `Takeout` directory which you downloaded to the same level
   as this program. If it split up the directory into several parts, move them
   all into a new folder named `Takeout`

1. Run elastic search on terminal with `elasticsearch`

1. In a separate terminal pane, run program with the command:
`python3 analyzer.py`
