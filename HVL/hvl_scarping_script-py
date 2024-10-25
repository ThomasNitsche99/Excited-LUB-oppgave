import requests
from bs4 import BeautifulSoup

# URLs for the study programs at HVL
program_page_hvl_url = {
    "Bachelor i informasjonsteknologi": "https://www.hvl.no/studier/studieprogram/informasjonsteknologi-bergen/2024h/studieplan/",
    "Bachelor i ingeniørfag, data": "https://www.hvl.no/studier/studieprogram/dataingenior/2024h/studieplan/"
}

# Function to scrape the study course page
def scrape_hvl_program_page(program_name, url):
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Function to extract sections (Kunnskap, Ferdigheiter, Generell kompetanse)
        def extract_section(heading):
            # Find the <p> element with the <i> tag that contains the heading
            section_heading = soup.find('i', string=heading)
            if section_heading:
                # Find the next <ul> that contains the list items
                content = section_heading.find_parent('p').find_next('ul')
                if content:
                    return '\n'.join([li.get_text(strip=True) for li in content.find_all('li')])
            return None

        # Extract the sections
        ferdigheter = extract_section("Ferdigheiter:")
        kunnskaper = extract_section("Kunnskap:")
        generell_kompetanse = extract_section("Generell kompetanse:")

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
for name, url in program_page_hvl_url.items():
    scrape_hvl_program_page(name, url)

print("All scraping complete. Check the text files for each study program.")
