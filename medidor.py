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
    base_chart = {
        "values": [40, 10, 10, 10, 10, 10, 10],
        "labels": ["-", "0", "20", "40", "60", "80", "100"],
        #"domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)'
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside",
    }

    percentual = porcentagem / 2


    def pathSeta(percentual):
        def calculaRetaInclinada(tamanho, angulo, x0=0.5, y0=0.5):
            seno = math.sin(math.radians(angulo))
            coseno = math.cos(math.radians(angulo))
            catetoOposto = seno * tamanho
            catetoAdj = coseno * tamanho
            catetoAdj = catetoAdj * 0.92 # para manter a proporção
            print('{:.4f} {:.4f}'.format(x0-catetoAdj, y0+catetoOposto))
            return x0-catetoAdj, y0+catetoOposto

        angulo = percentual * 180 / 100.00
        x1, y1 = calculaRetaInclinada(0.15, angulo)

        x2, y2 = calculaRetaInclinada(0.005, angulo-90)

        x3, y3 = calculaRetaInclinada(0.005, angulo+90)

        #path = 'M 0.495 0.5 L {:.4f} {:.4f} L 0.505 0.5 Z'.format(x1, y1)
        path = 'M {:.4f} {:.4f} L {:.4f} {:.4f} L {:.4f} {:.4f} Z'.format(x2, y2, x1, y1, x3, y3)
        print(path)
        return path


    def ajustaSetorGrafico(percentual):
        if percentual >= 10:
            val = 10
        else:
            val = percentual
        percentual = percentual-val
        return percentual, val


    path = pathSeta(porcentagem)

    percentual, val1 = ajustaSetorGrafico(percentual)
    percentual, val2 = ajustaSetorGrafico(percentual)
    percentual, val3 = ajustaSetorGrafico(percentual)
    percentual, val4 = ajustaSetorGrafico(percentual)
    percentual, val5 = ajustaSetorGrafico(percentual)

    meter_chart = {
        "values": [50, val1, val2, val3, val4, val5, (100-porcentagem)/2],
        ##"values": [50, 5, 20, 12, 0, 8, 5],
        "labels": ["Lotação do Caminhão", "Vazio", "Pouco", "Médio", "Bom", "Cheio", "-"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(232,226,202)',
                'rgb(226,210,172)',
                'rgb(223,189,139)',
                'rgb(223,162,103)',
                'rgb(220,148,78)',
                'rgb(255, 255, 255)'
            ]
        },
        #"domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none",
        "sort": False,
    }

    layout = {
        "autosize": True,
        "paper_bgcolor": 'rgba(0,0,0,0)',
        "plot_bgcolor": 'rgba(0,0,0,0)',
        'margin': {
            'l': 15,
            'r': 27,
            'b': 20,
            't': 0,
            'pad': 5
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
                'path': path,
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                #'xref': 'paper',
                #'yref': 'paper',
                'x': 0.5,
                'y': 0.45,
                'text': '{:.0f} %'.format(porcentagem),
                'showarrow': False
            }
        ]
    }

    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0

    fig = {
        "data": [base_chart, meter_chart],
        "layout": layout
    }

    return fig