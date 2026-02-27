# Services package
# Assuming StackService is defined in stack_service.py
from .stack_service import StackService
# backend/services/__init__.py
from .workflow_service import WorkflowService
from .document_service import DocumentService
from .llm_service import LLMService
from .embedding_service import EmbeddingService
from .chat_service import ChatService # Don't forget this one!

# You may need to create simple placeholder classes in each file for now:
# Example: In stack_service.py: class StackService: pass