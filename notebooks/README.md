# Project Title

## Overview

This project consists of several Jupyter notebooks designed for different purposes:
1. `GNewsScraper.ipynb`: Scrapes news articles using Google News.
2. `NLPEventClassification.ipynb`: Classifies events based on their descriptions using NLP techniques.
3. `SEC10KDocumentScraper.ipynb`: Scrapes and processes 10-K documents from the SEC.
4. `TextUtility.ipynb`: Provides various text processing utilities.
5. `README.md`: Project documentation.

## Requirements

- Python 3.7+
- Jupyter Notebook
- Required Python libraries specified in each notebook:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `numpy`
  - `spacy`
  - `transformers`
  - `torch`

## Installation

1. **Optional:** Set up a virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Start Jupyter Notebook:
    ```
    jupyter notebook
    ```

2. Open the desired notebook:
    - `GNewsScraper.ipynb`
    - `NLPEventClassification.ipynb`
    - `SEC10KDocumentScraper.ipynb`
    - `TextUtility.ipynb`

3. Run the cells in the notebook to execute the code.

### GNewsScraper.ipynb

This notebook is designed to scrape news articles from Google News. It performs the following tasks:
- Searches Google News for articles based on a user-defined query.
- Extracts relevant information such as the article title, link, and publication date.
- Stores the scraped data in a structured format (e.g., Pandas DataFrame) for further analysis.

### NLPEventClassification.ipynb

This notebook focuses on classifying events based on their descriptions using Natural Language Processing (NLP) techniques. It includes the following features:
- Loads and preprocesses text data related to events.
- Uses SpaCy for basic NLP tasks such as tokenization, lemmatization, and named entity recognition.
- Implements advanced NLP models from the Hugging Face Transformers library to classify events.
- Evaluates model performance and provides visualizations of the classification results.

### SEC10KDocumentScraper.ipynb

This notebook is designed to scrape and process 10-K documents from the SEC. It performs the following tasks:
- Searches the SEC EDGAR database for 10-K filings based on a user-defined query.
- Extracts and processes the text of the 10-K documents.
- Analyzes the text data to extract relevant financial information.

### TextUtility.ipynb

This notebook provides various text processing utilities. It includes:
- Functions for text cleaning and preprocessing, such as removing stopwords, punctuation, and special characters.
- Utilities for handling and transforming text data to prepare it for NLP models.
- Examples demonstrating how to use these helper functions within other notebooks or scripts.
