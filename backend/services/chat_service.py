from sqlalchemy.orm import Session
from typing import List, Optional, TYPE_CHECKING
import uuid

# Import models and schemas
from models import Conversation, ChatMessage
from schemas import ChatMessageCreate

# --- MODIFICATION START ---
# Only import for type checking purposes to break the circular dependency
if TYPE_CHECKING:
    from .workflow_service import WorkflowService 
# ---------------------------


class ChatService:
    # Use string literal for type hint
    def __init__(self, workflow_service: 'WorkflowService'):
        """
        Initializes ChatService, primarily injecting the WorkflowService 
        to execute the AI logic.
        """
        self.workflow_service = workflow_service

    # --- CRUD Methods (using model_dump for modern Pydantic) ---

    def create_conversation(self, db: Session, workflow_id: int, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(
            workflow_id=workflow_id,
            title=title or f"Conversation {uuid.uuid4().hex[:8]}"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def get_conversation(self, db: Session, conversation_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def create_message(self, db: Session, message: ChatMessageCreate) -> ChatMessage:
        # Fixed: Using model_dump() for modern Pydantic usage
        db_message = ChatMessage(**message.model_dump()) 
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    def get_messages(self, db: Session, conversation_id: int) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(
            ChatMessage.conversation_id == conversation_id
        ).order_by(ChatMessage.created_at).all()

    # --- CORE EXECUTION METHOD ---

    async def send_message(self, db: Session, conversation_id: int, message: str) -> str:
        """
        Logs the user message, executes the associated workflow, and logs the response.
        """
        conversation = self.get_conversation(db, conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        # 1. Create and log the user message
        user_message_data = {
            "conversation_id": conversation_id,
            "role": "user",
            "content": message
        }
        self.create_message(db, ChatMessageCreate(**user_message_data))
        
        try:
            # 2. Execute the workflow associated with this conversation
            workflow_id = conversation.workflow_id
            
            # --- EXECUTION: Call the injected WorkflowService ---
            ai_response = await self.workflow_service.execute_workflow(
                db=db, 
                workflow_id=workflow_id, 
                query=message
            )
            # ---------------------------------------------------
            
        except Exception as e:
            ai_response = f"Error: The workflow failed to execute. Details: {str(e)}"
            print(f"Chat execution failed for conversation {conversation_id}: {e}")


        # 3. Create and log the AI message
        ai_message_data = {
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": ai_response
        }
        self.create_message(db, ChatMessageCreate(**ai_message_data))
        
        return ai_response