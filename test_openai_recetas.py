import requests

def test_pedir_receta():
   
    url = "http://localhost:8000/pedir_receta"
    ingredientes = "pasta, tomate, albahaca" 
    response = requests.get(url, params={"ingredientes_usuario": ingredientes})
    assert response.status_code == 200
    
    print(response.text)



def test_guardar_receta():
    # URL de tu servidor de FastAPI
    url = "http://localhost:8000/guardar_receta"

    # Datos para enviar en la solicitud POST
    data = {
        "prompt_usuario": "Dime una receta nueva con pollo y verduras.",
        "respuesta_ia": "Aquí tienes una deliciosa receta de pollo con verduras..."
    }

    # Realizar una solicitud POST al endpoint '/guardar_receta' con los datos especificados
    response = requests.post(url, json=data)
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    assert response.status_code == 200
    
    # Imprimir la respuesta del servidor
    print(response.json())

# Ejecutar la función de prueba
test_guardar_receta()
