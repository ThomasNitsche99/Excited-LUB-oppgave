# USN LUB Scraping

[🇳🇴 Click here for norwegian version](README.md)

This folder contains the logic for scraping the USN websites to extract learning outcomes (LUB) from various study programs.

## Overview

The main class responsible for the scraping logic is `usn_lub`, which is implemented in the [usn_lub_class.py](../USN/usn_lub_class.py) file. This class handles the following tasks:

- Fetching HTML content from the USN study program pages.
- Parsing the HTML to find relevant tags containing learning outcomes.
- Extracting and cleaning the content under these tags.
- Exporting the extracted content to `.txt` files.

## Usage

To run the scraping script and generate the `.txt` files containing the learning outcomes, execute the [script.py](../USN/script.py) file. This script initializes the `USN_lub` class with the necessary parameters and calls the main method to start the scraping process.

To add more study program and add relevant tags to extract text from, visit [script.py](../USN/script.py)

## Requirements

The requirements (needed modules) for running the script is defined in [`Requirements.txt`](../USN/requirements.txt)

```bash
pip install -r requirements.txt
```
