import requests
from bs4 import BeautifulSoup

# Study programs to scrape. Add to this list in order to scrape more programs, following the same format. 
study_programs = {
    "Informatikk-Datateknologi-bachelor": "https://www.uib.no/studier/BAMN-DTEK",
    "Kunstig-intelligens-bachelor": "https://www.uib.no/studier/BASV-AIKI"
}

university = "UIB"

# Function to extract learning outcomes
def extract_learning_outcomes(study_programs: dict):
    
    for key, value in study_programs.items():
        program = key
        program_url = value
        try:
            print(f"Fetching page content from {program_url}...")
            response = requests.get(program_url)
            response.raise_for_status()
            print("Page content fetched successfully.")

            # Parsing the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find the "Kva lærer du?" heading
            heading = soup.find(lambda tag: tag.name in ["h2", "h3"] and "Kva lærer du?" in tag.text)
            if heading:
                print("Found 'Kva lærer du?' section. Extracting content...")
                content_section = []
                # Gather all content until the next heading (like h2 or h3)
                for sibling in heading.find_next_siblings():
                    if sibling.name in ["h2", "h3"]:
                        break
                    content_section.append(sibling.get_text(separator="\n", strip=True))

                # Join the content for easier saving to file
                content_text = "\n".join(content_section)

                
                # Save the extracted content to the file
                file_name = f"{university}_{program}_LearningOutcomes.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(content_text)
                    
                print(f"Learning outcomes extracted and saved to '{file_name}'.")
            else:
                print(f"Could not find the 'Kva lærer du?' section on the page: {url}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

# Run the extraction for each URL in the list
if __name__ == "__main__":
    print("Starting the UiB learning outcomes scraping process...")
    extract_learning_outcomes(study_programs)
    print("Scraping complete. Check the generated text files for each study program.")
