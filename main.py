from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

#Definieren der Farbcodes
colors = {
    'background' : '#838b8b',
    'text' : '#FFFFFF',
    'titel' : '#ffa500',
    'balken' : '#ffa500'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


#daten importieren
df = pd.read_excel(r"C:\Users\ramon\Git\Plotly_Dashboard\data\KANTON_ZUERICH_Primaersektor.xls")
print(df.head())

#entferne der Zeilen, die "Region" oder "ganzer Kanton" beinhalten
df_kanton_bezirk = df[df['GEBIET_NAME'].str.contains('Region') == False]                             #definiert als df_gemeinde alle daten die nicht "Region" beinhalten
df_bezirk = df_kanton_bezirk[df_kanton_bezirk['GEBIET_NAME'].str.contains('ganzer Kanton') == False]    #definiert als df_gemeinde alle daten die nicht "ganzer Kanton" beinhalten
df_gemeinde = df_bezirk[df_bezirk['GEBIET_NAME'].str.contains('Bezirk') == False]           #definiert als df_gemeinde alle daten die nicht "Bezirk" beinhalten
print(df_gemeinde.head())

#nach GEBIETS_NAME gruppieren
df_gemeinde_group= df_gemeinde.groupby('GEBIET_NAME')
df_gemeinde_mean= df_gemeinde.groupby('GEBIET_NAME').mean()
print(df_gemeinde_mean.head())

#Plot erstellen
plot_gemeinde_mean = px.bar(df_gemeinde_mean, y='INDIKATOR_VALUE', barmode='group')


#Layout anpassen
plot_gemeinde_mean.update_layout(
    plot_bgcolor=colors['background'],      #Hintergrundfareb hinter den Balken
    paper_bgcolor=colors['background'],     #Hintergrundfarbe hinter Text
    font_color=colors['text'],
)



#Erstellen der Beschriftung des Dashboards
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[       #Hintergrundfarbe hinter Titel bestimmen
    html.H1(
        children='Dashboard',                                                           #Titel: Dashboard
        style={
            'textAlign': 'center',                                                      #Zentriert darstellen
            'color': colors['titel']                                                     #Textfarbe bestimmen
    }),
    html.Div(children='Durchschnittliche Anzahl Arbeitsstätten im Primärsektor nach Gemeinden.',
        style={                                                                         #Plotbeschritung erstellen
            'textAlign': 'center',                                                          #Beschriftung zentrieren
            'color': colors['text']                                                         #Textfarbe bestimmen
    }),
    html.Div(children='Wählen sie eine Gemeinde',
        style={
            'color' : colors['text']
        }),
        html.Div([
            dcc.Dropdown(
                df_gemeinde_group['GEBIET_NAME'].unique(),
                id='xaxis-column'
            )
        ],  style={'width': '48%', 'display': 'inline-block'})
    ])

dcc.Graph(
    id='mean_plot',
    figure=plot_gemeinde_mean
)


#In Browser darstellen
if __name__ == '__main__':
    app.run_server(debug=True)

