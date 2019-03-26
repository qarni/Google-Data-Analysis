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
email_counts = data_manipulation.aggregateDataByDate("graph_data/email_data.csv")


app.layout = html.Div([
    
    html.H1(children='Google Pensieve'),

    dcc.Graph(
        id='Google Photos Over Time',
        figure={
            'data': [{
                'x':photo_counts['date'],
                'y':photo_counts['counts'],
                'mode':'lines+markers',
                'line': {
                    'width': 3
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Count per Day'},
                hovermode='closest', 
                title="Google Photos Over Time"
            )
        }
    ),

    dcc.Graph(
        id='Gmail Over Time',
        figure={
            'data': [{
                'x':email_counts['date'],
                'y':email_counts['counts'],
                'mode':'lines+markers',
                'line': {
                    'width': 3
                }
            }],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Count per Day'},
                hovermode='closest', 
                title="Gmail Over Time"
            )
        }
    )


])

if __name__ == "__main__":
    app.run_server(debug=True)
