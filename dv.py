import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
unemp_data=pd.read_csv("Processed_Unemp.csv")
app = dash.Dash(__name__)

df = pd.read_csv('agriculturedv.csv')
dffv = pd.read_csv('gvadv.csv')

app.layout = html.Div([
    html.Div(
        [
            html.H1("Impact of Covid-19 on Various Sectors"),
        ],
        style={'background-color': 'lightgray', 'text-align': 'center', 'padding': '20px', 'font-size': '24px'},
    ),

    html.Div(
        [
            dcc.Link("Agriculture", href="/agriculture", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            dcc.Link("Mining", href="/mining", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            dcc.Link("Construction", href="/construction", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            dcc.Link("GVA", href="/gdp", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            dcc.Link("AQI", href="/aqi", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            dcc.Link("Unemployment", href="/unemployment", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            dcc.Link("Covid Deaths", href="/covid_deaths", style={'color': 'white', 'text-decoration': 'none', 'margin': '10px', 'padding': '10px'}),
            # Add links for other sectors
        ],
        style={'background-color': 'black', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
    ),

    html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ],
        style={'padding': '20px', 'font-size': '18px'},
    ),

    html.Div(id='gdp-bar-chart-container'),  # Container for the Agriculture chart
    html.Div(id='gdp-line-chart-container'),  # Container for the Mining chart
    html.Div(id='sunburst-chart-container'),  # Container for the Sunburst chart
    html.Div(id='construction-line-chart-container'),
    dcc.Graph(id='unemployment-map'),
    dcc.Slider(
        id='month-slider',
        min=unemp_data['Month'].min(),
        max=unemp_data['Month'].max(),
        value=unemp_data['Month'].min(),
        marks={month: str(month) for month in unemp_data['Month'].unique()},
    ),
    
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/agriculture':
        return html.H2("Agriculture Data Goes Here")
    else:
        return html.H2("Covid - 19 Impact")
    # Add similar code blocks for other sectors

@app.callback(Output('gdp-bar-chart-container', 'children'), [Input('url', 'pathname')])
def update_gdp_bar_chart(pathname):
    if pathname == '/agriculture':
        agriculture_data = df.copy()
        figure = {
            'data': [
                {'x': agriculture_data['Period'], 'y': agriculture_data['GDP'], 'type': 'bar', 'name': 'GDP'},
            ],
            'layout': {
                'title': 'Agriculture GDP by Period',
                'xaxis': {'title': 'Period'},
                'yaxis': {'title': 'GDP'},
            }
        }
        return dcc.Graph(id='gdp-bar-chart', figure=figure)

@app.callback(Output('gdp-line-chart-container', 'children'), [Input('url', 'pathname')])
def update_gdp_line_chart(pathname):
    if pathname == '/mining':
        mdf = pd.read_csv('miningdv.csv')
        figure = {
            'data': [
                {'x': mdf['Month'], 'y': mdf['GDP'], 'type': 'line', 'name': 'GDP'},
            ],
            'layout': {
                'title': 'Mining GDP Over Time',
                'xaxis': {'title': 'Month'},
                'yaxis': {'title': 'GDP'},
            }
        }
        return dcc.Graph(id='gdp-line-chart', figure=figure)

@app.callback(Output('sunburst-chart-container', 'children'), [Input('url', 'pathname')])
def update_sunburst_chart(pathname):
    if pathname == '/gdp':
        fig = px.sunburst(dffv, path=['Sector', 'ConstantPrice'], values='SharesinCurrentPercent', color='CurrentPrice', title="Sector Hierarchy")
        return dcc.Graph(id='sunburst-chart', figure=fig)
dfc=pd.read_csv('constructiondv.csv')

import plotly.graph_objs as go

@app.callback(Output('construction-line-chart-container', 'children'), [Input('url', 'pathname')])
def update_construction_line_chart(pathname):
    if pathname == '/construction':
        fig = px.bar(dfc, x='Month', y='GDP', title='Construction GDP Over Time',
                        labels={'GDP': 'GDP Value', 'Month': 'Time Period'},
                        animation_frame='Month',  # Add animation frame
                        color='GDP', height=400,width=650)
            
            # Set a fixed range for the y-axis
        fig.update_layout(yaxis=dict(range=[0, dfc['GDP'].max() + 1000]))
        fig.update_xaxes(categoryorder='total ascending', categoryarray=dfc['Month'])
        return dcc.Graph(id='construction-line-chart-container',figure=fig)
    

@app.callback(Output('unemployment-map', 'figure'), [Input('month-slider', 'value')])
def update_unemployment_map(selected_month,pathname):
    # Define latitude and longitude coordinates for some Indian states (you can add more)
    if pathname == '/unemployment':
        india_states = {
            'Andhra Pradesh': (15.9129, 79.7400),
            'Karnataka': (15.3173, 75.7139),
            'Kerala': (10.8505, 76.2711),
            'Tamil Nadu': (11.1271, 78.6569),
            'Maharashtra': (19.7515, 75.7139),
            'Uttar Pradesh': (26.8467, 80.9462),
            'Bihar': (25.0961, 85.3131),
            'Rajasthan': (27.0238, 74.2179),
            'Gujarat': (22.2587, 71.1924),
            'West Bengal': (22.9868, 87.8550),
            'Madhya Pradesh': (23.4733, 77.9470),
            'Punjab': (31.1471, 75.3412),
            'Haryana': (29.0588, 76.0856),
            'Jharkhand': (23.6102, 85.2799),
            'Odisha': (20.9517, 85.0985),
            'Chhattisgarh': (21.2787, 81.8661),
            'Assam': (26.2006, 92.9376),
            'Telangana': (17.1232, 79.2089),
            'Uttarakhand': (30.0668, 79.0193),
            'Himachal Pradesh': (31.1048, 77.1734),
            'Jammu and Kashmir': (33.7782, 76.5762),
            'Goa': (15.2993, 74.1240),
            'Tripura': (23.9408, 91.9882),
            'Manipur': (24.6637, 93.9063),
            'Nagaland': (26.1584, 94.5624),
            'Meghalaya': (25.4670, 91.3662),
            'Arunachal Pradesh': (27.1004, 93.6166),
            'Sikkim': (27.5330, 88.5122),
            'Mizoram': (23.1645, 92.9376),
            'Lakshadweep': (10.5667, 72.6417),
            'Puducherry': (11.9416, 79.8083),
            'Chandigarh': (30.7333, 76.7794),
            'Dadra and Nagar Haveli and Daman and Diu': (20.1809, 73.0169),
            'Ladakh': (34.1526, 77.5770),
            'Lakshadweep': (10.5667, 72.6417)
        }

        fig = go.Figure()

        for state, (latitude, longitude) in india_states.items():
            state_data = unemp_data[(unemp_data['State'] == state) & (unemp_data['Month'] == selected_month)]
            fig.add_trace(go.Scattergeo(
                locationmode="ISO-3",
                lon=[longitude] * len(state_data),
                lat=[latitude] * len(state_data),
                text=state_data['Month'],
                mode="markers",
                marker=dict(
                    size=state_data['Unemployment Rate'] * 1,
                    colorscale="Viridis",
                    cmin=unemp_data['Unemployment Rate'].min(),
                    cmax=unemp_data['Unemployment Rate'].max(),
                    color=state_data['Unemployment Rate'],
                    colorbar=dict(title="Unemployment Rate"),
                ),
            ))

        fig.update_geos(
            projection_type="mercator",
            center=dict(lon=78, lat=23),
            scope='asia',
        )
        fig.update_layout(
            title=f"Unemployment Rate in Indian States in Quater {selected_month}",
        )

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
