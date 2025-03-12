import requests
import pdfplumber
from io import BytesIO

# Dictionary of study programs and their PDF URLs
study_programs = {
    "Bachelor-i-informasjonsteknologi - Frontend-og-mobilutvikling": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2025/seit/bachelor-i-informasjonsteknologi---frontend--og-mobilutvikling_kull-2025.pdf",
    "Bachelor-i-informasjonsteknologi - Interaktivt-design": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2024/seit/bachelor-i-informasjonsteknologi---interaktivt-design-kull-2024.pdf",
    "Bachelor-i-informasjonsteknologi - Kunstig-intelligens": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2023/seit/bachelor-i-informasjonsteknologi---kunstig-intelligens-2023.pdf", 
    "Bachelor-i-informasjonsteknologi - Programmering": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2024/seit/bachelor-i-informasjonsteknologi---programmering-kull-2024.pdf",
    "Bachelor-i-informasjonsteknologi - Spillteknologi": "https://www.kristiania.no/globalassets/programbeskrivelser/hoyskole/2022/norsk/bachelor-i-informasjonsteknologi---spillteknologi-kull-2022.pdf" 
}

university = "Kristiania"

def extract_info_from_pdf(pdf_url, program_name):
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            sections = {
                "Kunnskap": "",
                "Ferdigheter": "",
                "Generell kompetanse": "",
                "Kandidaten skal kunne": "",
                "Obligatoriske emner": ""
            }
            current_section = None
            collecting_text = False
            collecting_courses = False

            for page_num, page in enumerate(pdf.pages, start=1):
                # Skip the first two pages
                if page_num < 3:
                    continue  

                text = page.extract_text() or ""
                
                # Hente læringsutbytte-seksjoner
                if "læringsutbytte" in text.lower():
                    collecting_text = True

                if collecting_text:
                    if "studiets struktur" in text.lower():
                        collecting_text = False  # Stopper læringsutbytte-seksjonen

                    for line in text.splitlines():
                        line = line.strip()
                        if line.lower().startswith("kunnskap"):
                            current_section = "Kunnskap"
                        elif line.lower().startswith("ferdigheter"):
                            current_section = "Ferdigheter"
                        elif line.lower().startswith("generell kompetanse"):
                            current_section = "Generell kompetanse"
                        elif line.lower().startswith("kandidaten"):
                            current_section = "Kandidaten skal kunne"

                        if current_section and line.startswith("•"):  
                            sections[current_section] += line + "\n"
                        elif current_section and line.startswith("kandidaten"):
                            sections[current_section] += line + "\n"

                # Hente obligatoriske emner
                if "Studiets struktur" in text:
                    collecting_courses = True

                if collecting_courses:
                    for line in text.splitlines():
                        line = line.strip()
                        if line.startswith("Valgemner") or line.startswith("Tabell"):  
                            collecting_courses = False
                            break
                        if line and not any(char.isdigit() for char in line[:2]):  # Fjerne studiepoeng-linjer
                            sections["Obligatoriske emner"] += "- " + line + "\n"

            # Lagre all informasjon i én tekstfil per studieprogram
            file_name = f"{university}_{program_name}_Info.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                for section_name, content in sections.items():
                    if content.strip():
                        file.write(f"{section_name}:\n{content}\n")

            print(f"Extraction complete for {program_name}. Check '{file_name}' for the results.")
    else:
        print(f"Failed to retrieve PDF from {pdf_url}. Status code: {response.status_code}")

# Loop gjennom alle programmer og ekstraher info
for program_name, pdf_url in study_programs.items():
    extract_info_from_pdf(pdf_url, program_name)

print("All extraction complete. Check the text files for each study program.")
