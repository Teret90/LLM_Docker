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



app = FastAPI()
app.mount("/static", StaticFiles(directory="template"), name=("index.html","chef_1.jpg"))
templates = Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/pedir_receta')
async def receta(ingredientes_usuario: str):
    prompt_template = PromptTemplate.from_template(
        "Dime una receta nueva con estos ingredientes {ingredientes}."
    )

 
    llm = ChatOpenAI(api_key=openai_key)

    # Define el rol del usuario en el prompt
    prompt_usuario = {"role": "user", "content": prompt_template.format(ingredientes=ingredientes_usuario)}

    # Hacemos la llamada al modelo de lenguaje con el prompt completo
    respuesta = llm.invoke([{"role": "system", "content": "Eres un gran chef y nutricionista sólo sabes de esos campos, puedes dar recetas con menos de 500 palabras con los ingredientes que te diga el usuario en el prompt, si no te da ningún ingrediente tienes que darle una receta aleatoria con los ingredientes que quieras, cada vez una nueva. Escribes es español, si alguien mete otras palabras que no sean ingredientes responde amablemente que no puedes darles información que no sea de recetas"}, prompt_usuario])
    print("Respuesta del modelo:", respuesta.content)

        # Formatear la respuesta con saltos de línea HTML
    respuesta_formateada = respuesta.content.replace('\n', '<br>')

    print("Respuesta del modelo:", respuesta_formateada)

    # Devolver la respuesta formateada
    return respuesta_formateada


# Función asíncrona para guardar el prompt del usuario y la respuesta de la ia en la base de datos de render
@app.post('/guardar_receta')
async def insert(data: dict, background_tasks: BackgroundTasks):
    pregunta = data.get("prompt_usuario")
    respuesta = data.get("respuesta_ia")

    # Realizar tareas en segundo plano, como guardar en la base de datos
    background_tasks.add_task(save_to_database, pregunta, respuesta)

    return {"message": "Datos recibidos, se guardarán en la base de datos de render."}


async def save_to_database(prompt_usuario: str, respuesta_ia: str):
    try:
        print("Guardando datos en la base de datos...")
        print("Prompt Usuario:", prompt_usuario)
        print("Respuesta IA:", respuesta_ia)
        
        # Conectar a la base de datos PostgreSQL
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            # Comprobar si la tabla existe, y si no, crearla
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

                # Ejecutar la consulta SQL para insertar los datos en la tabla
                await connection.execute(
                    "INSERT INTO recetas (prompt_usuario, respuesta_ia) VALUES ($1, $2)",
                    prompt_usuario, respuesta_ia
                )
        print("Datos guardados correctamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar datos en la base de datos: {e}")




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)