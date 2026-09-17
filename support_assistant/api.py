from fastapi import FastAPI

from .graph import graph
from .models import AskResponse


app = FastAPI(
    title="Zepto Support Assistant",
    description="RAG-based Zepto policy assistant",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Zepto Support Assistant is running"
    }


@app.post("/ask", response_model=AskResponse)
def ask_question(question: str):

    result = graph.invoke({
        "question": question
    })

    response = AskResponse(
        answer=result.get("answer", ""),
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0)
    )

    return response