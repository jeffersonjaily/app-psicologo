from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Token Hugging Face do usuário
HF_TOKEN = "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"

# Inicializa o pipeline com o modelo em português
pipe = pipeline(
    "text-generation",
    model="recogna-nlp/bode-7b-alpaca-pt-br",
    use_auth_token=HF_TOKEN
)

# Inicializa o app FastAPI
app = FastAPI()

# Permite chamadas CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para produção, especifique o domínio correto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo da requisição
class ChatInput(BaseModel):
    message: str

# Rota de chat
@app.post("/chat")
async def chat_endpoint(chat: ChatInput):
    try:
        # Gera a resposta com até 100 tokens
        output = pipe(chat.message, max_new_tokens=10000, do_sample=True)[0]["generated_text"]
        return {"response": output}
    except Exception as e:
        return {"response": f"Erro interno: {str(e)}"}
