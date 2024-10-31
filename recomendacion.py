from owlready2 import *
from collections import Counter

# Cargar la ontología
ontology_path = 'peliculas.rdf'  # Cambia esto a la ruta de tu archivo OWL
onto = get_ontology(ontology_path).load()

def recommend_based_on_genre(genero):
    # Intentar encontrar películas con variaciones de "Horror"
    horror_movies = []
    for movie in onto.Movie.instances():
        if hasattr(movie, 'has_genre'):# Verificar que la película tenga el atributo has_genre
            #print(movie.has_genre, type(movie.has_genre),'aa')
            if genero in str(movie.has_genre):
                if hasattr(movie, 'rating') and movie.rating:
                    # Agregar la película y su rating a la lista; rating[0] para obtener el valor
                    horror_movies.append((movie.title, movie.rating[0]))

    horror_movies.sort(key=lambda x: x[1], reverse=True)
# Imprimir resultados
    if horror_movies:
        top_10_movies = horror_movies[:10]
        print(f"\nPelículas de género {genero} encontradas:")
        for movie in top_10_movies:
            print(movie)
    else:
        print(f"No se encontraron películas de género {genero}.")

#recommendation = recommend_based_on_genre('Genre_Horror')
#recommendation

def recommend_based_on_user(user_id, cuantas):
    movies = []
    for movie in onto.Movie.instances():
        if user_id in str(movie.is_watched_by):
            if str(movie) not in movies:
                movies.append(str(movie))

    users = []
    for user in onto.User.instances():
        for movie in movies:
            #print(movie)
            if movie in str(user.has_watched):
                if str(user) not in users:
                    users.append(str(user))

    movies_new = []
    for movie_new in onto.Movie.instances():
        for user in users:
            if user in str(movie_new.is_watched_by):
                if str(movie_new) not in movies:
                    movies_new.append(str(movie_new))

    # Contar las ocurrencias de cada elemento
    conteo = Counter(movies_new)

    # Ordenar los elementos por cantidad de mayor a menor
    ordenado = sorted(conteo, key=conteo.get, reverse=True)

    if cuantas<len(movies_new):
        return ordenado[:cuantas]
    else:
        return 'Error, no se pueden recomendar tantas peliculas.'

r = recommend_based_on_user('User_102040', 100000)
print(r)