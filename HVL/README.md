# HVL LUB Scraping

This folder contains the logic for scraping the HVL websites to extract learning outcomes (LUB) from various study programs.

## Overview

This folder consist of one script [`hvl_scraping_script.py`](../HVL/hvl_scraping_script.py), which retrieves the learning outcomes from the study programs defined in the script.

New study programs can be added directly to the script, in the `program_page_hvl_url` dictionary.

### NB!
HVL creates a new webpage for learning outcomes for each new cohort, more specifically one for each autumn semester.

Remember to update the URL which is scraped in order to get the most recent learning outcomes.

## Output

The `.txt` files will be saved to the output folder

## Usage

Run the script [`hvl_scraping_script.py`](../HVL/hvl_scraping_script.py) for producing `.txt`files with the learning outcomes for each study program.

## Requirements

The rquirements (needed modules) for running the script is defined in [`Requirements.txt`](../HVL/requirements.txt)

```bash
pip install -r requirements.txt
