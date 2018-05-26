import plotly.graph_objs as go

def create_fig(df):
    trace1 = go.Scatter(
        x=df['Per'],
        y=df['NAV'],
        name='NAV'
    )
    trace2 = go.Scatter(
        x=df['Per'],
        y=df['Uitgegeven aandelen'],
        name='Uitgegeven aandelen',
        yaxis='y2'
    )
    data = [trace1, trace2]
    layout = go.Layout(
        yaxis=dict(
            title='NAV'
        ),
        yaxis2=dict(
            title='Uitgegeven aandelen',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig
