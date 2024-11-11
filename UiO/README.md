# UiO LUB Scraping

This folder contains the logic for scraping the USN websites to extract learning outcomes (LUB) from various study programs.

## Overview

The folder contains two scripts;
* [`uio_script.py`](../UiO/uio_script.py) : Script which scrapes the UIO website trough using vrtx=source, meaning the LUBS are fetched similar to using a API. 

* [`uio_web_scraping.py`](../UiO/uio_web_scraping.py) : Script which scrapes the UIO website directly by using the redered HTML on the website. 

## Usage

To scrape the LUB's, either of the scripts can be used. Both will generate a `.txt` with the learning outcomes for each study program defined in the scripts.