from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

#Definieren der Farbcodes
colors = {
    'background' : '#000000',
    'text' : '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


#daten importieren
df = pd.read_excel(r"C:\Users\ramon\Git\Plotly_Dashboard\data\KANTON_ZUERICH_Primaersektor.xls")
print(df.head())

#entferne der Zeilen, die "Region" oder "ganzer Kanton" beinhalten
df_gemeinde = df[df['GEBIET_NAME'].str.contains('Region') == False]                             #definiert als df_gemeinde alle daten die nicht "Region" beinhalten
df_gemeinde = df_gemeinde[df_gemeinde['GEBIET_NAME'].str.contains('ganzer Kanton') == False]    #definiert als df_gemeinde alle daten die nicht "ganzer Kanton" beinhalten
df_gemeinde = df_gemeinde[df_gemeinde['GEBIET_NAME'].str.contains('Bezirk') == False]           #definiert als df_gemeinde alle daten die nicht "Bezirk" beinhalten


#nach GEBIETS_NAME gruppieren
df_gemeinde= df_gemeinde.groupby('GEBIET_NAME').mean()
print(df_gemeinde.head())

#Plot erstellen
fig = px.bar(df_gemeinde, y='INDIKATOR_VALUE', barmode='group')

#Layout anpassen
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#Spalteninhalt zuweisen



#Erstellen der Beschriftung des Dashboards
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[       #Hintergrundfarbe bestimmen
    html.H1(
        children='Dashboard',                                                           #Titel: Dashboard
        style={
            'textAlign': 'center',                                                      #Zentriert darstellen
            'color': colors['text']                                                     #Textfarbe bestimmen
    }),
    html.Div(children='Durchschnittliche Anzahl Arbeitsstätten im Primärsektor nach Gemeinden.',
        style={                                                                         #Plotbeschritung erstellen
            'textAlign': 'center',                                                          #Beschriftung zentrieren
            'color': colors['text']                                                         #Textfarbe bestimmen
    }),
    html.Div(children=[
            html.Label('Dropdown'),
            dcc.Dropdown(['GEBIET_NAME']),




        ], ),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

#In Browser darstellen
if __name__ == '__main__':
    app.run_server(debug=True)

