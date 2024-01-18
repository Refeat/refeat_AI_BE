from pydantic import BaseModel
from typing import List, Optional



class AiChatModel(BaseModel):
    project_id : int
    document_id : List[str] = []
    history : List[List[str]] = []
    query: str
    
    
class UploadDocumentDto(BaseModel):
    project_id : int
    document_id : str
    path : str
    file_type : str
     
      
        