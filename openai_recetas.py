from fastapi import FastAPI, HTTPException
import uvicorn
import sqlite3
import os
from cred import openai_key, DATABASE_URL

from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncpg


# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Montar la carpeta estática para servir archivos estáticos como el HTML
app.mount("/static", StaticFiles(directory="template"), name=("index.html"))

# Instanciar el motor de plantillas Jinja2
templates = Jinja2Templates(directory="template")

# Ruta principal para la página de inicio
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para solicitar una receta
@app.get('/pedir_receta')
async def receta(ingredientes_usuario: str):
    """
    Endpoint para solicitar una receta basada en ingredientes proporcionados por el usuario.

    Args:
        ingredientes_usuario (str): Cadena de texto con los ingredientes proporcionados por el usuario.

    Returns:
        str: Respuesta formateada de la IA con una receta sugerida.
    """

    prompt_template = PromptTemplate.from_template(
        "Dime una receta nueva con estos ingredientes {ingredientes}."
    )

 
    llm = ChatOpenAI(api_key=openai_key)

    
    prompt_usuario = {"role": "user", "content": prompt_template.format(ingredientes=ingredientes_usuario)}

    
    respuesta = llm.invoke([{"role": "system", "content": "Eres un gran chef y nutricionista sólo sabes de esos campos, puedes dar recetas con menos de 500 palabras con los ingredientes que te diga el usuario en el prompt, si no te da ningún ingrediente tienes que darle una receta aleatoria con los ingredientes que quieras, cada vez una nueva. Escribes es español, si alguien mete otras palabras que no sean ingredientes responde amablemente que no puedes darles información que no sea de recetas"}, prompt_usuario])
    print("Respuesta del modelo:", respuesta.content)

    respuesta_formateada = respuesta.content.replace('\n', '<br>')

    print("Respuesta del modelo:", respuesta_formateada)

    return respuesta_formateada


# Ruta para guardar el prompt del usuario y la respuesta de la IA en la base de datos
@app.post('/guardar_receta')
async def insert(data: dict, background_tasks: BackgroundTasks):
    """
    Endpoint para guardar el prompt del usuario y la respuesta de la IA en la base de datos.

    Args:
        data (dict): Diccionario con los datos a ser guardados.
        background_tasks (BackgroundTasks): Tareas en segundo plano para guardar en la base de datos.

    Returns:
        dict: Mensaje de confirmación de recepción de datos.
    """
    pregunta = data.get("prompt_usuario")
    respuesta = data.get("respuesta_ia")

    background_tasks.add_task(save_to_database, pregunta, respuesta)

    return {"message": "Datos recibidos, se guardarán en la base de datos de render."}


async def save_to_database(prompt_usuario: str, respuesta_ia: str):
    try:
        print("Guardando datos en la base de datos...")
        print("Prompt Usuario:", prompt_usuario)
        print("Respuesta IA:", respuesta_ia)
        
        # Conectar a la base de datos PostgreSQL
        async with asyncpg.create_pool(DATABASE_URL) as pool:

            async with pool.acquire() as connection:
                await connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS recetas (
                        id SERIAL PRIMARY KEY,
                        prompt_usuario TEXT,
                        respuesta_ia TEXT
                    )
                    """
                )

                await connection.execute(
                    "INSERT INTO recetas (prompt_usuario, respuesta_ia) VALUES ($1, $2)",
                    prompt_usuario, respuesta_ia
                )
        print("Datos guardados correctamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar datos en la base de datos: {e}")

# Ruta para mostrar el historial de recetas guardadas
@app.get('/mostrar_historial')
async def historial():
    """
    Endpoint para mostrar el historial de recetas guardadas en la base de datos.

    Returns:
        list: Lista de objetos de tipo asyncpg.Record(similares a diccionarios), cada uno representando una fila de la tabla de recetas.
    """

    try:
        
        conn = await asyncpg.connect(DATABASE_URL)
        
        
        historial = await conn.fetch("SELECT id, prompt_usuario, respuesta_ia FROM recetas")
        print(historial)
        
        
        await conn.close()
        
        
        return historial
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el historial: {e}")


# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)