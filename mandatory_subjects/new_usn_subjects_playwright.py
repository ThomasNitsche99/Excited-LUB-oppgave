from playwright.sync_api import sync_playwright
import json
import os
import time
import csv
from datetime import datetime
from firecrawl_app import app
from pydantic import BaseModel

# Load config
with open("config_mandatory.json", "r", encoding="utf-8") as file:
    config_data = json.load(file)

# Firecrawl schema
class DummySchema(BaseModel):
    obligatorise_emner: list[str]

class USN_mandatory_section_playwright:

    def __init__(self, programs: dict) -> None:
        self.study_programs = programs
        self.current_year = datetime.now().year
        self.university = "USN"
        os.makedirs("screenshots", exist_ok=True)

    def export_to_csv_file(self, program: str, subjects: list[str]):
        file_path = "Mandatory_subjects.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(["Skole", "Studie program", "Læringsutbytte type", "Læringsutbytte"])

            for subject in subjects:
                writer.writerow([self.university, program, "Obligatoriske_emner", subject.strip()])
                print(f"✍️ Writing row: {self.university}, {program}, Obligatoriske_emner, {subject.strip()}")

        print(f"📄 Appended all content to {file_path}")

    def extract_subjects_firecrawl_from_html(self, html: str, prompt_list: list[str], url: str) -> list[str]:
        print(f"🧠 Using Firecrawl to extract mandatory subjects from rendered HTML...")
        # Convert single string prompt to list
        if isinstance(prompt_list, str):
            prompt_list = [prompt_list]
            
        for prompt in prompt_list:
            try:
                result = app.extract(
                    [url],
                    {
                        "prompt": prompt,
                        "schema": DummySchema.model_json_schema()
                    }
                )
                subjects = result.get("data", {}).get("obligatorise_emner", [])
                if subjects:
                    print(f"✅ Successfully extracted {len(subjects)} subjects using prompt.")
                    return subjects
                else:
                    print(f"⚠️ Prompt returned no subjects.")
            except Exception as e:
                print(f"⚠️ Firecrawl HTML prompt failed: {prompt}\nError: {e}")
        return []

    def prepare_and_extract(self, program: str, url: str, prompts: list[str]):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            print(f"\n🌍 Navigating to {url}")
            page.goto(url)
            time.sleep(5)

            # Try to accept cookies
            try:
                godta_button = page.wait_for_selector("//button[contains(text(), 'Godta alle')]", timeout=3000)
                if godta_button:
                    godta_button.click()
                    print("✅ Accepted cookies.")
                    time.sleep(2)
            except Exception as e:
                print(f"⚠️ No cookie popup found or could not click: {e}")

            # Try expanding all + buttons
            try:
                expand_buttons = page.query_selector_all("i.expandicon.plusicon")
                if expand_buttons:
                    print(f"✅ Found {len(expand_buttons)} expandable sections. Expanding...")
                    for btn in expand_buttons:
                        try:
                            btn.click()
                            time.sleep(0.5)
                        except Exception as e:
                            print(f"⚠️ Could not click button: {e}")
                    time.sleep(2)
            except Exception as e:
                print(f"⚠️ Could not find or expand sections: {e}")

            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{program.replace(' ', '_')}_{timestamp}.png"
            page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved to {screenshot_path}")

            # Extract HTML
            html = page.content()
            browser.close()

            subjects = self.extract_subjects_firecrawl_from_html(html, prompts, url)
            return subjects

    def main(self):
        usn_config = config_data.get("USN")
        usn_prompts = usn_config["prompt_mandatory_subjects"]
        # Convert single string prompt to list
        if isinstance(usn_prompts, str):
            usn_prompts = [usn_prompts]

        for program, url in usn_config["mandatory_subjects"].items():
            print(f"\n🔍 Processing program: {program}")
            subjects = self.prepare_and_extract(program, url, usn_prompts)
            if subjects:
                self.export_to_csv_file(program, subjects)
            else:
                print(f"⚠️ No subjects extracted for {program}.")

if __name__ == "__main__":
    scraper = USN_mandatory_section_playwright({})
    scraper.main()
