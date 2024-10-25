

# For the study programs: 

# Bachelor i informasjonsteknologi – Frontend- og mobilutvikling
# Bachelor i informasjonsteknologi – Interaktivt design
# Bachelor i informasjonsteknologi – Kunstig intelligens
# Bachelor i informasjonsteknologi – Programmering
# Bachelor i informasjonsteknologi – Spillteknologi

import requests
import pdfplumber
from io import BytesIO
import re

# Dictionary of study programs and their PDF URLs
study_programs = {
    "Bachelor i informasjonsteknologi - Frontend- og mobilutvikling": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2024/seit/bachelor-i-informasjonsteknologi-frontend-og-mobilutvikling-kull-2024.pdf",
    "Bachelor i informasjonsteknologi - Interaktivt design": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2024/seit/bachelor-i-informasjonsteknologi---interaktivt-design-kull-2024.pdf",
    "Bachelor i informasjonsteknologi - Kunstig intelligens": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2023/seit/bachelor-i-informasjonsteknologi---kunstig-intelligens-2023.pdf", 
    "Bachelor i informasjonsteknologi - Programmering": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2024/seit/bachelor-i-informasjonsteknologi---programmering-kull-2024.pdf",
    "Bachelor i informasjonsteknologi - Spillteknologi": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2022/norsk/bachelor-i-informasjonsteknologi---spillteknologi-kull-2022.pdf" 
}

def extract_learning_outcomes_from_pdf(pdf_url):
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            sections = {
                "Kunnskap": "",
                "Ferdigheter": "",
                "Generell kompetanse": ""
            }
            current_section = None
            collecting_text = False
            
            for page in pdf.pages:
                text = page.extract_text() or ""
                
                # Search for the "Læringsutbytte" section
                if "læringsutbytte" in text.lower():
                    collecting_text = True

                # If we are collecting text, check for sections
                if collecting_text:
                    if "studiets struktur" in text.lower():
                        collecting_text = False  # Stop collecting if we hit this section

                    # Process each line of the current page
                    for line in text.splitlines():
                        line = line.strip()
                        # Check for section headers
                        if line.lower().startswith("kunnskap"):
                            current_section = "Kunnskap"
                            sections[current_section] += line + "\n"  # Include the header
                        elif line.lower().startswith("ferdigheter"):
                            current_section = "Ferdigheter"
                            sections[current_section] += line + "\n"  # Include the header
                        elif line.lower().startswith("generell kompetanse"):
                            current_section = "Generell kompetanse"
                            sections[current_section] += line + "\n"  # Include the header
                        elif current_section and line.startswith("•"):  # Bullet points
                            sections[current_section] += line + "\n"
                        elif current_section and line.startswith("kandidaten"):  # Candidate statements
                            sections[current_section] += line + "\n"

            # Save the extracted information to a text file
            file_name = pdf_url.split("/")[-1].replace(".pdf", ".txt")
            with open(file_name, 'w', encoding='utf-8') as file:
                for section_name, content in sections.items():
                    if content.strip():  # Ensure there's content to write
                        file.write(f"{section_name}:\n{content}\n")

            print(f"Extraction complete for {file_name}. Check '{file_name}' for the results.")
    else:
        print(f"Failed to retrieve PDF for {pdf_url}. Status code: {response.status_code}")

# Loop through all study programs and extract information from each PDF
for program_name, pdf_url in study_programs.items():
    extract_learning_outcomes_from_pdf(pdf_url)

print("All extraction complete. Check the text files for each study program.")
