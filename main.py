import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import webbrowser
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Load the CSV data (assuming 'data.csv' is in the same directory as this script)
df = pd.read_csv('data.csv')

# Drop the 'diagnosis' column if it exists
if 'diagnosis' in df.columns:
    df.drop(columns=['diagnosis'], inplace=True)

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
            {'label': 'Heat Map', 'value': 'heatmap'},
            {'label': 'Confusion Matrix', 'value': 'confusion'}
        ],
        value='bar',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
        value=df.columns[0],  # Default value is the first column
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Graph(id='graph', style={'height': '80vh'}),  # Set the height to 80% of the viewport height
    html.Button('Open in Plotly Dash', id='web-link', n_clicks=0, style={'margin': '20px'})
], style={'backgroundColor': '#111111', 'color': '#7FDBFF', 'fontFamily': 'Arial'})

@app.callback(
    Output('graph', 'figure'),
    [Input('graph-type', 'value'), Input('column-dropdown', 'value')])
def update_graph(graph_type, selected_column):
    try:
        if graph_type == 'scatter':
            fig = px.scatter(df, x=df.index, y=selected_column, title=f'Scatter Plot of {selected_column}', color=selected_column)
        elif graph_type == 'histogram':
            fig = px.histogram(df, x=selected_column, title=f'Histogram of {selected_column}', color=selected_column)
        elif graph_type == 'pie':
            fig = px.pie(df, names=selected_column, title=f'Pie Chart of {selected_column}', color=selected_column)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        elif graph_type == 'bar':
            fig = px.bar(df, x=df.index, y=selected_column, title=f'Bar Chart of {selected_column}', color=selected_column)
        elif graph_type == 'line':
            fig = px.line(df, x=df.index, y=selected_column, title=f'Line Chart of {selected_column}', color=selected_column)
        elif graph_type == 'treemap':
            fig = px.treemap(df, path=[selected_column], title=f'Treemap of {selected_column}', color=selected_column)
        elif graph_type == 'heatmap':
            plt.figure(figsize=(12, 10))  # Increase the figure size
            sns.heatmap(df.corr(), annot=True, cmap='RdBu_r', fmt='.2f')  # Use 'RdBu_r' colormap
            plt.title('Heatmap of Correlation Matrix')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            fig = go.Figure(data=go.Image(source='data:image/png;base64,{}'.format(base64.b64encode(buf.getvalue()).decode())))
        elif graph_type == 'confusion':
            # Placeholder for confusion matrix (not implemented in detail here)
            fig = go.Figure(data=go.Heatmap(
                x=df.columns,
                y=df.columns,
                z=df.corr(),
                colorscale='Viridis'
            ))
            fig.update_layout(title=f'Confusion Matrix of {selected_column}')
        else:
            fig = px.bar(df, x=df.index, y=selected_column, title=f'Bar Chart of {selected_column}', color=selected_column)

        fig.update_layout(
            template='plotly_dark'
        )

        return fig

    except Exception as e:
        print(f"Error updating graph: {e}")
        return {}

@app.callback(
    Output('web-link', 'n_clicks'),
    [Input('web-link', 'n_clicks')])
def open_web_browser(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        webbrowser.open('http://localhost:9074')  # Change the port number here as well
    return n_clicks

if __name__ == '__main__':
    app.run_server(debug=True, port=9074)  # Change the port number here
