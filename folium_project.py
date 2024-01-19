import folium
import requests
m = folium.Map(location=[37, 0], zoom_start=2.5, tiles='Stamen Terrain')
response = requests.get('https://restcountries.com/v3.1/all').json()


for country_data in response:
    print(country_data['name']['common'])

    if country_data['latlng']:

        lat = country_data['latlng'][0]
        long = country_data['latlng'][1]

        folium.Marker(
            [lat, long], popup="<i>{}</i><br><i>{}</i>".format(country_data['name']['common'], country_data['population']), icon=folium.Icon(color="green", icon="info-sign")).add_to(m)

    else:
        continue


m.save("F://API stuff//folium_project//index.html")
