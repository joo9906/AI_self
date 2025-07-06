# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from chat import chat
from retriever import retriever

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(req: MessageRequest):
    print(f"\n-------------\nReceived message: {req.message}\n for session: {req.session_id}\n ---------------")
    
    context = retriever(req.message)
    reply = chat(req.session_id, req.message, context)
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8443,
        ssl_certfile="./selfsigned.crt",
        ssl_keyfile="./selfsigned.key"
    )
