import dash
from dash import dcc, html, Input, Output   # modern Dash imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import webbrowser

# Load the CSV data (assuming 'data.csv' is in the same directory as this script)
df = pd.read_csv('data.csv')

# Drop the 'diagnosis' column if it exists
if 'diagnosis' in df.columns:
    df.drop(columns=['diagnosis'], inplace=True)

# Precompute correlation matrix for heatmap / "confusion" view
corr = df.corr()

# Create the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Breast Cancer Analysis', style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Histogram', 'value': 'histogram'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Tree Map', 'value': 'treemap'},
            {'label': 'Heat Map (Correlation)', 'value': 'heatmap'},
            {'label': 'Confusion Matrix (Dummy)', 'value': 'confusion'}
        ],
        value='bar',
        style={'width': '50%', 'margin': 'auto'}
    ),

    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0],  # Default value is the first column
        style={'width': '50%', 'margin': 'auto', 'marginTop': '10px'}
    ),

    dcc.Graph(id='graph', style={'height': '80vh'}),

    html.Button(
        'Open in Plotly Dash',
        id='web-link',
        n_clicks=0,
        style={'margin': '20px'}
    )
], style={'backgroundColor': '#111111', 'color': '#7FDBFF', 'fontFamily': 'Arial'})


@app.callback(
    Output('graph', 'figure'),
    [Input('graph-type', 'value'),
     Input('column-dropdown', 'value')]
)
def update_graph(graph_type, selected_column):
    try:
        if graph_type == 'scatter':
            fig = px.scatter(
                df,
                x=df.index,
                y=selected_column,
                title=f'Scatter Plot of {selected_column}',
                color=selected_column
            )

        elif graph_type == 'histogram':
            fig = px.histogram(
                df,
                x=selected_column,
                title=f'Histogram of {selected_column}',
                color=selected_column
            )

        elif graph_type == 'pie':
            fig = px.pie(
                df,
                names=selected_column,
                title=f'Pie Chart of {selected_column}',
                color=selected_column
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

        elif graph_type == 'bar':
            fig = px.bar(
                df,
                x=df.index,
                y=selected_column,
                title=f'Bar Chart of {selected_column}',
                color=selected_column
            )

        elif graph_type == 'line':
            fig = px.line(
                df,
                x=df.index,
                y=selected_column,
                title=f'Line Chart of {selected_column}',
                color=selected_column
            )

        elif graph_type == 'treemap':
            fig = px.treemap(
                df,
                path=[selected_column],
                title=f'Treemap of {selected_column}',
                color=selected_column
            )

        elif graph_type == 'heatmap':
            # Correlation heatmap using only Plotly
            fig = px.imshow(
                corr,
                x=corr.columns,
                y=corr.index,
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1,
                title='Heatmap of Correlation Matrix'
            )

        elif graph_type == 'confusion':
            # Dummy confusion-matrix-style heatmap using correlation matrix
            fig = go.Figure(
                data=go.Heatmap(
                    x=corr.columns,
                    y=corr.index,
                    z=corr.values,
                    colorscale='Viridis',
                    zmin=-1,
                    zmax=1
                )
            )
            fig.update_layout(title='Confusion Matrix (using correlation as placeholder)')

        else:
            fig = px.bar(
                df,
                x=df.index,
                y=selected_column,
                title=f'Bar Chart of {selected_column}',
                color=selected_column
            )

        fig.update_layout(template='plotly_dark')
        return fig

    except Exception as e:
        print(f"Error updating graph: {e}")
        return go.Figure()


@app.callback(
    Output('web-link', 'n_clicks'),
    [Input('web-link', 'n_clicks')]
)
def open_web_browser(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        webbrowser.open('http://localhost:9174')
    return n_clicks


if __name__ == '__main__':
    app.run(debug=True, port=9174)
