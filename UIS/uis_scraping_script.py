import requests
from bs4 import BeautifulSoup

# URL of the UiS page to scrape
url = "https://www.uis.no/nb/studier/datateknologi-bachelor#/"

# Function to extract learning outcomes
def extract_learning_outcomes(url):
    try:
        print(f"Fetching page content from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        print("Page content fetched successfully.")

        # Parsing the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Look for the "Om studiet" section
        heading = soup.find(lambda tag: tag.name in ["h2", "h3"] and "Om studiet" in tag.text)
        if heading:
            print("Found 'Om studiet' section. Extracting content...")
            content_section = []
            # Gather all content until the next heading (like h2 or h3)
            for sibling in heading.find_next_siblings():
                if sibling.name in ["h2", "h3"]:
                    break
                content_section.append(sibling.get_text(separator="\n", strip=True))

            # Join the content for easier saving to file
            content_text = "\n".join(content_section)

            # Saving to a text file
            file_name = "uis_learning_outcomes.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(content_text)
                
            print(f"Learning outcomes extracted and saved to '{file_name}'.")
        else:
            print("Could not find the 'Om studiet' section on the page.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Run the extraction
if __name__ == "__main__":
    print("Starting the UiS learning outcomes scraping process...")
    extract_learning_outcomes(url)
    print("Scraping complete. Check 'uis_learning_outcomes.txt' for the results.")
