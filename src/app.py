import json
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input, State, ctx, ALL, no_update
import dash_bootstrap_components as dbc
from .classes.Unit import Unit
from .classes.Pool import Pool
from .classes.Shop import Shop
from .classes.util import number_shops, cdf_plot, n_other_shop_distribution, n_pool_shop_distribution

# Initialize the app - incorporate css
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "TFT Rolling: Probability of Hitting a Unit"

server = app.server

# Initialize game state
pool = Pool()
shops = [Shop(i) for i in range(1,12)]

cost_colors = ['secondary', 'success','primary', '4-cost', 'warning']


# Unit selection buttons
unit_collapse_buttons = html.Div(
    dbc.Container(
        [ 
            dbc.Button(
                f"{i}",
                id={'type': 'collapse-btn', 'cost': i},
                className="me-1",
                n_clicks=0,
                color=[cost_colors[i-1]],
                outline=True,
                style={'width': '18%'},
            ) for i in range(1, 6)
        ]
    )
)
collapse_group = dbc.Container([
    dbc.Collapse([
        dbc.Button(
            unit_name, 
            id={
                'index':unit_name, 
                'type': 'btn-unit', 
                'cost':i
                }, 
            color=[cost_colors[i-1]], 
            outline=True, 
            className="me-1", 
            n_clicks=0) 
        for unit_name in sorted(pool.unit_dict[i])
        ],
        id={'type': 'collapse', 'cost': i},
        is_open=False) 
    for i in range (1, 6)
])

# Inputs to describe game state
controls = html.Div([
    html.Div(
        children=[
            html.P('Select a unit and cost (default is random 4-cost)'),
            unit_collapse_buttons,
            html.Br(),
            collapse_group,
            dcc.Store('selected-unit', 
                      data=json.dumps({
                          'unit_name': '4-cost Unit',
                          'cost': 4
                      })),
            html.Br(),
            html.P('Star level of desired unit'),
            dcc.Dropdown(
                options=[1, 2, 3], 
                value=2, 
                id='star-level'),
            html.Br(),
            html.P('Level'),
            dcc.Dropdown(
                options=list(range(1, 11)), 
                value=8, 
                id='level'),
            html.Br(),
            html.P("Number of desired unit you've already purchased"),
            dcc.Dropdown(
                options=list(range(9)), 
                value=0, 
                id='nteam'),
            html.Br(),
            html.P('Number of desired unit on other boards and benches'),
            dbc.Input(
                placeholder='Integer (0+)', 
                type='number',
                value=0, 
                id='nother'),
            html.Br(),
            html.P('Number of others units of the same cost out of the pool'),
            dbc.Input(
                placeholder='Integer (0+)', 
                type='number',
                value=0, 
                id='n_out_of_pool'),
            html.Br(),
            html.Br(),
            html.Div(
                dbc.Button(
                    'Submit',
                    # [dbc.Spinner(size="sm"), " Loading..."],
                    id='submit-val', 
                    n_clicks=0),
                className="d-grid gap-2 col-12 mx-auto"
            ),

        ]
    )
])

# Output information and graphs
output = dbc.Card(
    [
        dbc.Container([
            html.Br(),
            html.Div(id='roll-string', children=''),
            html.Br(),
            ]),
        dbc.Container(
            dbc.Tabs([
                dbc.Tab(
                    dcc.Graph(id='roll-prob-plot', config = {'displayModeBar': False}), 
                    label='Roll Probability',
                    ),
                dbc.Tab(
                    dcc.Graph(id='n-other-plot', config = {'displayModeBar': False}), 
                    label='Units Held'),
                dbc.Tab(
                    dcc.Graph(id='n-pool-plot', config = {'displayModeBar': False}),
                    label='Pool Size'
                    )
            ])
        )
    ])

# define layout
app.layout = dbc.Container([
    html.Div(className='row',children='TFT: Expected Number of Rolls', style = {'textAlign': 'center', 'fontSize': 30}),
    html.Hr(),
    dbc.Row([
        dbc.Col(controls, width=4),
        dbc.Col(output, width=8)  
        ]),
    ])

@callback(
    Output(component_id='roll-string', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='nother', component_property='value'),
    State(component_id='n_out_of_pool', component_property='value'),
    State(component_id='level', component_property='value'),
)
def update_number_of_shops(n_clicks:int, unit_data:str, star_level:int, nteam:int, nother:int, n_out_of_pool:int, level:int)->str:
    """
    Callback running classes.util.number_shops() to calculate the expected number of shops given 
    the inputs from the user. The function returns a string to be displayed in the output
    panel in the roll-string div.
    
    Args:
        n_clicks (int): How many times the submit button has been clicked
        unit_data (str): json string of unit data, comes from the selected unit button
        star_level (int): Star level of the unit, reads from star-level dropdown
        nteam (int): The number of the selected unit you have on your team, input from the nteam dropdown
        nother (int): The number of the selected unit on other boards and benches, input from the nother input
        n_out_of_pool (int): The number of units of the same cost as the desired unit that are out of the pool, 
            input from the n_out_of_pool input
        level (int): Your team level, input from the level dropdown

    Returns:
        str: The expected number of shops until the desired unit is hit, formatted as a string
    """
    
    text = 'Expected # of shops:'

    if n_clicks > 0:
        unit_data = json.loads(unit_data)
        text = 'Expected # of shops until {} {} star: {}'.format(
            unit_data['unit_name'],
            star_level,
            number_shops(
                Unit(unit_data['unit_name'], unit_data['cost']), 
                nteam=nteam, 
                npool=pool.size(unit_data['cost']) - n_out_of_pool - nteam - nother, 
                nother=nother, 
                star=star_level,
                level=level, 
                shop=shops[level-1],
                round_to_int=True
                )
            )

    return text

@callback(
    Output(component_id='roll-prob-plot', component_property='figure'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='nother', component_property='value'),
    State(component_id='n_out_of_pool', component_property='value'),
    State(component_id='level', component_property='value'),
)
def roll_probability(n_clicks:int, unit_data:str, star_level:int, nteam:int, nother:int, n_out_of_pool:int, level:int):
    """
    Callback running classes.util.cdf_plot() to display CDF for the probability of hitting the desired unit
    star level after a certain number of rolls. Please see classes.util.cdf_plot() for more details on the how
    the CDF is calculated. 
    
    Args:
        n_clicks (int): How many times the submit button has been clicked
        unit_data (str): json string of unit data, comes from the selected unit button
        star_level (int): Star level of the unit, reads from star-level dropdown
        nteam (int): The number of the selected unit you have on your team, input from the nteam dropdown
        nother (int): The number of the selected unit on other boards and benches, input from the nother input
        n_out_of_pool (int): The number of units of the same cost as the desired unit that are out of the pool, 
            input from the n_out_of_pool input
        level (int): Your team level, input from the level dropdown

    Returns:
        plotly.graph_objects._figure.Figure: CDF barplot of the probability of hitting the desired unit
    """
    
    if n_clicks > 0:
        
        unit_data = json.loads(unit_data)
        fig = cdf_plot(
            Unit(unit_data['unit_name'], unit_data['cost']), 
            nteam=nteam, 
            npool=pool.size(unit_data['cost']) - n_out_of_pool - nteam - nother, 
            nother=nother, 
            star=star_level,
            level=level, 
            shop=shops[level-1]
        )
    
    else:
        
        fig = px.bar()
        fig.update_layout(
            xaxis_title="Shop rolls",
            yaxis_title="Probability of hitting",
            title="Probability of hitting a unit as you roll",
            template="simple_white",
            font_size=14,
            title_font_size=20,
        )

    return fig

@callback(
    Output(component_id='n-other-plot', component_property='figure'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='n_out_of_pool', component_property='value'),
    State(component_id='level', component_property='value'),
)
def n_other_plot(n_clicks:int, unit_data:str, star_level:int, nteam:int, n_out_of_pool:int, level:int):
    """
    Callback running classes.util.n_other_shop_distribution() to display the expected number of shops
    until the desired unit star level is hit as the copies of this unit in the pool changes. Please see
    classes.util.n_other_shop_distribution() for more details on the how the expected number of shops is calculated.

    Args:
        n_clicks (int): How many times the submit button has been clicked
        unit_data (str): json string of unit data, comes from the selected unit button
        star_level (int): Star level of the unit, reads from star-level dropdown
        nteam (int): The number of the selected unit you have on your team, input from the nteam dropdown
        n_out_of_pool (int): The number of units of the same cost as the desired unit that are out of the pool, 
            input from the n_out_of_pool input
        level (int): Your team level, input from the level dropdown

    Returns:
        plotly.graph_objects._figure.Figure: Bar plot showing expected number of shops. 
    """
    
    
    if n_clicks > 0:
        unit_data = json.loads(unit_data)
        fig = n_other_shop_distribution(
            Unit(unit_data['unit_name'], unit_data['cost']), 
            nteam=nteam, 
            npool=pool.size(unit_data['cost']) - n_out_of_pool - nteam, 
            star=star_level,
            level=level, 
            shop=shops[level-1]
        )
    else:
        fig = px.bar()
        fig.update_layout(
            xaxis_title="# of unit left in pool",
            yaxis_title="Expected # of shops",
            title="Effect of # left in pool on expected # of shops",
            template="simple_white",
            font_size=14,
            title_font_size=20,
        )
        fig.update_traces(hovertemplate="# Left: %{x}<br>Expected # Shops: %{y}")
   

    return fig

@callback(
    Output(component_id='n-pool-plot', component_property='figure'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='nother', component_property='value'),
    State(component_id='level', component_property='value'),
)
def n_pool_plot(n_clicks,unit_data, star_level, nteam, nother, level):
    """
    Callback running classes.util.n_pool_shop_distribution() to display the expected number of shops
    until the desired unit star level is hit as pool size of that unit's cost changes. Please see
    classes.util.n_pool_shop_distribution() for more details on the how the expected number of shops is calculated.

    Args:
        n_clicks (int): How many times the submit button has been clicked
        unit_data (str): json string of unit data, comes from the selected unit button
        star_level (int): Star level of the unit, reads from star-level dropdown
        nteam (int): The number of the selected unit you have on your team, input from the nteam dropdown
        nother (int): The number of the selected unit on other boards and benches, input from the nother input
        level (int): Your team level, input from the level dropdown

    Returns:
        plotly.graph_objects._figure.Figure: Bar plot showing expected number of shops.
    """
    
    if n_clicks > 0:
        unit_data = json.loads(unit_data)
        fig = n_pool_shop_distribution(
            Unit(unit_data['unit_name'], unit_data['cost']), 
            nteam=nteam, 
            nother=nother, 
            star=star_level,
            level=level, 
            shop=shops[level-1],
            units_per_cost=len(set(unit.name for unit in pool.units[unit_data['cost']]))
        )
    else:
        fig = px.bar()
        fig.update_layout(
            xaxis_title="# of other same-costs left in pool",
            yaxis_title="Expected # of shops",
            title="Effect of same-cost pool size on expected # of shops",
            template="simple_white",       
            font_size=14,
            title_font_size=20,
        )
        fig.update_traces(hovertemplate="# Left: %{x}<br>Expected # Shops: %{y}")
    return fig

    
@callback(
    [Output({"type": "btn-unit", "index": ALL, "cost":ALL}, "className"),
     Output("selected-unit", "data")], 
    Input({"type": "btn-unit", "index":ALL, "cost":ALL}, "n_clicks"),
    Input({"type": "btn-unit", "index":ALL, "cost":ALL}, "id"),
    prevent_initial_call=True)
def btn_active(n_clicks:list, ids:list) -> list:
    """
    Callback to update the class of selected button (btn-unit) to "active",
    which changes its color. Callback also updates the selected unit data in the store.

    Args:
        n_clicks (list): List of number of times a btn-unit has been clicked
        ids (list): List of ids of the btn-units

    Returns:
        list: List of new button class names
        str: JSON string of the selected unit and cost
    """
    
    # If no button is clicked, return default class names
    if not ctx.triggered or not any(n_clicks):
        return ["me-1" for _ in n_clicks]

    button_index = ctx.triggered_id['index']
    # Determine the active button and assign "active" class
    return [
        "me-1 active" if button_index == id_['index'] else "me-1" for id_ in ids
    ], json.dumps({'unit_name':ctx.triggered_id['index'], 'cost':ctx.triggered_id['cost']})
    
@callback(
    [Output({"type": "collapse", "cost": ALL}, "is_open"),
     Output({"type": "collapse-btn", "cost": ALL}, "className")],
    Input({"type": "collapse-btn", "cost": ALL}, "n_clicks"),
    Input({"type": "collapse-btn", "index":ALL, "cost":ALL}, "id"),
    State({"type": "collapse", "cost": ALL}, "is_open"),
    prevent_initial_call=True)
def toggle_collapse(n_clicks:list, collapse_btn_ids:list, is_open:list) -> list:
    """
    Callback to toggle the collapse of the unit selection buttons.
    The function also updates the class of the selected collapse button to "active",

    Args:
        n_clicks (list): List of number of times a collapse button has been clicked
        collapse_btn_ids (list): List of ids of the collapse buttons
        is_open (list): List of boolean values indicating if the collapse is open

    Returns:
        list: List of boolean values indicating if the collapse is open
        list: List of new collapse button class names
    """
    # If no button is clicked, return default class names
    if not ctx.triggered or not any(n_clicks):
        return [False for _ in n_clicks], ["me-1" for _ in n_clicks]

    # Determine the active button and assign "active" class
    button_cost = ctx.triggered_id['cost']
    return [
        not is_open[i] if i == button_cost - 1 else False for i in range(5)
    ], [
        "me-1 active" if i == button_cost - 1 else "me-1" for i in range(5)
    ]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)