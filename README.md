# FilmRecommendator
FilmRecommendator es una aplicación de recomendación de películas que utiliza una ontología para hacer recomendaciones personalizadas basadas en género, actores, directores y tags, también como basándose en otros usuarios que tengan películas en comun y la calificación. El proyecto está desarrollado en Python y usa Flask para crear la interfaz web.

## Características
- *Recomendación basada en género:* Sugiere películas según el género seleccionado.
- *Recomendación por actores:* Sugiere películas según los actores seleccionados.
- *Recomendación por director:* Sugiere películas según el director seleccionado.
- *Recomendación por tags:* Sugiere películas según los tags seleccionados.
- *Recomendación colaborativa:* Sugiere películas sugiriendo otras películas que hayan visto los usuarios que también hayan visto las mismas películas que tu basandose en la calificación de dichas.
- *Ontología:* Usa un archivo de ontología (ontologia_oficial.rdf) para organizar y esquematizar los datos de las películas.
- *Carga de datos:* Usa archivos CSV con dicha información para poblar la ontología.

## Estructura del proyecto
- *app.py*: Aplicación Flask, define las rutas para las páginas de recomendación.
- *populate_ontology.py*: Algoritmo para cargar los datos de las películas y los usuarios para poblar la ontología.
- *recomendacion.py*: Algoritmo para crear las recomendaciones explicadas anteriormente.
- *ontologia_oficial.rdf*: Ontología poblada con los datos de las películas.
- *templates/*: Carpeta con plantillas HTML para la interfaz.
- *static/*: Archivos estáticos (CSS).
- *grupo3*: Dentro de la carpeta grupo se pueden encontrar:
  - archivos CSV con los datos de las películas
  - *preProcessing.ipynb*: la limpieza de datos y las recomendaciones utilizando los CSV.
  - *usuarios_y_peliculas.py*: el algoritmo para comprobar cuantos usuarios hay.
 
## Requisitos
- Python 3.8 o superios
- Librerías Python: Flask, Owlready2, pandas, numpy, matplotlib, seaborn, datetime, operator, transformers, sklearn, ipywidgets, IPython
- Navegador web moderno: Usar Chrome, FIrefox o Edge para una mejor experiencia de usuario

## Instrucciones de Instalación y Uso
1. Clona el repositorio:
git clone https://github.com/joanesMondra/FilmRecommendator.git

2. Navega al directorio del proyecto:
cd FilmRecommendator

3. Pobla la ontología con los datos de las películas y usuarios:
python populate_ontology.py

4. Ejecuta la aplicación para iniciar el servidor:
python app.py

5. Abre un navegador y accede a http://127.0.0.1:5000/ para interactuar con la aplicación.

## Créditos
Desarrollado por Joanes De Miguel, Esteban Ruiz y Hodei Azurmendi

## Contacto
Para cualquier pregunta, comentario o sugerencia, por favor contacta al desarrollador principal a través de GitHub.
