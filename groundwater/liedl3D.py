import json
import plotly

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.special import erf


def create_liedl3DPlot(parameters):
    Ca, Cd, Ct, g, M, Th, Tv, W= parameters

    # Functions
    def f_lm(x):  # Liedl 2011- f(x) = 0
        return erf(W / (np.sqrt(4 * Th * x))) * np.exp(-Tv * x * (np.pi / (2 * M)) ** 2) - (np.pi / 4) * (
                (g * Ct + Ca) / (g * Cd + Ca))

    def df_lm(x):  # FD estimate df
        h = 1e-4
        return (f_lm(x + h) - f_lm(x - h)) / (2 * h)

    # Finding the appropriate starting value

    ma_1 = -1 / (np.pi * (Th / W ** 2) * np.log(1 - (0.25 * np.pi * ((g * Ct + Ca) / (g * Cd + Ca)))))
    ma_2 = -2 / (np.pi ** 2 * (Tv / M ** 2)) * np.log(0.25 * np.pi * ((g * Ct + Ca) / (g * Cd + Ca)))
    ma_3 = 4 / np.pi ** 2 * (M ** 2 / Tv) * np.log((4 / np.pi) * ((g * Cd + Ca) / (g * Ct + Ca)))

    ma_x0 = np.minimum(np.maximum(ma_1, ma_2), ma_3)

    min_x0 = np.minimum(-1 / (np.pi * (Th / W ** 2) * np.log(1 - (0.25 * np.pi * ((g * Ct + Ca) / (g * Cd + Ca))))), \
                        -2 / (np.pi ** 2 * (Tv / M ** 2)) * np.log(0.25 * np.pi * ((g * Ct + Ca) / (g * Cd + Ca))))

    if ma_x0 == ma_3:
        x0 = ma_x0
    else:
        x0 = min_x0

    # Newton Raphson simulation using FD to obtain Lmax

    def NR(x):
        iterat = 0
        tol = 1e-06
        h = f_lm(x) / df_lm(x)

        while abs(h) >= tol:
            h = f_lm(x) / df_lm(x)
            x = x - h
            iterat += 1
        return x

    lMax = NR(x0)
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
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON, lMax
