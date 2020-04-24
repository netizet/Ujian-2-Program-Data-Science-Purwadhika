import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
    )

tsa = pd.read_csv('~/Downloads/tsv.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('Ujian Modul 2 Dashboard TSA'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Tabs([
        dcc.Tab(value='Tab-1', label = 'DataFrame Table', children =[html.Div(children=[
            html.Div([
                html.P('Smoker'),
                dcc.Dropdown(value='',
                id='filter-smoker',
                options=[{'label': 'No','value': 'No'},
                {'label': 'Yes','value': 'Yes'},
                {'label': 'None','value': ''}])],
                className='col-3'),
            html.Br(),
            html.Div([
                html.P('Max Rows:'),
                dcc.Input(id ='filter-row',
                type = 'number',
                value = 10)], 
                className = 'row col-3'),
            html.Div(children =[
                html.Button('search',id = 'filter')],
                className = 'row col-4'),

            html.Div(id='div-table', children=[generate_table(tips)])

            dcc.Tab(value='Tab-2', label = 'Bar Chart', children =[
                html.Div([html.Div([
                    html.Div([html.P('Category 1'),
                        dcc.Dropdown(value='sex',
                                    id='filter-category-bar1',
                                    options=[{'label': 'Sex','value': 'sex'}, 
                                             {'label': 'Smoker','value': 'smoker'},
                                             {'label': 'Day','value': 'day'},
                                             {'label': 'Time','value': 'time'},
                                             {'label': 'Size','value': 'size'}])
                                                 ], className = 'col-3'),
                           
                        html.Div([html.P('Category 2'),
                        dcc.Dropdown(value='sex',
                                    id='filter-category-bar2',
                                    options=[{'label': 'Sex','value': 'sex'}, 
                                             {'label': 'Smoker','value': 'smoker'},
                                             {'label': 'Day','value': 'day'},
                                             {'label': 'Time','value': 'time'},
                                             {'label': 'Size','value': 'size'}])
                                                 ], className = 'col-3'),
            
                        html.Div([html.P('Numerical'),
                        dcc.Dropdown(value='tip',
                                    id='filter-number-bar',
                                    options=[{'label': 'Tip','value': 'tip'}, 
                                             {'label': 'Total Bill','value': 'total_bill'},
                                            ])
                                                 ], className = 'col-3'),

                                                ], className = 'row'),
        dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': tips['smoker'], 'y': tips['tip'], 'type': 'box', 'name': 'smoker'},
                {'x': tips['sex'], 'y': tips['tip'], 'type': 'violin', 'name': 'sex'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
    ])]),
    dcc.Tab(value='Tab-3', label = 'Scatter Chart', children= [
        html.Div(children = [html.Div([html.P('Category'),
            dcc.Graph(
                id = 'graph-scatter',
                figure = {'data': [
                    go.Scatter(
                        x = tips[tips['day'] == i]['tip'],
                        y = tips[tips['day'] == i]['total_bill'],
                        mode='markers',
                        name = 'Day {}'.format(i)
                        ) for i in tips['day'].unique()
                    ],
                    'layout':go.Layout(
                        xaxis= {'title': 'Tip'},
                        yaxis={'title': ' Total Bill'},
                        title= 'Tips Dash Scatter Visualization Separated by day',
                        hovermode='closest'
                    )
                }
            )])
            ]),
            dcc.Tab(value='Tab-4', label = 'Pie Chart',children=[
                html.Div(children = [html.Div([
                        html.Div([html.P('Numerical'),
                        dcc.Dropdown(value='tip',
                                    id='filter-number',
                                    options=[{'label': 'Tip','value': 'tip'}, 
                                             {'label': 'Total Bill','value': 'total_bill'},
                                            ])
                                                 ], className = 'col-4'),

                                                ], className = 'row'),
        dcc.Graph(
        id = 'pie-chart',
        figure = {
            'data':[
        go.Pie(labels = [i for i in tips['sex'].unique()], 
        values= [tips[tips['sex'] == i]['tip'].mean() for i in tips['sex'].unique()]
        )],
        'layout': go.Layout(title = 'Tip mean divided by Sex')}
    )])
    ]),            
    
    ],content_style={
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'padding': '44px'
            })
], style={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })

@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'), 
    State(component_id = 'filter-smoker', component_property = 'value'),
    State(component_id = 'filter-sex', component_property = 'value'),
    State(component_id = 'filter-day', component_property = 'value'),
    State(component_id = 'filter-time', component_property = 'value')]
)
def update_table(n_clicks,row, smoker, sex, day, time):
    tips = sns.load_dataset('tips')
    if smoker != '':
        tips = tips[tips['smoker'] == smoker]
    if sex != '':
        tips = tips[tips['sex'] == sex]
    if day != '':
        tips = tips[tips['day'] == day]
    if time != '':
        tips = tips[tips['time'] == time]
    children = [generate_table(tips, page_size = row)]
    return children

#Update Pie Chart
@app.callback(Output('pie-chart', 'figure'),
               [Input('filter-category', 'value'),
                Input('filter-number', 'value')])
def update_pie(category,number):
    return {
            'data':[
        go.Pie(labels = [i for i in tips[category].unique()], 
        values= [tips[tips[category] == i][number].mean() for i in tips[category].unique()]
        )],
        'layout': go.Layout(title = '{} mean divided by {}'.format(number,category))}

#Update Scatter plot
@app.callback(Output('graph-scatter', 'figure'),
              [Input('filter-category-scatter', 'value')])
def update_scatter(category):
    return {'data': [
                    go.Scatter(
                        x = tips[tips[category] == i]['tip'],
                        y = tips[tips[category] == i]['total_bill'],
                        mode='markers',
                        name = '{} {}'.format(category.capitalize(), i)
                        ) for i in tips[category].unique()
                    ],
                    'layout':go.Layout(
                        xaxis= {'title': 'Tip'},
                        yaxis={'title': ' Total Bill'},
                        title= 'Tips Dash Scatter Visualization Separated by {}'.format(category),
                        hovermode='closest'
                    )
                }

@app.callback(Output('example-graph', 'figure'),
            [Input('filter-category-bar1', 'value'),
            Input('filter-type-1', 'value'),
            Input('filter-category-bar2', 'value'),
            Input('filter-type-2', 'value'),
            Input('filter-number-bar', 'value')])
def update_bar(category1, type1, category2, type2, number):
    return {
            'data': [
                {'x': tips[category1], 'y': tips[number], 'type': type1, 'name': category1},
                {'x': tips[category2], 'y': tips[number], 'type': type2, 'name': category2}
            ],
            'layout': {
                'title': 'Tips Dash Data Visualization'
            }
        }            

    
if __name__ == '__main__':
    app.run_server(debug=True)

