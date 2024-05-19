# Project Title

## Overview

This project consists of several Jupyter notebooks designed for different purposes:
1. `gnews_scraper.ipynb`: Scrapes news articles using Google News.
2. `NLPEventClassification.ipynb`: Classifies events based on their descriptions using NLP techniques.
3. `text_helper.ipynb`: Provides helper functions for text processing tasks.

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

<!-- 1. Clone the repository:
    ```
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ``` -->

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
    - `gnews_scraper.ipynb`
    - `NLPEventClassification.ipynb`
    - `text_helper.ipynb`

3. Run the cells in the notebook to execute the code.

### gnews_scraper.ipynb

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

### text_helper.ipynb

This notebook provides various helper functions for text processing tasks. It includes:
- Functions for text cleaning and preprocessing, such as removing stopwords, punctuation, and special characters.
- Utilities for handling and transforming text data to prepare it for NLP models.
- Examples demonstrating how to use these helper functions within other notebooks or scripts.
