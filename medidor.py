import plotly.graph_objs as go
import plotly.offline as ploff
import math

def fazHtmlBarraHorizontal(porcentagem):
    trace1 = go.Bar(
        y=['Peso', 'Entregas'],
        x=[5, 4],
        name='Percentual',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(
                color='rgba(246, 78, 139, 1.0)',
                width=2)
        )
    )
    trace2 = go.Bar(
        y=['Peso', 'Entregas'],
        x=[5, 6],
        name='Disponível',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(
                color='rgba(58, 71, 80, 1.0)',
                width=2)
        )
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack',
        height=300
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def fazHtmlMedidor(porcentagem):
    # --- Styling Constants ---
    # Modern color palette (gradient of blues for meter_chart)
    METER_CHART_COLORS = [
        '#E0F7FA',  # Lightest cyan/blue - for "Vazio"
        '#B2EBF2',  # Light cyan/blue
        '#80DEEA',  # Medium cyan/blue
        '#4DD0E1',  # Stronger cyan/blue
        '#26C6DA'   # Darker cyan/blue - for "Cheio"
    ]
    BACKGROUND_WHITE_COLOR = 'rgb(255, 255, 255)'
    EMPTY_GAUGE_SEGMENT_COLOR = 'rgb(240, 240, 240)' # Light grey for unused part of meter

    BASE_CHART_LABEL_COLOR = 'rgb(120, 120, 120)'  # Neutral grey for "0", "20", ...
    BASE_CHART_LINE_COLOR = 'rgb(200, 200, 200)'   # Light grey for base chart lines

    POINTER_COLOR = 'rgb(60, 60, 60)'             # Dark grey for pointer
    POINTER_LINE_COLOR = 'rgb(30, 30, 30)'        # Darker grey for pointer border
    
    ANNOTATION_TEXT_COLOR = 'rgb(50, 50, 50)'     # Dark grey for central percentage text
    INSIDE_LABEL_TEXT_COLOR = 'rgb(0, 0, 0)'      # Black for "Vazio", "Pouco", ... for readability on light blue

    BASE_CHART_LABEL_FONT_SIZE = 10
    METER_CHART_LABEL_FONT_SIZE = 10 # For "Vazio", "Pouco", etc.
    ANNOTATION_FONT_SIZE = 18
    
    # --- Chart Definitions ---

    base_chart = {
        "values": [40, 10, 10, 10, 10, 10, 10], # 40 for invisible top, 6 * 10 for segments
        "labels": ["-", "0", "20", "40", "60", "80", "100"],
        "marker": {
            "colors": [
                BACKGROUND_WHITE_COLOR, # Invisible top part
                BACKGROUND_WHITE_COLOR, # Segment for "0" label (mostly invisible)
                BACKGROUND_WHITE_COLOR, # Segment for "20" label
                BACKGROUND_WHITE_COLOR, # etc.
                BACKGROUND_WHITE_COLOR,
                BACKGROUND_WHITE_COLOR,
                BACKGROUND_WHITE_COLOR
            ],
            "line": {
                "width": 0.5, # Thinner line for base chart
                "color": BASE_CHART_LINE_COLOR 
            }
        },
        "name": "GaugeBase",
        "hole": .4, # Inner hole size
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108, # Rotates chart to start "0" at the right place
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside",
        "textfont": {
            "color": BASE_CHART_LABEL_COLOR,
            "size": BASE_CHART_LABEL_FONT_SIZE
        }
    }

    # The gauge visually represents 0-100% across its colored segments.
    # The original code divides the input `porcentagem` by 2 for segment calculation.
    effective_percentage_for_segments = porcentagem / 2

    # Helper function to calculate pointer path for the gauge
    def _calculate_pointer_path(percentage_value, pointer_base_x=0.5, pointer_base_y=0.5):
        """
        Calculates the SVG path for the gauge's pointer.
        The pointer reflects the original `percentage_value` (0-100).
        """
        # Constants for pointer geometry
        POINTER_LENGTH = 0.14 # Slightly shorter to not overlap hole edge too much
        POINTER_WIDTH_FACTOR = 0.01 # Slightly wider base for the pointer
        ARROW_ANGLE_OFFSET = 90  # Angle offset for the sides of the pointer arrow head
        
        # This factor adjusts the horizontal projection of the pointer.
        # It was likely empirically determined to make the pointer look right within the gauge's aspect ratio.
        CATETO_ADJ_PROPORTION_FACTOR = 0.92

        def _calculate_rotated_point_for_pointer(length, angle_degrees, x0, y0):
            """
            Calculates a point (x, y) by rotating around a center (x0, y0) by a given angle.
            This is used to determine the vertices of the pointer triangle.
            """
            angle_rad = math.radians(angle_degrees)
            sine_val = math.sin(angle_rad)
            cosine_val = math.cos(angle_rad)
            
            # y_displacement is based on sine: y_displacement = sine_val * length
            # x_displacement is based on cosine, adjusted by CATETO_ADJ_PROPORTION_FACTOR:
            # x_displacement = cosine_val * length * CATETO_ADJ_PROPORTION_FACTOR
            #
            # The coordinates are calculated for a standard Cartesian system,
            # then adapted by the Plotly 'paper' reference frame (0,0 bottom-left, 1,1 top-right).
            # x0, y0 is the center of rotation (typically 0.5, 0.5 for the gauge center).
            #
            # For x-coordinate:
            #   A positive cosine (angle between -90 and 90, i.e. right half) means x_displacement is positive.
            #   We subtract it from x0 (x0 - x_displacement), so pointer moves left from center.
            # For y-coordinate:
            #   A positive sine (angle between 0 and 180, i.e. upper half) means y_displacement is positive.
            #   We add it to y0 (y0 + y_displacement), so pointer moves up from center.
            # This orientation matches how the angle is calculated for the gauge (0 degrees top, 180 bottom).
            
            final_x = x0 - (cosine_val * length * CATETO_ADJ_PROPORTION_FACTOR)
            final_y = y0 + (sine_val * length)
            return final_x, final_y

        # The gauge is semi-circular (180 degrees). Map the input percentage (0-100) to this angular range.
        # An input `percentage_value` of 0 corresponds to an angle of 0 degrees.
        # An input `percentage_value` of 100 corresponds to an angle of 180 degrees.
        # This angle is relative to the gauge's "zero" point. Given the gauge rotation,
        # angle 0 might be "straight up" or "left" depending on `rotation` in `base_chart`.
        # The original `rotation: 108` for `base_chart` and `rotation: 90` for `meter_chart`
        # means the 0-100 scale runs roughly from left to right.
        angle_for_pointer = percentage_value * 180 / 100.0

        # Tip of the pointer
        x1, y1 = _calculate_rotated_point_for_pointer(POINTER_LENGTH, angle_for_pointer, pointer_base_x, pointer_base_y)
        
        # Base points of the pointer (creating a triangular shape)
        # These points are perpendicular to the main pointer line, forming the base of the triangle.
        x2, y2 = _calculate_rotated_point_for_pointer(POINTER_WIDTH_FACTOR, angle_for_pointer - ARROW_ANGLE_OFFSET, pointer_base_x, pointer_base_y)
        x3, y3 = _calculate_rotated_point_for_pointer(POINTER_WIDTH_FACTOR, angle_for_pointer + ARROW_ANGLE_OFFSET, pointer_base_x, pointer_base_y)
        
        # SVG path for a triangle: M(ove) to point 2, L(ine) to point 1 (tip), L(ine) to point 3, Z (close path)
        return f'M {x2:.4f} {y2:.4f} L {x1:.4f} {y1:.4f} L {x3:.4f} {y3:.4f} Z'

    # Helper function to distribute the percentage into 5 segments for the gauge display
    def _distribute_percentage_to_segments(percentage_to_distribute, num_segments=5, max_value_per_segment=10):
        """
        Distributes the given percentage_to_distribute across a specified number of segments.
        Each segment can hold a maximum value (max_value_per_segment).
        Returns a list of values representing each segment.
        """
        segments = [0.0] * num_segments # Use float for potentially fractional percentages
        remaining_percentage = float(percentage_to_distribute) # Ensure it's float

        for i in range(num_segments):
            if remaining_percentage <= 0: # No more percentage to distribute
                break
            
            value_for_this_segment = min(remaining_percentage, float(max_value_per_segment))
            segments[i] = value_for_this_segment
            remaining_percentage -= value_for_this_segment
            
        return segments

    pointer_path = _calculate_pointer_path(porcentagem) # Use original `porcentagem` for pointer direction

    # Calculate the values for the 5 colored segments of the gauge.
    # These segments visually represent the `effective_percentage_for_segments`.
    segment_values = _distribute_percentage_to_segments(effective_percentage_for_segments, 5, 10)

    # The `meter_chart` is a pie chart used to show the gauge's colored segments.
    # It's designed as a semi-circle.
    # The first value in `meter_chart["values"]` is a large transparent segment (50)
    # that creates the semi-circle effect with `rotation: 90`.
    # The next 5 values are the colored segments calculated above.
    # The last value is the remaining "empty" part of the active gauge area.
    # The sum of the 5 colored segments + this empty part should equal 50 (to match the first transparent segment).
    # Original calculation for the empty part: (100 - porcentagem) / 2.
    # This is equivalent to 50 - (porcentagem / 2) = 50 - effective_percentage_for_segments.
    # Since sum(segment_values) is `effective_percentage_for_segments` (if it's <= 50),
    # the empty part is `50 - sum(segment_values)`.
    
    total_of_colored_segments = sum(segment_values)
    # Ensure empty_segment_value is not negative if total_of_colored_segments somehow exceeds 50
    # (e.g. if effective_percentage_for_segments > 50)
    empty_segment_value = max(0, 50.0 - total_of_colored_segments) 

    meter_chart_values = [50.0] + segment_values + [empty_segment_value]

    meter_chart_display_labels = ["", "Vazio", "Pouco", "Médio", "Bom", "Cheio", ""] # Adjusted for new colors
    
    meter_chart_marker_colors = \
        [BACKGROUND_WHITE_COLOR] + \
        METER_CHART_COLORS + \
        [EMPTY_GAUGE_SEGMENT_COLOR]

    meter_chart = {
        "values": meter_chart_values,
        "labels": meter_chart_display_labels,
        "marker": {
            'colors': meter_chart_marker_colors,
            'line': { 'width': 0.5, 'color': BASE_CHART_LINE_COLOR } # Thin lines between segments
        },
        "name": "GaugeMeter",
        "hole": .3, # Smaller hole for the meter part, creates layered effect
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90, # Aligns this pie with the base_chart's visible arc
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "textfont": {
            "color": INSIDE_LABEL_TEXT_COLOR,
            "size": METER_CHART_LABEL_FONT_SIZE
        },
        "hoverinfo": "none",
        "sort": False,
    }

    layout = {
        "autosize": True,
        "paper_bgcolor": 'rgba(0,0,0,0)', # Transparent background
        "plot_bgcolor": 'rgba(0,0,0,0)',  # Transparent plot area
        'margin': {
            'l': 15, # Left margin
            'r': 27, # Right margin
            'b': 10, # Bottom margin (reduced a bit)
            't': 10, # Top margin (reduced a bit)
            'pad': 4 # Padding
        },
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': pointer_path,
                'fillcolor': POINTER_COLOR,
                'line': {
                    'color': POINTER_LINE_COLOR,
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'x': 0.5,
                'y': 0.42, # Adjusted y for better centering with new hole sizes
                'text': '{:.0f}%'.format(porcentagem), # Added % symbol
                'showarrow': False,
                'font': {
                    'size': ANNOTATION_FONT_SIZE,
                    'color': ANNOTATION_TEXT_COLOR
                }
            }
        ]
    }

    # Ensure base_chart line width is 0 if it's meant to be invisible (original logic)
    # However, a thin line was configured above, which might be desirable.
    # For now, respecting the 'original logic' if it was truly to hide lines.
    # Re-evaluating: base_chart lines are the ticks/scale, so they should be visible.
    # The above change to base_chart['marker']['line']['width'] = 0.5 is intentional.
    # base_chart['marker']['line']['width'] = 0 # This would hide the scale lines.

    fig = {
        "data": [base_chart, meter_chart],
        "layout": layout
    }

    return fig