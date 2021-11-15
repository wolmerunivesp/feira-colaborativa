# Rotas sem identificação
# -----------------------
from operator import le
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db
from geopy.geocoders import Nominatim
from functools import partial
import pycep_correios
from app.models.models import Grupo
from app.models.models import User
from app.controllers.limpa_cep import limpa_cep
import folium

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/grupos')
@login_required
def grupos():
    return render_template('grupos.html')


@main.route('/listar_grupos')
@login_required
def listar_grupos():
    lista_de_grupos = Grupo.query.all()

    coordenadas = []
    for grupo in lista_de_grupos:
        coordenadas.append([grupo.name, grupo.latitude, grupo.longitude])
        # print(coordenadas[0][0])
    # print(coordenadas)

    localizacoes = folium.Map(location=[-23.2038503, -45.8697245], zoom_start=13, tiles="OpenStreetMap")
    for coordenada in coordenadas:
        folium.Marker(
            [coordenada[1], coordenada[2]],
            popup="<i>{fname}</i>".format(fname = coordenada[0])
        ).add_to(localizacoes)
    
    return localizacoes._repr_html_()
    
    


    # return render_template("grupos.html", lista_de_grupos=lista_de_grupos)


    # ----- funciona ------
    # lista_de_grupos = Grupo.query.all()
    # return render_template("grupos.html", lista_de_grupos=lista_de_grupos)


#  folium.Marker(
#             [coordenada[], -121.6625],
#             popup="<i>Mt. Hood Meadows</i>",
#             tooltip=tooltip
#         ).add_to(localizacoes)

    # localizacoes = folium.Map(location=[-23.2038503, -45.8697245], zoom_start=13, tiles="OpenStreetMap")
    # for grupo in lista_de_grupos:

    #     localizacoes.Marker(
    #         location=[grupo.latitude, grupo.longitude],
    #         popup=grupo.name,
    #         icon=folium.Icon(icon="cloud"),
    #     ).add_to(folium_map)



    # return localizacoes._repr_html_()






    

@main.route('/criar_grupo')
@login_required
def grupo():
    return render_template('criar_grupo.html', id=current_user.id, tel=current_user.telefone)


@main.route('/criar_grupo', methods=['POST'])
def criar_grupo():

    db.create_all()
    geolocator = Nominatim(user_agent="sanchesnsb@gmail.com")
    geocode = partial(geolocator.geocode, language="pt-br")


    admin = request.form.get('id_admin')
    name = request.form.get('nome_grupo')
    cep = limpa_cep(request.form.get('cep'))
    if request.form.get('frequencia') == '7':
        semanalmente = 1
        quinzenalmente = 0
    else:
        semanalmente = 0
        quinzenalmente = 1
    verdura = request.form.get('verdura')
    legume = request.form.get('legume')
    fruta = request.form.get('fruta')
    tempero = request.form.get('tempero')

    # transforma o CEP em Dic. com o endereco dividido em cidade, bairro e etc.
    endereco = pycep_correios.get_address_from_cep(request.form.get('cep'))

    #transforma o 'endereco' um dicionario com lat. e log.
    localizacao = geolocator.geocode(f"{endereco['logradouro']} {endereco['cidade']} {endereco['uf']} Brasil ")

    latitude = localizacao.latitude
    longitude = localizacao.longitude
    whatsapp = 'https://api.whatsapp.com/send?phone=55{}'.format(limpa_cep(request.form.get('tel')))
    


      # Retorna ao usuario se o email já existe
    grupo = Grupo.query.filter_by(name=name).first()

    if grupo:
        flash('Grupo já criado')
        return redirect(url_for('main.criar_grupo'))
    
    #Criando novo usuário
    novo_grupo = Grupo(admin=admin, name=name, cep=cep, semanalmente=semanalmente, quinzenalmente=quinzenalmente, verdura=verdura, legume=legume, fruta=fruta, tempero=tempero, latitude=latitude, longitude=longitude, whatsapp=whatsapp)

    # Adicionando o usuário ao banco de dados
    db.session.add(novo_grupo)
    db.session.commit()
    flash('Grupo criado com sucesso')
    return redirect(url_for('main.criar_grupo'))

# @main.route('/mapa')
# @login_required
# def mapa():
#     start_coords = (46.9540700, 142.7360300)
#     mapa = folium.Map(location=start_coords, zoom_start=14)
#     return mapa._repr_html_()
