import json
from typing import List, Optional, Set
from pydantic import BaseModel
from awindex.models import IndexRecord
from datetime import datetime
from slugify import slugify

def generate_pub_path(pub):
     slug = slugify(pub.title, max_length=64)
     path = f"ipres-{pub.year}/papers/{slug}"
     return path

# Pydantic data model for simple conference output records:
class Publication(BaseModel):
    source_name: str
    landing_page_url: Optional[str] = None
    document_url: Optional[str] = None
    slides_url: Optional[str] = None
    notes_url: Optional[str] = None
    stream_url: Optional[str] = None
    submission_url: Optional[str] = None # To store the URL to the original submission document (rarely available)
    year: int
    title: str
    abstract: Optional[str] = None
    language: str
    creators: Optional[List[str]] = None
    institutions: List[str]
    license: Optional[str] = None # Using the US spelling of license as that's common in our sources (e.g. CC license usage).
    size: Optional[int]
    type: str = 'paper'
    date: Optional[datetime] = None
    keywords: List[str] = []

    # Helper to generate the result in Awesome Indexes form:
    def to_index_record(self) -> IndexRecord:
        # Construct:
        ir = IndexRecord(
            source=self.source_name,
            source_url="https://www.digipres.org/publications/",
            url=f"https://www.digipres.org/publications/ipres/{generate_pub_path(self)}/",
            title=self.title,
            creators=self.creators,
            abstract=self.abstract,
            date=self.date,
            language="en",
            type=self.type,
            categories=None, 
            license=self.license,
            metadata={
                'citation_conference_title': f'iPRES {self.year}',
            },
            links={}
        )
        # Optional data:
        if self.keywords and len(self.keywords) > 0:
            ir.keywords = self.keywords
        if self.institutions and len(self.institutions) > 0:
            ir.metadata['institutions'] = json.dumps(self.institutions)
        # Links
        if self.landing_page_url:
            ir.links['citation_public_url'] = self.landing_page_url
        if self.document_url:
            ir.links['citation_pdf_url'] = self.document_url
        if self.slides_url:
            ir.links['citation_conference_slides_url'] = self.slides_url
        if self.notes_url:
            ir.links['citation_conference_notes_url'] = self.notes_url
        if self.stream_url:
            ir.links['citation_conference_recording_url'] = self.stream_url
        if self.submission_url:
            ir.links['citation_conference_submission_url'] = self.submission_url

        return ir