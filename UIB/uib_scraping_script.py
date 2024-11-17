import requests
from bs4 import BeautifulSoup

# List of URLs for different UiB study programs
urls = [
    "https://www.uib.no/studier/BAMN-DTEK/plan",
    "https://www.uib.no/studier/BASV-AIKI/plan"
]

# Function to extract learning outcomes
def extract_learning_outcomes(url):
    try:
        print(f"Fetching page content from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        print("Page content fetched successfully.")

        # Parsing the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the "Kva lærer du?" heading
        heading = soup.find(lambda tag: tag.name in ["h2", "h3"] and "Læringsutbyte" in tag.text)
        if heading:
            print("Found 'Læringsutbyte' section. Extracting content...")
            content_section = []
            # Gather all content until the next heading (like h2 or h3)
            for sibling in heading.find_next_siblings():
                if sibling.name in ["h2", "h3"]:
                    break
                content_section.append(sibling.get_text(separator="\n", strip=True))

            # Join the content for easier saving to file
            content_text = "\n".join(content_section)

            # Generate a unique filename based on the URL
            program_name = url.split("/")[-2]  # Extracts a unique part from the URL
            file_name = f"uib_{program_name}_learning_outcomes.txt"
            
            # Save the extracted content to the file
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
    for url in urls:
        extract_learning_outcomes(url)
    print("Scraping complete. Check the generated text files for each study program.")