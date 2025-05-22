from dash import html, dcc
import dash_daq as daq
import medidor
import base64

# Style dictionary for the main gauge graph
GRAPH_STYLE = {'height': '100%'}

# Styles for retornaMedidor
# MEDIDOR_WRAPPER_STYLE = { # Corresponds to original medidorWrapper2
# If it's just for ID, no specific style dict is needed here.
# }

# MEDIDOR_OUTER_CONTAINER_STYLE = { # Corresponds to original medidorWrapper
    # This also seems like a structural div, specific inline styles might not be needed if handled by classes.
# }

MEDIDOR_ASPECT_RATIO_CONTAINER_STYLE = { # Corresponds to original medidorContainer
    'position': 'relative', # For positioning the inner absolute div
    'width': '100%',             # Take full width of its parent
    'padding-top': '50%',        # Creates an aspect ratio of 2:1 (width:height). Height is 50% of width.
                                 # The graph will be placed absolutely within this box.
    'overflow': 'hidden',        # Hide parts of the graph that might overflow if not perfectly sized.
    'display': 'block',          # Ensure it behaves as a block element.
    # 'content': '' was present, but it's not a standard CSS property and likely has no effect. Removed.
}

MEDIDOR_INNER_GRAPH_CONTAINER_STYLE = { # Corresponds to original medidorInt1
    'position': 'absolute',
    'top': '0',
    'left': '0', # Added for completeness, ensuring it starts from top-left
    'height': '200%',            # This makes the graph container twice as tall as MEDIDOR_ASPECT_RATIO_CONTAINER_STYLE's height.
                                 # Since padding-top: 50% sets height relative to width, if width is W, height is 0.5W.
                                 # Then 200% of 0.5W is W. So the graph itself is rendered in a square area (W x W).
                                 # The gauge itself is likely designed for a square, and this ensures it.
    'width': '100%',
    # 'backgroundColor': 'inherited' is unusual and often default. Removing unless visual regression.
}


def retornaMedidor(porcentagem, id=''):
    """
    Creates a Dash HTML component for a gauge indicator.
    The gauge is rendered using a Plotly figure from medidor.fazHtmlMedidor.
    This function structures the gauge within HTML Divs for layout and styling.
    """
    # The structure is:
    # Wrapper (optional, for ID)
    #  OuterContainer (structural)
    #   AspectRatioBox (creates a 2:1 box, e.g., 200px wide, 100px tall)
    #    InnerGraphContainer (absolute, 200% height of AspectRatioBox, making it effectively 1:1 for the graph)
    #     Graph
    
    gauge_figure = medidor.fazHtmlMedidor(porcentagem)

    inner_graph_container = html.Div(
        dcc.Graph(
            id=f'{id}-graph' if id else 'gauge-graph', # Ensure graph has an ID if parent has one
            figure=gauge_figure,
            style=GRAPH_STYLE
        ),
        className='medidorInt1', # Keep original class name for potential CSS
        style=MEDIDOR_INNER_GRAPH_CONTAINER_STYLE
    )

    aspect_ratio_container = html.Div(
        inner_graph_container,
        className='medidorContainer', # Keep original class name
        style=MEDIDOR_ASPECT_RATIO_CONTAINER_STYLE
    )

    # The original 'medidorWrapper' and 'medidorWrapper2' seemed primarily for structure or ID.
    # We can simplify if they don't have distinct styling or functional roles beyond holding the ID.
    # For now, let's use one main wrapper that takes the ID.
    
    main_wrapper = html.Div(
        aspect_ratio_container,
        id=id if id else None, # Assign ID to this main wrapper
        className='medidorWrapper' # Use a general class name
    )
    
    return main_wrapper


# --- Styling Constants for Delivery Bar ---
DELIVERY_TEXT_COLOR = 'rgb(70, 70, 70)' # Consistent dark grey for text
DELIVERY_BAR_HEIGHT = '25px' # Sleeker bar height

# Color scheme for the GraduatedBar (shades of blue, consistent with gauge)
# Ranges: 0-5 (low), 5-10 (medium), 10-15 (optimal), >15 (over capacity)
DELIVERY_BAR_RANGES = {
    "#A0DEFF": [0, 5],    # Light Blue
    "#70CFFF": [5, 10],   # Medium Blue
    "#40BFFF": [10, 15],  # Strong Blue
    "#607D8B": [15, 100] # Cool Grey for over capacity (max extended to 100 for visual range)
}
# Note: entregasMax will dynamically set the top range for the grey color if it exceeds 15.

# Styles for retornaBarraEntregas
BARRA_ENTREGAS_MAIN_CONTAINER_STYLE = {
    'display': 'flex',        # Use flexbox for robust alignment
    'alignItems': 'center',   # Vertically center items in the flex container
    'padding': '5px 0',       # Add some vertical padding
}

BARRA_ENTREGAS_H3_STYLE = {
    'display': 'inline-block', # Keep it inline for flex layout
    'color': DELIVERY_TEXT_COLOR,
    'fontSize': '1em',      # Relative font size, can be adjusted
    'marginRight': '10px',    # Space before the truck icon
    'marginLeft': '5px',     # Space before the text
    'lineHeight': DELIVERY_BAR_HEIGHT, # Align text baseline with bar center
}

BARRA_ENTREGAS_IMAGE_STYLE = {
    # className='truckIcon' will handle most styling (e.g. actual image size)
    'verticalAlign': 'middle', # Good for general alignment if not in flex
    'marginRight': '8px',     # Space after truck icon, before bar
    'height': '24px',         # Explicit height for the icon if not set by CSS
    'width': 'auto',          # Maintain aspect ratio
}

BARRA_ENTREGAS_BAR_WRAPPER_STYLE = {
    'display': 'inline-block', # Keep it inline for flex layout
    'height': DELIVERY_BAR_HEIGHT,    # Consistent height
    'verticalAlign': 'middle', # Align with text/icon if not perfectly handled by flex
}

BARRA_ENTREGAS_GRADUATED_BAR_STYLE = {
    'display': 'inline-block',
    'textAlign': 'center',
    'height': DELIVERY_BAR_HEIGHT, # Matches the wrapper height
    'width': '250px' # Explicit width, was size property before
}


def retornaBarraEntregas(entregasAtual, app, id=''):
    """
    Creates a Dash HTML component for displaying delivery count with a graduated bar.
    Includes a title (H3), a truck icon, and the graduated bar.
    """
    entregasMaxFixed = 15 # The "optimal" max for color scaling
    
    # Adjust entregasMax for the daq.GraduatedBar's actual maximum value
    # If entregasAtual is higher than 15, the bar should extend to entregasAtual.
    # Otherwise, it should extend to at least 15 to show the full "optimal" range.
    current_bar_max = max(entregasAtual, entregasMaxFixed)

    # Update ranges for "over capacity" color if entregasAtual > entregasMaxFixed
    current_bar_ranges = {**DELIVERY_BAR_RANGES} # Create a mutable copy
    if entregasAtual > entregasMaxFixed:
         # The grey color should start from entregasMaxFixed up to current_bar_max
        current_bar_ranges["#607D8B"] = [entregasMaxFixed, current_bar_max]
    else:
        # Ensure the last defined range (blue) goes up to entregasMaxFixed
        current_bar_ranges["#40BFFF"] = [10, entregasMaxFixed]
        # If current_bar_max is greater than 15 due to entregasAtual being, say, 12,
        # but we want the grey part to only show if entregasAtual > 15,
        # we remove the grey part if not needed.
        if "#607D8B" in current_bar_ranges and entregasMaxFixed >= current_bar_max :
            # Remove the grey part if current_bar_max is just the fixed max (15)
            # and deliveries are not over capacity.
             if entregasAtual <= entregasMaxFixed:
                del current_bar_ranges["#607D8B"]


    # Title for the delivery bar
    title_text = html.H3(
        f"{entregasAtual:.0f} entregas",
        style=BARRA_ENTREGAS_H3_STYLE
    )

    # Truck icon
    truck_image = html.Img(
        src=app.get_asset_url('truck-icon.png'),
        className='truckIcon', # Styling primarily via CSS class
        style=BARRA_ENTREGAS_IMAGE_STYLE
    )

    # Graduated bar showing delivery progress
    graduated_bar = daq.GraduatedBar(
        id=f'{id}-bar' if id else 'delivery-bar',
        color={
            "gradient": True, # Enable gradient effect if supported/desired by colors
            "ranges": current_bar_ranges
        },
        showCurrentValue=False, # Value is shown in H3
        max=current_bar_max,  # Dynamically set max for the bar
        value=entregasAtual,
        style=BARRA_ENTREGAS_GRADUATED_BAR_STYLE,
        # size prop is removed as width is now in style
    )

    # Wrapper for the graduated bar
    bar_wrapper = html.Div(
        graduated_bar,
        className='barWrapper', # Keep class for CSS
        style=BARRA_ENTREGAS_BAR_WRAPPER_STYLE
    )

    # Main container for all elements
    main_container = html.Div(
        [title_text, truck_image, bar_wrapper],
        id=id if id else None, # Assign ID to the main container
        style=BARRA_ENTREGAS_MAIN_CONTAINER_STYLE
    )
    
    return main_container
