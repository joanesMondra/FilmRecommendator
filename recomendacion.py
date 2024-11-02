from owlready2 import *
from collections import Counter

# Cargar la ontología
ontology_path = 'ontologia_oficial.rdf'  # Cambia esto a la ruta de tu archivo OWL
onto = get_ontology(ontology_path).load()

def recommend_based_on_genre(genero):
    # Intentar encontrar películas con variaciones del género
    horror_movies = []
    for movie in onto.Movie.instances():
        if hasattr(movie, 'has_genre'):  # Verificar que la película tenga el atributo has_genre
            if genero in str(movie.has_genre):
                if hasattr(movie, 'rating') and movie.rating:
                    # Agregar la película y su rating a la lista; rating[0] para obtener el valor
                    horror_movies.append((movie.title, movie.rating[0]))

    # Ordenar películas por su rating en orden descendente
    horror_movies.sort(key=lambda x: x[1], reverse=True)

    # Devolver los títulos de las mejores 10 películas
    if horror_movies:
        top_10_movies = horror_movies[:10]
        return [movie[0] for movie in top_10_movies]
    else:
        return ["No se encontraron películas de género " + genero + "."]


#recommendation = recommend_based_on_genre('Genre_Horror')
#recommendation

def recommend_based_on_actors(*args):
    # Intentar encontrar películas con variaciones de "Horror"
    actor_movies = []
    for movie in onto.Movie.instances():
        flag = 1
        for elem in args:
            if elem not in str(movie.has_actor):
                flag = 0
        if flag == 1:
            actor_movies.append(movie.title)
    if len(actor_movies) == 0:
        return "Error: no hay peliculas con ese/esos actor(es), prueba con otro(s) actor(es)"
    return actor_movies

a = recommend_based_on_actors('Actor_Dany_Boon')
print(a)

def recommend_based_on_director(*args):
    # Intentar encontrar películas con variaciones de "Horror"
    director_movies = []
    for movie in onto.Movie.instances():
        flag = 1
        for elem in args:
            if elem not in str(movie.has_director):
                flag = 0
        if flag == 1:
            director_movies.append(movie.title)
    if len(director_movies) == 0:
        return "Error: no hay peliculas con es@ director(a), prueba con otr@ director(a)"
    return director_movies

d = recommend_based_on_director('Director_Marcos_Siega')
print(d)

def recommend_based_on_tags(*args):
    movie_tags = []
    #flag = 0
    for movie in onto.Movie.instances():
        flag = 1
        for elem in args:
            if elem not in str(movie.tags):
                flag = 0
        if flag == 1:
            movie_tags.append(movie.title)
    if len(movie_tags) == 0:
        return "Error: no hay peliculas con esos tags, prueba con otros o con alguno de ellos."
    return movie_tags

t = recommend_based_on_tags('family', 'classic')
print(t)

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
                    movies_new.append(str(movie_new.title))

    # Contar las ocurrencias de cada elemento
    conteo = Counter(movies_new)

    # Ordenar los elementos por cantidad de mayor a menor
    ordenado = sorted(conteo, key=conteo.get, reverse=True)

    if cuantas<len(movies_new):
        return ordenado[:cuantas]
    else:
        return 'Error, no se pueden recomendar tantas peliculas.'

r = recommend_based_on_user('User_102040', 10)
print(r)