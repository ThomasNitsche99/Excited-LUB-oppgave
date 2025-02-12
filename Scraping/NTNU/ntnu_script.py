from bs4 import BeautifulSoup
import requests
import json

# Bachelor i programmering
# Bachleor i informatikk
# Bachelor i ingeniørfag - data Trondheim
# Bachleor i Ingeniør fag Data - Ålesund 


def fetch_ntnu_program_info(api_key, program_codes):
    base_url = "https://gw-ntnu.intark.uh-it.no/fsprod-api"

    headers = {
        "X-Gravitee-Api-Key": api_key,
        "Accept": "application/json"  
    }
    
    for code in program_codes:
    
        try:
            response = requests.get(f"{base_url}/studieprograminfoer/{code}", headers=headers)
            response.raise_for_status()
            json_data = response.json()

            json_str = json.dumps(json_data, indent=2)
            print(json_str)  


           # Extract the 'xmlInformasjon' field
            xml_info = json_data.get("xmlInformasjon", "")
            
            # Parse the XML content for better readability
            soup = BeautifulSoup(xml_info, "html.parser")
            formatted_info = soup.get_text(separator="\n").strip()

            # Save the formatted information to a text file
            with open(f"{code}_formatted.txt", "w", encoding="utf-8") as file:
                file.write("Læringsutbyttebeskrivelse:\n\n")
                file.write(formatted_info)
                
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP-feil: {http_err}")
        except Exception as err:
            print(f"Annen feil oppstod: {err}")

if __name__ == "__main__":
    api_key = "318ec9a5-2ee1-4dc4-8e48-cfc8ca1b1481"
    program_codes = [
        "BIT,LUB-FERHET,NORSK,2024,H%C3%98ST",
        "BIDATA,LUB-FERHET,NORSK,2024,H%C3%98ST",
        "BPROG,LUB-FERHET,NORSK,2024,H%C3%98ST",

    ]
    
    fetch_ntnu_program_info(api_key, program_codes)
