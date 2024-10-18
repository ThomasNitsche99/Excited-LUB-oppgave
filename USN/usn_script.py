import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from pyshadow.main import Shadow
import re

def generate_LUB_USN() -> None:
    #----Setup----
    
    #Extract current year, used for fectching the newest LUB's
    current_year = datetime.now().year
    
    program_codes = ['ITIS', 'ING2'] #Legg till studieprogramcoder i denne listen for å hente LUB's
    
    for code in program_codes:
        print(f"Retrieving LUB's for {code} ...")
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('window-size=1920x1080')
            driver = webdriver.Chrome(options=chrome_options)
            shadow = Shadow(driver)
            shadow.chrome_driver.get(f"https://www.usn.no/studier/studie-og-emneplaner/#/studieplan/{code.upper()}_{current_year}_H%C3%98ST")
            
            #Sleep for 5 seconds to wait for website to load all content
            time.sleep(5)
            
            #----Retrieving content----
            
            # Find the shadow root element containing the h2 element
            shadow_root_content = shadow.find_element("usn-context")
                
            # Fetch the HTML content of the shadow root element
            shadow_html_content = shadow_root_content.get_attribute('outerHTML')
            
            # print(html_content+ "\n\n\n\n")
            
            #Construct in bs4
            soup = BeautifulSoup(shadow_html_content, 'html.parser')
            
            def clean_text(text:str) -> str:
                return re.sub(r'\W+', '', text).strip().lower()
            
            def find_relevant_tags():
                tag_names = ["kunnskap", "ferdigheter", "generell kompetanse"]
                relevant_tags = []
                
                try:
                    for name in tag_names:
                        for tag in soup.find_all(string=True):
                            cleaned_tag_text = clean_text(tag)
                            if cleaned_tag_text == clean_text(name) and tag.strip() == tag:
                                relevant_tags.append(tag.parent)
                    if len(relevant_tags) == 0:
                        raise Exception("Not all tags found")
                    
                    return relevant_tags
                
                except Exception as err:
                    print(f"Did not find any tags containing the relevant names, error: {err}")
            
            print(find_relevant_tags())
            
            def get_relevant_html():
                return

            # # Find the h2 tag with the text 'Læringsutbytte'
            # læringsutbytte_h2 = soup.find('h2', string=re.compile('læringsutbytte', re.IGNORECASE))

            # # Initialize a list to collect all relevant HTML
            # extracted_html = []

            # # Find all elements following the "Læringsutbytte" h2 until the next h2
            # for sibling in læringsutbytte_h2.find_next_siblings():
            #     # Stop when the next h2 is found
            #     if sibling.name == 'h2':
            #         break
                
            #     # Append each sibling to the extracted HTML list
            #     extracted_html.append(str(sibling))

            # # Join the extracted HTML content into a single string
            # læringsutbytte_content = ''.join(extracted_html)
            
            # #Construct the new content in new bs4
            # soup_læringsutbytte = BeautifulSoup(læringsutbytte_content, 'html.parser')
            
            # #Find all h3 tags (Kunnskap, ferdigheter, generell kunnskap)
            # h3_tags = soup_læringsutbytte.find_all("h3")
            
            # with open(f"{code}.txt", "w", encoding="utf-8") as file:
                
            #     for h3 in h3_tags:    
            #         #Write header to file
            #         heading = h3.get_text()
            #         file.write(f"Content under '{heading}': \n\n")
                    
            #         # Find all elements under this h3 tag until the next h3 tag
            #         for sibling in h3.find_next_siblings():
            #             if sibling.name == 'h3':
            #                 break
            #             else:
            #                 if sibling.name == 'ul':
            #                     for li in sibling.find_all('li'):
            #                         # Extract and print the text from each list item (li)
            #                         text = li.get_text(separator=' ', strip=True)
            #                         file.write(f"Kandidaten {text} \n\n")

            #         file.write('---\n\n')  # Separator between sections
                    
        
            driver.close()
                
        except Exception as err:
            print(f"An Error occurred: {err}")
            
            
if __name__ == "__main__":
    generate_LUB_USN()