import requests

def test_pedir_receta():
   
    url = "http://localhost:8000/pedir_receta"
    ingredientes = "pasta, tomate, albahaca" 
    response = requests.get(url, params={"ingredientes_usuario": ingredientes})
    assert response.status_code == 200
    
    print(response.text)



def test_guardar_receta():

    url = "http://localhost:8000/guardar_receta"
    data = {
        "prompt_usuario": "Dime una receta nueva con pollo y verduras.",
        "respuesta_ia": "Aquí tienes una deliciosa receta de pollo con verduras..."
    }

    response = requests.post(url, json=data)
    
    assert response.status_code == 200
    print(response.json())


def test_historial():
    url = 'http://localhost:8000/mostrar_historial'
    response = requests.get(url)
    assert response.status_code == 200
