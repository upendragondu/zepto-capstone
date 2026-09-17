from langgraph.graph import StateGraph, START, END

from .models import AgentState
from .intent import classify_intent
from .vector_store import search_policies
from .config import TOP_K
from .prompt import build_policy_prompt


def classify_intent_node(state: AgentState):
    question = state["question"]

    intent = classify_intent(question)

    return {
        "intent": intent
    }


def retrieve_and_answer_node(state: AgentState):
    question = state["question"]

    results = search_policies(
        question,
        top_k=TOP_K
    )

    documents = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return {
            "answer": "I could not find a relevant Zepto policy.",
            "sources": [],
            "confidence": 0.0
        }

    distance = distances[0] if distances else 1.0

    # Convert Chroma distance into a simple confidence score
    confidence = max(
        0.0,
        min(1.0, 1.0 / (1.0 + distance))
    )

    context = "\n\n".join(documents)

    prompt = build_policy_prompt(
        question,
        context
    )

    # MOCK_LLM response
    answer = (
        "According to the available Zepto policy information: "
        + documents[0]
    )

    sources = ids

    return {
        "answer": answer,
        "sources": sources,
        "confidence": round(confidence, 3)
    }


def direct_answer_node(state: AgentState):
    return {
        "answer": (
            "I can only answer Zepto policy questions. "
            "Please ask about refunds, delivery, cancellation, "
            "payments, returns, replacements, accounts, or offers."
        ),
        "sources": [],
        "confidence": 1.0
    }


def route_after_intent(state: AgentState):
    if state["intent"] == "policy":
        return "retrieve_and_answer"

    return "direct_answer"


graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "classify_intent",
    classify_intent_node
)

graph_builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer_node
)

graph_builder.add_node(
    "direct_answer",
    direct_answer_node
)


graph_builder.add_edge(
    START,
    "classify_intent"
)

graph_builder.add_conditional_edges(
    "classify_intent",
    route_after_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph_builder.add_edge(
    "retrieve_and_answer",
    END
)

graph_builder.add_edge(
    "direct_answer",
    END
)


graph = graph_builder.compile()