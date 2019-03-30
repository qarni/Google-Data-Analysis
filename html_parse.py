from bs4 import BeautifulSoup, SoupStrainer
from queue import Queue
from datetime import datetime

import data_manipulation

def parse_search():

    visitsDataQueue = Queue()
    searchesDataQueue = Queue()

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

        except Exception:
            print(date)
            pass
    
    # print as csv
    data_manipulation.createDateCSV(visitsDataQueue, "graph_data/visit_data.csv")
    data_manipulation.createDateCSV(searchesDataQueue, "graph_data/search_data.csv")
