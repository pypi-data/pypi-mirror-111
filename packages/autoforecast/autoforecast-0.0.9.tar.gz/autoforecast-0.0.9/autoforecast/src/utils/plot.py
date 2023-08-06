import plotly.graph_objects as go

from autoforecast.src.utils.logger import LOG


def plot_scatter(y_true, y_pred, x):
    fig = go.Figure(data=go.Scatter(x=x, y=y_true, name="true"))
    # fig.add_trace(go.Scatter(x=x, y=y_true, name='true'))
    fig.add_trace(go.Scatter(x=x, y=y_pred, name="pred"))
    title = "my title"
    LOG.debug(title)
    fig.show()
