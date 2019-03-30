import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import data_manipulation, search

# source for stylesheets: plotly website
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

photo_counts = data_manipulation.aggregateDataByDate(
    "graph_data/photo_data.csv")
colorsForPhotos, shapesForPhotos, sizesForPhotos = data_manipulation.createMarkerProperties(
    photo_counts, "rgba(31, 119, 180, 1)")

sent_email_counts = data_manipulation.aggregateDataByDate(
    "graph_data/sent_email_data.csv")
colorsForSent, shapesForSent, sizesForSent = data_manipulation.createMarkerProperties(
    sent_email_counts, "rgba(31, 119, 180, 1)")

received_email_counts = data_manipulation.aggregateDataByDate(
    "graph_data/received_email_data.csv")
colorsForReceived, shapesForReceived, sizesForReceived = data_manipulation.createMarkerProperties(
    received_email_counts, "rgba(255, 127, 14, 1)")

app.layout = html.Div([

    html.H1(children='Google Pensieve'),

    dcc.Graph(
        id='Google Photos Over Time',
        figure={
            'data': [{
                'x': photo_counts['date'],
                'y': photo_counts['counts'],
                'mode': 'lines+markers',
                'line': {
                    'width': 1
                },
                'marker': {
                    'color': colorsForPhotos,
                    'symbol': shapesForPhotos,
                    'size': sizesForPhotos,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Number of Photos'},
                hovermode='closest',
                title="Google Photos Over Time"
            )
        }
    ),

    dcc.Graph(
        id='Gmail Over Time',
        figure={
            'data': [{
                'x': sent_email_counts['date'],
                'y': sent_email_counts['counts'],
                'name': 'Sent Emails',
                'mode': 'lines+markers',
                'line': {
                    'width': 1
                },
                'marker': {
                    'color': colorsForSent,
                    'symbol': shapesForSent,
                    'size': sizesForSent,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            },
                {
                'x': received_email_counts['date'],
                'y': received_email_counts['counts'],
                'name': 'Received Emails',
                'mode':'lines+markers',
                'line': {
                    'width': 1
                },
                'marker': {
                    'color': colorsForReceived,
                    'symbol': shapesForReceived,
                    'size': sizesForReceived,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Number of Emails'},
                hovermode='closest',
                title="Gmail Over Time"
            )
        }
    ),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'password', 'value': 'password'},
            {'label': 'bank', 'value': 'bank'},
            {'label': 'SSN', 'value': 'SSN'},
            {'label': 'VERY_LIKELY', 'value': 'VERY_LIKELY'}
        ],
        value=['password', 'bank', 'SSN'],
        multi=True
    ),
    html.Div(id='output-container')
])

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_output(value):
    # TODO: actually take these values, convert them to a list, and sent to risk search
    # TODO: once all this is working, the graphs will also all have to be updated with callbacks
    
    #return 'You have selected "{}"'.format(value)
    return str(search.riskSearch(value))


if __name__ == "__main__":
    app.run_server(debug=True)
