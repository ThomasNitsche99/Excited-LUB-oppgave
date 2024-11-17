import requests
from bs4 import BeautifulSoup

# Study programs to scrape. Add to this list in order to scrape more programs, following the same format. 
study_programs = {
    "Informatikk-digital-økonomi-og-ledelse-(bachelor)":"https://www.uio.no/studier/program/informatikk-ledelse/hva-lerer-du/",
    "Informatikk-digital-økonomi-og-ledelse-(master)": "https://www.uio.no/studier/program/informatikk-ledelse-master/hva-lerer-du/",
    "Informatikk-design-bruk-interaksjon-(bachelor)": "https://www.uio.no/studier/program/inf-design/hva-lerer-du/",
    "Informatikk-programmering-og-systemarkitektur-(bachelor)": "https://www.uio.no/studier/program/informatikk-programmering/hva-lerer-du/"
}

university = "UIO"

# Function to scrape the learning outcomes from each page
def scrape_program_page(study_programs: dict):
    
    for key, value in study_programs.items():
        program = key
        url = value
        # Send the request to the program page
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Function to extract sections (Kunnskaper, Ferdigheter, Generell kompetanse)
            def extract_section(heading):
                """
                Extracts text from <p> tags and <li> items following the specified <h2> heading
                until the next <h2> is found.

                Args:
                heading (str): The text content of the <h2> heading to start extraction.
                soup (BeautifulSoup): The BeautifulSoup object containing the HTML.

                Returns:
                list: A list of strings with the extracted content.
                """
                section_heading = soup.find('h2', string=heading)
                content = []

                if section_heading:
                    # Iterate through siblings until the next <h2> is found
                    for sibling in section_heading.find_next_siblings():
                        # Stop if the next <h2> is reached
                        if sibling.name == 'h2':
                            break
                        # Add text from <p> tags
                        if sibling.name == 'p':
                            content.append(sibling.get_text(strip=True))
                        # Add text from <li> items within <ul> tags
                        elif sibling.name == 'ul':
                            content.extend([li.get_text(strip=True) for li in sibling.find_all('li')])

                return content

            # Extract the sections
            ferdigheter = extract_section("Ferdigheter")
            kunnskaper = extract_section("Kunnskaper")
            generell_kompetanse = extract_section("Generell kompetanse")

            # Create a single text file for each study program
            file_name = f"{university}_{program}_LearningOutcomes.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                if kunnskaper:
                    file.write("Kunnskaper:\n")
                    for item in kunnskaper:
                        file.write(f"{item}\n")
                    file.write(f"\n\n")    
                    
                if ferdigheter:
                    file.write("Ferdigheter:\n")
                    for item in ferdigheter:
                        file.write(f"{item}\n")
                    file.write(f"\n\n") 
                    
                if generell_kompetanse:
                    file.write("Generell kompetanse:\n")
                    for item in generell_kompetanse:
                        file.write(f"{item}\n")
                    file.write(f"\n\n")    

            print(f"Scraping complete for {program}. File saved as {file_name}.")
        else:
            print(f"Failed to retrieve page for {program}. Status code: {response.status_code}")


if __name__ == "__main__": 
    
    print("Starting the UIO learning outcomes scraping process...")
    scrape_program_page(study_programs=study_programs)
    print("Scraping complete. Check the text files for each study program.")