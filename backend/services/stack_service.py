
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Stack
from schemas import StackCreate, StackUpdate

class StackService:
    def create_stack(self, db: Session, stack: StackCreate) -> Stack:
        # Use model_dump() instead of dict()
        db_stack = Stack(**stack.model_dump())
        db.add(db_stack)
        db.commit()
        db.refresh(db_stack)
        return db_stack

    def get_stacks(self, db: Session) -> List[Stack]:
        return db.query(Stack).all()

    def get_stack(self, db: Session, stack_id: int) -> Optional[Stack]:
        return db.query(Stack).filter(Stack.id == stack_id).first()

    def update_stack(self, db: Session, stack_id: int, stack: StackUpdate) -> Optional[Stack]:
        db_stack = db.query(Stack).filter(Stack.id == stack_id).first()
        if not db_stack:
            return None
        
        # Use model_dump(exclude_unset=True)
        update_data = stack.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_stack, field, value)
        
        db.commit()
        db.refresh(db_stack)
        return db_stack

    def delete_stack(self, db: Session, stack_id: int) -> bool:
        db_stack = db.query(Stack).filter(Stack.id == stack_id).first()
        if not db_stack:
            return False
        
        db.delete(db_stack)
        db.commit()
        return True