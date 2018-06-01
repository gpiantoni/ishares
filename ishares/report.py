import plotly.graph_objs as go
from plotly.offline import plot
from docutils.core import publish_file

from .constants.paths import PLOTLY_PATH, SRC_PATH, HTML_PATH


REPORT_NAV = """
.. raw:: html

    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

.. raw:: html
    :file: img/{fig_name}.html
"""


def write_report(fig, fund_id):

    fig_name = fund_id + '_NAV'
    save_plotly_fig(fig, fig_name)
    report = REPORT_NAV.format(fig_name=fig_name)

    rst_file = SRC_PATH / (fund_id + '.rst')
    html_file = HTML_PATH / (fund_id + '.html')

    with rst_file.open('w') as f:
        f.write(report)

    publish_file(
        source_path=str(rst_file),
        destination_path=str(html_file),
        writer_name='html',
        )


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


def save_plotly_fig(fig, name):
    div = plot(fig, include_plotlyjs=False, output_type='div', show_link=False)
    with (PLOTLY_PATH / (name + '.html')).open('w') as f:
        f.write(div)
