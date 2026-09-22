from dotenv import load_dotenv
from anthropic import Anthropic
import os
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

herramienta = {
    "name": "registrar_datos_dia",
    "description": "Extrae los datos de comida y entrenamiento mencionados en el mensaje del usuario",
    "input_schema": {
        "type": "object",
        "properties": {
            "comidas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tipo": {
                            "type": "string",
                            "enum": ["alimento_individual", "plato_compuesto"],
                            "description": "individual si es un alimento simple (pollo, arroz, brócoli...), compuesto si es un plato con varios ingredientes mezclados (boloñesa, lasaña, curry...)"
                        },
                        "nombre": {"type": "string"},
                        "cantidad_min_g": {"type": "number"},
                        "cantidad_max_g": {"type": "number"},
                        "estado": {
                            "type": "string",
                            "enum": ["crudo", "cocinado"],
                            "description": "Si el usuario no lo especifica claramente, asume 'crudo' por defecto"
                        },
                        "estado_confirmado": {
                            "type": "boolean",
                            "description": "true si el usuario dijo explícitamente el estado, false si se ha asumido por defecto"
                        }
                    },
                    "required": ["tipo", "nombre", "cantidad_min_g", "cantidad_max_g", "estado", "estado_confirmado"]
                }
            },
            "entrenamiento": {
                "type": "object",
                "properties": {
                    "entreno": {"type": "boolean"},
                    "grupo_muscular": {"type": "string"},
                    "ejercicios": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string"},
                                "series": {"type": "number"},
                                "repeticiones": {"type": "number"},
                                "peso_kg": {"type": "number"}
                            },
                            "required": ["nombre", "series", "repeticiones"]
                        }
                    }
                },
                "required": ["entreno"]
            }
        },
        "required": ["comidas", "entrenamiento"]
    }
}

def extraer(mensaje_usuario):
    respuesta = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=[herramienta],
        tool_choice={"type": "tool", "name": "registrar_datos_dia"},
        messages=[
            {"role": "user", "content": mensaje_usuario}
        ]
    )
    for bloque in respuesta.content:
        if bloque.type == "tool_use":
            return bloque.input
    return None


mensaje = "200g de pollo, 50 de brócoli, 50 de pimientos y 100 de arroz cocido, y entrené pecho: press banca 4 series de 8 repeticiones a 60kg"
datos = extraer(mensaje)
print(json.dumps(datos, indent=2, ensure_ascii=False))