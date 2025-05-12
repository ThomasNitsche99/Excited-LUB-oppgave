# 🚀🚀 Learning Outcome Extraction 🚀🚀

[🇳🇴 Click here for norwegian version](README.md)

This folder contains code for extracting Learning Outcome Descriptions for study programs at specified schools in Norway.

## Table of Contents 📑

- [🔍 How it works](#how-it-works)
- [⚙️ Setup](#setup)
- [📤 Extraction of learning outcomes and output](#extraction-of-learning-outcomes-and-output)
- [🔄 Comparison of learning outcomes](#comparison-of-learning-outcomes)
- [🔗 Help with URLs containing years](#help-with-urls-containing-years)
- [📁 File structure](#file-structure)
- [📋 Requirements for running](#requirements-for-running)
- [📝 Notes](#notes)

## How it works

Extraction of learning outcomes is done using the **Extract** function provided by [Firecrawl](https://www.firecrawl.dev/). Firecrawl is designed to make the extraction of information from websites, known as scraping, an easier process. By utilizing AI, this becomes a fairly seamless process and only requires the definition of a *prompt* to specify what kind of information should be extracted and how the AI model should retrieve it.

The [Extract](https://www.firecrawl.dev/extract) function gives users the ability to define an interface for how the extracted information should be presented. This modeling makes it easier to work with and use the data that is extracted.

It is possible to change how the scraped data is represented. This is done by modifying `NestedModel(BaseModel)` in `firecrawl_app.py`. Here you can define a different structure for how the data should be organized and stored.

To see the file structure and a description of files, see [File Structure](#file-structure)

## Setup

The Python file called [`firecrawl_app.py`](firecrawl_app.py) is where the Firecrawl instance itself, as well as the model for the data, is defined.

**NOTE!** Firecrawl requires an API key. This is not pushed to the repository but is distributed to those who request it. The API key is retrieved from a `.env` file, so make sure to create this file in the root folder of the project with the following content:

```python
FIRECRAWL_API_KEY = "your_api_key_here"
```

All schools and corresponding study programs are defined in the file [`config.json`](config.json). For each school, the study program and corresponding URL where learning outcomes can be found are specified. A specific *prompt* to be used when extracting learning outcomes is also defined here.

The reason why each school defines its own *prompt* is that the schools' websites and presentation of learning outcomes vary. In this way, it is not possible to have a universal *prompt*, as you will encounter the need to give specific instructions for each of the schools/websites to extract the correct information in the right way. Remember that the prompt used for each school is not necessarily the best. It can always be changed!

If you want to add more schools or study programs, you can simply add them to the [`config.json`](config.json) file. The setup in the file is easy to understand.

## Extraction of learning outcomes and output

To extract learning outcomes for all study programs and schools, run the Jupyter notebook [`learning_outcomes.ipynb`](learning_outcomes.ipynb). This will be based on `config.json`

It will also be possible to extract learning outcomes for just one school. Then run the file called [`learning_outcomes_single.ipynb`](learning_outcomes_single.ipynb). Make sure to define the necessary parameters in the file.

When running the scripts, a CSV file will be created containing:

- *school*
- *study_program*
- *learning_outcome type (knowledge, skill or general_competence)*
- *learning_outcome*.

Example:

| School | Study Program | Learning Outcome Type | Learning Outcome |
|-------|--------------|---------------------|----------------|
|   UiO   |     Computer Science        |  Knowledge                   |   the candidate ...             |

### Excel format

After running the script that creates CSV files, an Excel file will also be created. This includes some formatting to make the Excel file easier to read. The file will have the same name as the CSV file that is created, just with the extension `.xlx`.

## Comparison of learning outcomes

A script has also been created to compare two CSV files. The purpose is to be able to see if learning outcomes have changed over a period. For the comparison to work correctly, it is important that the CSV files to be compared are extracted using the scripts described in "Extraction of learning outcomes and output", so that the format and columns are the same.

To compare learning outcomes for all study programs and schools, run the Jupyter notebook [`learning_outcomes_differences.ipynb`](learning_outcomes.ipynb). Make sure to define the necessary parameters in the file. Here you should add the two CSV files you want to compare.

By running the script, if there are any differences, a CSV file named "learning_outcome_differences.csv" will be created, containing:

- *school*
- *study_program*
- *learning_outcome type (knowledge, skill or general_competence)*
- *learning_outcome*
- *learning outcome exsists in file x*

## Help with URLs containing years

Some URLs contain year numbers (for different cohorts), which means that as the year changes, learning outcomes for this cohort will get a new URL.

This means that to extract the latest learning outcome descriptions, the URL being scraped from must be changed.  

**For example:**

- for cohort 2024:
    <https://www.uia.no/studier/program/data-ingeniorutdanning-bachelor/studieplaner/2024h.html>

- for cohort 2025:
    <https://www.uia.no/studier/program/data-ingeniorutdanning-bachelor/studieplaner/2025h.html>

Therefore, a script has been created in [`url_helper.ipynb`](url_helper.ipynb) that scans the `config.json` file and extracts URLs that contain year numbers in a natural way. Then the script will try to "ping" the same URL for the study program, but with the current year. The script gives feedback for each relevant school and study program.  

This is intended as a tool to check if you are updated with the latest information for each study program.

<span style="color:red">NB!</span> Even if the script says that there is a newer URL than the one in `config.json`, it may be that this page does not contain content. Always check the newer page before you potentially change the URL!

#### <span style="color:red">**UIT** and **KRISTIANIA** contain year numbers, but these work somewhat differently. Both of these schools present learning outcome descriptions in a PDF. These URLs are difficult to update, as you retrieve PDFs over the internet from URLs that are differently formatted. </span>

## File structure

| File | type | Description |
|-------|--------------|---------------------|
|[`requirements.txt`](requirements.txt)|txt|Python file containing various helper functions|
|[`.env`](.env)|Environment Variables|Definition of Firecrawl API key. NB! Must be created manually. See [Setup](#setup)|
|[`config.json`](config.json)|JSON|Definition of schools, study programs with corresponding URLs and *prompt*|
|[`firecrawl_app.py`](firecrawl_app.py)|Python|Definition of Firecrawl app and data modeling|
|[`utils/helpers.py`](utils/helpers.py)|Python|Python file containing various helper functions|
|[`learning_outcomes.ipynb`](learning_outcomes.ipynb)|Jupyter Notebook|Notebook for extraction of learning outcomes for all defined schools|
|[`learning_outcomes_single.ipynb`](learning_outcomes_single.ipynb)|Jupyter Notebook|Notebook for extraction of learning outcomes for one school|
|[`learning_outcomes_differences.ipynb`](learning_outcomes_differences.ipynb)|Jupyter Notebook|Notebook for comparison of learning outcomes|
|[`url_helper.ipynb`](url_helper.ipynb)|Jupyter Notebook|Notebook for help with URL addresses for study programs containing year numbers|
|[`Scraping/USN`](Scraping/USN/README.en.md)|Folder|Contains code for scraping learning outcomes from USN|

## Requirements for running

To run the project, the following Python packages are required:

- `firecrawl` - Used in `firecrawl_app.py` for web scraping functionality
- `pydantic` - Used for data modeling and validation in `firecrawl_app.py`
- `python-dotenv` - Used to load environment variables from `.env` file
- `pandas` - Used in `utils/helpers.py` for data manipulation and CSV/Excel operations
- `openpyxl` - Used for Excel file formatting and styling
- `beautifulsoup4` - Used in `usn_lub_class.py` for HTML parsing
- `selenium` - Used for web automation and browser control
- `pyshadow` - Used for handling shadow DOM elements in web scraping

To install these dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Note: For Selenium to work optimally, you must also have the appropriate browser driver installed (ChromeDriver in this case, as seen in the code). This is typically installed separately from the Python packages.

# Notes

### About Prompts

Remember that the prompt used for each school is not necessarily the best. The one that comes with this codebase has been used for testing and kept due to good results. <span style="color:green">**This prompt can always be changed!**</span>

### Limitations in Scraping

Due to difficulties with USN's websites (using shadow-root), Firecrawl cannot scrape the learning outcomes. This is because the way the website's code is structured does not make the desired information immediately available. Therefore, it is currently not possible to scrape USN's websites with Firecrawl. In the [`Scraping/USN`](Scraping/USN) folder, there is old code for scraping that handles shadow-root, but the code itself has room for improvement. This can be used temporarily. This will produce text files containing the learning outcomes. Read the `README.md` file for instructions.

UIT presents learning outcomes in the form of PDFs. Firecrawl can scrape PDFs, but the structure of this PDF is so convoluted that it somehow fails to do so (even though it manages Kristiania which also has it in PDF). This can be looked into further.

#### <span style="color:red">**Because of this, it is currently not possible to extract learning outcomes for UIT and USN with the existing solution!** </span>

### Other things

As mentioned, Kristiania presents learning outcomes through PDFs. In recent times, it has been discovered that these update, but are not directly available on Kristiania's website, but rather can be downloaded. Since you can open downloaded PDFs directly in the browser, it is possible to change the URL of Kristiania's study programs to point directly to the PDF's location locally on the PC. We acknowledge that this leads to more work than we would like. 