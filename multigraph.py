import dash
import dash_html_components as html
import os
import flask
import mydash as md
import sqlcon
import dash_table
import dash_core_components as dcc
import sys
import traceback
from dash.dependencies import Output, Input

def log(texto):
    path = os.path.dirname(os.path.abspath(__file__))+"\\PainelLog.txt"
    if os.path.exists(path):
        open_command = 'a'
    else:
        open_command = 'w'

    f = open(path, open_command)
    f.write(texto)
    f.close()

app = dash.Dash()

def tabelaEntregas(leitor, codTransp, id=''):
    df = leitor.getDadosEntregas(codTransp)

    df.head(5)
    print('teste')
    print(df)
    return html.Div([
        html.Div([
            dash_table.DataTable(
                id=id,
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={
                    'whiteSpace': 'normal',
                    'textOverflow': 'ellipsis',
                    'minWidth': '10px',
                    'maxHeight': '30px',
                    'fontWeight': 'bold',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#93cacc'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#ddeeef'
                    }
                ],
                style_header={
                    'fontWeight': '900',
                    'color': 'white',
                    'backgroundColor': '#008489',
                    'borderColor': '#014b4e',
                },
                style_table={
                    'width': '100%',
                    'minHeight': '100px',
                    'border': 'thin lightgrey solid',
                    'backgroundColor': 'inherited'
                }
            )],
            style={'width': '100%'}
        )],
        className='tableContainer flexBox')

def DivCaminhao(Descricao, codTransp):
    retorno = ''

    leitor = sqlcon.LeitorCaminhoes(True)
    try:
        caminhao = leitor.getDadosCaminhao(codTransp)
		
        if caminhao.PesoMax > 0:
            perc = float(caminhao.PesoBruto*100/caminhao.PesoMax)
        else:
            perc = float(0)

        retorno = html.Div([
                html.H2(codTransp+'-'+Descricao),
                md.retoraBarraEntregas(caminhao.NroEntregas, app, 'barra'+codTransp),
                html.H3('%.0f de %.0f KG' % (caminhao.PesoBruto, caminhao.PesoMax)),
                md.retornaMedidor(perc, 'medidor'+codTransp),
                tabelaEntregas(leitor, codTransp, 'table'+codTransp)
                #html.H3('Valor dos pedidos: R$ 37500,00')
            ], className="grafico flexContainer")
    finally:
        leitor.close()

    return retorno

#app.css.config.serve_locally = True

layout = {
    'margin': {
        'l': 5,
        'r': 5,
        'b': 20,
        't': 20,
        'pad': 5
    },
}


def retornaDivDados():
    try:
        return html.Div([
            DivCaminhao('Sérgio', '001612'),
            DivCaminhao('Paulo', '001650'),
            DivCaminhao('Alex', '001640'),
        ], className="mainContainer flexBox")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        lines = '-'.join(lines)
        print(lines)
        log(lines)


app.layout = \
    html.Div([
        dcc.Interval(
            id='interval',
            interval=60 * 1000,  # in milliseconds
            n_intervals=0
        ),
        html.H1('Controle de Entregas', id='Titulo'),
        html.Div([
            #retornaDivDados() Vai ser atualizado no callback
            ], id='containerDados', className='flexContainer flexBox'
        )], className='main2 flexContainer')


@app.callback([Output('containerDados', 'children')],
              [Input('interval', 'n_intervals')])
def update_graph(n):
    return [retornaDivDados()]



# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server

# css_directory = os.getcwd()
# print(css_directory)
# stylesheets = ['styleGrid.css']
# static_css_route = '/static/'
#
#
# @app.server.route('{}<stylesheet>'.format(static_css_route))
# def serve_stylesheet(stylesheet):
#     if stylesheet not in stylesheets:
#         raise Exception(
#             '"{}" is excluded from the allowed static files'.format(
#                 stylesheet
#             )
#         )
#     return flask.send_from_directory(css_directory, stylesheet)
#
#
# for stylesheet in stylesheets:
#     app.css.append_css({"external_url": "/static/{}".format(stylesheet)})

#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

#app.scripts.append_script({"external_url": 'https://code.jquery.com/jquery-3.2.1.min.js'})

log('Iniciando servidor...')
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')