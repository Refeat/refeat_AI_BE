from pydantic import BaseModel
from typing import List, Optional



class AiChatModel(BaseModel):
    project_id : int
    query: str
    
    
class UploadDocumentDto(BaseModel):
    project_id : int
    document_id : str
    path : str
    file_type : str
     
      
class DeleteDocument(BaseModel):
    project_id : int
    document_id : str