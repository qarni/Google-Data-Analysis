import csv
import json
from datetime import datetime

import pandas as pd
import numpy as np

import search


def createDateCSV(dataQueue, csvFilename):
    """
    Converts the given dataQueue with json vars into a csv file
    """

    full_json_list = []
    while dataQueue.qsize():
        full_json_list.append(dataQueue.get())

    with open(csvFilename, mode='w') as csv_file:
        col_names = full_json_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=col_names)

        writer.writeheader()
        for item in full_json_list:
            writer.writerow(item)


def addColumnForFlags(counts):
    """
    adds/updates the flags column in a given counts panda data frame based on if the filenames
    from that day are in the risk list provided from elastic search

    TODO: once a user can create their own flag list, pass it through here to search

    Returns @counts
    """
    #TODO: get this from app.py later
    risk_list = ["password", "bank", "SSN", "VERY_LIKELY"]

    risk_list = search.riskSearch(risk_list)

    def risk(row):
        for filename in risk_list:
            
            # if it is a json
            if filename[0] == "{":
                filename = filename.split(":")
                filename = filename[len(filename)-1]
                filename = filename.split("'")
                filename = filename[1]
            else:
                # if it is a filename
                # remove the .json at the end of the filename
                filename = str(filename[:-len(".json")])
            if filename in row[2]:
                return "true"
        return "false"

    counts['risk'] = counts.apply(risk, axis=1)

    return counts


def splitEmailCSV():
    """
    Split the full email csv file into sent and received email csv files
    Saves the new csvs
    """

    origEmailCSV = "graph_data/email_data.csv"
    sentEmailCSV = "graph_data/sent_email_data.csv"
    receivedEmailCSV = "graph_data/received_email_data.csv"

    origEmail = pd.read_csv(origEmailCSV)

    sentEmail = origEmail.loc[origEmail['mailbox'].str.contains(
        "Sent") == True]
    receivedEmail = origEmail.loc[origEmail['mailbox'].str.contains(
        "Sent") == False]

    sentEmail.to_csv(sentEmailCSV, index=False)
    receivedEmail.to_csv(receivedEmailCSV, index=False)


def aggregateDataByDate(filename):
    """
    Reads a csv file and turns it into a panda data frame
    Then aggregares the data and groups it by date, with a count for each date
    Also adds the hover text, which contains the names of all files for that date 
    that were included in the csv

    Returns @counts
    """

    data = pd.read_csv(filename)
    date_group = data.groupby('date')

    def getHoverText(row):
        try:
            # can only show max 24 things... i think
            datetimeobject = datetime.strptime(row[0], '%Y-%m-%d')
            date = datetimeobject.strftime('%b %d')

            filenames = list(date_group['filename'].get_group(row[0]))[0:23]
            filenames = ", <br>".join(str(name) for name in filenames)
            final_text = "Date: " + str(date) + " Count: " + str(row[1]) + "<br>Files:<br>" + filenames
        except:
            return "Date: " + str(date) + " Count: " + str(row[1]) 
        return final_text

    counts = data['date'].value_counts()
    counts = counts.rename_axis('date').reset_index(name='counts')
    counts['hover_text'] = counts.apply(getHoverText, axis=1)
    counts = counts.sort_values(by=['date'])

    counts = addColumnForFlags(counts)

    counts.to_csv(filename+"pd.csv")

    return counts


def createMarkerProperties(counts, main_color):
    """
    Creates lists of marker properties based on if that row is a "risk" row or not
    """

    riskColor = "rgba(238, 16, 16, 1)"

    defaultShape = "circle"
    riskShape = "star-dot"

    defaultSize = 8
    riskSize = 10

    colors = []
    shapes = []
    sizes = []

    for index, row in counts.iterrows():
        if str(row['risk']) == "true":
            colors.append(riskColor)
            shapes.append(riskShape)
            sizes.append(riskSize)
        else:
            colors.append(main_color)
            shapes.append(defaultShape)
            sizes.append(defaultSize)
    return colors, shapes, sizes


def test_getJsonListAgain():
    """This was just for testing/debugging"""

    photo_data_json_filename = "photo_data.json"
    with open(photo_data_json_filename) as read:
        orig = json.load(read)
        data_list = orig['photo_data']

    return data_list
