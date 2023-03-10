from dash import dcc, html, Input, Output, State
from app import app
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import flag
import emoji
import getViewLike
import datetime
from pathlib import Path

PLOTLY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/2449px-NASA_logo.svg.png"
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", alt="nasa-logo")),
                    dbc.Col(
                        dbc.NavbarBrand("JAMES WEBB SPACE TELESCOPE LAUNCH", className="ml-2")
                    ),
                ],
                align="center",
            ),
            style={'marginLeft': '20px'}
        ),
    ],
    color="dark",
    dark=True,
    sticky="top",
    className="justify-content-between"
)

f = open("01_Sentiment.txt", "r")
text = f.read()
text_lst = text.split(',')
result = []
for i in range(len(text_lst)):
    if text_lst[i] != '':
        result.append(text_lst[i])

opinion = 0
nonOpinion = 0
positive = 0
neutral = 0
negative = 0
for i in result:
    if i == 'O':
        nonOpinion += 1
    else:
        opinion += 1
        if i == '1':
            positive += 1
        elif i == '0':
            neutral += 1
        else:
            negative += 1

df = pd.DataFrame({'Sentiment': ['Opinion', 'Opinion', 'Opinion', 'Non-Opinion'],
                   'Emotion':   ['Positive', 'Neutral', 'Negative', None],
                   'Comment Count': [positive, neutral, negative, nonOpinion]})

sentiment_sum_fig = px.sunburst(df, path=["Sentiment", "Emotion"],values='Comment Count',width=700)
sentiment_sum_fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
sentiment_sum_fig.update_traces(rotation=180, selector=dict(type='sunburst'))

SENTIMENT = [
    dbc.CardHeader(html.H5("Sentiment analysis")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id='sentiment-sum-bar',figure=sentiment_sum_fig),
                    ),
                ]
            )
        ]
    ),
]

df_emoji = pd.read_csv('02_Emoji.csv', header=None)
df_emoji = df_emoji.rename(columns={0: 'name', 1: 'count'})
df_emoji_flt = df_emoji.loc[0:19,:]
emoji_name_lst = df_emoji_flt['name'].values.tolist()
emoji_name_lst_rev = emoji_name_lst[::-1]
emoji_count_lst = df_emoji_flt['count'].values.tolist()
emoji_count_lst_rev = emoji_count_lst[::-1]

emoji_figure = go.Figure(
    go.Bar(
        y=emoji_count_lst_rev,
        x=emoji_name_lst_rev,
    )
)
emoji_figure.update_layout(
    height=550,
    margin=dict(t=20, b=20, l=100, r=20, pad=4)
)
for i in range(len(emoji_figure.data[0].x)):
    x = emoji_figure.data[0].x[i]
    y = emoji_figure.data[0].y[i]
    if Path('./assets/' + x + '.svg').is_file():
        EMOJI_SVG = app.get_asset_url(x + '.svg')
    else:
        EMOJI_SVG = app.get_asset_url(x + '.png')
    emoji_figure.add_layout_image(
        source=EMOJI_SVG,
        x=x,
        y=y + 350,
        xref="x",
        yref="y",
        xanchor="center",
        sizex=300,
        sizey=300,
    )
emoji_figure.update_layout(xaxis={"visible":False})
emoji_figure.update_yaxes(range=[0, 4500])
EMOJI = [
    dbc.CardHeader(html.H5("Frequently Used Emojis")),
    dbc.CardBody(
        [
            dcc.Graph(id="frequency-emoji-fig", figure=emoji_figure)
        ]
    ),
]

df_comment = pd.read_csv('03_Comment.csv')
df_comment = df_comment.rename(columns={'0': 'count', 'Unnamed: 0': 'name'})
df_comment = df_comment.sort_values(by=['count'], ascending=False)
df_comment = df_comment.reset_index(drop=True)
df_comment_flt = df_comment.loc[0:19,:]
comment_name_lst = df_comment_flt['name'].values.tolist()
comment_name_lst_rev = comment_name_lst[::-1]
comment_name_count = df_comment_flt['count'].values.tolist()
comment_name_count_rev = comment_name_count[::-1]

frequency_figure_data = go.Figure(
    go.Bar(
        y=comment_name_count_rev,
        x=comment_name_lst_rev,
    )
)
frequency_figure_data.update_layout(
    height=550,
    margin=dict(t=20, b=100, l=100, r=100, pad=4)
)
frequency_figure_data.update_traces(texttemplate=comment_name_count_rev,textposition="inside")
USER = [
    dbc.CardHeader(html.H5("Top Participated User")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-user",
                            children=[dcc.Graph(id="user-bar", figure=frequency_figure_data)],
                            type="default",
                        )
                    ),
                ]
            )
        ]
    ),
]

df_peaktime = pd.read_csv('04_PeakTime.csv')
df_peaktime = df_peaktime.rename(columns={'0': 'count', 'Unnamed: 0': 'time'})
df_peaktime = df_peaktime.reset_index()
fig_peaktime = px.line(df_peaktime.iloc[3900:4000,:], x='time', y='count', markers=True)
PEAKTIME = [
    dbc.CardHeader(html.H5("Peaktime Comment")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-peaktime",
                            children=[dcc.Graph(id='peaktime',figure=fig_peaktime)],
                            type="default",
                        )
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            dcc.RangeSlider(0, 7644, 100, value=[3900, 4000], id='time-range-slider', marks=None)
                        ])
                    ]),
                ]
            ),
        ]
    ),
]

view = getViewLike.getView()
current = datetime.datetime.now()
update_text = str(current.year) + '-' + str(current.month) + '-' + str(current.day) + ' ' + str(current.hour) + ':' + str(current.minute)
VIEWCOUNT = [
    dbc.CardHeader(html.H5("View Count")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.P(view, style={"marginBottom": "0px"}),
                        style={"textAlign": "center", "fontSize": "50px", "marginBottom": "0px"}
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.P('last updated: ' + update_text),
                        style={"textAlign": "right", "fontSize": "10px", "marginBottom": "0px"}
                    ),
                ]
            ),
        ],
        style={"paddingBottom": "0px", "paddingTop": "0px"}
    ),
]

like = getViewLike.getLike()
current = datetime.datetime.now()
update_text = str(current.year) + '-' + str(current.month) + '-' + str(current.day) + ' ' + str(current.hour) + ':' + str(current.minute)
LIKECOUNT = [
    dbc.CardHeader(html.H5("Like Count")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.P(like, style={"marginBottom": "0px"}),
                        style={"textAlign": "center", "fontSize": "50px", "marginBottom": "0px"}
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.P('last updated: ' + update_text),
                        style={"textAlign": "right", "fontSize": "10px", "marginBottom": "0px"}
                    ),
                ]
            ),
        ],
        style={"paddingBottom": "0px", "paddingTop": "0px"}
    ),
]

count_all_comment  = df_peaktime['count'].sum()
current = datetime.datetime.now()
update_text = str(current.year) + '-' + str(current.month) + '-' + str(current.day) + ' ' + str(current.hour) + ':' + str(current.minute)
COMMENT = [
    dbc.CardHeader(html.H5("Comment Count")),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.P("{:.2f}".format(count_all_comment/1000) + ' k', style={"marginBottom": "0px"}),
                        style={"textAlign": "center", "fontSize": "50px", "marginBottom": "0px"}
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.P('last updated: ' + update_text),
                        style={"textAlign": "right", "fontSize": "10px", "marginBottom": "0px"}
                    ),
                ]
            ),
        ],
        style={"paddingBottom": "0px", "paddingTop": "0px"}
    ),
]

VIDEO = [
    html.Iframe(
        src="https://www.youtube.com/embed/7nT7JGZMbtM",
        title="JamesWebbVideo",
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",
        height="500px"
    )
]

NAVBAR2 = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col([
                        html.A(dbc.Button("Home", outline=False, color="#FFFF", className="me-2", href="", target="_blank"), href='#video-card')
                    ]),
                    dbc.Col([
                        html.A(dbc.Button("PeakTime", outline=False, color="#FFFF", className="me-2", href="", target="_blank"), href='#peaktime-card')
                    ]),
                    dbc.Col([
                        html.A(dbc.Button("Sentiment", outline=False, color="#FFFF", className="me-2", href="", target="_blank"), href='#sentiment-card')
                    ]),
                    dbc.Col([
                        html.A(dbc.Button("Emoji", outline=False, color="#FFFF", className="me-2", href="", target="_blank"), href='#emoji-card')
                    ]),
                    dbc.Col([
                        html.A(dbc.Button("Comment", outline=False, color="#FFFF", className="me-2", href="", target="_blank"), href='#user-card')
                    ]),
                    dbc.Col([
                        dbc.Button("About", outline=False, color="#FFFF", id="open-lg", className="me-2", n_clicks=0),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("About")),
                                dbc.ModalBody([
                                    html.P('Member'),
                                    html.Ul([
                                        html.Li('Napasakon Monbut 6420422009'),
                                        html.Li('Natchapat Youngchoay 6420422013'),
                                    ])
                                ]),
                            ],
                            id="modal-lg",
                            size="lg",
                            is_open=False,
                        )
                    ])
                ],
                align="center",
            ),
            style={'marginLeft': '20px'}
        ),
    ],
    color="#FFFF",
    dark=True,
    sticky="top",
    className="justify-content-between"
)

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(VIDEO)),], style={"marginTop": 30}, id='video-card'),
        dbc.Row([dbc.Col(dbc.Card(VIEWCOUNT)), dbc.Col(dbc.Card(COMMENT)), dbc.Col(dbc.Card(LIKECOUNT))], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(PEAKTIME)),], style={"marginTop": 30}, id='peaktime-card'),
        dbc.Row([dbc.Col(dbc.Card(SENTIMENT)),], style={"marginTop": 30}, id='sentiment-card'),
        dbc.Row([dbc.Col(dbc.Card(EMOJI)),], style={"marginTop": 30}, id='emoji-card'),
        dbc.Row([dbc.Col(dbc.Card(USER)),], style={"marginTop": 30, "paddingBottom": 30}, id='user-card'),
    ],
    className="mt-12",
)

app.layout = html.Div(id='main-layout', children=[NAVBAR, NAVBAR2, BODY],
    style={
        "backgroundImage": "url('https://images8.alphacoders.com/125/1255266.png')",
        "backgroundRepeat": "no-repeat",
        "backgroundAttachment": "fixed",
        "backgroundSize": "cover"
    }
)

@app.callback(
    Output('peaktime', 'figure'),
    [Input('time-range-slider', 'value')])
def update_output(value):
    fig_peaktime = px.line(df_peaktime.iloc[value[0]:value[1],:], x='time', y='count', markers=True)
    return fig_peaktime

def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output("modal-lg", "is_open"),
    Input("open-lg", "n_clicks"),
    State("modal-lg", "is_open"),
)(toggle_modal)

if __name__ == '__main__':
    app.run_server(debug=True)
