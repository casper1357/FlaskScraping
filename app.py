from flask import Flask, render_template, request, Response
from sqlite.database_handling import *

import sqlite3
import io
import random
import pandas as pd
import json
import plotly
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/poe_streamers')
def poe_streamers():
    data = get_viewer_data()
    xnames = []
    xasciinames = []
    yviews = []
    ytotal_views = []
    for i in data[0]:
        xnames.append(i[0])
        yviews.append(i[1])
    for i in data[1]:
        xasciinames.append(i[0])
        ytotal_views.append(i[1])
    print(f"ASCII: {xasciinames}. VIEWS: {ytotal_views}")
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Scatter(x=xnames, y=yviews, name="Viewers"), row=1, col=1)
    fig.add_trace(go.Scatter(x=xasciinames, y=ytotal_views, name="Total views"), row=1, col=2)
    fig.update_layout(title_text='Top 10 POE streamers', title_x=0.5, font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print("Updated '/poe_streamers'")
    return render_template("poe_streamers.html", data=data, graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
    app.run()