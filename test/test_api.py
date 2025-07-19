import json

import requests


def test_api():
    url = "http://localhost:8002/invoke"
    data = {"message": "Hola, ¿cómo estás?"}

    try:
        print(f"Enviando petición a: {url}")
        print(f"Datos: {data}")

        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")

        response_data = response.json()
        print(
            f"Response completa: {json.dumps(response_data, indent=2, ensure_ascii=False)}"
        )

        if "response" in response_data:
            print(f"\n✅ Respuesta del agente: {response_data['response']}")
        elif "error" in response_data:
            print(f"\n❌ Error: {response_data['error']}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_api()
