from pydantic import BaseModel
from typing import List

class DocumentUpload(BaseModel):
    document: str

class SearchQuery(BaseModel):
    query: str
