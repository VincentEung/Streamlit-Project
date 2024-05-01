import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")

############################### Functions##############################

#@st.cache(allow_output_mutation=True)
def load_data(path):
    df = pd.read_csv(path, warn_bad_lines=True, error_bad_lines=False,low_memory=False)
    return df.sample(frac = .10)

def cleanning(df):
    df.drop(labels = ['adresse_suffixe','adresse_numero','ancien_code_commune','ancien_nom_commune',
                        'ancien_id_parcelle','numero_volume', 'lot1_numero',
                        'lot1_surface_carrez','lot2_surface_carrez','lot2_numero','lot3_numero',
                        'lot3_surface_carrez','lot4_numero','lot4_surface_carrez',
                       'lot5_numero','lot5_surface_carrez'],axis=1,inplace=True)
    df.dropna(subset=['valeur_fonciere','surface_terrain','longitude','latitude','code_commune',
     'nom_commune','code_type_local','type_local','surface_reelle_bati','nombre_pieces_principales',
     'nature_culture_speciale','code_nature_culture_speciale'],axis=0, inplace=True)
    df['Prix/m2'] = df['valeur_fonciere']/df['surface_terrain']
    return df

def bar_prix_metre_carre(df):
    df=df.groupby(['code_commune'])['Prix/m2'].mean()
    st.bar_chart(df)

def prix_date_mutation(df):
    df = px.bar(df, x='date_mutation', y='Prix/m2')
    st.plotly_chart(df)

def hist_surface_local(df):
    df = px.histogram(df, y='surface_reelle_bati', x='type_local')
    st.plotly_chart(df)

def prix_surface(df):
    c = alt.Chart(df).mark_bar().encode(
    x=alt.X('Prix/m2',bin=alt.Bin(maxbins=5)),
    y='surface_reelle_bati')
    st.altair_chart(c,use_container_width=True)

def prix_departement(df):
    df = px.pie(df, values='Prix/m2', names='code_departement')
    df.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(df)

def prix_nature_culture(df):
    plot = plt.figure(figsize=(25,15))
    sns.barplot(data=df, x="nature_culture", y="Prix/m2")
    st.pyplot(plot)

def prix_local(df):
    c = alt.Chart(df).mark_circle().encode(x=('type_local'),y='Prix/m2').interactive()
    st.altair_chart(c,use_container_width=True)

def prix_code_nature_culture(df):
    fig =px.scatter(df, x="code_nature_culture", y="Prix/m2", color='nature_mutation')
    fig.update_layout(width = 800)
    st.plotly_chart(fig)

def map(df):
    df = df[['code_departement', 'nature_culture', 'longitude','latitude']]
    df = df[df['code_departement'].str.contains('94')]
    df = df[df['nature_culture']==('jardins')]
    coordonnees=df[['longitude', 'latitude']]
    st.dataframe(df)
    return coordonnees

############################## Main Part##############################

def main():

    st.title('Bienvenue sur la page accueil ! ')
    st.header('Data Vizualtion - 2022')
    st.write('👈Au sein de la sidebar, vous serez apte à afficher toute la visualisation que vous désirez selon une année de votre choix.👈')
    
    with st.sidebar:
        st.header('Programmé par :')
        st.write('Vincent Eung🧑')
        st.write('BIA 1💻')
        st.write('Student Code ✅ : 20190605')

        image = Image.open('pdp.jpg')
        st.image(image)

        ############ 3 checkbocks ############    

        st.header('Cocher une ou plusieurs cases pour afficher lannée souhaitée :')
        choice = st.checkbox("2020")
        choice2 = st.checkbox("2019")
        choice3 = st.checkbox("2018")

    select = st.radio("Si vous désirez afficher le tableau, sélectionner un des boutons suivants :",('Reset','2020','2019','2018'))

    if select == '2020':    
        df_2020 = load_data("full_2020.csv")
        cleanning(df_2020)
        st.write(df_2020)
    elif select == '2019':    
        df_2019 = load_data("full_2019.csv")
        cleanning(df_2019)
        st.write(df_2019)
    elif select == '2018':    
        df_2020 = load_data("full_2018.csv")
        cleanning(df_2018)
        st.write(df_2018)
   
    if choice:
        df_2020 = load_data("full_2020.csv")
        cleanning(df_2020)
    
    ########## 2 internals streamlit plots have been used ############

        #st.bar 

        st.header('Ci-dessous tous les prix par metre carré à toutes les communes  : ')
        bar_prix_metre_carre(df_2020)

        # st.map

        st.header('Voici ma map qui affiche tous les points dans le 72e arrondissement avec des jardins:')
        coord = map(df_2020)
        st.map(coord)

    ########## 4 externals streamlit plots have been used ############    

        st.header('Affchage de tous les prix par metre carre en fonction de la date de mutation')
        prix_date_mutation(df_2020)

        st.header('Affchage de tous les types de local en fonction de la surface reelle')
        hist_surface_local(df_2020)

        st.header('Tous les prix de la surface_reelle par rapport à l année 2020')
        prix_surface(df_2020)

        st.header('Affchage de tous les prix par metre carre en fonction des departements')
        prix_departement(df_2020)

        ###############Extra plot###################

        st.header('Affichage de tous les prix au metre carré en fonction de la nature de la culture')
        prix_nature_culture(df_2020)

        st.header('Affichage du prix par metre carre moyen pour chaque type de local')
        st.write('Pour voir les points en plus grand vous avez la possibilité de zommer sur le graphe')
        prix_local(df_2020)

        st.header('Affichage des différents type de code de la nature culture par metre carre')
        prix_code_nature_culture(df_2020)



    if choice2:
        df_2019 = load_data("full_2019.csv")
        df_2019 = cleanning(df_2019)
        
        ########## 2 internals streamlit plots have been used ############

        st.header('Ci-dessous tous les prix par metre carré à toutes les communes  : ')
        bar_prix_metre_carre(df_2019)

        # st.map
        
        st.header('Voici ma map qui affiche tous les points dans le 72e arrondissement avec des jardins:')
        coord = map(df_2019)
        st.map(coord)

    ########## 4 externals streamlit plots have been used ############    

        st.header('Affchage de tous les prix par metre carre en fonction de la date de mutation')
        prix_date_mutation(df_2019)

        st.header('Affchage de tous les types de local en fonction de la surface reelle')
        hist_surface_local(df_2019)

        st.header('Tous les prix de la surface_reelle par rapport à l année 2019')
        prix_surface(df_2019)

        st.header('Affchage de tous les prix par metre carre en fonction des departements')
        prix_departement(df_2019)

        ###############Extra plot###################

        st.header('Affichage de tous les prix au metre carré en fonction de la nature de la culture')
        prix_nature_culture(df_2019)

        st.header('Affichage du prix par metre carre moyen pour chaque type de local')
        st.write('Pour voir les points en plus grand vous avez la possibilité de zommer sur le graphe')
        prix_local(df_2019)

        st.header('Affichage des différents type de code de la nature culture par metre carre')
        prix_code_nature_culture(df_2019)

    if choice3:

        df_2018 = load_data("full_2018.csv")
        df_2018 = cleanning(df_2018)
        
        ########## 2 internals streamlit plots have been used ############

        st.header('Ci-dessous tous les prix par metre carré à toutes les communes  : ')
        bar_prix_metre_carre(df_2018)

        # st.map

        st.header('Voici ma map qui affiche tous les points dans le 72e arrondissement avec des jardins:')
        coord = map(df_2018)
        st.map(coord)

    ########## 4 externals streamlit plots have been used ############    

        st.header('Affchage de tous les prix par metre carre en fonction de la date de mutation')
        prix_date_mutation(df_2018)

        st.header('Affchage de tous les types de local en fonction de la surface reelle')
        hist_surface_local(df_2018)

        st.header('Tous les prix de la surface_reelle par rapport à l année 2018')
        prix_surface(df_2018)

        st.header('Affchage de tous les prix par metre carre en fonction des departements')
        prix_departement(df_2018)

        ###############Extra plot###################

        st.header('Affichage de tous les prix au metre carré en fonction de la nature de la culture')
        prix_nature_culture(df_2018)

        st.header('Affichage du prix par metre carre moyen pour chaque type de local')
        st.write('Pour voir les points en plus grand vous avez la possibilité de zommer sur le graphe')
        prix_local(df_2018)

        st.header('Affichage des différents type de code de la nature culture par metre carre')
        prix_code_nature_culture(df_2018)


main()