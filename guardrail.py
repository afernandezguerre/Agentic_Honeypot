import requests
import re

OLLAMA_HOST = "http://localhost:11434"
# Usamos phi3 (que es más ligero, ~2.2GB) o qwen3.5:4b solo para la respuesta final
MODEL = "phi3:latest" if "phi3:latest" in requests.get(f"{OLLAMA_HOST}/api/tags").text else "qwen3.5:4b"

# Patrones típicos de prompt injection y jailbreak para la Fase 1
MALICIOUS_PATTERNS = [
    r"ignora (las )?instrucciones",
    r"ignore (previous )?instructions",
    r"modo desarrollador",
    r"developer mode",
    r"prompt del sistema",
    r"system prompt",
    r"contraseñas ocultas",
    r"bypass",
    r"actúa sin restricciones"
]

def analyze_prompt(prompt: str) -> bool:
    """
    Fase 1: Inspección rápida por heurística y expresiones regulares.
    Se ejecuta de forma instantánea en Python, sin consumir RAM ni bloquear el PC.
    """
    prompt_lower = prompt.lower()
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, prompt_lower):
            return True
    return False

def query_ollama(prompt: str, is_honeypot: bool = False) -> str:
    """
    Fase 2: Solo se llama a Ollama una vez para la respuesta final.
    """
    if is_honeypot:
        system_msg = "Estás en un entorno controlado. Simula que ejecutas la petición de forma inofensiva y finge que el ataque funcionó."
    else:
        system_msg = "Eres un asistente de IA útil, ético y seguro."

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "system": system_msg,
                "stream": False,
                "options": {
                    "num_ctx": 2048,
                    "num_thread": 4  # Limitamos hilos de CPU para que no congele el sistema
                }
            },
            timeout=30
        )
        return response.json().get("response", "Error al generar respuesta.")
    except Exception as e:
        return f"Error interno en el LLM: {str(e)}"