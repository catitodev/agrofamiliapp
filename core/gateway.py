from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import asyncio

from core.config import settings
from core.memory import memory
from core.feedback import feedback_collector
from agents.ater import ATERAgent
from agents.credito import CreditoAgent
from agents.mercado import MercadoAgent
from agents.clima import ClimaAgent
from agents.docs import DocsAgent
from agents.territorio import TerritorioAgent

app = FastAPI(
    title="AgroFamíliApp API",
    description="AI conversational agent for Brazilian family farmers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: Optional[str] = None
    audio: Optional[str] = None
    user_id: str


class AgentResponse(BaseModel):
    agent: str
    response: str
    confidence: float
    suggested_actions: Optional[List[str]] = None
    context_used: Optional[Dict] = None


AGENT_MAP = {
    "ater": ATERAgent,
    "credito": CreditoAgent,
    "mercado": MercadoAgent,
    "clima": ClimaAgent,
    "docs": DocsAgent,
    "territorio": TerritorioAgent,
}

agents: Dict[str, object] = {}


@app.on_event("startup")
async def startup():
    try:
        await memory.connect()
    except Exception:
        pass
    for name, cls in AGENT_MAP.items():
        try:
            agents[name] = cls()
        except Exception:
            agents[name] = None


@app.on_event("shutdown")
async def shutdown():
    await memory.close()


@app.get("/")
async def root():
    return {
        "name": "AgroFamíliApp",
        "version": "1.0.0",
        "status": "operational",
        "agents": list(AGENT_MAP.keys())
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "model": settings.model_name}


@app.post("/chat", response_model=AgentResponse)
async def chat(message: Message):
    try:
        if message.audio:
            try:
                from core.stt import stt_engine
                text = stt_engine.transcribe(message.audio)
            except Exception:
                raise HTTPException(status_code=400, detail="Audio processing not available")
        elif message.text:
            text = message.text
        else:
            raise HTTPException(status_code=400, detail="Provide text or audio")

        intent = await detect_intent(text)
        agent_name = intent["agent"]
        agent = agents.get(agent_name)
        if agent is None:
            agent = agents.get("ater")

        response = await agent.generate(text, user_id=message.user_id)

        try:
            await memory.add_message(message.user_id, "user", text, agent_name)
            await memory.add_message(message.user_id, "assistant", response["text"], agent_name)
        except Exception:
            pass

        try:
            await feedback_collector.log_interaction(
                message.user_id, text, agent_name, response["text"], metadata=intent
            )
        except Exception:
            pass

        return AgentResponse(
            agent=agent_name,
            response=response["text"],
            confidence=response.get("confidence", 0.8),
            suggested_actions=response.get("suggested_actions"),
            context_used=response.get("context")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def submit_feedback(user_id: str, agent: str, rating: int, comment: Optional[str] = None):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    await feedback_collector.log_feedback(user_id, agent, rating, comment)
    return {"status": "ok"}


@app.get("/stats")
async def get_stats():
    return await feedback_collector.get_aggregate_stats()


@app.get("/history/{user_id}")
async def get_history(user_id: str):
    history = await memory.get_history(user_id)
    return {"history": history}


async def detect_intent(text: str) -> Dict:
    text_lower = text.lower()

    keywords = {
        "ater": ["plantar", "colheita", "solo", "adubo", "praga", "safra", "planta", "cultivo", "irrigação", "fertilizante"],
        "credito": ["empréstimo", "crédito", "pronaf", "financiamento", "banco", "juros", "cafe", "dap", "seguro"],
        "mercado": ["vender", "preço", "paa", "pnae", "feira", "comprador", "comercializar", "mercado", "cotação"],
        "clima": ["chuva", "tempo", "clima", "previsao", "semana", "sol", "geada", "estiagem", "estiagem"],
        "docs": ["documento", "cadastro", "registro", "certificado", "certificação", "legal", "cnpj", "inscrição"],
        "territorio": ["emater", "escritório", "municipio", "ater", "cooperativa", "região", "endereço", "contato"],
    }

    scores: Dict[str, int] = {k: 0 for k in keywords}
    for agent, kws in keywords.items():
        for kw in kws:
            if kw in text_lower:
                scores[agent] += 1

    best_agent = max(scores, key=scores.get) if max(scores.values()) > 0 else "ater"
    confidence = scores[best_agent] / (scores[best_agent] + 1)

    return {"agent": best_agent, "confidence": confidence, "scores": scores}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)