# # backend/services/document_service.py
# from sqlalchemy.orm import Session
# from typing import List, Optional, Any, TYPE_CHECKING
# from models import Document
# from schemas import DocumentResponse
# from pathlib import Path
# import uuid
# import os
# import aiofiles
# import fitz  # PyMuPDF
# from chromadb import Client, Settings
# from chromadb.utils import embedding_functions

# # Type checking to avoid circular imports during runtime
# if TYPE_CHECKING:
#     from .embedding_service import EmbeddingService 

# class DocumentService:
#     def __init__(self, embedding_service: 'EmbeddingService'):
#         self.embedding_service = embedding_service
#         self.upload_dir = Path("uploads")
#         self.upload_dir.mkdir(exist_ok=True)
        
#         # --- Initialize ChromaDB Client ---
#         self.chroma_client = Client(Settings(persist_directory="./chroma_db_data"))
#         os.makedirs("./chroma_db_data", exist_ok=True)
        
#         # We assume the embedding function will be retrieved/managed by the EmbeddingService, 
#         # but for Chroma initialization, we use a simple default/mock:
#         self.collection = self.chroma_client.get_or_create_collection(
#             name="genai_stack_collection"
#         )


#     # --- Document Upload and Text Extraction ---

#     async def upload_document(self, db: Session, file, stack_id: Optional[int] = None) -> Document:
#         """Uploads, saves, and processes a document for text extraction and embedding."""
#         file_extension = Path(file.filename).suffix
#         unique_filename = f"{uuid.uuid4()}{file_extension}"
#         file_path = self.upload_dir / unique_filename
        
#         # Save file asynchronously
#         content_bytes = await file.read()
#         async with aiofiles.open(file_path, 'wb') as f:
#             await f.write(content_bytes)
        
#         # Extract text content (runs synchronously, consider FastAPI executor for production)
#         text_content = self._extract_text(file_path, file.content_type)
        
#         # Create document record
#         document = Document(
#             stack_id=stack_id,
#             filename=unique_filename,
#             original_filename=file.filename,
#             file_path=str(file_path),
#             file_size=len(content_bytes),
#             file_type=file.content_type,
#             content=text_content,
#             is_processed=False
#         )
        
#         db.add(document)
#         db.commit()
#         db.refresh(document)
        
#         # Trigger background embedding process
#         await self.process_document_in_background(document.id, text_content, stack_id)

#         return document

#     def _extract_text(self, file_path: Path, file_type: str) -> str:
#         """Extract text from supported formats (PDF via PyMuPDF)."""
#         if 'pdf' in file_type.lower() or file_path.suffix.lower() == '.pdf':
#             try:
#                 with fitz.open(file_path) as doc:
#                     text = "".join(page.get_text() for page in doc)
#                 return text
#             except Exception as e:
#                 print(f"Error extracting text with PyMuPDF: {e}")
#                 return ""
#         # Add logic for other file types (docx, txt, etc.)
#         return ""


#     # --- RAG Core Logic ---
    
#     def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
#         """Simple text chunking utility."""
#         chunks = []
#         start = 0
#         while start < len(text):
#             end = start + chunk_size
#             chunk = text[start:end]
#             chunks.append(chunk)
#             start += chunk_size - overlap
#         return chunks


#     async def process_document_in_background(self, document_id: int, text_content: str, stack_id: int):
#         """Generates embeddings and stores them in ChromaDB (simulating background task)."""
#         if not text_content:
#             return

#         chunks = self._chunk_text(text_content)
        
#         # Get embeddings from the dedicated service
#         try:
#             embeddings_list = await self.embedding_service.create_embeddings(chunks, model="text-embedding-3-small")
#         except Exception as e:
#             print(f"Embedding generation failed: {e}")
#             return
            
#         if not embeddings_list:
#             return

#         # Prepare data for ChromaDB
#         self.collection.add(
#             embeddings=embeddings_list,
#             documents=chunks,
#             metadatas=[{"stack_id": stack_id, "doc_id": document_id}] * len(chunks),
#             ids=[f"{document_id}_chunk_{i}" for i in range(len(chunks))]
#         )
#         print(f"Stored {len(chunks)} chunks for document {document_id} in ChromaDB.")
        
#         # NOTE: You would update the DB record here to set is_processed=True


#     def retrieve_context(self, query: str, stack_id: int, n_results: int = 5) -> str:
#         """Retrieves relevant document chunks from ChromaDB based on the query."""
#         if not self.collection:
#             return ""
            
#         # ChromaDB requires the embedding function to be configured when querying
#         # If the collection was created without an EF, we must generate the query embedding manually:
#         try:
#             query_embedding = self.embedding_service.create_embeddings([query], model="text-embedding-3-small")[0]
#         except Exception as e:
#             print(f"Failed to generate query embedding: {e}")
#             return ""

#         results = self.collection.query(
#             query_embeddings=[query_embedding],
#             n_results=n_results,
#             where={"stack_id": stack_id}
#         )
        
#         # Combine snippets into a single context string
#         context = "\n---\n".join(results.get("documents", [[]])[0])
#         return context


#     # --- Utility Methods ---

#     def get_document(self, db: Session, document_id: int) -> Optional[Document]:
#         return db.query(Document).filter(Document.id == document_id).first()

#     def get_documents_by_stack(self, db: Session, stack_id: int) -> List[Document]:
#         return db.query(Document).filter(Document.stack_id == stack_id).all()

#     def delete_document(self, db: Session, document_id: int) -> bool:
#         document = db.query(Document).filter(Document.id == document_id).first()
#         if not document:
#             return False
        
#         # Delete file from filesystem
#         try:
#             os.remove(document.file_path)
#         except FileNotFoundError:
#             pass
        
#         # Delete from ChromaDB (Optional but recommended)
#         self.collection.delete(where={"doc_id": document_id})
        
#         db.delete(document)
#         db.commit()
#         return True

#     def process_document(self, db: Session, document_id: int) -> bool:
#         # This function is now mainly a placeholder; the core logic is in process_document_in_background
#         document = self.get_document(db, document_id)
#         if not document:
#             return False
        
#         document.is_processed = True
#         db.commit()
#         return True
# backend/services/document_service.py
from sqlalchemy.orm import Session
from typing import List, Optional, TYPE_CHECKING
from models import Document # Assuming 'Document' model is defined here
from pathlib import Path
import uuid
import os
import aiofiles
import fitz # PyMuPDF
from chromadb import Client, Settings

# Type checking to avoid circular imports during runtime
if TYPE_CHECKING:
    from .embedding_service import EmbeddingService 

# ChromaDB persistence setup
CHROMA_DIR = "./chroma_db_data"

class DocumentService:
    def __init__(self, embedding_service: 'EmbeddingService'):
        self.embedding_service = embedding_service
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        
        # --- Initialize ChromaDB Client (Persistent) ---
        self.chroma_client = Client(Settings(persist_directory=CHROMA_DIR))
        os.makedirs(CHROMA_DIR, exist_ok=True)
        
        # Create or get the collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="genai_stack_collection"
        )

    # --- RAG Core Logic Utilities ---
    
    def _extract_text(self, file_path: Path, file_type: str) -> str:
        """Extract text from supported formats (PDF via PyMuPDF)."""
        if 'pdf' in file_type.lower() or file_path.suffix.lower() == '.pdf':
            try:
                with fitz.open(file_path) as doc:
                    text = "".join(page.get_text() for page in doc)
                return text
            except Exception as e:
                print(f"Error extracting text with PyMuPDF: {e}")
                return ""
        return ""

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Simple text chunking utility."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks


    async def _process_and_store_embeddings(self, db: Session, document_id: int, text_content: str, stack_id: int):
        """Generates embeddings and stores them in ChromaDB, then updates DB."""
        if not text_content:
            print(f"Skipping embeddings for document {document_id}: No text content.")
            return

        chunks = self._chunk_text(text_content)
        
        try:
            # CRITICAL: AWAIT the embedding service call
            embeddings_list = await self.embedding_service.create_embeddings(chunks, model="text-embedding-3-small")
        except Exception as e:
            print(f"Embedding API call failed for doc {document_id}: {e}")
            return
            
        if not embeddings_list:
            print(f"Embedding list was empty for document {document_id}.")
            return

        # Store in ChromaDB
        self.collection.add(
            embeddings=embeddings_list,
            documents=chunks,
            metadatas=[{"stack_id": stack_id, "doc_id": document_id}] * len(chunks),
            ids=[f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        )
        
        # CRITICAL FIX: Update the DB record after successful ChromaDB storage
        db.query(Document).filter(Document.id == document_id).update({"is_processed": True})
        db.commit()
        print(f"Stored {len(chunks)} chunks for document {document_id} in ChromaDB.")


    # --- Document Upload and Processing (RAG Storage) ---

    async def upload_document(self, db: Session, file, stack_id: Optional[int] = None) -> Document:
        """Uploads, saves, and processes a document for text extraction and embedding."""
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.upload_dir / unique_filename
        
        # 1. Save file asynchronously
        content_bytes = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content_bytes)
        
        # 2. Extract text content
        text_content = self._extract_text(file_path, file.content_type)
        
        # 3. Create initial DB record
        document = Document(
            stack_id=stack_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=len(content_bytes),
            file_type=file.content_type,
            content=text_content,
            is_processed=False # Will be set to True after embedding
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # 4. Process embeddings and store in ChromaDB (synchronously within the request for assignment simplicity)
        await self._process_and_store_embeddings(db, document.id, text_content, stack_id)

        return document

    
    # --- Context Retrieval (RAG Search) ---
    
    async def retrieve_context(self, query: str, stack_id: int, n_results: int = 5) -> str:
        """Retrieves relevant document chunks from ChromaDB based on the query."""
        if not self.collection:
            return ""
            
        # CRITICAL FIX: AWAIT the asynchronous call to the embedding service
        try:
            query_embedding_list = await self.embedding_service.create_embeddings([query], model="text-embedding-3-small")
        except Exception as e:
            print(f"Failed to generate query embedding for retrieval: {e}")
            return ""

        if not query_embedding_list:
            return ""

        # Search ChromaDB using the first (and only) generated query embedding
        results = self.collection.query(
            query_embeddings=query_embedding_list[0], 
            n_results=n_results,
            where={"stack_id": stack_id}
        )
        
        # Combine snippets into a single context string
        if results.get("documents") and results["documents"][0]:
            context = "\n---\n".join(results["documents"][0])
            return context
        
        return ""

    # --- Utility Methods ---
    
    # ... (other utility methods like get_document, delete_document remain the same) ...

    def get_document(self, db: Session, document_id: int) -> Optional[Document]:
        return db.query(Document).filter(Document.id == document_id).first()

    def get_documents_by_stack(self, db: Session, stack_id: int) -> List[Document]:
        return db.query(Document).filter(Document.stack_id == stack_id).all()

    def delete_document(self, db: Session, document_id: int) -> bool:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return False
        
        # Delete file from filesystem and ChromaDB
        try:
            os.remove(document.file_path)
            self.collection.delete(where={"doc_id": document_id})
        except Exception as e:
             print(f"Error deleting resources for doc {document_id}: {e}")
            
        db.delete(document)
        db.commit()
        return True