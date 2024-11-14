import requests
from bs4 import BeautifulSoup

# Study programs to scrape. Add to this list in order to scrape more programs, following the same format. 
study_programs = {
    "dat-bachelorstudium-i-ingeniorfag-data": "https://www.hiof.no/studier/programmer/dat-bachelorstudium-i-ingeniorfag-data/hva-lerer-du/",
    "avf-bachelorstudium-i-arbeids-og-velferdsfag": "https://www.hiof.no/studier/programmer/avf-bachelorstudium-i-arbeids-og-velferdsfag/hva-lerer-du/"
}

university = "HIOF"

# Function to extract learning outcomes
def extract_learning_outcomes(study_program: dict):
    for key, value in study_program.items():
        program = key
        url = value
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Look for headings that likely contain the "learning outcomes" section
            possible_sections = ["Studiets læringsutbytte", "Hva lærer du?"]
            
            # Attempt to find the content based on possible section headings
            content_section = None
            for heading_text in possible_sections:
                heading = soup.find(lambda tag: tag.name == "h2" and heading_text in tag.text)
                if heading:
                    # Gather all content until the next heading (like h2 or h3)
                    content_section = []
                    for sibling in heading.find_next_siblings():
                        if sibling.name in ["h2", "h3"]:
                            break
                        content_section.append(sibling.get_text(separator="\n", strip=True))
                        content_section.append("\n")
                    # Join the content for easier saving to file
                    content_section = "\n".join(content_section)
                    break
                    
            if content_section:
                # Saving to a text file
                file_name = f"{university}_{program}_LearningOutcomes.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(content_section)
                    
                
                    
                print(f"Learning outcomes extracted and saved to '{file_name}'.")
            else:
                print("Could not find the learning outcomes section on the page. Please check if the structure has changed.")
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")

# Run the extraction
if __name__ == "__main__":
    print("Starting the HIOf learning outcomes scraping process...")
    extract_learning_outcomes(study_program=study_programs)
    print("Scraping complete. Check the text files for each study program.")
