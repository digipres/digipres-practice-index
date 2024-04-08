from typing import List, Optional, Set
from pydantic import BaseModel
from datetime import datetime

# Pydantic data model for simple conference output records:
class Publication(BaseModel):
    source_name: str
    landing_page_url: Optional[str] = None
    document_url: Optional[str] = None
    slides_url: Optional[str] = None
    notes_url: Optional[str] = None
    year: int
    title: str
    abstract: Optional[str] = None
    language: str
    creators: Optional[List[str]] = None
    institutions: List[str]
    license: Optional[str] = None
    size: Optional[int]
    type: str = 'paper'
    date: Optional[datetime] = None
    keywords: List[str] = []
