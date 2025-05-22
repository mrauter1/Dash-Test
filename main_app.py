import dash
from dash import html # Updated import
# If using Dash version < 2.0, core components might be needed for other things, but not directly for this layout.
# from dash import dcc

# Import custom components
from mydash import retornaMedidor, retornaBarraEntregas

# Initialize the Dash app
# Link to an external CSS file that will be created in the 'assets' folder.
external_stylesheets = ['assets/custom_styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # Expose server for deployments

# --- Application Layout Styles have been moved to assets/custom_styles.css ---

# Define the layout of the application
app.layout = html.Div(
    className='main-app-container', # Styles from CSS
    children=[
        html.H1(
            "Operational Dashboard",
            className='app-title' # Styles from CSS
        ),

        html.Div(
            className='component-wrapper', # Styles for sections from CSS
            children=[
                html.H3(
                    "Gauge Indicator Example",
                    className='section-title' # Styles for section titles from CSS
                ),
                html.Div(
                    retornaMedidor(porcentagem=75, id='gauge-1'),
                    className='gauge-display-wrapper' # Styles from CSS for centering
                )
            ]
        ),

        html.Div(
            className='component-wrapper', # Styles for sections from CSS
            children=[
                html.H3(
                    "Delivery Bar Example",
                    className='section-title' # Styles for section titles from CSS
                ),
                # The retornaBarraEntregas component has its own internal flex styling for its children
                retornaBarraEntregas(entregasAtual=10, app=app, id='delivery-bar-1')
            ]
        ),
        
        # Example of components side-by-side (could be more complex)
        # This div uses both component-wrapper for general appearance and component-row for specific layout (if any in CSS)
        html.Div(
            className='component-wrapper component-row', # Combined classes
            style={'display': 'flex', 'justifyContent': 'space-around', 'alignItems': 'flex-start'}, # Flex styles remain inline
            children=[
                 html.Div(
                    style={'flex': 1, 'paddingRight': '10px'}, # Flex item for gauge
                    children=[
                        html.H4(
                            "Gauge 2 (30%)",
                            className='subsection-title' # Styles for subsection titles from CSS
                        ),
                        retornaMedidor(porcentagem=30, id='gauge-2')
                    ]
                ),
                html.Div(
                    style={'flex': 1, 'paddingLeft': '10px'}, # Flex item for bar
                    children=[
                        html.H4(
                            "Delivery Bar 2 (Over Capacity)",
                            className='subsection-title' # Styles for subsection titles from CSS
                        ),
                        retornaBarraEntregas(entregasAtual=18, app=app, id='delivery-bar-2')
                    ]
                )
            ]
        )
    ]
)

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
