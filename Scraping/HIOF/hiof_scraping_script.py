import requests
from bs4 import BeautifulSoup
import os
import re

# Study programs to scrape learning outcomes
study_programs = {
    "Bachelor i ingeniørfag - data, dataingeniør": "https://www.hiof.no/studier/programmer/dat-bachelorstudium-i-ingeniorfag-data/hva-lerer-du/",
    "Bachelorstudium i arbeids- og velferdsfag": "https://www.hiof.no/studier/programmer/avf-bachelorstudium-i-arbeids-og-velferdsfag/hva-lerer-du/"
}

# Study programs to scrape mandatory subjects
Study_programs_Mandatory_subjects = {
    "Bachelor i ingeniørfag - data, dataingeniør": "https://www.hiof.no/studier/programmer/dat-bachelorstudium-i-ingeniorfag-data/oppbygging/",
    "Bachelorstudium i arbeids- og velferdsfag": "https://www.hiof.no/studier/programmer/avf-bachelorstudium-i-arbeids-og-velferdsfag/oppbygging/"
}

university = "HIOF"

# Define the output directory (ensuring it exists)
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output")
os.makedirs(output_dir, exist_ok=True)

def extract_learning_outcomes(study_program: dict):
    """
    Extracts the learning outcomes from each study program page and saves them into a combined text file.
    """
    for program_name, url in study_program.items():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Look for headings that likely contain the "learning outcomes" section
            possible_sections = ["Studiets læringsutbytte", "Hva lærer du?"]
            content_section = None
            
            for heading_text in possible_sections:
                heading = soup.find(lambda tag: tag.name == "h2" and heading_text in tag.text)
                if heading:
                    # Gather all content until the next heading (like h2 or h3)
                    section_text = []
                    for sibling in heading.find_next_siblings():
                        if sibling.name in ["h2", "h3"]:
                            break
                        section_text.append(sibling.get_text(separator="\n", strip=True))
                        section_text.append("\n")
                    content_section = "\n".join(section_text)
                    break
            
            if content_section:
                # Use the same file name for combined output
                file_name = f"{university}_{program_name}.txt"
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("Learning Outcomes\n")
                    file.write(content_section.strip())
                print(f"Learning outcomes extracted and saved to '{file_name}'.")
            else:
                print(f"Could not find the learning outcomes section on the page for '{program_name}'.")
        else:
            print(f"Failed to retrieve page for '{program_name}'. Status code: {response.status_code}")

def extract_mandatory_subjects(study_programs: dict):
    """
    Extracts the mandatory subjects from the 'oppbygging' pages and appends them to the same text file
    used for learning outcomes.
    """
    for program_name, url in study_programs.items():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find all headers containing "Obligatoriske emner"
            headers = soup.find_all(
                lambda tag: tag.name in ["h2", "h3", "h4", "h5"] 
                and "Obligatoriske emner" in tag.get_text()
            )
            if not headers:
                print(f"Mandatory subjects section not found for '{program_name}'.")
                continue
            
            course_lines = []
            
            # Process each "Obligatoriske emner" header block
            for header in headers:
                block_lines = []
                for sibling in header.find_next_siblings():
                    if sibling.name and sibling.name.startswith('h'):
                        break
                    if "sist hentet" in sibling.get_text(strip=True).lower():
                        break
                    block_lines.append(sibling.get_text(separator="\n", strip=True))
                
                block_text = "\n".join(block_lines).strip()
                block_courses = block_text.split("stp")
                for course_block in block_courses:
                    course_block = course_block.strip()
                    if course_block:
                        fields = course_block.splitlines()
                        line = "\t".join(fields)
                        course_lines.append(line)
            
            final_courses = "\n".join(course_lines)
            final_courses = re.sub(r"\s*stp", "sp", final_courses)
            
            if final_courses.strip():
                final_output = "\n\nObligatoriske emner\n" + final_courses.strip()
            else:
                final_output = "\n\nObligatoriske emner\n(Ingen obligatoriske emner funnet)"
            
            # Append mandatory subjects to the same file used for learning outcomes
            file_name = f"{university}_{program_name}.txt"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(final_output)
            print(f"Mandatory subjects appended to '{file_name}'.")
        else:
            print(f"Failed to retrieve page for '{program_name}'. Status code: {response.status_code}")

if __name__ == "__main__":
    print("Starting the HIOF scraping process...")
    
    # 1. Extract learning outcomes and create the file
    extract_learning_outcomes(study_program=study_programs)
    
    # 2. Extract mandatory subjects and append them to the same file
    extract_mandatory_subjects(study_programs=Study_programs_Mandatory_subjects)
    
    print("Scraping complete. Check the combined text files in the 'output' folder.")
