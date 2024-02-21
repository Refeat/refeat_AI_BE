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
    lang: str
     
      
class DeleteDocument(BaseModel):
    project_id : int
    document_id : str
    

class AddColumn(BaseModel):
    title: str
    
    
class GetColumn(BaseModel):
    title: str
    is_general: bool
    document_id: str