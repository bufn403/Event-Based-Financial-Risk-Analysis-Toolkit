# Project Title

## Overview

This project provides an API for calculating similarity scores between headlines and risk factor segments from company reports using Natural Language Processing (NLP) techniques. It uses both traditional NLP and BERT-based methods to compute these similarities. Additionally, the project generates graph data to visualize relationships between companies and events based on shared risk factors.


## Features

- Calculate similarity between headlines and risk factor segments using:
    - Traditional NLP similarity
    - BERT-based similarity
- Generate graph data to visualize relationships between companies and events
- API endpoint to access similarity scores and graph data

## Requirements

- Python 3.7+
- Flask
- SpaCy
- PyTorch
- Transformers
- Pandas
- NetworkX

## Installation
**Optional:** Set up a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:

```
pip install -r requirements.txt
```

## Usage
1. Run the Flask application:

```
python app.py
```

2. Access the API at http://127.0.0.1:5000/.

## API Endpoints

### Endpoint: /calculate_nlp_similarity

**Method: GET**

**Parameters:**
- **file_path** (str): Path to the CSV file containing risk factors.
- **year** (int): Year to filter the data.
- **headline** (str): Headline text to compare.

**Example Request:**
```
curl -X POST http://127.0.0.1:5000/calculate_nlp_similarity \
    -H "Content-Type: application/json" \
    -d '{"file_path": "data/risk_factors.csv", "year": 2023, "headline": "Sample Headline"}'
```

**Example Response:**
```
{
    "company": "Sample Company",
    "headline": "Sample Headline",
    "similarity_score": 0.75,
    "similarity_evaluation": "High Similarity",
    "highest_similarity_segment": "Sample risk factor text segment."
}
```

### Calculate BERT Similarity
#### Endpoint: /calculate_bert_similarity

**Method: GET**

**Parameters:**

- **file_path** (str): Path to the CSV file containing risk factors.
- **year** (int): Year to filter the data.
- **headline** (str): Headline text to compare.

**Example Request:**
```
curl -X POST http://127.0.0.1:5000/calculate_bert_similarity \
    -H "Content-Type: application/json" \
    -d '{"file_path": "data/risk_factors.csv", "year": 2023, "headline": "Sample Headline"}'
```
**Example Response:**
```
{
    "company": "Sample Company",
    "headline": "Sample Headline",
    "similarity_score": 0.80,
    "similarity_evaluation": "High Similarity",
    "highest_similarity_segment": "Sample risk factor text segment."
}
```

### Generate Graph Data
#### Endpoint: /generate_graph_data

**Method: GET**

**Parameters:**
- :**file_path:** (str): Path to the CSV file containing company and event data.
- :**min_connections:** (int): Minimum number of shared events to include a company in the graph.

Example Request:
```
curl -X POST http://127.0.0.1:5000/generate_graph_data \
    -H "Content-Type: application/json" \
    -d '{"file_path": "data/company_events.csv", "min_connections": 3}'
```
Example Response:
```
{
    "nodes": [
        {
            "id": "Sample Company_1",
            "label": "Sample Company",
            "shape": "circle",
            "color": "#ff0000",
            "sector": "Finance",
            "ticker": "SC",
            "response": "Positive"
        },
        {
            "id": "Sample Event",
            "label": "Sample Event",
            "shape": "square",
            "color": "#00ff00",
            "title": "Event",
            "connected_companies": ["Sample Company_1"],
            "event_type": "Merger"
        }
    ],
    "edges": [
        {
            "from": "Sample Company_1",
            "to": "Sample Event"
        }
    ]
}
```
