import json
import plotly

import pandas as pd
import plotly.graph_objs as go


def create_singlePlot(lMax):
    df = pd.read_csv('groundwater/static/original.csv')
    trace1 = go.Scatter(
        x=[df['Site No.'].size / 2],
        y=[lMax],
        name='User Plume Length(LMax)',
        mode='markers',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    trace2 = go.Scatter(
        x=df['Site No.'],
        y=df['Plume length[m]'],
        mode='markers',
        name='Original Database Plume Length(LMax)',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        titlefont=dict(
            size=25
        ),
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        legend={
            "xanchor": "right",
            "y": 1,
            "x": 1
        },
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Site Number',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Plume Length (m)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
