from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel(r"C:\Users\ramon\Git\Plotly_Dashboard\data\KANTON_ZUERICH_Primaersektor.xls")
print(df.head())


df_gemeinde = df[df['GEBIET_NAME'].str.contains('Region') == False]
df_gemeinde = df_gemeinde[df_gemeinde['GEBIET_NAME'].str.contains('ganzer Kanton') == False]

fig = px.histogram(df_gemeinde, x="INDIKATOR_VALUE" ,nbins=100)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

