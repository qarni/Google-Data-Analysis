import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import data_manipulation
import search

# colors for graphs
COLOR_1 = "rgba(1, 94, 186, 1)"   # blue
COLOR_2 = "rgba(114, 196, 114, 1)"   # green

# source for stylesheets: plotly website
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

photo_counts = data_manipulation.aggregateDataByDate(
    "graph_data/photo_data.csv")
colorsForPhotos, shapesForPhotos, sizesForPhotos = data_manipulation.createMarkerProperties(
    photo_counts, COLOR_1)

sent_email_counts = data_manipulation.aggregateDataByDate(
    "graph_data/sent_email_data.csv")
colorsForSent, shapesForSent, sizesForSent = data_manipulation.createMarkerProperties(
    sent_email_counts, COLOR_1)

received_email_counts = data_manipulation.aggregateDataByDate(
    "graph_data/received_email_data.csv")
colorsForReceived, shapesForReceived, sizesForReceived = data_manipulation.createMarkerProperties(
    received_email_counts, COLOR_2)

visits_counts = data_manipulation.aggregateDataByDate(
    "graph_data/visit_data.csv")
colorsForVisits, shapesForVisits, sizesForVisits = data_manipulation.createMarkerProperties(
    visits_counts, COLOR_1)

search_counts = data_manipulation.aggregateDataByDate(
    "graph_data/search_data.csv")
colorsForSearch, shapesForSearch, sizesForSearch = data_manipulation.createMarkerProperties(
    search_counts, COLOR_2)

youtube_search_counts = data_manipulation.aggregateDataByDate(
    "graph_data/youtube_search_data.csv")
colorsForYoutubeSearch, shapesForYoutubeSearch, sizesForYoutubeSearch = data_manipulation.createMarkerProperties(
    visits_counts, COLOR_1)

youtube_watch_counts = data_manipulation.aggregateDataByDate(
    "graph_data/youtube_watched_data.csv")
colorsForYoutubeWatch, shapesForYoutubeWatch, sizesForYoutubeWatch = data_manipulation.createMarkerProperties(
    visits_counts, COLOR_2)

app.layout = html.Div([

    html.H1(children='Google Pensieve'),

    dcc.Graph(
        id='Google Photos Over Time',
        figure={
            'data': [{
                'x': photo_counts['date'],
                'y': photo_counts['counts'],
                'text': photo_counts['hover_text'],
                'hoverinfo': 'text',
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
                'text': sent_email_counts['hover_text'],
                'hoverinfo': 'text',
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
                'text': received_email_counts['hover_text'],
                'hoverinfo': 'text',
                'name': 'Received Emails',
                'mode':'lines+markers',
                'line': {
                    'width': 1,
                    'color': COLOR_2
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

    dcc.Graph(
        id='Google Searches/Visits Over Time',
        figure={
            'data': [{
                'x': visits_counts['date'],
                'y': visits_counts['counts'],
                'text': visits_counts['hover_text'],
                'hoverinfo': 'text',
                'name': 'Site Visits Directly from Google',
                'mode': 'lines+markers',
                'line': {
                    'width': 1
                },
                'marker': {
                    'color': colorsForVisits,
                    'symbol': shapesForVisits,
                    'size': sizesForVisits,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            },
            {
                'x': search_counts['date'],
                'y': search_counts['counts'],
                'text': search_counts['hover_text'],
                'hoverinfo': 'text',
                'name': 'Searches',
                'mode': 'lines+markers',
                'line': {
                    'width': 1,
                    'color': COLOR_2
                },
                'marker': {
                    'color': colorsForSearch,
                    'symbol': shapesForSearch,
                    'size': sizesForSearch,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Number of Interactions'},
                hovermode='closest',
                title="Google Searches/Visits Over Time"
            )
        }
    ),

    dcc.Graph(
        id='YouTube Searches/Watches Over Time',
        figure={
            'data': [{
                'x': youtube_search_counts['date'],
                'y': youtube_search_counts['counts'],
                'text': youtube_search_counts['hover_text'],
                'hoverinfo': 'text',
                'name': 'YouTube Searches',
                'mode': 'lines+markers',
                'line': {
                    'width': 1
                },
                'marker': {
                    'color': colorsForYoutubeSearch,
                    'symbol': shapesForYoutubeSearch,
                    'size': sizesForYoutubeSearch,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            },
            {
                'x': youtube_watch_counts['date'],
                'y': youtube_watch_counts['counts'],
                'text': youtube_watch_counts['hover_text'],
                'hoverinfo': 'text',
                'name': 'YouTube Video Watches',
                'mode': 'lines+markers',
                'line': {
                    'width': 1,
                    'color': COLOR_2
                },
                'marker': {
                    'color': colorsForYoutubeWatch,
                    'symbol': shapesForYoutubeWatch,
                    'size': sizesForYoutubeWatch,
                    'opacity': .8,
                    'line': {
                        'width': .2
                    }
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Number of Interactions'},
                hovermode='closest',
                title="YouTube Searches/Watches Over Time"
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

    # return 'You have selected "{}"'.format(value)
    return str(search.riskSearch(value))


if __name__ == "__main__":
    app.run_server(debug=True)
