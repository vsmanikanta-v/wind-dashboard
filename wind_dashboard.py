import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
# Sample wind speed data for three locations (monthly average)
locations = {
    "Chennai": [5.1, 5.3, 5.7, 6.0, 6.2, 6.1, 5.9, 5.8, 5.5, 5.3, 5.2, 5.0],
    "Hyderabad": [4.2, 4.3, 4.6, 5.0, 5.3, 5.5, 5.1, 4.9, 4.7, 4.5, 4.4, 4.3],
    "Jaipur": [3.9, 4.0, 4.2, 4.6, 5.0, 5.2, 5.1, 4.8, 4.6, 4.4, 4.2, 4.0],
}

# Turbine power curve (simplified)
wind_speeds = np.arange(0, 25, 1)
power_output = [0 if v < 3 else min(1.2 * (v - 3) ** 2, 1500) for v in wind_speeds]

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Wind Energy Feasibility Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Wind Energy Feasibility Dashboard", style={'textAlign': 'center'}),

    html.Label("Select Location:"),
    dcc.Dropdown(
        id='location-dropdown',
        options=[{'label': loc, 'value': loc} for loc in locations.keys()],
        value='Chennai'
    ),

    dcc.Graph(id='historical-graph'),
    dcc.Graph(id='forecast-graph'),
    dcc.Graph(id='power-curve')
], style={'width': '85%', 'margin': 'auto', 'fontFamily': 'Arial'})

# Callbacks for graphs
@app.callback(
    Output('historical-graph', 'figure'),
    Output('forecast-graph', 'figure'),
    Output('power-curve', 'figure'),
    Input('location-dropdown', 'value')
)
def update_dashboard(location):
    months = pd.date_range("2023-01-01", periods=12, freq='M')
    speeds = locations[location]

    # Historical wind speed data
    df_hist = pd.DataFrame({
        "Month": months,
        "Wind Speed (m/s)": speeds
    })

    fig_hist = px.line(df_hist, x="Month", y="Wind Speed (m/s)",
                       title=f"Historical Wind Speeds - {location}",
                       markers=True)

    # Forecast (dummy model: shift and add noise)
    next_months = pd.date_range("2024-01-01", periods=6, freq='M')
    forecast = pd.Series(np.roll(speeds, -6)[:6]) + np.random.normal(0, 0.2, 6)

    df_forecast = pd.DataFrame({
        "Month": next_months,
        "Forecasted Wind Speed (m/s)": forecast
    })

    fig_forecast = px.line(df_forecast, x="Month", y="Forecasted Wind Speed (m/s)",
                           title=f"Forecasted Wind Speeds - {location}",
                           markers=True)

    # Power curve
    df_power = pd.DataFrame({
        "Wind Speed (m/s)": wind_speeds,
        "Estimated Power Output (kW)": power_output
    })

    fig_power = px.line(df_power, x="Wind Speed (m/s)", y="Estimated Power Output (kW)",
                        title="Wind Turbine Power Curve", markers=True)

    return fig_hist, fig_forecast, fig_power

# Run server
if __name__ == '__main__':
    app.run(debug=True)