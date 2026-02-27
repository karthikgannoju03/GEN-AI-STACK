# # backend/services/workflow_service.py
# from sqlalchemy.orm import Session
# from typing import List, Optional, Dict, Any, TYPE_CHECKING # Import TYPE_CHECKING
# from models import Workflow, WorkflowExecution
# from schemas import WorkflowCreate, WorkflowUpdate
# import json
# from datetime import datetime

# # Import non-circular dependencies
# from .llm_service import LLMService
# from .document_service import DocumentService

# # --- MODIFICATION START ---
# # Only import for type checking purposes to break the circular dependency
# if TYPE_CHECKING:
#     from .chat_service import ChatService 
# # ---------------------------


# class WorkflowService:
#     # Use string literal for ChatService type hint
#     def __init__(self, llm_service: LLMService, document_service: DocumentService, chat_service: 'ChatService'):
#         """Initializes WorkflowService with required external service dependencies."""
#         self.llm_service = llm_service
#         self.document_service = document_service
#         self.chat_service = chat_service

#     # --- CRUD Methods (Using model_dump) ---
#     def create_workflow(self, db: Session, workflow: WorkflowCreate) -> Workflow:
#         db_workflow = Workflow(**workflow.model_dump())
#         db.add(db_workflow)
#         db.commit()
#         db.refresh(db_workflow)
#         return db_workflow

#     def get_workflow(self, db: Session, workflow_id: int) -> Optional[Workflow]:
#         return db.query(Workflow).filter(Workflow.id == workflow_id).first()

#     def update_workflow(self, db: Session, workflow_id: int, workflow: WorkflowUpdate) -> Optional[Workflow]:
#         db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
#         if not db_workflow:
#             return None
        
#         update_data = workflow.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(db_workflow, field, value)
        
#         db.commit()
#         db.refresh(db_workflow)
#         return db_workflow

#     def delete_workflow(self, db: Session, workflow_id: int) -> bool:
#         db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
#         if not db_workflow:
#             return False
        
#         db.delete(db_workflow)
#         db.commit()
#         return True

#     # --- CORE EXECUTION LOGIC (The logic remains correct) ---
#     async def execute_workflow(self, db: Session, workflow_id: int, query: str) -> str:
#         """Loads the workflow configuration and executes the node chain using injected services."""
#         workflow = self.get_workflow(db, workflow_id)
#         if not workflow:
#             raise ValueError("Workflow not found")
        
#         # Create execution record
#         execution = WorkflowExecution(
#             workflow_id=workflow_id,
#             input_query=query,
#             status="running",
#             # Assuming created_at is handled by the model default
#         )
#         db.add(execution)
#         db.commit()
        
#         try:
#             # 1. Parse nodes and edges 
#             nodes: List[Dict[str, Any]] = workflow.nodes
#             edges: List[Dict[str, Any]] = workflow.edges
            
#             # ... (rest of the logic remains the same, using self.llm_service and self.document_service)
#             llm_node = next((node for node in nodes if node.get('type') == 'LLM (OpenAI)'), None)
#             knowledge_base_node = next((node for node in nodes if node.get('type') == 'KnowledgeBase'), None)
            
#             if not llm_node:
#                 raise ValueError("Workflow must include an LLM Engine component.")

#             llm_config = llm_node.get('data', {}).get('config', {})
#             context = ""
            
#             # 3. Execute KnowledgeBase 
#             # ... logic to check connection and call self.document_service.retrieve_context
            
#             # 4. Execute LLM Engine
#             response = await self.llm_service.generate_workflow_response(
#                 query=query,
#                 model=llm_config.get('Model', 'gpt-4o-mini'),
#                 temperature=llm_config.get('Temperature', 0.7),
#                 max_tokens=llm_config.get('Max tokens', 1000),
#                 context=context,
#                 custom_prompt=llm_config.get('Prompt', None),
#                 use_web_search=llm_config.get('WebSearchTool', False)
#             )
            
#             # 5. Finalize execution record
#             execution.output_response = response
#             execution.status = "completed"
#             db.commit()
            
#             return response
            
#         except Exception as e:
#             db.rollback() 
#             execution.status = "failed"
#             execution.error_message = str(e)
#             db.commit()
#             raise e
# --- CORE EXECUTION LOGIC ---
# backend/services/workflow_service.py
from sqlalchemy.orm import Session # <-- FIX 1: Import Session
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from models import Workflow, WorkflowExecution
from schemas import WorkflowCreate, WorkflowUpdate
import json
from datetime import datetime

# Import non-circular dependencies
from .llm_service import LLMService
from .document_service import DocumentService

# Fix 2: Break circular dependency using TYPE_CHECKING
if TYPE_CHECKING:
    from .chat_service import ChatService 


class WorkflowService:
    # Use string literal for ChatService type hint
    def __init__(self, llm_service: LLMService, document_service: DocumentService, chat_service: 'ChatService'):
        """Initializes WorkflowService with required external service dependencies."""
        self.llm_service = llm_service
        self.document_service = document_service
        self.chat_service = chat_service

    # --- CRUD Methods ---
    def create_workflow(self, db: Session, workflow: WorkflowCreate) -> Workflow:
        db_workflow = Workflow(**workflow.model_dump())
        db.add(db_workflow)
        db.commit()
        db.refresh(db_workflow)
        return db_workflow

    def get_workflow(self, db: Session, workflow_id: int) -> Optional[Workflow]:
        return db.query(Workflow).filter(Workflow.id == workflow_id).first()

    def update_workflow(self, db: Session, workflow_id: int, workflow: WorkflowUpdate) -> Optional[Workflow]:
        db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not db_workflow:
            return None
        
        update_data = workflow.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_workflow, field, value)
        
        db.commit()
        db.refresh(db_workflow)
        return db_workflow

    def delete_workflow(self, db: Session, workflow_id: int) -> bool:
        db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not db_workflow:
            return False
        
        db.delete(db_workflow)
        db.commit()
        return True

    def update_workflow_structure(
        self, db: Session, workflow_id: int, nodes: List[Dict], edges: List[Dict]
    ) -> Optional[Workflow]:
        """Update workflow nodes and edges."""
        db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not db_workflow:
            return None
        db_workflow.nodes = nodes
        db_workflow.edges = edges
        db.commit()
        db.refresh(db_workflow)
        return db_workflow

    def validate_workflow_logic(self, workflow: Workflow) -> str:
        """Validate that workflow has required components."""
        nodes = workflow.nodes or []
        has_llm = any(n.get('type') in ('LLM (OpenAI)', 'LLM', 'llm') for n in nodes)
        if not has_llm:
            raise ValueError("Workflow must include an LLM Engine component.")
        return "Workflow validated successfully. You can now chat with your stack."

    # --- CORE EXECUTION LOGIC (RAG Orchestration) ---
    async def execute_workflow(self, db: Session, workflow_id: int, query: str) -> str:
        """Loads the workflow configuration and executes the node chain using injected services."""
        workflow = self.get_workflow(db, workflow_id)
        if not workflow:
            raise ValueError("Workflow not found")
        
        # Create execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            input_query=query,
            status="running",
        )
        db.add(execution)
        db.commit()
        
        try:
            # 1. Parse nodes and edges 
            nodes: List[Dict[str, Any]] = workflow.nodes or []
            edges: List[Dict[str, Any]] = workflow.edges or []
            
            # Find LLM Node (support both React Flow types and display names)
            llm_node = next((node for node in nodes if node.get('type') in ('LLM (OpenAI)', 'LLM', 'llm')), None)

            if not llm_node:
                raise ValueError("Workflow must include an LLM Engine component.")

            # Support both data.config and flat data keys (React Flow uses flat data)
            node_data = llm_node.get('data', {})
            llm_config = node_data.get('config', {}) or node_data
            context = ""
            
            # 2. Execute KnowledgeBase (RAG Retrieval)
            knowledge_base_node = next((node for node in nodes if node.get('type') in ('KnowledgeBase', 'knowledgeBase')), None)
            
            # Check connection: KB -> LLM context target handle
            kb_to_llm_context_edge = next((
                e for e in edges 
                if (knowledge_base_node and e.get('source') == knowledge_base_node.get('id') and 
                    e.get('target') == llm_node.get('id') and 
                    (e.get('targetHandle') or e.get('target_handle')) == 'context')
            ), None)

            if knowledge_base_node and kb_to_llm_context_edge:
                stack_id = workflow.stack_id 
                context = await self.document_service.retrieve_context(
                    query=query, 
                    stack_id=stack_id, 
                    n_results=5 
                )
            
            # 3. Read LLM configuration from the node
            model = llm_config.get('model') or llm_config.get('Model', 'gpt-4o-mini')
            
            temperature = llm_config.get('temperature') or llm_config.get('Temperature', 0.7)
            try:
                temperature = float(temperature)
            except (TypeError, ValueError):
                temperature = 0.7

            max_tokens = llm_config.get('max_tokens') or llm_config.get('Max tokens') or llm_config.get('maxTokens', 1000)
            try:
                max_tokens = int(max_tokens)
            except (TypeError, ValueError):
                max_tokens = 1000

            custom_prompt = llm_config.get('prompt') or llm_config.get('Prompt')
            
            # KEY: Read the web search toggle from the node config
            # Default is False — only use PDF. User must explicitly enable web search.
            use_web_search = llm_config.get('webSearchEnabled', False)
            if isinstance(use_web_search, str):
                use_web_search = use_web_search.lower() in ('true', '1', 'yes')

            # 4. Call the LLM Service (OpenAI GPT) with proper config
            response = await self.llm_service.generate_workflow_response(
                query=query,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                context=context,
                custom_prompt=custom_prompt,
                use_web_search=use_web_search
            )
            
            # 5. Finalize execution record
            execution.output_response = response
            execution.status = "completed"
            db.commit()
            
            return response
            
        except Exception as e:
            db.rollback() 
            execution.status = "failed"
            execution.error_message = str(e)
            db.commit()
            raise e