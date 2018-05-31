
COLS = [
    'Product-\ncode', 'ISIN',
    'Naam en aandelenklasse',
    'TER', 'Methodologie',
    'Beleggingscategorie', 'Sector / Thema', 'Regio',
    'Markt', 'Strategieën', 'Land', 'Aandelen-\nklasse',
    'Aantal uitstaande aandelen',
    'op jaarbasis (5 jr. (%))', 'Kenmerken (Uitkeringsrendement (%))'
]

df.loc[
    (df['ISIN'].isin(degiro_isin) &
    (df['Gebruik van\ninkomsten'] == 'Herbeleggend')  ),
    COLS].sort_values('TER')


from pandas import DataFrame
from datetime import date

bought = {
    'ISIN': [
        'IE00B4L5YC18',
    ],
    'Value': [
        50.92,
    ],
    'Currency': [
        'EUR',
        ],
    'Date': [
        date(2018, 5, 16),
        ]
    }
bought = DataFrame(bought)


change = (df.loc[1, 'NAV']  - bought['Value'].item()) / bought['Value'].item() * 100

trace1 = go.Scatter(
    x=df['Per'],
    y=df['NAV'],
    name='NAV'
)
trace2 = go.Scatter(
    x=[bought['Date'].item(), df.loc[1, 'Per']],  #TODO
    y=[bought['Value'].item(), bought['Value'].item()],
    mode='line',
    name='bought',
)
data = [trace1, trace2]
layout = go.Layout(
    yaxis=dict(
        title='NAV'
    ),
    annotations=[
        dict(
            x=df.loc[1, 'Per'],
            y=df.loc[1, 'NAV'],
            xref='x',
            yref='y',
            text=f'{change:0.3}%',
            showarrow=True,
            ax=0,
            ay=-40 * sign(change)
        ),
    ])
fig = go.Figure(data=data, layout=layout)
iplot(fig)
