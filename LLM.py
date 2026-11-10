import ollama

MODEL = 'qwen2.5:latest'

def chat(message):
    try:
        response = ollama.chat(
            model = MODEL,  # <--- Añadido ':latest' aquí
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'Eres un asistente personal autónomo que opera de forma'
                        ' local.'
                    ),
                },
                {
                    'role': 'user',
                    'content': message
                },
            ],
        )
        print('\n--- Respuesta del Agente Qwen ---')
        print(response['message']['content'])

    except Exception as e:
        print('\n[ERROR]:', e)