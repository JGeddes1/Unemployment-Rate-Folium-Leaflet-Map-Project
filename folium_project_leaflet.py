import folium
import requests
m = folium.Map(location=[37, 0],
               zoom_start=2.5,
               tiles='https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
               attr='My Data Attribution')

geojson = r"F:\API stuff\folium_project\ukdata.json"

g = folium.GeoJson(
    geojson,
    name="geojson",

).add_to(m)


folium.GeoJsonTooltip(fields=["name"]).add_to(g)

m.save("F://API stuff//folium_project//index.html")
