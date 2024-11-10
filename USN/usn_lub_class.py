from bs4 import BeautifulSoup, Tag
from datetime import datetime
from selenium import webdriver
import time
from pyshadow.main import Shadow
import re

class USN_lub:
    
    def __init__(self, programs: dict, tag_names: list[str]) -> None:
        self.tag_names = tag_names
        self.study_programs = programs
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.shadow = Shadow(self.driver)
        self.current_year = datetime.now().year
        
    
    def clean_text(self, text:str) -> str:
        """Function for cleaning input text

        Args:
            text (str): The str to be stripped and lowered

        Returns:
            str: The processed, cleaned string
        """
        return re.sub(r'\W+', '', text).strip().lower()
            
    def get_HTML_from_url(self,code: str) -> str | None: 
        """_summary_
        
        Fetches the relevant HTML from the URL containing the LUB's of the study_program.
        The HTML for USN is hidden in so called "shadow-DOM". Therefore the pyshdaow module is used. 
        
        Note: 
            Change the URL if the site where LUB's are listed is changed

        Args:
            code (str): The program code

        Raises:
            Exception: If no content found or any other error occur. 

        Returns:
            _type_: a string
        """
        
        try:
            # Change this URL if the site of the LUB's changes. 
            self.shadow.chrome_driver.get(f"https://www.usn.no/studier/studie-og-emneplaner/#/studieplan/{code.upper()}_{self.current_year}_H%C3%98ST")
            time.sleep(5)
            
            shadow_root_content = self.shadow.find_element("usn-context") #MÅ gjøre mer feilsikkert
            shadow_html_content = shadow_root_content.get_attribute('outerHTML')


            #If both unlike None
            if shadow_root_content and shadow_html_content:
                print(f"HTML content found and retrieved for {code}")
                return str(shadow_html_content)
            
            else:
                raise Exception(f"Could not find any content: {shadow_root_content}")
            
        
        except Exception as err:
            print(f"Something went wrong: {err}")
            
    def find_relevant_tags(self, soup_object: BeautifulSoup) -> list[Tag] | None:
        
        """
        Finds the relevant tags in the soup object containing the LUB's.

        Raises:
            Exception: If no tags found or any other error occur.

        Returns:
            _type_: a list of tags
        """
        relevant_tags = []
                
        try:
            for name in self.tag_names:
                for tag in soup_object.find_all(string=True):
                    cleaned_tag_text = self.clean_text(tag)
                    cleaned_name = self.clean_text(name)
                    if cleaned_tag_text == cleaned_name and tag.strip() == tag:
                        relevant_tags.append(tag.parent)
                        
            #If not all tags found -> Warning (Script will produce text for the tags it found)
            if len(relevant_tags) < 3:
                print(f"Warning: Did not find all tags")
                print(f"Found: {relevant_tags}")
                                
            else:
                print(f"Found all tags: {relevant_tags}")
                                
            #If none was found -> Raise exception
            if len(relevant_tags) == 0:
                raise Exception("No tags found")
                        
            return relevant_tags
                
                #If something went wrong -> Ecxeption
        except Exception as err:
            print(f"Something went wrong, error: {err}")
    
    def clean_content_in_list(self, text_items):
        """
        Cleans a list of text items by removing items with unwanted content, 
        such as 'Kandidaten', empty strings, and unnecessary whitespace.
        Also removes newline characters from each text item.

        Args:
        text_items (list): A list of strings to be cleaned.

        Returns:
        list: A cleaned list of strings.
        """
        cleaned_items =  [
            item.strip() for item in text_items
            if item.strip() and item.strip() != "Kandidaten" and "\n" not in item
        ]
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(cleaned_items))
    
    def get_content_for_LUBS(self, relevant_tags: list[Tag]):
        """
        Extracts the content under the relevant tags in the soup object.

        Args:
            relevant_tags (list[Tag]): A list of relevant tags in the soup object.

        Returns:
            _type_: a dictionary containing LUBS under each of the relevant tags.
        """
        extracted_content = {}
        html_tags = ["h6","h5","h4","h3","h2","h1",]
        
        for tag in relevant_tags:
            tag_key = tag.get_text()
            tag_name = self.clean_text(tag.get_text())
            tag_html_name = tag.name  # Get the HTML tag name (e.g., 'h3')
            
            content = []
            i = 0
            #Tracerse elements until we reach a stopping condition
            for sibling in tag.find_all_next():
                #Stop if we reach another relevant tag
                if sibling in relevant_tags and sibling != tag:
                    break
                
                #Stop if we encounter the same HTML tag as the current relevant tag
                if sibling.name == tag_html_name:
                    break
                
                #Break if we meet a "greater" tag than the one we are looking for
                if sibling.name in html_tags:
                    break
                
                if self.clean_text(sibling.get_text()) == tag_name:
                    break
                
                #Append sibling as string to content
                content.append(sibling.get_text().strip())
                
            # Need to clean each item in list
            cleaned_list = self.clean_content_in_list(content)
            
            # Join the content and add to the dictionary with tag_name as the key
            extracted_content[tag_key] = cleaned_list
            print(f" Content under '{tag_key}' extracted")
        
        print("All content extracted")
        return extracted_content
    
    def export_to_text_file(self, program:str, code:str, content:dict):
        """
        Exports the content to a text file with the name of the program and the code.

        Args:
            program (str): The study program from USN
            code (str): The code for the program
            content (dict): The dictionary containing the content to be exported
        """
        with open(f"{program}-({code}).txt", "w", encoding="utf-8") as file:
                
                for key, value in content.items():
                    file.write(f"Content under '{key.lower()}':\n\n")
                    
                    for item in value:
                        file.write(f"{item} \n\n")
                    
                    file.write("---")    
                    file.write("\n\n")
                    
        print("Content exported to text file")
    
    def main(self):
        for key, value in self.study_programs.items():
            code = value['code']
            print(f"Processing {code}")
            shadow_HTML_content = self.get_HTML_from_url(value['code'])
            soup = BeautifulSoup(shadow_HTML_content, 'html.parser')
            relevant_tags = self.find_relevant_tags(soup_object=soup)
            content = self.get_content_for_LUBS(relevant_tags)
            self.export_to_text_file(key, code, content)
            print(f"Finished processing {code} \n\n")
            
        print("Shutting down driver...")    
        self.driver.quit()



if __name__ == "__main__":
    pass
    