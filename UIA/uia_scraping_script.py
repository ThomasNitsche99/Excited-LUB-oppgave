import requests
from bs4 import BeautifulSoup

# URL for the study program at the University of Agder
url = "https://www.uia.no/studier/program/data-ingeniorutdanning-bachelor/studieplaner/2024h.html#toc9"

# Function to scrape the study course page
def scrape_uia_program_page(url):
    # Send the request to the program page
    response = requests.get(url)
    
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
        with open('uia_dataingenior_learning_outcomes.txt', 'w', encoding='utf-8') as file:
            if kunnskaper:
                file.write("Kunnskaper:\n" + kunnskaper + "\n\n")
            if ferdigheter:
                file.write("Ferdigheter:\n" + ferdigheter + "\n\n")
            if generell_kompetanse:
                file.write("Generell kompetanse:\n" + generell_kompetanse + "\n\n")

        print("Scraping complete. File saved as 'uia_dataingenior_learning_outcomes.txt'.")
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

# Run the scraper
scrape_uia_program_page(url)

print("Scraping complete. Check the text file for the study program.")
