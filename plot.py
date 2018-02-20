import plotly
from plotly.graph_objs import *
import random
import psycopg2
import pandas as pd

plotly.tools.set_credentials_file(username='freshcelery', api_key='BPkD7p4zF4fx8YRsWVDM')
plotly.tools.set_config_file(world_readable=False, sharing='private')

conn = psycopg2.connect(dbname='fighters', user='fighters', password='')
cursor = conn.cursor()
get_sql = """SELECT * FROM fighter;"""

scale = 5000
fighters = []

try:
    cursor.execute(get_sql)
except (Exception, psycopg2.DatabaseError) as error:
        print(error)

sql_results = cursor.fetchall()

str(sql_results)

df = pd.DataFrame( [[ij for ij in i] for i in sql_results] )
df.rename(columns={0: 'id', 1: 'name', 2: 'birthplace', 3: 'age', 4: 'height', 5: 'reach', 6: 'record', 7: 'latitude', 8: 'longitude', 9: 'weight_class'}, inplace=True)
data =[ dict(
    type = 'scattergeo',
    locationmode = 'country names',
    lon = df['longitude'],
    lat = df['latitude'],
    text = df['name'],
    marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            )
        ))]
print(data[1])

layout = dict(
    title = 'UFC Fighters by location',
        showlegend = True,
        geo = dict(
            scope='world',
            projection=dict( type='Mercator'),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
)

fig = dict( data=data, layout=layout)
plotly.offline.plot(fig)