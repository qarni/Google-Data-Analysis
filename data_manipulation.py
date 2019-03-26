import csv
import json

import pandas as pd

date_group = []

def createDateCSV(dataQueue, csvFilename):

    full_json_list = []
    while dataQueue.qsize():
        full_json_list.append(dataQueue.get())

    with open(csvFilename, mode='w') as csv_file:
        col_names = full_json_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=col_names)

        writer.writeheader()
        for item in full_json_list:
            writer.writerow(item)

def getHoverText(row):
    filenames = list(date_group['filename'].get_group(row[0]))
    filenames = ", ".join(str(name) for name in filenames)
    final_text = "Count: " + str(row[1]) + "\n Files:\n" + filenames
    return final_text

def aggregateDataByDate(filename):
    global date_group

    data = pd.read_csv(filename)

    date_group = data.groupby('date')

    counts = data['date'].value_counts()
    counts = counts.rename_axis('date').reset_index(name='counts')
    #counts['hover_text'] = counts.apply(getHoverText, axis=1)
    counts = counts.sort_values(by = ['date'])

    return counts

def test_getJsonListAgain():
    photo_data_json_filename = "photo_data.json"
    with open(photo_data_json_filename) as read:
        orig = json.load(read)
        data_list = orig['photo_data']

    return data_list
