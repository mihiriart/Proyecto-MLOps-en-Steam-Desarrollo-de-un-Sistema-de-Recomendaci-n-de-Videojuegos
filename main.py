"""
FUNCIONES CREADAS PARA EL PROYECTO FINAL INDIVIDUAL 1 DE DATA SCIENCE DE SOY HENRY
                            - STEAM GAMES - 

FUNCIONES PARA ALIMENTAR LA API
"""

#librerías
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, List, Union
import pandas as pd
import scipy as sp
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.metrics.pairwise import cosine_similarity


# Instanciamos la aplicación

app = FastAPI()


# Dentro del script
df_games = pd.read_parquet("Data/steam_games.parquet")
df_user_items = pd.read_parquet("Data/users_items.parquet")
df_games_and_reviews = pd.read_parquet("Data/games_reviews.parquet")
modelo_railway = pd.read_parquet("Data/modelo_railway.parquet")



@app.get("/", response_class=HTMLResponse)
async def inicio():
    template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas sobre juegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam, su fuente confiable para consultas especializadas sobre la plataforma de videojuegos.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=template)



# Antes de la definición de la función
df_user_items['item_id'] = df_user_items['item_id'].astype(str)
df_games['item_id'] = df_games['item_id'].astype(str)


@app.get("/playtimegenre/{genero}", name="PLAYTIMEGENRE")
async def PlayTimeGenre(genero: str) -> str:
    """
    La siguiente función devuelve el año con más horas de juego para un género
    ...

    Ejemplos de entrada:
                        Action, Adventure, RPG, Strategy, Simulation, Casual, etc.
    """
    # Convertimos el género proporcionado a minúsculas para una comparación sin distinción de mayúsculas
    genero = genero.lower()

    # Filtramos los juegos por género de manera más flexible
    df_filtered = df_games[df_games['genres'].str.lower().str.contains(fr'\b{genero}\b', na=False)]

    if not df_filtered.empty:
        df_merged = pd.merge(df_user_items, df_filtered[['item_id', 'release_year']], left_on='item_id', right_on='item_id')

        # Verificamos si la longitud de df_filtered es mayor a cero, es decir, se encontraron géneros
        result = "Año con más horas jugadas para el género {}: {}".format(genero.capitalize(), df_merged.groupby('release_year')['playtime_hours'].sum().idxmax())
    else:
        result = "Año con más horas jugadas para género {}: {}".format(genero.capitalize(), "Género no encontrado en la base de datos")

    return result
    
    




# Segunda función
@app.get("/userforgenre/{genero}", name="USERFORGENRE")
async def UserForGenre(genero: str) -> Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]:
    # ...

    """
    La siguiente función devuelve información sobre el usuario con más horas jugadas para un género específico
    ...

    Ejemplo de entrada:
                        Action, Adventure, RPG, Strategy, Simulation, Casual, etc.
    """

    # Convertimos el género proporcionado a minúsculas para una comparación sin distinción de mayúsculas
    genero = genero.lower()

    # Filtramos los juegos por género de manera más flexible
    df_filtered = df_games[df_games['genres'].str.lower().str.contains(fr'\b{genero}\b', na=False)]

    if not df_filtered.empty:
        df_user_items['item_id'] = df_user_items['item_id'].astype(str)

        # Convertimos la columna 'item_id' en df_filtered a tipo 'str'
        df_filtered['item_id'] = df_filtered['item_id'].astype(str)

        df_merged = pd.merge(df_user_items, df_filtered[['item_id', 'release_year']], on='item_id')

        # Filtramos los datos desde el año 2003 en adelante
        df_merged = df_merged[df_merged['release_year'] >= 2003]
        user_with_most_playtime = df_merged.groupby('user_id')['playtime_hours'].sum().idxmax()
        playtime_by_year = df_merged.groupby(['release_year', 'user_id'])['playtime_hours'].sum().reset_index()
        playtime_by_year = playtime_by_year[playtime_by_year['user_id'] == user_with_most_playtime]
        playtime_by_year = playtime_by_year.rename(columns={'release_year': 'Año', 'playtime_hours': 'Horas'})

        # Convertimos las horas a enteros
        playtime_by_year['Horas'] = playtime_by_year['Horas'].astype(int)

        result = {
            "Usuario con más horas jugadas para Género {}:".format(genero.capitalize()): user_with_most_playtime,
            "Horas jugadas": [{"Año": str(row['Año']), "Horas": row['Horas']} for _, row in playtime_by_year.iterrows()]
        }
    else:
        result = {"Usuario con más horas jugadas para Género {}:".format(genero.capitalize()): "Género no encontrado en la base de datos", "Horas jugadas": []}

    return result





# Tercera función
@app.get('/UsersRecommend')
def UsersRecommend(año: int):

    """
    La siguiente función devuelve un top 3 de juegos recomendados por usuarios para un año específico
    ...

    Ejemplo de entrada:
                        Año (int): Año del que se necesite la consulta
    """




    # Verificamos si el año está dentro del rango esperado
    rango_aceptado = range(2010, 2016)
    if año not in rango_aceptado:
        return {"message": "Mi base de datos solo tiene registros entre 2010 y 2015"}

    # Aquí cargamos el DataFrame
    df_games_and_reviews = pd.read_parquet("Data/games_reviews.parquet")

    # Filtramos por el año deseado en las fechas de lanzamiento y publicación
    df_filtered = df_games_and_reviews[
        (df_games_and_reviews['release_year'] == año)
    ]

    # Filtramos por comentarios recomendados y sentiment_analysis positivo/neutral
    df_filtered = df_filtered[
        (df_filtered['recommend'] == True) & (df_filtered['sentiment_analysis'].isin([0, 1, 2]))
    ]

    # Obtenemos el top 3 de juegos recomendados
    top_games = df_filtered['app_name'].value_counts().head(3)

    # Modificamos la estructura del resultado
    result = {juego: count for juego, count in top_games.items()}

    return result



# Cuarta función
@app.get('/UsersWorstDeveloper')
def UsersWorstDeveloper(anio:int):
    '''
    Muestra el top 3 de desarrolladoras MENOS recomendados por usuarios
    para el año dado

    Argumentos:
        Año (int): Año del que se necesite la consulta

    ''' 
    mascara = (df_games_and_reviews['release_year'] == anio)   
    df_worst_reviews_3 = df_games_and_reviews[mascara]
    developer_counts = df_worst_reviews_3['developer'].value_counts().head(3)
 
    resultados = []
    for puesto, (developer, count) in enumerate(developer_counts.items(), start=1):                            
        resultados.append({f"Puesto {puesto}": developer})

    return resultados






#Quinta función
@app.get("/sentimentanalysis/{empresa_desarrolladora}", name="SENTIMENTANALYSIS")
async def sentiment_analysis(empresa_desarrolladora: str) -> Union[str, Dict[str, Dict[str, int]]]:
    # ...

    """
    La siguiente función devuelve el análisis de sentimientos para una empresa desarrolladora específica
    ...

    Ejemplo de Entrada:
                        Valve, Ubisoft, Treyarch, etc.
    """

    # Filtramos por desarrolladora
    df_filtered_developer = df_games_and_reviews[df_games_and_reviews['developer'] == empresa_desarrolladora]

    # Verificamos que haya datos para la desarrolladora
    if not df_filtered_developer.empty:
        # Contamos los sentimientos y mapeamos el número del sentimiento a su etiqueta correspondiente
        sentiment_counts = df_filtered_developer['sentiment_analysis'].value_counts().reset_index(drop=True)
        sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
        sentiment_counts.index = sentiment_counts.index.map(sentiment_mapping)

        result = {empresa_desarrolladora: sentiment_counts.to_dict()}
    else:
        result = {"message": 'No cuento con los registros de esa empresa en mi base de datos'}

    return result





#Modelo de recomendacion item_item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id: int):
    
    """La siguiente funcion genera una lista de 5 juegos similares a un juego dado (id)
    
    Parametros:
    
        El id del juego para el que se desean encontrar juegos similares. Ej: 10

    Retorna:
    
         Un diccionario con 5 juegos similares 
    """
    game = modelo_railway[modelo_railway['item_id'] == id]

    if game.empty:
        return("El juego '{id}' no posee registros.")
    
    # Obtiene el índice del juego dado
    idx = game.index[0]

    # Toma una muestra aleatoria del DataFrame df_games
    sample_size = 2000  # Define el tamaño de la muestra (ajusta según sea necesario)
    df_sample = modelo_railway.sample(n=sample_size, random_state=42)  # Ajusta la semilla aleatoria según sea necesario

    # Calcula la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([modelo_railway.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # Obtiene las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # Ordena los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtiene los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Lista de juegos similares (solo nombres)
    similar_game_names = df_sample['app_name'].iloc[similar_game_indices].tolist()

    return {"similar_games": similar_game_names}