import requests
from bs4 import BeautifulSoup

# List of specific program URLs
program_urls = {
    "informatikk_ledelse": "https://www.uio.no/studier/program/informatikk-ledelse-master/hva-lerer-du/",
    "inf_design": "https://www.uio.no/studier/program/inf-design/hva-lerer-du/",
    "informatikk_programmering": "https://www.uio.no/studier/program/informatikk-programmering/hva-lerer-du/"
}

# Function to scrape the learning outcomes from each page
def scrape_program_page(program_name, url):
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
        with open(f'{program_name}_learning_outcomes.txt', 'w', encoding='utf-8') as file:
            if kunnskaper:
                
                file.write("Content under 'Kunnskaper':\n")
                
                for item in kunnskaper:
                    file.write(f"{item}\n")
                
                file.write(f"---")
                file.write(f"\n\n")    
                                
            if ferdigheter:
                
                file.write("Content under 'Ferdigheter':\n")
                
                for item in ferdigheter:
                    file.write(f"{item}\n")
                    
                file.write(f"---")
                file.write(f"\n\n") 
                   
            if generell_kompetanse:
                
                file.write("Content under 'Generell kompetanse':\n")
                
                for item in generell_kompetanse:
                    file.write(f"{item}\n")
                    
                file.write(f"---")
                file.write(f"\n\n")    

        print(f"Scraping complete for {program_name}. File saved as '{program_name}_learning_outcomes.txt'.")
    else:
        print(f"Failed to retrieve page for {program_name}. Status code: {response.status_code}")


if __name__ == "__main__": 
    
    # Loop through all program URLs and scrape each one
    for name, url in program_urls.items():
        scrape_program_page(name, url)

    print("All scraping complete")

