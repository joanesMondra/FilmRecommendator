import pandas as pd
import ast
from owlready2 import get_ontology, Thing, DataProperty, FunctionalProperty, ObjectProperty

# Cargar archivos CSV con límite de 1000 filas
movies_df = pd.read_csv('grupo3/merged_movies.csv')  # Solo las primeras 1000 películas
tags_df = pd.read_csv('grupo3/tags.csv')

# 1. Converter la columna 'movieId' a INT
movies_df['movieId'] = movies_df['movieId'].astype(int)

# Cargar la ontología existente
ontology = get_ontology('pelicula_ontology.rdf').load()

# Definir clases y propiedades si no existen
# Definir clases y propiedades si no existen en la ontología
with ontology:
    # Clase base para personas
    class Person(Thing):
        pass

    # Subclases de Person
    class Actor(Person):
        pass
    class Director(Person):
        pass
    class User(Person):
        pass

    # Clase base para películas
    class Movie(Thing):
        pass
    # Subclase de Movie para géneros específicos
    class GenreMovie(Movie):
        pass

    # Clase para géneros
    class Genre(Thing):
        pass

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

    class rating(DataProperty, FunctionalProperty):
        domain = [Movie]
        range = [str]

    class tags(DataProperty, FunctionalProperty):
        domain = [Movie]
        range = [str]

    # Propiedades de objeto
    class has_actor(ObjectProperty):
        domain = [Movie]
        range = [Actor]

    class has_director(ObjectProperty):
        domain = [Movie]
        range = [Director]

    class has_genre(ObjectProperty):
        domain = [Movie]
        range = [Genre]

    class is_genre_of(ObjectProperty):
        domain = [Genre]
        range = [Movie]

    class is_actor_of(ObjectProperty):
        domain = [Actor]
        range = [Movie]

    class is_director_of(ObjectProperty):
        domain = [Director]
        range = [Movie]

    class has_watched(ObjectProperty):
        domain = [Movie]
        range = [User]

    class is_watched_by(ObjectProperty):
        domain = [User]
        range = [Movie]
        inverse_property = has_watched



genre_instances = {}
actor_instances = {}
director_instances = {}
user_instances = {}
tag_instances = {}

genres = set([genre for sublist in movies_df['genres'].str.split('|').dropna() for genre in sublist])
tags = set([tag for sublist in movies_df['tag'].str.split('|').dropna() for tag in sublist])

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
        movie.rating = str(float(row['valoracion_media']))
        movie.tags = str(row['tag'])
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
print(tags_df['userId'].nunique())
#print(movies_df['userId'].nunique())
count=0
for index, row in tags_df.iterrows():
    user_id = row['userId']
    user_id_str = f"User_{int(row['userId'])}"
    movie_id_str = f"Movie_{int(row['movieId'])}"

    if int(row['movieId']) in movies_df['movieId'].astype('int'):

        #print("True: ", row['movieId'])
        movie = Movie(movie_id_str)
        if 'userId' in row:
            if user_id_str not in user_instances:
                user_instance = User(user_id_str)
                user_instances[user_id_str] = user_instance
            else:
                user_instance = user_instances[user_id_str]

            user_instance.has_watched.append(movie)
            movie.is_watched_by.append(user_instance)
            count+=1
    #else:
        #print("False: ", row['movieId'])


print(count)
print(len(user_instances))

# Guardar la ontología actualizada
ontology.save(file='pelicula_ontology.rdf', format="rdfxml")
print("Ontología actualizada guardada como 'peliculas.rdf'")
