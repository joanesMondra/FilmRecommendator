from flask import Flask, render_template, request, jsonify
from recomendacion import (recommend_based_on_genre, recommend_based_on_actors,
                           recommend_based_on_director, recommend_based_on_tags, recommend_based_on_user)

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para las páginas de recomendación
@app.route('/genre')
def genre():
    return render_template('genre.html')

@app.route('/actor')
def actor():
    return render_template('actor.html')

@app.route('/director')
def director():
    return render_template('director.html')

@app.route('/tags')
def tags():
    return render_template('tags.html')

@app.route('/user')
def user():
    return render_template('user.html')

# Ruta para procesar recomendaciones
@app.route('/recommend/<type>', methods=['POST'])
def recommend(type):
    data = request.get_json()
    if type == 'genre':
        data = request.get_json()
        if type == 'genre':
            genre = data['genre']
            recommendations = recommend_based_on_genre(genre)
        # Otros tipos de recomendación
        return jsonify({'recommendations': recommendations})
    elif type == 'actor':
        actor = data['actor']
        recommendations = recommend_based_on_actors(actor)
    elif type == 'director':
        director = data['director']
        recommendations = recommend_based_on_director(director)
    elif type == 'tags':
        tags = data['tags']
        # Convertimos los tags de un string separado por comas a una lista de argumentos
        tag_list = [tag.strip() for tag in tags.split(',')]
        # Pasamos los tags como argumentos usando *
        recommendations = recommend_based_on_tags(*tag_list)
    elif type == 'user':
        user_id = data['user_id']
        num_movies = int(data['num_movies'])
        recommendations = recommend_based_on_user(user_id, num_movies)
    else:
        # Devuelve un error si el tipo de recomendación no es válido
        return jsonify({'error': 'Invalid recommendation type'}), 400

    # Devuelve las recomendaciones al cliente en formato JSON
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)

# Comentarios sobre la funcionalidad del código
# 1. Este archivo define una aplicación Flask que proporciona diferentes rutas para ofrecer recomendaciones de películas.
# 2. Cada ruta (/genre, /actor, /director, /tags, /user) renderiza una página HTML específica para el tipo de recomendación solicitado.
# 3. La ruta /recommend/<type> recibe solicitudes POST para procesar recomendaciones según el tipo (género, actor, director, tags o usuario).
# 4. Dependiendo del tipo de recomendación, se llama a una función específica que devuelve una lista de recomendaciones.
# 5. La respuesta se envía de vuelta al cliente en formato JSON para ser mostrada en la interfaz de usuario.

