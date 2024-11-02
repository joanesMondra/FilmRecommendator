import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Cargar el dataset
df = pd.read_csv('merged_movies.csv')

# Crear la columna 'combined_features' que contiene todos los datos relevantes para la similitud
df['combined_features'] = df['genres'] + ' ' + df['director'] + ' ' + df['actors'] + ' ' + df['tag']

# Vectorizar las características combinadas
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Calcular la matriz de similitud coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_movies_based_on_content(movie_title, num_films=10):
    try:
        # Obtener el índice de la película en el DataFrame
        idx = df[df['title'] == movie_title].index[0]
        # Calcular las puntuaciones de similitud
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_films+1]  # Obtener las películas más similares
        movie_indices = [i[0] for i in sim_scores]

        # Mostrar resultados detallados
        print(f"Películas similares a '{movie_title}':")
        for i, index in enumerate(movie_indices):
            movie = df.iloc[index]
            print(f"{i+1}: {movie['title']}")
            print(f"    Director: {movie['director']}")
            print(f"    Año: {movie['year']}")
            print(f"    Actores: {movie['actors']}")
            print(f"    Género: {movie['genres']}")
            print(f"    IMDb: {movie['link_imdb']}")
            print(f"    TMDb: {movie['link_tmdbId']}")
            print(f"    Valoración media: {movie['valoracion_media']}")
            print("")

    except IndexError:
        print(f"La película '{movie_title}' no se encontró en el dataset.")

if __name__ == "__main__":
    # Interacción con el usuario
    movie_title = input("Ingrese el título de la película: ")
    try:
        num_films = int(input("Ingrese el número de películas recomendadas (predeterminado 10): "))
    except ValueError:
        num_films = 10  # Valor predeterminado si la entrada no es válida

    # Generar y mostrar las recomendaciones
    recommend_movies_based_on_content(movie_title, num_films)
