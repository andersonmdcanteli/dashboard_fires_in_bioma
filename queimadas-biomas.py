import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('biomas_dados_historicos.csv', encoding='latin-1') # lendo os dados

app = dash.Dash() # Criando a aplicação
server = app.server

# criando uma variável para armazenar os estados, para o usuario poder utilizar o dropdown e trocar de estado
biome_options = []
for biome in df['Bioma'].unique():
    biome_options.append({'label': biome, 'value': biome})

# Criando o layout
app.layout = html.Div([
    # cabeçalho
    html.Div([
        # Titulo
        html.H1("Dados de focos de queimadas por Bioma no Brasil entre os anos de 1998 e 2020",
                style = {'textAlign': 'center', # alinhando o titulo ao centro
                         'fontFamily': 'Roboto', # alterando a fonte do H1
                         'paddingTop': 20}), # adicionando um padding no topo
        # Aviso
        html.P("Selecione um bioma:",
              style = {'fontFamily': 'Roboto'}),
        # Dropdown
        html.Div([
            dcc.Dropdown(id = 'biome-picker', # id do dropdown
                     value = 'Amazônia', # seta o valor inicial,
                     options = biome_options, # as opções que vão aparecer no dropdown
                     clearable = False, # permite remover o valor (acho importante manter false para evitar problemas)
                     )
        ], style = {'width': '33%',
                            'display': 'inline-block'})
    ]),
    # Grafico de dispersão
    html.Div([
        # Titulo do gráfico de dispersão
        html.H3(id='titulo-scatter',
                style={'textAlign': 'center',
                       'fontFamily' : "Roboto",
                       'paddingTop': 15
                      }
               ),
        # O gráfico de dispersão
        dcc.Graph(id = 'scatter-plot')
         ], style = {'paddingLeft': '10%',
                     'padingRight': '10%',
                     'width': '80%',
                     'display': 'inline-block'}
    ),
    # Grafico de barras
    html.Div([
        # Titulo do gráfico de dispersão
        html.H3(id = 'titulo-barplot',
               style = {'textAlign': 'center',
                        'fontFamily': 'Roboto',
                        'paddingTop': 10
                       }
               ),
        # Gráfico de barras
        dcc.Graph(id = 'bar-plot')
    ], style = {'paddingLeft': '10%',
                     'padingRight': '10%',
                     'width': '80%',
                     'display': 'inline-block'}
    ),
    # Grafico de pizza
    html.Div([
        #Titulo de gráfico de rosquinha
        html.H3(id = 'titulo-pie',
               style = {'textAlign': 'center',
                        'fontFamily': 'Roboto',
                        'paddingTop': 10
                       }
               ),
        # Gráfico de rosquinha
        dcc.Graph(id = 'pie-plot')
    ], style = {'paddingLeft': '10%',
                     'padingRight': '10%',
                     'width': '80%',
                     'display': 'inline-block'}
    ),
    # Referencia
    html.Div([
        html.Label(["Fonte: ",
                html.A('queimadas.dgi.inpe.br',
                       href='http://queimadas.dgi.inpe.br/queimadas/portal-static/estatisticas_estados/'),
                        ". Acesso em 27/01/2021"
                   ]),
        html.Label([
            html.P(["Desenvolvido por Anderson Canteli (andersonmdcanteli@gmail.com)"])
        ])
            ], style={'textAlign': 'center',
                       'fontFamily' : "Roboto",
                       'paddingTop': 15
                      }
    )


])


# Grafico de rosquinha
@app.callback(Output('pie-plot', 'figure'),
              [Input('biome-picker', 'value')])
def update_pie_plot(selected_biome):

    df_aux = df[df['Bioma'] == selected_biome] # data frame filtrado baseado no selected_biome
    df_aux.reset_index(drop=True, inplace=True) # resetando o indice para facilitar a vida

    traco = [go.Pie(
                labels = df_aux['Ano'], # adicionando os labels das fatias de pizza
                values = df_aux['Total'], # adicionando o tamanho das fatais de pizza
                insidetextorientation='radial', # mudando a orientação do texto dentro das fatias
                hole=.3, # transformando a pizza em uma rosquinha
                )
            ]
    return {
            'data': traco,
            'layout': go.Layout(
                    annotations=[dict(text = 'Total', # Colocando o que será inserido dentro do buraco
                                      x = .5, # posição de x do centro do buraco da rosquinha
                                      y = 0.5, # posição de y do centro do buraco da rosquinha
                                      font_size = 24, # tamanho da fonte
                                      font_family = "Roboto", # alterando a fonte do texto
                                      showarrow = False, # removendo a seta que vem por padrão inserida
                                     )],
                  )
            }

# Titulo do gráfico de rosquinha
@app.callback(Output('titulo-pie', 'children'),
             [Input('biome-picker', 'value')])
def update_titulo_pie(selected_biome):
    return "Porcentagem do TOTAL de focos de queimadas por ano durante todo o período no bioma: " + str(selected_biome)



# Grafico de barras
@app.callback(Output('bar-plot', 'figure'),
              [Input('biome-picker', 'value')])
def update_bar_plot(selected_biome):

    df_aux = df[df['Bioma'] == selected_biome] # data frame filtrado baseado no selected_biome
    df_aux.reset_index(drop=True, inplace=True) # resetando o indice para facilitar a vida

    traco = [go.Bar(
            x = df_aux['Ano'], # os dados do eixo x
            y = df_aux['Total'], # dados do eio y
            name = selected_biome, # nome do bioma
            hovertemplate = ['Total de focos de queimadas: ' + i for i in [str(i) for i in (df_aux['Total'])]],
                )
            ]
    return {
            'data': traco,
            'layout': go.Layout(
                              xaxis = dict(title = 'Anos', linecolor='rgba(0,0,0,1)', tickmode = 'array', tickvals = df_aux['Ano'], ticktext = df_aux['Ano']), # adicionando nome eo eixo x, barra (y=0) na cor preta, e fixando o ano abaixo de todas as barras
                              yaxis = dict(title = 'Total de queimadas por ano', linecolor='rgba(0,0,0,1)', tickformat=False), # adicionando nome no eixo y, passando uma linha preta em x = 0, e removendo a formatação padrão dos ticks, para que não apareça o K
                              showlegend=True, # adicionando a legenda
                              hoverlabel=dict(bgcolor="white", # alterando a cor de fundo do hover
                                                font_size=16, # alterando o tamanho da letra no hover
                                                font_family="Roboto") # alterando a fonte do hover

                                )
                }


# Titulo do gráfico de barras
@app.callback(Output('titulo-barplot', 'children'),
             [Input('biome-picker', 'value')])
def update_titulo_barplot(selected_biome):
    return "Número TOTAL focos de queimadas por ano durante todo o período no bioma: " + str(selected_biome)


# Grafico de dispersão
@app.callback(Output('scatter-plot', 'figure'),
              [Input('biome-picker', 'value')])
def update_scatter(selected_biome):

    df_aux = df[df['Bioma'] == selected_biome] # data frame filtrado baseado no selected_biome
    df_aux.reset_index(drop=True, inplace=True) # resetando o indice para facilitar a vida

    tracos = [] # lista vazia para apendar os traços
    for i in range(df_aux.shape[0]):
        tracos.append(go.Scatter(
                            x = df_aux.columns.values[1:13], # os dados do eixo x
                            y = df_aux.loc[i][1:13], # acessando os dados dos meses (dados do eixo y)
                            mode = 'lines+markers', # define o tipo de gráfico, neste caso vai ter linhas e marcadores
                            name = str(df_aux['Ano'][i]), # adiciono o nome do traço
                            hovertemplate = df_aux.columns.values[1:13] + ' de ' + str(df_aux['Ano'][i]) + '<br>nº de focos: '
                            + [str(i) for i in list(df_aux.loc[i][1:13])] , # alterando o template do hover
        ))
    return {
        'data': tracos,
        'layout': go.Layout(
                           showlegend=True, # garante que a legenda será mostrada
                           hovermode = "closest", # garante que o hover irá mostrar os dados do ponto mais próximo a seta do mouse
                           hoverlabel=dict(bgcolor="white", # altera a cor de fundo
                                            font_size=16, # altera o tamanho da fonte
                                            font_family="Roboto"), # altera a fonte de texto
                           xaxis = dict(title = 'Meses', linecolor='rgba(0,0,0,1)'), # Nome do eixo x / adiciona uma linha preta em y=0
                           yaxis = dict(title = 'Número de focos de queimadas', linecolor='rgba(0,0,0,1)'),
                          )
    }

# Titulo do gráfico de dispersão
@app.callback(Output('titulo-scatter', 'children'),
             [Input('biome-picker', 'value')])
def update_titulo_scatter(selected_biome):
    return "Número de focos de queimadas por mês no bioma: " + str(selected_biome)


# Rodando a aplicação através de um servidor
if __name__ == '__main__':
    # app.run_server(debug = True, use_reloader = False)
    app.run_server()
