import pandas as pd
from owlready2 import get_ontology, Thing, DataProperty, FunctionalProperty, ObjectProperty

# Cargar archivos CSV con límite de 1000 filas
movies_df = pd.read_csv('grupo3/merged_movies.csv')  # Solo las primeras 1000 películas

# 1. Converter la columna 'movieId' a INT
movies_df['movieId'] = movies_df['movieId'].astype(int)

# Cargar la ontología existente
ontology = get_ontology('pelis_ontology_1000.rdf').load()

# Definir clases y propiedades si no existen
with ontology:
    class Movie(Thing):
        pass
    class Actor(Thing):
        pass  # Nueva clase Actor

    class Director(Thing):
        pass  # Nueva clase Director

    class Genre(Thing):
        pass  # Nueva clase para los géneros

    # Propiedades de datos
    class title(DataProperty, FunctionalProperty):
        domain = [Movie]
        range = [str]

    class imdbId(DataProperty, FunctionalProperty):
        domain = [Movie]
        range = [str]

    class tmdbId(DataProperty, FunctionalProperty):
        domain = [Movie]
        range = [str]

    class has_actor(ObjectProperty):
        domain = [Movie]
        range = [Actor]  # Relación entre películas y actores

    class has_director(ObjectProperty):
        domain = [Movie]
        range = [Director]  # Relación entre películas y directores

    # Nueva propiedad de objeto para relacionar películas con géneros
    class has_genre(ObjectProperty):
        domain = [Movie]
        range = [Genre]  # Relación entre película y género

    class is_genre_of(ObjectProperty):
        domain = [Genre]
        range = [Movie]  # Relación inversa entre género y película

    class is_actor_of(ObjectProperty):
        domain = [Actor]
        range = [Movie]

    class is_director_of(ObjectProperty):
        domain = [Director]
        range = [Movie]

# # Definir subclases para cada género y relacionarlas con películas
# genres = [
#     'Crime', 'Mystery', 'Thriller', 'Comedy', 'Documentary', 'Children', 'Drama', 'War', 'Action', 'Horror',
#     'Sci_Fi', 'Adventure', 'Romance', 'Fantasy', '(no genres listed)', 'Musical', 'Animation', 'Western', 'IMAX', 'Film_Noir'
# ]

genre_instances = {}
actor_instances = {}
director_instances = {}
genres = set([genre for sublist in movies_df['genres'].str.split('|').dropna() for genre in sublist])

for genre in genres:
    # Crear instancias de géneros
    genre_instance = Genre(f"Genre_{genre.replace(' ', '_')}")
    genre_instances[genre] = genre_instance

created_movie_ids = set()
# Mapear películas, actores y directores (solo las primeras 1000 filas)
for index, row in movies_df.iterrows():
    # Limpiar y asegurar que los IDs están en el formato correcto
    movies_df['tmdbId'] = pd.to_numeric(movies_df['tmdbId'], errors='coerce').fillna(0).astype(int)
    movies_df['movieId'] = pd.to_numeric(movies_df['movieId'], errors='coerce').fillna(0).astype(int)
    movies_df['imdbId'] = pd.to_numeric(movies_df['imdbId'], errors='coerce').fillna(0).astype(int)

    # Crear el ID de la película asegurando que sea un entero
    movie_id = int(row['movieId'])  # Convertir directamente a int
    movie_id_str = f"Movie_{movie_id}"  # Crear el identificador

    # Comprobar si la película ya existe para evitar duplicados
    if movie_id_str not in created_movie_ids:  # Verificar en el conjunto
        movie = Movie(movie_id_str)
        movie.title = row['title']

        # Asignar ID de IMDB y TMDB si están disponibles
        if 'imdbId' in row and pd.notna(row['imdbId']):
            movie.imdbId = str(int(row['imdbId']))
        if 'tmdbId' in row and pd.notna(row['tmdbId']):
            movie.tmdbId = str(int(row['tmdbId']))

        # Relacionar géneros
        movie_genres = row['genres'].split('|') if 'genres' in row else []
        for genre in movie_genres:
            if genre in genre_instances:
                genre_instance = genre_instances[genre]
                movie.has_genre.append(genre_instance)  # Relacionar película con género
                genre_instance.is_genre_of.append(movie)  # Relación inversa género -> película

        # Relacionar actores
        if 'actors' in row:
            actors = row['actors'].split('|') if '|' in row['actors'] else row['actors'].split(',')
            actors = [actor.strip() for actor in actors]  # Eliminar espacios en blanco
            for actor_name in actors:
                if actor_name not in actor_instances:
                    actor_instance =  Actor(f"Actor_{actor_name.replace(' ', '_')}")
                    actor_instances[actor_name] = actor_instance
                else:
                    actor_instance = actor_instances[actor_name]
                movie.has_actor.append(actor_instance)
                actor_instance.is_actor_of.append(movie)

        # Relacionar director (solo uno)
        if 'director' in row and pd.notna(row['director']):
            # Tomar el director
            director_name = row['director'].strip()  # Asegúrate de limpiar espacios
            if director_name not in director_instances:
                director_instance = Director(f"Director_{director_name.replace(' ', '_')}")
                director_instances[director_name] = director_instance
            else:
                director_instance = director_instances[director_name]

            # Crear la relación entre película y director usando append
            movie.has_director.append(director_instance)  # Relación con el director único
            director_instance.is_director_of.append(movie)  # Relación inversa

        # Agregar el ID de la película creada al conjunto
        created_movie_ids.add(movie_id_str)

# Guardar la ontología actualizada
ontology.save(file='merged_movie_solo.owl', format="rdfxml")
print("Ontología actualizada guardada como 'updated_pelis_1000_lines.owl'")
