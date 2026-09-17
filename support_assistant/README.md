# Zepto Support Assistant

## Overview

The Zepto Support Assistant answers Zepto policy-related questions using a retrieval-based workflow.

The module uses policy documents, Sentence Transformers embeddings, ChromaDB vector search, LangGraph for workflow orchestration, Pydantic for response validation, and FastAPI for the API endpoint.

The project runs with `MOCK_LLM=True` by default, so an external LLM API key is not required.

## Pipeline Architecture

```text
User Question
      |
      v
classify_intent
      |
      +--------------------+
      |                    |
   policy                general
      |                    |
      v                    v
retrieve_and_answer   direct_answer
      |
      v
ChromaDB
      |
      v
Top 3 Policy Documents
      |
      v
Prompt Construction
      |
      v
Pydantic Validation
      |
      v
JSON Response
```

## Main Components

### 1. Policy Corpus

The `policies/` directory contains eight policy documents:

* Account
* Cancellation
* Delivery
* Offers
* Payments
* Refunds
* Replacements
* Returns

These documents are used as the knowledge corpus for retrieval.

### 2. Embeddings

Policy documents are converted into vector embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 3. Vector Database

ChromaDB stores the policy embeddings and retrieves the most relevant documents for a user question.

The system retrieves the top 3 relevant policy documents.

### 4. Intent Classification

The system uses mock keyword-based intent classification.

Questions are classified as either:

* `policy`
* `general`

Policy questions are sent to retrieval.

General questions receive a direct response explaining that the assistant only answers Zepto policy questions.

### 5. LangGraph

The workflow is implemented using LangGraph `StateGraph`.

The main nodes are:

```text
classify_intent
retrieve_and_answer
direct_answer
```

The graph routes the question according to the detected intent.

### 6. FastAPI

The application exposes:

```text
POST /ask
```

Example request:

```json
{
  "question": "What is the refund policy?"
}
```

## Example Call Transcripts

The following examples were run with `MOCK_LLM=True`.

### Example 1 — Refund Policy

Request:

```json
{
  "question": "What is the refund policy?"
}
```

Response:

```json
{
  "answer": "According to the refund policy, refunds are processed according to the applicable refund conditions.",
  "sources": [
    "refunds",
    "returns",
    "payments"
  ],
  "confidence": 0.0
}
```

### Example 2 — Cancellation Policy

Request:

```json
{
  "question": "What is the cancellation policy?"
}
```

Response:

```json
{
  "answer": "According to the cancellation policy, cancellation requests are handled according to the applicable cancellation conditions.",
  "sources": [
    "cancellation",
    "refunds",
    "returns"
  ],
  "confidence": 0.138
}
```

### Example 3 — General Question

Request:

```json
{
  "question": "What is the capital of India?"
}
```

Response:

```json
{
  "answer": "I can only answer Zepto policy questions.",
  "sources": [],
  "confidence": 1.0
}
```

## Running the Application

Activate the virtual environment and run:

```powershell
uvicorn support_assistant.api:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Building the Vector Store

Run:

```powershell
python -m support_assistant.build_db
```

This loads the policy documents, generates embeddings, and stores them in ChromaDB.

## Testing

Run:

```powershell
python -m support_assistant.test_graph
```

## Docker

The module includes a `Dockerfile` for containerized execution.

## Configuration

The default configuration uses:

```text
MOCK_LLM=True
TOP_K=3
```

No external LLM API key is required for the default mock implementation.

## Optional Extensions

No live Hugging Face Space deployment was attempted.

The default implementation uses `MOCK_LLM=True`; no real-LLM free-tier deployment is required for the core module.
