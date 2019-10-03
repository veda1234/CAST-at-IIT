import json
import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib
import plotly
import plotly.graph_objs as go

matplotlib.use('Agg')


def exponenial_func(x, a, b, c):
    return a * np.exp(-b * x) + c


def create_scatterplot(feature, parameter, table_data, index):
    df = pd.read_csv('groundwater/static/original.csv')
    original_parameter_data = df[parameter].values.tolist()
    user_data = [item[index] for item in table_data]
    user_plume_length = [item[4] for item in table_data]
    merged_list = original_parameter_data + user_data
    y = df['Plume length[m]'].values.tolist() + user_plume_length

    index_of_nan = []
    for i in range(len(merged_list)):
        if str(merged_list[i]) == 'nan':
            index_of_nan += [i]

    for i in range(len(index_of_nan) - 1, -1, -1):
        element = y[index_of_nan[i]]
        y.remove(element)

    merged_list = [x for x in merged_list if str(x) != 'nan']

    if feature == 'Exponential':
        # exponential
        popt, pcov = curve_fit(exponenial_func, merged_list, y, p0=(1, 1e-6, 1))
        xx = np.linspace(1, len(merged_list), len(merged_list))
        yy = exponenial_func(xx, *popt)

        trace1 = go.Scatter(
            x=df[parameter],
            y=df['Plume length[m]'],
            mode='markers',
            marker=go.scatter.Marker(color='#ffa600', size=14),
            name='Original Data'
        )

        trace2 = go.Scatter(
            x=user_data,
            y=user_plume_length,
            mode='markers',
            marker=go.scatter.Marker(color='#003f5c', size=14),
            name='User Data'
        )

        trace3 = go.Scatter(
            x=xx,
            y=yy,
            mode='lines',
            marker=go.scatter.Marker(color='#bc5090'),
            line=dict(width=3),
            name='Fit'
        )
        layout = go.Layout(
            title='<b>Scatter Plot For Exponential Fit</b>',
            titlefont=dict(
                size=18,

            ),
            legend={
                "xanchor": "right",
                "y": 1,
                "x": 1
            },
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(229,229,229)',
            xaxis=dict(
                title=parameter,
                showgrid=True,
                gridcolor='rgb(255,255,255)',
                titlefont=dict(
                    size=18
                )
            ),
            yaxis=dict(
                title='<b>Plume Length</b>',
                showgrid=True,
                gridcolor='rgb(255,255,255)'
            )
        )
        data = [trace1, trace2, trace3]
    elif feature == 'Linear':
        # Generated linear fit
        slope, intercept, r_value, p_value, std_err = stats.linregress(merged_list, y)
        line = []
        for i in range(len(merged_list)):
            line.append(slope * merged_list[i] + intercept)
        trace1 = go.Scatter(
            x=df[parameter],
            y=df['Plume length[m]'],
            mode='markers',
            marker=go.scatter.Marker(color='#ffa600', size=14),
            name='Original Data'
        )

        trace2 = go.Scatter(
            x=user_data,
            y=user_plume_length,
            mode='markers',
            marker=go.scatter.Marker(color='#003f5c', size=14),
            name='User Data'
        )

        trace3 = go.Scatter(
            x=merged_list,
            y=line,
            mode='lines',
            line=dict(width=3),
            marker=go.scatter.Marker(color='#bc5090'),
            name='Fit'
        )
        layout = go.Layout(
            title='<b>Scatter Plot For Linear Fit</b>',
            titlefont=dict(
                size=18
            ),
            legend={
                "xanchor": "right",
                "y": 1,
                "x": 1
            },
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(229,229,229)',
            xaxis=dict(
                title=parameter,
                showgrid=True,
                gridcolor='rgb(255,255,255)',
                titlefont=dict(
                    size=18
                )
            ),
            yaxis=dict(
                title='<b>Plume Length</b>',
                showgrid=True,
                gridcolor='rgb(255,255,255)'
            )
        )
        data = [trace1, trace2, trace3]
    elif feature == 'Power 2':
        # calculate polynomial
        z = np.polyfit(merged_list, y, 2)
        f = np.poly1d(z)
        # calculate new x's and y's
        x_new = np.linspace(1, len(merged_list), len(merged_list))
        y_new = f(x_new)
        trace1 = go.Scatter(
            x=df[parameter],
            y=df['Plume length[m]'],
            mode='markers',
            marker=go.scatter.Marker(color='#ffa600', size=14),
            name='Original Data'
        )

        trace2 = go.Scatter(
            x=user_data,
            y=user_plume_length,
            mode='markers',
            marker=go.scatter.Marker(color='#003f5c', size=14),
            name='User Plume Length Data'
        )

        trace3 = go.Scatter(
            x=x_new,
            y=y_new,
            mode='lines',
            line=dict(width=3),
            marker=go.scatter.Marker(color='#bc5090'),
            name='Fit'
        )
        data = [trace1, trace2, trace3]
        layout = go.Layout(
            title='<b>Scatter Plot For Polynomial Power 2</b>',
            titlefont=dict(
                size=18
            ),
            legend={
                "xanchor": "right",
                "y": 1,
                "x": 1
            },
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(229,229,229)',
            xaxis=dict(
                title=parameter,
                showgrid=True,
                gridcolor='rgb(255,255,255)',
                titlefont=dict(
                    size=18
                )
            ),
            yaxis=dict(
                title='<b>Plume Length</b>',
                showgrid=True,
                gridcolor='rgb(255,255,255)'
            )
        )
    else:
        # calculate polynomial
        z = np.polyfit(merged_list, y, 3)
        f = np.poly1d(z)
        # calculate new x's and y's
        x_new = np.linspace(1, len(merged_list), len(merged_list))
        y_new = f(x_new)
        trace1 = go.Scatter(
            x=df[parameter],
            y=df['Plume length[m]'],
            mode='markers',
            marker=go.scatter.Marker(color='#ffa600', size=14),
            name='Original Data'
        )

        trace2 = go.Scatter(
            x=user_data,
            y=user_plume_length,
            mode='markers',
            marker=go.scatter.Marker(color='#003f5c', size=14),
            name='User Data'
        )
        trace3 = go.Scatter(
            x=x_new,
            y=y_new,
            mode='lines',
            line=dict(width=3),
            marker=go.scatter.Marker(color='#bc5090'),
            name='Fit'
        )
        data = [trace1, trace2, trace3]
        layout = go.Layout(
            title='<b>Scatter Plot For Polynomial Power 3</b>',
            titlefont=dict(
                size=18
            ),
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(229,229,229)',
            legend={
                "xanchor": "right",
                "y": 1,
                "x": 1
            },
            xaxis=dict(
                title=parameter,
                showgrid=True,
                gridcolor='rgb(255,255,255)',
                titlefont=dict(
                    size=18
                )
            ),
            yaxis=dict(
                title='<b>Plume Length</b>',
                showgrid=True,
                gridcolor='rgb(255,255,255)'
            )
        )

    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
