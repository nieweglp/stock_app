# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:10:58 2020

@author: Paul
"""

import pandas as pd
import yfinance
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# pip install yfinance
# pip install dash

companies_list = ['AMZN', 'GOOG', 'MSFT']

msft = yfinance.Ticker("MSFT")
df_msft = msft.history(period='max')[['Close']]

amzn = yfinance.Ticker("AMZN")
df_amzn = amzn.history(period='max')[['Close']]

goog = yfinance.Ticker("GOOG")
df_goog = goog.history(period='max')[['Close']]

data_dict = {'MSFT': df_msft, 'AMZN': df_amzn, 'GOOG': df_goog}

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='My stock app'),

    html.Div([
        html.Div(children='This app shows current stocks...'),
        dcc.Dropdown(
            id='companies_choice',
            options=[{'label': company, 'value': company}
                     for company in companies_list]
        )

    ], style={'width': '20%', 'display': 'inline-block'}),

    dcc.Graph(id='graph_plot')

])


@app.callback(
    Output('graph_plot', 'figure'),
    [Input('companies_choice', 'value')])
def update_figure(selected_company):
    if selected_company == None:
        return go.Figure()
    else:
        df_temp = data_dict[selected_company]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_temp.index,
                                 y=df_temp['Close'].values,
                                 mode='lines'))
        fig.update_layout(title='Stocks history for {} company'.format(selected_company),
                          xaxis_title='Date',
                          yaxis_title='Stock rate [USD]')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
