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
            section_heading = soup.find('h2', string=heading)
            if section_heading:
                content = section_heading.find_next('ul')
                if content:
                    return '\n'.join([li.get_text(strip=True) for li in content.find_all('li')])
            return None

        # Extract the sections
        ferdigheter = extract_section("Ferdigheter")
        kunnskaper = extract_section("Kunnskaper")
        generell_kompetanse = extract_section("Generell kompetanse")

        # Create a single text file for each study program
        with open(f'{program_name}_learning_outcomes.txt', 'w', encoding='utf-8') as file:
            if kunnskaper:
                file.write("Kunnskaper:\n" + kunnskaper + "\n\n")
            if ferdigheter:
                file.write("Ferdigheter:\n" + ferdigheter + "\n\n")
            if generell_kompetanse:
                file.write("Generell kompetanse:\n" + generell_kompetanse + "\n\n")

        print(f"Scraping complete for {program_name}. File saved as '{program_name}_learning_outcomes.txt'.")
    else:
        print(f"Failed to retrieve page for {program_name}. Status code: {response.status_code}")

# Loop through all program URLs and scrape each one
for name, url in program_urls.items():
    scrape_program_page(name, url)

print("All scraping complete. Check the text files for each study program.")

