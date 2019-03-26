import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html

import data_manipulation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

photo_counts = data_manipulation.aggregateDataByDate("graph_data/photo_data.csv")
sent_email_counts = data_manipulation.aggregateDataByDate("graph_data/sent_email_data.csv")
received_email_counts = data_manipulation.aggregateDataByDate("graph_data/received_email_data.csv")

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
                }
            }, 
            {
                'x': received_email_counts['date'],
                'y': received_email_counts['counts'],
                'name': 'Received Emails',
                'mode':'lines+markers',
                'line': {
                    'width': 1
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Number of Emails'},
                hovermode='closest', 
                title="Gmail Over Time"
            )
        }
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
