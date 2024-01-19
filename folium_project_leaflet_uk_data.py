import folium
import requests
import pandas as pd
import geopandas as gpd
import numpy as np
from flask import Flask, render_template

app = Flask(__name__)

# data = pd.DataFrame(r"F:\API stuff\folium_project\ukdata.json")

geojson = gpd.read_file(r"F:\API stuff\folium_project\ukdata.json")

m = folium.Map(location=[geojson.lat.mean(), geojson.long.mean()],
               zoom_start=5.5,
               tiles='https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
               attr='My Data Attribution')
# print(geojson.dtypes)
geojson = geojson[['OBJECTID', 'geometry']]
geojson['OBJECTID'] = geojson['OBJECTID'].map(str)

# remove isna
geojson['OBJECTID'] = geojson['OBJECTID'].str.replace(
    ',', '')
geojson['OBJECTID'] = geojson['OBJECTID'].replace(
    {'supressed': np.nan}).astype(str)

# print(geojson.head())
# print(geojson.dtypes)
region_employmentdata = f"F://API stuff//folium_project//employmentuk_1.csv"

region_data = pd.read_csv(region_employmentdata)
region_data["ID"] = region_data["ID"].map(str)
region_data["Unemployment"] = region_data["Unemployment"].map(str)
# region_data.info()
# region_data["ID"] = region_data["ID"].str.zfill(5)


# create new columns with correct data types and drop original columns
region_data['Unemployment_rate'] = region_data['Unemployment'].str.replace(
    ',', '')
region_data['Unemployment_rate'] = region_data['Unemployment_rate'].replace(
    {'supressed': np.nan}).astype(float)
region_data.drop(['Unemployment'], axis=1, inplace=True)

# Some magic reason feel like finish early use few minutes to work on last bit


# print(region_data)
# region_data.head()

region_data.info()
# Join the geojson with the regiondata
region_data_final = geojson.merge(
    region_data, left_on="OBJECTID", right_on="ID", how="outer")
region_data_final

print(region_data_final.head())

custom_scale = (region_data_final['Unemployment_rate'].quantile(
    (0, 0.2, 0.4, 0.6, 0.8, 1))).tolist()
folium.Choropleth(
    geo_data='F://API stuff//folium_project//ukdata.json',
    name="choropleth",
    data=region_data_final,
    threshold_scale=custom_scale,
    columns=["ID", "Unemployment_rate"],
    key_on="feature.properties.OBJECTID",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Unemployment Rate (%)",
    highlight=True,
    line_color='white'
).add_to(m)


# Add Customized Tooltips to the map
folium.features.GeoJson(
    data=region_data_final,
    name='New Cases Past 7 days (Per 100K Population)',
    smooth_factor=2,
    style_function=lambda x: {'color': 'black',
                              'fillColor': 'transparent', 'weight': 0.1},
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Region',
                'Unemployment_rate'
                ],
        aliases=["Region:",
                 "Unemployment Rate %:"

                 ],
        localize=True,
        sticky=False,
        labels=True,
        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
        max_width=800,),
    highlight_function=lambda x: {'weight': 3, 'fillColor': 'grey'},
).add_to(m)


m.save("F://API stuff//folium_project//map.html")


@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)
