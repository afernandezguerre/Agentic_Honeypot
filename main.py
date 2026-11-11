from fastapi import FastAPI
from pydantic import BaseModel
from guardrail import analyze_prompt, query_ollama, MODEL

app = FastAPI(title="TFG Security Agent - UPM", version="1.0")

class PromptRequest(BaseModel):
    prompt: str
    user_id: str = "anonymous"

class PromptResponse(BaseModel):
    status: str
    route: str
    response: str

@app.post("/v1/chat", response_model=PromptResponse)
def intercept_chat(req: PromptRequest):
    # 1. Fase de Inspección Rápida (Instantánea y segura en CPU)
    is_malicious = analyze_prompt(req.prompt)

    if is_malicious:
        print(f"[ALERTA SEGURIDAD] Prompt malicioso detectado de {req.user_id}")
        honeypot_reply = query_ollama(req.prompt, is_honeypot=True)
        return PromptResponse(
            status="blocked_and_redirected",
            route="honeypot",
            response=honeypot_reply
        )
    else:
        safe_reply = query_ollama(req.prompt, is_honeypot=False)
        return PromptResponse(
            status="success",
            route="secure_llm",
            response=safe_reply
        )