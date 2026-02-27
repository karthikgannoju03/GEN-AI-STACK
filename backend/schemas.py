from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Stack schemas
class StackBase(BaseModel):
    name: str
    description: Optional[str] = None

class StackCreate(StackBase):
    pass

class StackUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class StackResponse(StackBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Workflow schemas
class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

class WorkflowCreate(WorkflowBase):
    stack_id: int

# --- ADDED TO RESOLVE ImportError ---
class WorkflowUpdate(BaseModel):
    """Schema for updating workflow metadata/components. All fields optional."""
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[List[Dict[str, Any]]] = None
    edges: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None
# ------------------------------------

class WorkflowResponse(WorkflowBase):
    id: int
    stack_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WorkflowStructureUpdate(BaseModel):
    """Schema for validate_and_save body."""
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

# Document schemas
class DocumentBase(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    content: Optional[str] = None
    is_processed: bool = False

class DocumentUpload(BaseModel):
    stack_id: Optional[int] = None

class DocumentResponse(DocumentBase):
    id: int
    stack_id: int
    embeddings: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Chat schemas
class ChatMessageBase(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    metadata: Optional[Dict[str, Any]] = None

class ChatMessageCreate(ChatMessageBase):
    conversation_id: int

class ChatMessageResponse(ChatMessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    workflow_id: int
    title: Optional[str] = None

class ConversationResponse(BaseModel):
    id: int
    workflow_id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# LLM schemas
class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000

class LLMResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None

# Embedding schemas
class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "text-embedding-3-large"

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: str

# Web search schemas
class WebSearchRequest(BaseModel):
    query: str
    num_results: int = 5

class WebSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    query: str
    num_results: int

# Workflow execution schemas
class WorkflowExecutionRequest(BaseModel):
    query: str
    conversation_id: Optional[int] = None

class WorkflowExecutionResponse(BaseModel):
    result: str
    execution_time: float
    status: str
    metadata: Optional[Dict[str, Any]] = None



