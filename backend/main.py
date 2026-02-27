import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# import os
# from dotenv import load_dotenv

# --- Fix 1: Robust .env loading using Path ---
# Define the path to the ROOT .env file explicitly
ROOT_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=DOTENV_PATH)
# ---------------------------------------------


from database import get_db, engine
from models import Base
from schemas import (
    StackCreate, StackResponse, StackUpdate,
    WorkflowCreate, WorkflowResponse, WorkflowStructureUpdate,
    ChatMessageCreate, ChatMessageResponse,
    DocumentUpload, DocumentResponse,
    ConversationCreate, ConversationResponse
)
from services import (
    StackService, WorkflowService, ChatService, 
    DocumentService, LLMService, EmbeddingService
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GenAI Stack API",
    description="No-Code/Low-Code web application for building intelligent workflows",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODIFIED SERVICE INITIALIZATION BLOCK (The Critical Fix) ---

# 1. Initialize core dependencies (LLM and Embedding)
llm_service = LLMService()
embedding_service = EmbeddingService()

# 2. Initialize secondary services, passing their dependencies explicitly
# DocumentService needs EmbeddingService
document_service = DocumentService(embedding_service=embedding_service)

# 3. Handle circular dependency (ChatService needs WorkflowService, WFS needs ChatService)
# Initialize ChatService with a placeholder/None, and update it later.
# We also initialize StackService here as it has no dependencies.
chat_service = ChatService(workflow_service=None) 
stack_service = StackService()

# 4. Initialize WorkflowService (WFS depends on LLM, Document, and the placeholder ChatService)
workflow_service = WorkflowService(
    llm_service=llm_service,
    document_service=document_service,
    chat_service=chat_service
)

# 5. Final step: Complete the circular dependency chain
chat_service.workflow_service = workflow_service 
# --------------------------------------------------------------------------


@app.get("/")
async def root():
    return {"message": "GenAI Stack API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Stack endpoints
@app.post("/api/stacks", response_model=StackResponse)
async def create_stack(stack: StackCreate, db: Session = Depends(get_db)):
    return stack_service.create_stack(db, stack)

@app.get("/api/stacks", response_model=List[StackResponse])
async def get_stacks(db: Session = Depends(get_db)):
    return stack_service.get_stacks(db)

@app.get("/api/stacks/{stack_id}", response_model=StackResponse)
async def get_stack(stack_id: int, db: Session = Depends(get_db)):
    stack = stack_service.get_stack(db, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    return stack

@app.put("/api/stacks/{stack_id}", response_model=StackResponse)
async def update_stack(stack_id: int, stack: StackUpdate, db: Session = Depends(get_db)):
    updated_stack = stack_service.update_stack(db, stack_id, stack)
    if not updated_stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    return updated_stack

@app.delete("/api/stacks/{stack_id}")
async def delete_stack(stack_id: int, db: Session = Depends(get_db)):
    success = stack_service.delete_stack(db, stack_id)
    if not success:
        raise HTTPException(status_code=404, detail="Stack not found")
    return {"message": "Stack deleted successfully"}

# Workflow endpoints
@app.post("/api/workflows", response_model=WorkflowResponse)
async def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    return workflow_service.create_workflow(db, workflow)

@app.get("/api/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = workflow_service.get_workflow(db, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@app.post("/api/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: int, query: str, db: Session = Depends(get_db)):
    result = await workflow_service.execute_workflow(db, workflow_id, query)
    return {"result": result}
# backend/main.py (Add this endpoint below /api/workflows/{workflow_id}/execute)

@app.post("/api/workflows/{workflow_id}/validate_and_save")
async def validate_and_save_workflow(
    workflow_id: int, 
    body: WorkflowStructureUpdate,
    db: Session = Depends(get_db)
):
    """Validates the workflow structure and updates the database record."""
    try:
        # Use the service to update the workflow (nodes and edges)
        updated_workflow = workflow_service.update_workflow_structure(
            db, 
            workflow_id, 
            nodes=body.nodes, 
            edges=body.edges
        )
        if not updated_workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
            
        # Perform deeper validation in the service
        validation_message = workflow_service.validate_workflow_logic(updated_workflow)
        
        return {"message": validation_message, "status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
# Document endpoints
@app.post("/api/documents/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    stack_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return await document_service.upload_document(db, file, stack_id)

@app.get("/api/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    document = document_service.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    success = document_service.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}

# Chat endpoints
@app.post("/api/chat/conversations", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    return chat_service.create_conversation(db, conversation.workflow_id, conversation.title)

@app.post("/api/chat/messages", response_model=ChatMessageResponse)
async def create_chat_message(message: ChatMessageCreate, db: Session = Depends(get_db)):
    return chat_service.create_message(db, message)

@app.get("/api/chat/conversations/{conversation_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(conversation_id: int, db: Session = Depends(get_db)):
    return chat_service.get_messages(db, conversation_id)

@app.post("/api/chat/conversations/{conversation_id}/send")
async def send_message(
    conversation_id: int,
    body: dict = Body(...),
    db: Session = Depends(get_db)
):
    message = body.get("message", "")
    response = await chat_service.send_message(db, conversation_id, message)
    return {"response": response}

# LLM endpoints
@app.post("/api/llm/generate")
async def generate_response(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 1000
):
    response = await llm_service.generate_response(prompt, model, temperature, max_tokens)
    return {"response": response}

@app.post("/api/llm/embed")
async def create_embeddings(texts: List[str], model: str = "text-embedding-3-large"):
    embeddings = await embedding_service.create_embeddings(texts, model)
    return {"embeddings": embeddings}

# Web search endpoints
@app.post("/api/search/web")
async def web_search(query: str, num_results: int = 5):
    results = await llm_service.web_search(query, num_results)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)