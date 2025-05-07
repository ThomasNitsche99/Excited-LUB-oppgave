# 🎓📊 Mandatory Subjects Extraction

This folder contains code for extracting **mandatory subjects** from websites of various Norwegian universities using [Firecrawl](https://firecrawl.dev).

## Table of Contents

- [📌 What does this code do?](#what-does-this-code-do)
- [⚙️ Setup](#setup)
- [🚀 How to use the scripts](#how-to-use-the-scripts)
- [🔍 Prompt evaluation](#prompt-evaluation)
- [📁 File structure](#file-structure)
- [🧾 Dependencies](#dependencies)
- [⚠️ Limitations and known issues](#limitations-and-known-issues)

---

## What does this code do?

- Reads `config_mandatory.json` containing universities, study programs, and URLs
- For each study program:
  - Tests each defined prompt individually
  - Creates a "superprompt" combining all prompts
  - Extracts as many _mandatory subjects_ as possible by comparing all results
- Writes the results to CSV and Excel

---

## Setup

1. Ensure you have a `.env` file in the root directory:

```env
FIRECRAWL_API_KEY=your_api_key
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## How to use the scripts

### For all schools

Run `subjects_outcomes.ipynb` to extract mandatory subjects from all defined schools and study programs.

### For a single school

Run `subjects_outcomes_single.ipynb` to extract mandatory subjects from a specific school. Modify the parameters in the notebook to select the school and study program.

### Special cases

- For NTNU: Use `ntnu_subjects_selenium.ipynb`
- For USN: Use `usn_subjects_selenium.ipynb` or `new_usn_subjects_playwright.ipynb`

---

## Prompt evaluation

The code automatically evaluates different prompts for each study program and selects the one that gives the best results. This is done by:

1. Testing each prompt individually
2. Combining all prompts into one "superprompt"
3. Choosing the strategy that yields the most mandatory subjects

Results are saved in `Mandatory_subjects_best_prompts.csv` with information about which prompt strategy gave the best results.

---

## File structure

| File                                | Description                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `config_mandatory.json`             | Configuration file with schools, study programs, and prompts                 |
| `subjects_outcomes.ipynb`           | Main notebook for extraction from all schools                                |
| `subjects_outcomes_single.ipynb`    | Notebook for extraction from a single school                                 |
| `ntnu_subjects_selenium.ipynb`      | Special handling for NTNU                                                    |
| `usn_subjects_selenium.ipynb`       | Special handling for USN (Selenium)                                          |
| `new_usn_subjects_playwright.ipynb` | Special handling for USN (Playwright)                                        |
| `firecrawl_app.py`                  | Firecrawl application code                                                   |
| `utils/`                            | Helper functions                                                             |
| `combined_subjects_extraction.py`   | Script that extracts all schools including NTNU using Selenium and Firecrawl |
| `new_usn_subjects_playwright.py`    | Updated Playwright-based extraction for USN only                             |

---

## Dependencies

- Python 3.8+
- firecrawl
- pandas
- selenium (for NTNU and USN)
- playwright (for USN)
- python-dotenv

---

## Limitations and known issues

- Some schools (e.g., NTNU and USN) require special handling due to their website structure
- PDF-based study plans (e.g., from UIT and Kristiania) can be difficult to parse
- Some schools update their websites regularly, which can affect extraction
- Shadow DOM elements (especially at USN) can be challenging to handle

To handle these challenges, we use different strategies for different schools and have implemented several fallback mechanisms.
