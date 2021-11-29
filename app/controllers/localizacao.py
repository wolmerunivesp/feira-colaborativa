import folium

    
# define a localização com base nas coordenadas
mapa = folium.Map(
    location=[localizacao.latitude, localizacao.longitude],
    zoom_start=16
)

# Inclui: Balão de localização e janela popup
folium.Marker(
    [localizacao.latitude, localizacao.longitude],
    popup="<div class='jumbotron' style='width: 400px;'><h3>Grupo de CTA</h3><p>Grupop de destinado a compras semanais as sexta feiras de Frutas, Legumes e Verduras</p><p class='text-muted'><a href='#' class='btn btn-primary' role='button'>Enviar</a></p></div>",
    icon=folium.Icon(color="green", icon="map-marker"),
).add_to(mapa)
    




