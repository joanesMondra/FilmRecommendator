from owlready2 import *
import pandas as pd

# Cargar la ontología
onto = get_ontology("pelis.rdf").load()

with onto:
    class Movie(Thing):
        pass
    class User(Thing):
        pass
    class Rating(Thing):
        pass
    class Tag(Thing):
        pass
    class Link(Thing):
        pass

    #propiedades para Movie
    class hasTitle(Movie >> str, FunctionalProperty):
        pass
    class hasGenre(Movie >> str, FunctionalProperty):
        pass
    class hasYear(Movie >> int, FunctionalProperty):
        pass
    class hasDirector(Movie >> str, FunctionalProperty):
        pass
    class hasActor(Movie >> str, FunctionalProperty):
        pass

    #propiedades para Rating
    class givenBy(Rating >> User, FunctionalProperty):
        pass
    class ratesMovie(Rating >> Movie, FunctionalProperty):
        pass
    class hasRatingValue(Rating >> float, FunctionalProperty):
        pass
    class hasTimestamp(Rating >> str, FunctionalProperty):
        pass #ez dakit int o str hoi beidau

    #propiedades para Tag
    class taggedBy(Tag >> User, FunctionalProperty):
        pass
    class tagsMovie(Tag >> Movie, FunctionalProperty):
        pass
    class hasTagValue(Tag >> str, FunctionalProperty):
        pass
    class tagTimestamp(Tag >> str, FunctionalProperty):
        pass

    #propiedades para Links
    class linksMovie(Link >> Movie, FunctionalProperty):
        pass
    class hasImdbId(Link >> str, FunctionalProperty):
        pass
    class hasTmdbId(Link >> str, FunctionalProperty):
        pass

# Función auxiliar para crear individuos y asignarles propiedades
def create_individual(cls, name, **kwargs):
    if cls in onto.classes():  # Verifica si la clase existe en la ontología
        return cls(name, **kwargs)
    else:
        print(f"Clase {cls} no encontrada en la ontología.")
        return None


# Función para procesar un archivo CSV y poblar la ontología
def procesar_csv(file_path, entity_type, columns):
    # Cargar el archivo CSV
    df = pd.read_csv(file_path)

    # Iterar sobre cada fila en el DataFrame
    for _, row in df.iterrows():
        # Identificar el tipo de entidad que estamos procesando
        if entity_type == "movies":
            movie_id = f"Movie_{row['movieId']}"
            movie = create_individual(Movie, movie_id)
            movie.hasTitle = row['title']
            movie.hasGenre = row['genres']
            movie.hasYear = (row['year'])
            movie.hasDirector = row['director']
            movie.hasActor = row['actors']

        elif entity_type == "ratings":
            rating_id = f"Rating_{row['userId']}_{row['movieId']}"
            rating = create_individual(Rating, rating_id)
            user_id = f"User_{row['userId']}"
            movie_id = f"Movie_{row['movieId']}"

            # Crear o recuperar usuario y película
            user = create_individual(User, user_id)
            movie = create_individual(Movie, movie_id)

            rating.givenBy = user
            rating.ratesMovie = movie
            rating.hasRatingValue = float(row['rating'])
            rating.hasTimestamp = str(row['timestamp'])

        elif entity_type == "tags":
            tag_id = f"Tag_{row['userId']}_{row['movieId']}"
            tag = create_individual(Tag, tag_id)
            user_id = f"User_{row['userId']}"
            movie_id = f"Movie_{row['movieId']}"

            # Crear o recuperar usuario y película
            user = create_individual(User, user_id)
            movie = create_individual(Movie, movie_id)

            tag.taggedBy = user
            tag.tagsMovie = movie
            tag.hasTagValue = row['tag']
            tag.tagTimestamp = str(row['timestamp'])

        elif entity_type == "links":
            link_id = f"Link_{row['movieId']}"
            link = create_individual(Link, link_id)
            movie_id = f"Movie_{row['movieId']}"

            # Crear o recuperar la película
            movie = create_individual(Movie, movie_id)

            link.linksMovie = movie
            link.hasImdbId = str(row['imdbId'])
            link.hasTmdbId = str(row['tmdbId'])

    print(f"{entity_type.capitalize()} procesados correctamente.")


# Procesar los diferentes CSVs
procesar_csv("links.csv", "links", ["movieId", "imdbId", "tmdbId"])
procesar_csv("movies.csv", "movies", ["movieId", "title", "genres", "year", "director", "actors"])
procesar_csv("ratings.csv", "ratings", ["userId", "movieId", "rating", "timestamp"])
procesar_csv("tags.csv", "tags", ["userId", "movieId", "tag", "timestamp"])

# Razonar sobre la ontología (opcional)
sync_reasoner_pellet(infer_property_values=True)

# Guardar la ontología modificada
onto.save(file="ontologia_poblada.owl", format="rdfxml")
