import requests
from bs4 import BeautifulSoup

# Study programs to scrape. Add to this list in order to scrape more programs, following the same format. 
study_programs = {
    "data-ingeniorutdanning-bachelor": "https://www.uia.no/studier/program/data-ingeniorutdanning-bachelor/studieplaner/2024h.html#toc9",
}

university = "UIA"


# Function to scrape the study course page
def scrape_uia_program_page(study_program: dict):
    
    for key, value in study_program.items():
        program = key
        program_url = value
        # Send the request to the program page
        response = requests.get(program_url)
        
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Function to extract sections normally
            def extract_section(heading_text):
                heading = soup.find(lambda tag: tag.name in ['p', 'span'] and heading_text in tag.get_text())
                if heading:
                    ul_tag = heading.find_next('ul')
                    if ul_tag:
                        return '\n'.join([li.get_text(strip=True) for li in ul_tag.find_all('li')])
                return None
            
            # Special function for "Generell kompetanse" to stop at <h2>
            def extract_generell_kompetanse(heading_text):
                heading = soup.find(lambda tag: tag.name in ['p', 'span'] and heading_text in tag.get_text())
                if heading:
                    ul_tags = []
                    next_sibling = heading.find_next_sibling()
                    
                    # Loop to capture <ul> tags until we encounter a new <h2>
                    while next_sibling and next_sibling.name != 'h2':
                        if next_sibling.name == 'ul':
                            ul_tags.append(next_sibling)
                        next_sibling = next_sibling.find_next_sibling()
                    
                    # Extract all text from <li> elements in the collected <ul> lists
                    return '\n'.join([li.get_text(strip=True) for ul in ul_tags for li in ul.find_all('li')])
                return None

            # Extract the sections
            ferdigheter = extract_section("Ferdigheter")
            kunnskaper = extract_section("Kunnskap")
            generell_kompetanse = extract_generell_kompetanse("Generell kompetanse")  # Stopping at <h2> for this section

            # Create a single text file for the program
            file_name = f"{university}_{program}_LearningOutcomes.txt"

            with open(file_name, 'w', encoding='utf-8') as file:
                if kunnskaper:
                    file.write("Kunnskaper:\n" + kunnskaper + "\n\n")
                if ferdigheter:
                    file.write("Ferdigheter:\n" + ferdigheter + "\n\n")
                if generell_kompetanse:
                    file.write("Generell kompetanse:\n" + generell_kompetanse + "\n\n")

            print(f"Scraping complete. File saved as {file_name}.")
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")


# Run the extraction
if __name__ == "__main__":
    print("Starting the UIA learning outcomes scraping process...")
    scrape_uia_program_page(study_program=study_programs)
    print("Scraping complete. Check the text files for each study program.")
