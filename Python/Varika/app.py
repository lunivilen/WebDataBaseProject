from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

""" DATA INPUT """

oil = pd.read_csv("Oil.csv")
petrol = pd.read_csv("Petrol.csv")
plastic = pd.read_csv("Plastic.csv")
tar = pd.read_csv("Tar.csv")
row_data = pd.concat([oil, petrol["Price of petrol"], plastic["Price of plastic"], tar["Price of tar"]], axis=1)

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

""" CORRELATION CALCULATION """

oil_price = ((oil.drop(columns="Date")).to_numpy()).transpose()
petrol_price = ((petrol.drop(columns="Date")).to_numpy()).transpose()
plastic_price = ((plastic.drop(columns="Date")).to_numpy()).transpose()
tar_price = ((tar.drop(columns="Date")).to_numpy()).transpose()

petrol_cor = px.scatter(
    x=oil["Price of oil"],
    y=petrol["Price of petrol"],
    labels={'x': "Цена на нефть", 'y': "Цена на бензин"},
    trendline="ols",
    title="График корреляции для цен на бензин *cor. index= " +
          str(round((np.corrcoef(oil_price, petrol_price))[0][1], 2))
)

plastic_cor = px.scatter(
    x=oil["Price of oil"],
    y=plastic["Price of plastic"],
    labels={'x': "Цена на нефть", 'y': "Цена на пластик"},
    trendline="ols",
    title="График корреляции для цен на пластик *cor. index= " +
          str(round((np.corrcoef(oil_price, plastic_price))[0][1], 2))
)

tar_cor = px.scatter(
    x=oil["Price of oil"],
    y=tar["Price of tar"],
    labels={'x': "Цена на нефть", 'y': "Цена на гудрон"},
    trendline="ols",
    title="График корреляции для цен на гудрон *cor. index= " +
          str(round((np.corrcoef(oil_price, tar_price))[0][1], 2))
)

""" FILTER """

filter_t = dcc.RadioItems(
    ['Бензин', 'Пластик', 'Гудрон'],
    'Бензин',
    inline=True,
    style={"text-align": "center", "margin-top": "20px"},
    id="type_filter"
)

""" LAYOUT """

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Анализ влияния цены нефти на стоимость нефтепродуктов",
                style={"text-align": "center", "margin-bottom": "20px"}),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Анализ данных', value='tab-1'),
            dcc.Tab(label='Сырые данные', value='tab-2'),
        ]),
        html.Div(id='tabs-content', style={"margin-top": "10px"}),
    ], style={"margin-top": "20px"})
], fluid=True)

""" TABS """


@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(filter_t),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=dict(
                        data=[dict(
                            x=oil["Date"],
                            y=oil["Price of oil"],
                            name="oil price",
                            marker=dict(
                                color='rgb(55, 42, 42'
                            )
                        )],
                        layout=dict(
                            title='График динамики цены на нефть',
                            showlegend=True,
                            legend=dict(
                                x=0,
                                y=1.0
                            ),
                            margin=dict(l=40, r=0, t=40, b=30)
                        )
                    ),
                        id='my-graph-example'
                    )
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="change")
                ], width=6),
                html.Div("Как мы видим, чем больше производственных шагов необходимо предпринять индустрии, чтобы "
                         "получить ту или иную продукции, тем меньше её стоимость зависит от цены на саму нефть"),
                html.Div("Найдём индекс корреляции этих величин, а также воспользуемся диаграммами "
                         "рассеяния для более наглядного представляние последнего")
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=petrol_cor)
                ], width=4),
                dbc.Col([
                    dcc.Graph(figure=plastic_cor)
                ], width=4),
                dbc.Col([
                    dcc.Graph(figure=tar_cor)
                ], width=4),
                html.Div("Подводя итоги вышесказанного я на наглядных примерах продемонстрировал, что "
                         "зависимость индекса цен конечных нефтепродуктов от цены самой нефти уменьшается"
                         " по мере увелечинеия количства производственных ступеней")
            ])
        ], style={"font-size": "18px", "margin-left": "20px", "margin-right": "20px"})
    elif tab == 'tab-2':
        return html.Div([
            dash_table.DataTable(row_data.to_dict('records'), [{"name": i, "id": i} for i in row_data.columns])
        ], style={"margin-left": "35px", "margin-right": "35px"})


""" CALLBACK FILTER """


@app.callback(
    Output(component_id='change', component_property='figure'),
    Input(component_id='type_filter', component_property='value')
)
def update_type_figure(material):
    if material == "Бензин":
        fig = dict(
            data=[dict(x=petrol["Date"], y=petrol["Price of petrol"], name="petrol price",
                       marker=dict(color='rgb(153, 153, 0'))],
            layout=dict(
                title="График динамики цен на бензин",
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=50, b=30)
            )
        )
        return fig

    elif material == "Пластик":
        fig = dict(
            data=[dict(x=plastic["Date"], y=plastic["Price of plastic"], name="plastic price",
                       marker=dict(color='rgb(54, 125, 73'))],
            layout=dict(
                title="График динамики цен на пластик",
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=50, b=30)
            )
        )
        return fig

    else:
        fig = dict(
            data=[dict(x=tar["Date"], y=tar["Price of tar"], name="tar price",
                       marker=dict(color='rgb(150, 50, 70'))],
            layout=dict(
                title="График динамики цен на гудрон",
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=50, b=30)
            )
        )
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
