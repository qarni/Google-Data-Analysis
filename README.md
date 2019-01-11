# Google Photos Analysis
#### Fatima Qarni

### Things to get ready before use:

1. Make sure you have python installed.

#### Install Elastic Search:

1. Make sure you have java installed - at least Java8, and JDK 1.8 is
   recommended as of writing this readme.

1. Install elastic search: 
   https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html

1. Install elastic search for python:
`pip elasticsearch`


#### Set up Google Vision:

1. Set up google application creditials for Google Vision.

1. Once complete, download credentials file and run this command:
`export GOOGLE_APPLICATION_CREDENTIALS=[path_to_file]`


### To run this program:

1. Move your Google Photos Takeout files into a directory named `photos`.

1. Run elastic search on terminal with `elasticsearch`

1. In a separate terminal, run program with the command:
`python3 analyzer.py`
