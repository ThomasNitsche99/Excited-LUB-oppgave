from firecrawl_app import app
from pydantic import BaseModel
import os
import sys
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Define schema
class DummySchema(BaseModel):
    obligatorise_emner: list[str]

# Define NTNU study programs and their URLs
ntnu_programs = {
    "Bachelor i programmering": "https://www.ntnu.no/studier/studieplan#programmeCode=BPROG&year=2024",
    "Bachelor i informatikk": "https://www.ntnu.no/studier/studieplan#programmeCode=BIT&year=2024",
    "Bachelor i ingenioerfag, data": "https://www.ntnu.no/studier/studieplan#programmeCode=BIDATA&year=2024&dir=BIDATA-24-TRHEIM"
}

def extract_ntnu_subjects():
    print("\n Now extracting mandatory subjects from NTNU using Selenium")
    ntnu_rows = []
    
    # Set up Selenium with headless Chrome
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    for study_program, url in ntnu_programs.items():
        print(f"🔍 Extracting for: {study_program}")
        driver.get(url)
        time.sleep(3)

        # Force select 2024 from dropdown
        try:
            select_element = driver.find_element(By.CSS_SELECTOR, "select[aria-labelledby='velg_kull']")
            select = Select(select_element)
            select.select_by_value("2024")
            print("✅ Selected 2024")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Failed to select year for {study_program}: {e}")

        # Extract the loaded page
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")

        found_any = False
        for row in rows:
            if "O" in row.text:
                cols = row.find_all("td")
                if cols:
                    subject_code = cols[0].get_text(strip=True)
                    subject_name = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                    ntnu_rows.append({
                        "Skole": "NTNU",
                        "Studie program": study_program,
                        "Læringsutbytte type": "Obligatorise_emner",
                        "Læringsutbytte": f"{subject_code} {subject_name}"
                    })
                    found_any = True

        if not found_any:
            ntnu_rows.append({
                "Skole": "NTNU",
                "Studie program": study_program,
                "Læringsutbytte type": "Obligatorise_emner",
                "Læringsutbytte": ""
            })

    driver.quit()
    return ntnu_rows

def try_single_prompt(url, prompt):
    try:
        data = app.extract([url], {
            'prompt': prompt,
            'schema': DummySchema.model_json_schema()
        })
        return data.get("data", {}).get("obligatorise_emner", [])
    except Exception as e:
        print(f"Prompt failed: {prompt[:50]}...\nError: {e}")
        return []

def main():
    # Load config
    with open("config_mandatory.json", "r", encoding="utf-8") as f:
        config_data = json.load(f)

    # First, extract NTNU subjects using Selenium
    ntnu_rows = extract_ntnu_subjects()
    
    # Save NTNU data to CSV
    if ntnu_rows:
        df_ntnu = pd.DataFrame(ntnu_rows)
        df_ntnu.to_csv("Mandatory_subjects.csv", mode='w', header=True, index=False)
        print("✅ Saved NTNU data to Mandatory_subjects.csv")
    
    # Then process other schools using Firecrawl
    rows = []
    first_write = True

    for school, school_data in config_data.items():
        if school == "NTNU":  # Skip NTNU as we already processed it
            continue
            
        print(f"\n🏫 Now extracting mandatory subjects from {school}")

        for study_program, url in school_data["mandatory_subjects"].items():
            print(f" - Program: {study_program}")

            try:
                prompts = school_data["prompt_mandatory_subjects"]
                if isinstance(prompts, str):
                    prompts = [prompts]

                best_result = []
                best_strategy = ""

                # Try each prompt separately
                for prompt in prompts:
                    subjects = try_single_prompt(url, prompt)
                    print(f"   ➤ Prompt: {prompt[:40]}... → {len(subjects)} subjects")
                    if len(subjects) > len(best_result):
                        best_result = subjects
                        best_strategy = f"Single prompt: {prompt[:40]}..."

                # Try all prompts combined
                super_prompt = "\n".join(prompts)
                super_subjects = try_single_prompt(url, super_prompt)
                print(f"   🔁 Super prompt → {len(super_subjects)} subjects")

                # Use the best result
                if len(super_subjects) > len(best_result):
                    best_result = super_subjects
                    best_strategy = "Super prompt"

                if best_result:
                    for subject in best_result:
                        rows.append({
                            "Skole": school,
                            "Studie program": study_program,
                            "Læringsutbytte type": "Obligatorise_emner",
                            "Læringsutbytte": subject.strip(),
                        })
                else:
                    print("   ❌ No mandatory subjects found.")
                    rows.append({
                        "Skole": school,
                        "Studie program": study_program,
                        "Læringsutbytte type": "Obligatorise_emner",
                        "Læringsutbytte": "",
                    })

            except Exception as e:
                print(f"   ❗ Failed to extract for {study_program}: {e}")
                rows.append({
                    "Skole": school,
                    "Studie program": study_program,
                    "Læringsutbytte type": "Obligatorise_emner",
                    "Læringsutbytte": "",
                })

    # Save all collected rows
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv("Mandatory_subjects.csv", mode='a', header=False, index=False)
        print("\n✅ All mandatory subjects written to CSV!")

if __name__ == "__main__":
    main() 