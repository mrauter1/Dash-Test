import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import medidor
import base64

def retornaMedidor(porcentagem, id=''):
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([dcc.Graph('', figure=medidor.fazHtmlMedidor(porcentagem),
                                        style={'height': '100%'})],
                             className='medidorInt1',
                             style={'position': 'absolute', 'top': '0', 'height': '200%',
                                    'width': '100%', 'backgroundColor': 'inherited'}
                             )],
                        className='medidorContainer',
                        style={'position': 'relative', 'width': '100%', 'content': '', 'display': 'block',
                               'padding-top': '50%', 'overflow': 'hidden'})
                       ], className='medidorWrapper')
    ], id=id, className='medidorWrapper2')


def retoraBarraEntregas(entregasAtual, app, id=''):
    entregasMax=15

    if entregasAtual > entregasMax:
        entregasMax = entregasAtual

    return html.Div([html.H3("{:.0f} entregas".format(entregasAtual)),
                     html.Img(src=app.get_asset_url('truck-icon.png'),
                              className='truckIcon'
                              ),
                     #html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
                     html.Div([
                         daq.GraduatedBar(
                             id=id,
                             color={"gradient": True,
                                    "ranges": {"#872d00": [0, 5], "yellow": [5, 13], "green": [13, 15], "red": [15, entregasMax]}},
                             showCurrentValue=False,
                             max=entregasMax,
                             size=250,
                             # label='13 Entregas',
                             value=entregasAtual,
                             style={'display': 'inline-block',
                                    'textAlign': 'center', 'height': '40px'}
                         )],
                         style={'height': '40px', 'verticalAlign': 'top', 'display': 'inline-block'},
                         className='barWrapper'
                     )
                     ],
                    style={'whiteSpace': 'nowrap', 'verticalAlign': 'top'})
