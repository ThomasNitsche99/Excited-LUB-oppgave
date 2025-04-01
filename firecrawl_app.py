"""
    Sheet for initializing the Firecrawl App.
"""
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from dotenv import load_dotenv
import os 

# Load variables from .env into environment
load_dotenv()

#Set API key
api_key = os.getenv("FIRECRAWL_API_KEY")

# Initialize the Firecrawl app
app = FirecrawlApp(api_key=api_key)

# Model/Schema for the extracted data
class NestedModel(BaseModel):
    kunnskaper: list[str]
    ferdigheter: list[str]
    generell_kompetanse: list[str]

class ExtractSchema(BaseModel):
    læringsutbyttebeskrivelser: NestedModel

