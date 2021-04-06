# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:10:58 2020

@author: Paul
"""

import pandas as pd
import tweepy
import yfinance
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yaml
import text_analysis
import read_files

config = read_files.read_yaml_file('config.yaml')

consumer_key = config['TWITTER_ACCOUNT']['CONSUMER_KEY']
consumer_secret = config['TWITTER_ACCOUNT']['CONSUMER_SECRET']
access_token = config['TWITTER_ACCOUNT']['ACCESS_TOKEN']
access_token_secret = config['TWITTER_ACCOUNT']['ACCESS_TOKEN_SECRET']

authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
authenticate.set_access_token(access_token, access_token_secret)

api = tweepy.API(authenticate, wait_on_rate_limit=True)

df_names = read_files.read_stock_names_tickers('stocks_names.txt')
names_dict = df_names.to_dict()['name']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Stock analysis app',
            style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        html.Div(children='Choose stock, wich you are interested in'),
        dcc.Dropdown(
            id='companies_choice',
            options=[{'label': names_dict[company], 'value': company}
                     for company in names_dict]
        )

    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        dcc.RangeSlider(
            id='time_filter',
            updatemode='drag',
            marks={}
        )
    ], style={'width': '80%', 'display': 'inline-block'} ),
    html.Div([
    dcc.Graph(id='stock_plot'),
    dcc.Graph(id='sentiment_chart')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(id='current_tweets', style={'whiteSpace': 'pre-line', 'display': 'inline-block', 'width': '49%'})
] )

@app.callback(
    Output('stock_plot', 'figure'),
    [Input('companies_choice', 'value')])
def update_stock_plot(selected_company):
    if selected_company != None:
        df_temp = yfinance.Ticker(selected_company)
        df_temp = df_temp.history(period='max')[['Close']]
        # df_temp = df_temp.loc[slider_value]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_temp.index,
                                 y=df_temp['Close'].values,
                                 mode='lines'))
        fig.update_layout(title='Stocks history for {} company'.format(selected_company),
                          xaxis_title='Date',
                          yaxis_title='Stock rate [USD]')
        return fig
    else:
        return go.Figure()

@app.callback(
    Output('current_tweets', 'children'),
    Input('companies_choice', 'value'))
def update_tweets(selected_company):
    if selected_company != None:
        tweets = tweepy.Cursor(api.search, q=names_dict[selected_company], 
                            lang="en").items(100)
        tweets_content = [text_analysis.clean_text(tweet.text) + '\n' for tweet in tweets]
        return tweets_content[:20]

@app.callback(
    Output('sentiment_chart', 'figure'),
    Input('companies_choice', 'value'))
def update_sentiment_chart(selected_company):
    if selected_company != None:
        tweets = tweepy.Cursor(api.search, q=names_dict[selected_company], 
                            lang="en").items(100)
        df = pd.DataFrame([tweet.text for tweet in tweets], columns=['Tweets'])
        df['Tweets'] = df['Tweets'].apply(text_analysis.clean_text)
        df['Subjectivity'] =  df['Tweets'].apply(text_analysis.get_subjectivity)
        df['Polarity'] =  df['Tweets'].apply(text_analysis.get_polarity)
        df['Sentiment'] = df['Polarity'].apply(text_analysis.get_sentiment)
        df_sentiment_output = df['Sentiment'].value_counts().sort_index(ascending=False)
        fig = go.Figure()
        sentiment_color = {'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'}
        fig.add_trace(go.Bar(x=df_sentiment_output.index,
                            y=df_sentiment_output.values,
                            orientation='v',
                            marker=dict(
                                        color=[color for sentiment, color in sentiment_color.items() if sentiment in df_sentiment_output.index.to_list()],
                                        opacity=0.5)))
        return fig
    else:
      return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)
