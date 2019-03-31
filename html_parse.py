from bs4 import BeautifulSoup, SoupStrainer
from queue import Queue
from datetime import datetime

import data_manipulation

def parse_search():

    visitsDataQueue = Queue()
    searchesDataQueue = Queue()
    all_search_data = []

    class_for_content = "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"

    try:
        with open("Takeout/My Activity/Search/MyActivity.html", "r") as file:
            data=file.read()
    except Exception:
        print("Search Activity file was not found")
        return

    body = SoupStrainer('div', {'class': class_for_content})
    soup = BeautifulSoup(data, "html.parser", parse_only=body)
       
    # gets chunk for each search/visit
    divs = soup.find_all('div')
        
    for div in divs:
        try:
            category = ''.join(div.find('a').previous_siblings)
            content = div.find('a').text
            date = ''.join(div.find('br').next_siblings)

            date = ",".join(date.split(",", 2)[:2])
            datetimeobject = datetime.strptime(date, '%b %d, %Y')
            date = datetimeobject.strftime('%Y-%m-%d')

            new_json_entry = {
                'date': date,
                'filename': content,
                'hover_text': "",
                'content': content
            }

            # add to data queues
            if "Visited" in category:
                visitsDataQueue.put(new_json_entry)
            elif "Searched for" in category:
                searchesDataQueue.put(new_json_entry)
            
            all_search_data.append(new_json_entry)

        except Exception:
            print(date)
            pass
    
    # print as csv
    data_manipulation.createDateCSV(visitsDataQueue, "graph_data/visit_data.csv")
    data_manipulation.createDateCSV(searchesDataQueue, "graph_data/search_data.csv")

    return all_search_data

def parse_youtube():
    searchesDataQueue = Queue()
    watchedDataQueue = Queue()
    all_youtube_data = []

    class_for_content = "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"

    try:
        with open("Takeout/My Activity/YouTube/MyActivity.html", "r") as file:
            data=file.read()
    except Exception:
        print("YouTube Activity file was not found")
        return

    body = SoupStrainer('div', {'class': class_for_content})
    soup = BeautifulSoup(data, "html.parser", parse_only=body)
       
    # gets chunk for each search/watch
    divs = soup.find_all('div')

    for div in divs:
        try:
            category = ''.join(div.find('a').previous_siblings)
            content = div.find('a').text

            # if this is a watched video, then you have to get the date after the second <a>
            if "Searched for" in category:
                date = ''.join(div.find('br').next_siblings)
            elif "Watched" in category:
                breaks = div.find_all('br')
                date = ''.join(breaks[1].next_siblings)

            date = ",".join(date.split(",", 2)[:2])
            datetimeobject = datetime.strptime(date, '%b %d, %Y')
            date = datetimeobject.strftime('%Y-%m-%d')

            new_json_entry = {
                'date': date,
                'filename': content,
                'hover_text': "",
                'content': content
            }

            # add to data queues
            if "Watched" in category:
                watchedDataQueue.put(new_json_entry)
            elif "Searched for" in category:
                searchesDataQueue.put(new_json_entry)

            all_youtube_data.append(new_json_entry)

        except Exception:
            print(date)
            pass

    # print as csv
    data_manipulation.createDateCSV(watchedDataQueue, "graph_data/youtube_watched_data.csv")
    data_manipulation.createDateCSV(searchesDataQueue, "graph_data/youtube_search_data.csv")

    return all_youtube_data
