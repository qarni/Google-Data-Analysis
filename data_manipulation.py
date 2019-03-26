import csv
import json

import pandas as pd
from datetime import datetime

def createDateCSV(photoDataQueue):

    photo_data_csv_filename = "photo_data.csv"

    full_json_list = []
    while photoDataQueue.qsize():
        full_json_list.append(photoDataQueue.get())

    with open(photo_data_csv_filename, mode='w') as csv_file:
        col_names = full_json_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=col_names)

        writer.writeheader()
        for item in full_json_list:
            writer.writerow(item)

def convert_date_format(old_format):
    datetimeobject = datetime.strptime(old_format,'%b %d, %Y')
    return datetimeobject.strftime('%Y-%m-%d')        

def aggregateDataByDate():
    photo_data = pd.read_csv('photo_data.csv')

    photo_data['date'] = photo_data['date'].apply(convert_date_format)

    counts = photo_data['date'].value_counts()
    counts = counts.rename_axis('date').reset_index(name='counts')

    counts = counts.sort_values(by = ['date'])

    return counts

def test_getJsonListAgain():
    photo_data_json_filename = "photo_data.json"
    with open(photo_data_json_filename) as read:
        orig = json.load(read)
        data_list = orig['photo_data']

    return data_list
