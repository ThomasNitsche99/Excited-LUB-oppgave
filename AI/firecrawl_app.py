"""
    Sheet for initializing the Firecrawl App.
"""
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import Any, Optional, List

from dotenv import load_dotenv
import os 
import pprint

# Load variables from .env into environment
load_dotenv()
api_key = os.getenv("FIRECRAWL_API_KEY")

# Initialize the Firecrawl app
app = FirecrawlApp(api_key=api_key)

class NestedModel1(BaseModel):
    kunnskaper: list[str]
    ferdigheter: list[str]
    generell_kompetanse: list[str]

class ExtractSchema(BaseModel):
    læringsutbyttebeskrivelser: NestedModel1

# data = app.extract([
#   "https://uio.no/studier/program/informatikk-ledelse/hva-lerer-du/"
# ], {
#     'prompt': 'Extract all descriptions under "kunnskaper", "ferdigheter", and "generell kompetanse" from the "læringsutbyttebeskrivelser" ("Hva lærer du") section. Make sure to retrieve the descriptions listed in bold font as well. ',
#     'schema': ExtractSchema.model_json_schema(),
# })

# pprint.pprint(data)

