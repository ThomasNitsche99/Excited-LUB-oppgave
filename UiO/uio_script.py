import requests
from bs4 import BeautifulSoup


# Study programs to scrape. Add to this list in order to scrape more programs, following the same format. 
study_programs = {
    "Informatikk-programmering-og-systemarkitektur-(bachelor)": "informatikk-programmering",
    "Informatikk-design-bruk-interaksjon-(bachelor)": "inf-design",
    "Informatikk-digital-økonomi-og-ledelse-(bachelor)": "informatikk-ledelse",
    "Informatikk-digital-økonomi-og-ledelse-(master)": "informatikk-ledelse-master",
}

university = "UIO"

def generate_LUB_UiO(study_programs: dict) -> None:
        
    for key, value in study_programs.items():
        program = key
        code = value
        try:
            #Fetching JSON data
            response = requests.get(f"https://www.uio.no/studier/program/{code}/hva-lerer-du/?vrtx=source")
            response.raise_for_status()
            json_data = response.json()
            content = json_data["properties"]["content"]
            
            #Bs4
            soup = BeautifulSoup(content, 'html.parser')
            h2_tags = soup.find_all('h2')
            file_name = f"{university}_{program}_LearningOutcomes.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                for h2 in h2_tags:
                    # Initialize a list to hold the content under this <h2>
                    content = []
                    # Get all siblings after the current <h2>
                    for sibling in h2.find_next_siblings():
                        if sibling.name == 'h2':
                            # Stop if the next <h2> tag is found
                            break
                        else:
                            # Append the sibling to the content list
                            content.append(sibling)

                    heading = h2.get_text()
                    file.write(f"{heading}:\n")
                    
                    # Extract and print text from the content list
                    for element in content:
                        # Check if the element is a <p> or <li> tag
                        if element.name in ['p', 'li']:
                            text = element.get_text(separator=' ', strip=True)
                            file.write(text + '\n')  # Add an extra newline
                        elif element.name == 'ul':
                            # If the element is a <ul>, process its <li> children
                            for li in element.find_all('li'):
                                text = li.get_text(separator=' ', strip=True)
                                file.write(text + '\n')  # Add an extra newline
                        else:
                            # For other tags, extract text without adding extra newlines
                            text = element.get_text(separator=' ', strip=True)
                            file.write(text + '\n')
                    file.write('\n')  # Separator between sections
                    
            print(f"Learning outcomes extracted and saved to '{file_name}'.")
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
            
            
if __name__ == "__main__":     
    print("Starting the UIO learning outcomes scraping process...")
    generate_LUB_UiO(study_programs=study_programs)
    print("Scraping complete. Check the text files for each study program.")