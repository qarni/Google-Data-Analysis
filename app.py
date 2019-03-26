import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html

import data_manipulation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

counts = data_manipulation.aggregateDataByDate()
data = [go.Scatter(x=counts['date'], y=counts['counts'])]


app.layout = html.Div([
    
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=counts['date'],
                    y=counts['counts'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Count per Day'},
                hovermode='closest'
            )
        }
    )
])


if __name__ == "__main__":
    app.run_server(debug=True)   
#    py.iplot(data, filename = 'time-series-simple')