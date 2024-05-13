# Recomendador de Recetas con IA Generativa
!["¡Buen provecho!"](img/chef.jpeg)

## Descripción del Proyecto:

Este proyecto consiste en el desarrollo de una aplicación web que sirva como recomendador de recetas. Los usuarios podrán ingresar los ingredientes que deseen utilizar, y la aplicación se conectará con modelos de inteligencia artificial (IA) generativa para proporcionar sugerencias de recetas basadas en esos ingredientes. Además, los usuarios tendrán la opción de guardar estas interacciones en una base de datos alojada en un servidor en Render y acceder al historial de consultas y respuestas.

## Funcionalidades:

- **Recomendación de Recetas:** Los usuarios podrán ingresar los ingredientes que tengan disponibles a través de la interfaz de la aplicación. La aplicación se conectará con modelos de IA generativa para sugerir recetas basadas en esos ingredientes.

- **Guardar Interacciones:** Los usuarios tendrán la opción de guardar las interacciones realizadas, es decir, los ingredientes ingresados y las recetas sugeridas por la IA. Estas interacciones se almacenarán en una base de datos alojada en un servidor para su posterior consulta.

- **Consultar Historial:** La aplicación permitirá a los usuarios acceder al historial de sus interacciones anteriores. Podrán ver una lista de las consultas realizadas y las recetas sugeridas asociadas a cada consulta.

## Tecnologías Utilizadas:

- **Python:** El backend de la aplicación se desarrollará en Python utilizando el framework FastAPI para la creación de la API web.

- **OpenAI:** Se utilizará la plataforma OpenAI para acceder a modelos de IA generativa pre-entrenados que proporcionarán las sugerencias de recetas.

- **asyncpg:** Para la conexión y manipulación de la base de datos PostgreSQL donde se almacenarán las interacciones de los usuarios.

- **Docker:** La aplicación será dockerizada para facilitar su despliegue y ejecución en cualquier entorno.

## Estructura del Proyecto:

El proyecto estará organizado de la siguiente manera:

- **`app.py`:** Contendrá la lógica principal de la aplicación, incluyendo la definición de endpoints, la integración con OpenAI y la gestión de la base de datos.

- **`database.py`:** Archivo que contendrá la configuración y funciones relacionadas con la base de datos PostgreSQL.

- **`Dockerfile`:** Archivo para la creación de la imagen Docker de la aplicación.

- **`requirements.txt`:** Archivo que especificará las dependencias de Python necesarias para la aplicación.

- **`templates/`:** Carpeta que contendrá los archivos HTML para la interfaz de usuario de la aplicación.

- **`cred.py`:** Este archivo debe contener los credenciales del usuario que son: 
    - **openai_key**:"contraseña" (contiene la api-key de OpenAI para hacer llamadas al modelo de ia generativa)
    - **DATABASE_URL**: La url que necesitamos de Render para tener la base de datos guardada en el servidor
    (EJEMPLO)-->DATABASE_URL:"postgres://tu_usuario:tu_contraseña@tu_host:tu_puerto/tu_base_de_datos"

## Instalación y Ejecución:

### Copia el siguiente codigo de Docker hub para hacer pull de la imagen de docker y haz run de la imagen para poder inicializar la app,(**!Recuerda que debes tener abierto Docker Desktop!**)

- docker pull teret90/recetas:latest

-PARA EJECUTAR PUEDES HACERLO DESDE TERMINAL:

- docker run -p 8000:8000 teret90/recetas:latest

-O DESDE DOCKER DESKTOP, PULSANDO RUN EN LA IMAGEN E INICIALIZANDO LUEGO EL CONTENEDOR CON EL BOTON DE RUN.


##  Contribuciones y Contacto:

Si deseas contribuir al desarrollo de la aplicación o tienes alguna sugerencia, no dudes en abrir un issue o enviar un pull request en el repositorio de GitHub.

¡Esperamos que disfrutes utilizando nuestro recomendador de recetas con IA generativa!

