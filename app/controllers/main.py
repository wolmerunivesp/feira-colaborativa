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
    return render_template('grupos.html', grupos=Grupo.query.all())


@main.route('/listar_grupos')
@login_required
def listar_grupos():
    lista_de_grupos = Grupo.query.all()

    coordenadas = []
    for grupo in lista_de_grupos:
        coordenadas.append([grupo.name, grupo.latitude, grupo.longitude])

    localizacoes = folium.Map(location=[-23.2038503, -45.8697245], zoom_start=13, tiles="OpenStreetMap")
    for coordenada in coordenadas:
        folium.Marker(
            [coordenada[1], coordenada[2]],
            popup="<i>{fname}</i>".format(fname = coordenada[0])
        ).add_to(localizacoes)
    
    return localizacoes._repr_html_()  

@main.route('/criar_grupo')
@login_required
def grupo():
    return render_template('criar_grupo.html', id=current_user.id, tel=current_user.telefone)


@main.route('/criar_grupo', methods=['POST'])
@login_required
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

    if request.form.get('verdura') == '7':
        verdura = 1
    else:
        verdura = 0

    if request.form.get('legume') == '7':
        legume = 1
    else:
        legume = 0

    if request.form.get('tempero') == '7':
        tempero = 1
    else:
        tempero = 0

    if request.form.get('fruta') == '7':
        fruta = 1
    else:
        fruta = 0


    

    # transforma o CEP em Dic. com o endereco dividido em cidade, bairro e etc.
    endereco = pycep_correios.get_address_from_cep(request.form.get('cep'))

    # Retira a palavra'Rua' do logradouro porque estava provocando erro
    logradouro = endereco['logradouro'].replace("Rua ", " ")

    #transforma o 'endereco' um dicionario com lat. e log.
    localizacao = geolocator.geocode(logradouro, language="Pt-br", country_codes="Br")

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
