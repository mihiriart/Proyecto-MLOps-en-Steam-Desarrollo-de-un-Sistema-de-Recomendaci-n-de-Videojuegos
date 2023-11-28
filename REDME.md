Proyecto MLOps en Steam: Desarrollo de un Sistema de Recomendación de Videojuegos

Este documento presenta el proyecto realizado como parte del bootcamp de Machine Learning en Henry, que se enfocó en emular las funciones de un MLOps Engineer fusionando los roles de Data Engineer y Data Scientist en el entorno de la plataforma de juegos Steam.

Objetivo del Proyecto

El principal objetivo fue la creación de un Producto Mínimo Viable (MVP) que comprendiera una API y un modelo de Machine Learning capaz de llevar a cabo análisis de sentimientos en los comentarios de los usuarios, con el propósito de ofrecer un sistema de recomendación personalizado de videojuegos en la plataforma Steam.

Detalles de las Tareas Realizadas y Metodología

Proceso de ETL (Extracción, Transformación y Carga)

Se llevó a cabo un riguroso proceso de ETL para tres archivos JSON  ellos son: 1-user_reviews.json/2-user_items.json/3-steam_games.json,se incluyendo la limpieza de datos, transformación y preparación para su análisis posterior. Se empleó la biblioteca Natural Language Toolkit (NLTK) para el análisis de sentimientos en los comentarios de los usuarios, lo que implicó la creación de una nueva columna llamada 'sentiment_analysis'.

Análisis Exploratorio de Datos (EDA)

Se realizó un análisis detallado de los datos procesados después del ETL para identificar variables significativas. Este análisis fue crucial para identificar las características clave que serían relevantes en el proceso de 'feature engineering'.

Desarrollo de Funciones y Modelado de Machine Learning

Se crearon funciones específicas para tareas esenciales, como identificar usuarios con mayor tiempo de juego, generar recomendaciones de juegos por año, entre otras. Además, se construyó un modelo de recomendación basado en la similitud de género entre videojuegos, utilizando los datos procesados previamente.
Las funciones que se crearon fueron las siguientes: 
1- + def **PlayTimeGenre( *`genero` : str* )**:
     Debe devolver `año` con mas horas jugadas para dicho género.
2- + def **UserForGenre( *`genero` : str* )**:
     Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.   
3- + def **UsersRecommend( *`año` : int* )**:
     Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)  
4- + def **UsersWorstDeveloper( *`año` : int* )**:
     Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)    
5- + def **sentiment_analysis( *`empresa desarrolladora` : str* )**:
     Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total 
     de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.          

Implementación de FastAPI y Despliegue

La implementación de una API utilizando FastAPI fue exitosa, permitiendo un acceso eficiente a través de Railway. Las instrucciones detalladas para la ejecución local y el despliegue en https://web-production-4c58.up.railway.app/docs# están disponibles para revisión.

Resultados y Conclusiones

El proyecto destacó la aplicación práctica de habilidades en Data Engineering y Data Science en un escenario simulado. Aunque el MVP se completó con éxito, se identificaron áreas para mejoras futuras, especialmente en la optimización de procesos y la eficiencia de resultados.

El despliegue y la funcionalidad del proyecto pueden ser explorados en detalle en https://web-production-4c58.up.railway.app/docs# Adicionalmente, un video demostrativo detalla el funcionamiento y las funcionalidades implementadas.https://drive.google.com/file/d/10WV3PzYwo4EiwdWPXbu7kxoQ8i_6EiE5/view?usp=drive_link, https://drive.google.com/file/d/1r9kWQUZCiwZ14K2WGol2XX_6neawek3Q/view?usp=drive_link

