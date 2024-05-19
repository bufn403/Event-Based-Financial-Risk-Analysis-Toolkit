from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer, util
from transformers import BertTokenizer, BertModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
# import random
import yfinance as yf
import os
# from scraper import GoogleNewsFeedScraper
from collections import defaultdict
import ast
from itertools import chain
import networkx as nx


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")


model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)
nlp = spacy.load("en_core_web_sm")
# nlp = spacy.load("en_core_web_lg")

def load_data(file_path):
    return pd.read_csv(file_path)

def get_doc(text):
    doc = nlp(text)
    return doc

@app.route('/api/stock/<ticker>')
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    year = request.args.get('year', None)
    if not year:
        return jsonify({'error': 'Year parameter is required'}), 400

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    hist = stock.history(start=start_date, end=end_date)
    info = stock.info

    data = [{
        'date': index.strftime('%Y-%m-%d'),
        'close': row['Close']
    } for index, row in hist.iterrows()]

    print(info.get('totalRevenue'))

    additional_info = {
        'fullName': info.get('longName'),
        'revenue': info.get('totalRevenue'),
        'ebitda': info.get('ebitda'),
        'employees': info.get('fullTimeEmployees'),
        'headquarters': f"{info.get('city')}, {info.get('state')}, {info.get('country')}",
        'website': info.get('website'),
        'description': info.get('longBusinessSummary')
    }

    return jsonify({'historicalData': data, 'companyInfo': additional_info})

def segment_text(text):
    # Splits by sentences
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

def get_filtered_data(file_path, year):
    data = pd.read_csv(file_path)
    data['Year'] = pd.to_datetime(data['Fill Date'], utc=True).dt.year
    data_filtered = data[data['Year'] == int(year)]
    return data_filtered

def get_dict(row, headline, score, evaluation="None", segment="None"):
    return {
        "Ticker": row["Ticker"],
        "Company Name": row["Company Name"],
        "Fill Date": row["Fill Date"],
        "Year": row["Year"],
        "Headline": headline,
        "Highest Similarity Score": score,
        "Similarity Evaluation": evaluation, # This will be a string
        "Risk Section Representative Segment": segment
    }

# Will need to discuss this on the document as a concern
# Problems with text too long
# def truncate_text(text, max_length=50000):
#     return text if len(text) <= max_length else text[:max_length]

# @app.route('/get-events', methods=['GET'])
# def get_events():
#     file_path = "events.csv"
#     year = 2010
#     n=10

#     default_articles = 15
#     df = pd.read_csv(file_path)
#     df = df[df['Year'] == year]

#     event_list = df['Response'].explode().tolist()
#     samples = random.sample(event_list, n)
#     start_date = '2000-01-01'
#     end_date = f'{year}-12-31'
#     events = []
#     for sample in samples:
#         gnews = GoogleNewsFeedScraper(sample, start_date, end_date)
#         articles = gnews.scrape_google_news_feed()
#         while (len(articles) == 0):
#             new_sample = random.sample(event_list, 1)[0]
#             gnews = GoogleNewsFeedScraper(new_sample, start_date, end_date)
#             articles = gnews.scrape_google_news_feed()
#         ranked_articles = []
#         for i in range(min(len(articles), default_articles)):
#             event_doc = get_doc(sample)
#             article_doc = get_doc(articles[i]['Description'])
#             similarity_score = event_doc.similarity(article_doc)
#             ranked_articles.append((articles[i]['Description'], similarity_score))
#         ranked_articles.sort(key=lambda x: x[1], reverse=True)
#         events.append(ranked_articles[0][0])
#     return events

def process_file(file_path, year, headline):
    data_filtered = get_filtered_data(file_path, year)
    if data_filtered.empty:
        return None
    row = data_filtered.iloc[0]
    segments = segment_text(row['Risk Factors Text'])
    headline_embedding = model.encode([headline], batch_size=32, convert_to_tensor=True)
    segment_embeddings = model.encode(segments, batch_size=32, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(headline_embedding, segment_embeddings)[0]
    highest_similarity, highest_similarity_idx = torch.max(similarities, dim=0)
    highest_similarity_segment = segments[highest_similarity_idx]

    similarity_evaluation = None
    if highest_similarity.item() > 0.3:
        similarity_evaluation = "High Similarity"
    elif highest_similarity.item() > 0.2:
        similarity_evaluation = "Medium Similarity"
    else:
        similarity_evaluation = "Low Similarity"

    return get_dict(row, headline, highest_similarity.item(), similarity_evaluation, highest_similarity_segment)
    
def calculate_nlp_similarity(file_path, year, headline):
    data_filtered = get_filtered_data(file_path, year)
    if data_filtered.empty:
        return None
    similarities = []
    row = data_filtered.iloc[0]
    segment_doc = get_doc(row['Risk Factors Text'])
    headline_doc = get_doc(headline)
    for sent in segment_doc.sents:
        similarity_score = headline_doc.similarity(sent)
        similarities.append((sent.text, similarity_score))
    similarities.sort(key=lambda x: x[1], reverse=True)

    similarity_evaluation = None
    if similarity_score > 0.65:
        similarity_evaluation = "High Similarity"
    elif similarity_score > 0.45:
        similarity_evaluation = "Medium Similarity"
    else:
        similarity_evaluation = "Low Similarity"

    return get_dict(row, headline, similarities[0][1], similarity_evaluation, similarities[0][0])
    
def calculate_bert_similarity(file_path, year, headline):
    data_filtered = get_filtered_data(file_path, year)
    if data_filtered.empty:
        return None
    similarities = []
    row = data_filtered.iloc[0]
    segments = segment_text(row['Risk Factors Text'])
    for segment in segments:
        input_ids = tokenizer.encode(headline, segment, return_tensors="pt", max_length=5120, truncation=True)
        with torch.no_grad():
            outputs = model(input_ids)
            embeddings = outputs[0].squeeze(0)
            similarity = torch.cosine_similarity(embeddings[0], embeddings[1], dim=0)
        similarities.append((segment, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)


    similarity_evaluation = None
    if similarity > 0.65:
        similarity_evaluation = "High Similarity"
    elif similarity > 0.45:
        similarity_evaluation = "Medium Similarity"
    else:
        similarity_evaluation = "Low Similarity"

    return get_dict(row, headline, similarities[0][1], similarity_evaluation, similarities[0][0])
    
def calculate_tfidf_similarity(file_path, year, headline):
    data_filtered = get_filtered_data(file_path, year)
    if data_filtered.empty:
        return None
    similarities = []
    row = data_filtered.iloc[0]
    segments = segment_text(row['Risk Factors Text'])
    tfidf_vectorizer = TfidfVectorizer()
    for segment in segments:
        tfidf_matrix = tfidf_vectorizer.fit_transform([headline, segment])
        similarity_matrix = cosine_similarity(tfidf_matrix)
        similarities.append((segment, similarity_matrix[0][1]))
    similarities.sort(key=lambda x: x[1], reverse=True)

    similarity_evaluation = None
    if similarities[0][1] > 0.11:
        similarity_evaluation = "High Similarity"
    elif similarities[0][1] > 0.09:
        similarity_evaluation = "Medium Similarity"
    else:
        similarity_evaluation = "Low Similarity"

    return get_dict(row, headline, similarities[0][1], similarity_evaluation, similarities[0][0])
    
def get_jaccard_similarity(sentence1, sentence2):
    set1 = set(sentence1.split())
    set2 = set(sentence2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    jaccard_similarity = intersection / union if union != 0 else 0 
    return jaccard_similarity

def calculate_jaccard_similarity(file_path, year, headline):
    data_filtered = get_filtered_data(file_path, year)
    if data_filtered.empty:
        return None
    similarities = []
    row = data_filtered.iloc[0]
    segments = segment_text(row['Risk Factors Text'])
    for segment in segments:
        similarities.append((segment, get_jaccard_similarity(headline, segment)))
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    similarity_evaluation = None
    if similarities[0][1] > 0.05:
        similarity_evaluation = "High Similarity"
    elif similarities[0][1] > 0.03:
        similarity_evaluation = "Medium Similarity"
    else:
        similarity_evaluation = "Low Similarity"

    return get_dict(row, headline, similarities[0][1], similarity_evaluation, similarities[0][0])

def find_csv_directory(ticker):
    for root, dirs, files in os.walk('./companies'):
        for file in files:
            if file == f"{ticker.upper()}.csv":
                return root
    return None 

@app.route('/analyze-company', methods=['GET'])
def analyze_company():
    headline = request.args.get('headline', default=None, type=str)
    year = request.args.get('year', default=2024, type=str)
    ticker = request.args.get('ticker', default=None, type=str)
    model = request.args.get('model', default=None, type=str)
    print("Starting Analysis")
    print(f"Headline: {headline}")
    
    if headline is None:
        return jsonify({"Headline is required.": ""}), 500
    if year is None:
        return jsonify({"Year is required.": ""}), 500
    if ticker is None:
        return jsonify({"Ticker is required.": ""}), 500



    
    file = find_csv_directory(ticker) + f"/{ticker.upper()}.csv"
    if file is None:
        return None
    
    if model is None or model == "cosine":
        result = [process_file(file, year, headline)]
    elif model == "jaccard":
        result = [calculate_jaccard_similarity(file, year, headline)]
    elif model == "nlp":
        result = [calculate_nlp_similarity(file, year, headline)]
    elif model == "tfidf":
        result = [calculate_tfidf_similarity(file, year, headline)]
    elif model == "bert":
        result = [calculate_bert_similarity(file, year, headline)]
    else:
        return None


    result = pd.DataFrame(result)
    result = result.to_json(orient='records')
    print("Finished Analysis\n")
    return result

# Deprecated
@app.route('/analyze', methods=['GET'])
def analyze():
    headline = request.args.get('headline', default=None, type=str)
    year = request.args.get('year', default=2024, type=str)
    print("Starting Analysis")
    print(f"Headline: {headline}")
    
    if headline is None:
        return jsonify({"Headline is required.": ""}), 500

    files = ['XOM.csv', 'ETR.csv', 'PXD.csv']
    results = []
    for file in files:
        result = process_file("./companies/" + file, year, headline)
        if result:
            results.append(result)

    results = pd.DataFrame(results)
    response = results.to_json(orient='records')

    return response

@app.route('/company', methods=['GET'])
def company_risk_year():
    print("Company CSV requested")
    ticker = request.args.get('ticker', default=None, type=str)
    year = request.args.get('year', default=None, type=int)

    if ticker is None:
        return jsonify({"Ticker is required.": ""}), 500
    if year is None:    
        return jsonify({"Year is required.": ""}), 500

    file_name = f"./companies/{ticker.upper()}.csv"
    try:
        data = load_data(file_name)
        data['Year'] = pd.to_datetime(data['Fill Date']).dt.year
        data = data[data['Year'] == year]
        
        if data.empty:
            return jsonify({})

        return data.to_json(orient='records')

    except FileNotFoundError:
        print("File Not Found")
        return jsonify({"error": f"File for ticker {ticker.upper()} not found."}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/example', methods=['GET'])
def example():
    result = load_data("./example.csv")
    result = result.to_json(orient='records')
    
    return jsonify({"data": result})

@app.route('/get-tickers', methods=['GET'])
def extract_tickers():
    farma = request.args.get('farma', default=None, type=str)

    directory = "./companies"
    farma_maps = {
        "0": "",
        "1": "/Consumer/",
        "2": "/Manufacturing/",
        "3": "/HiTec/",
        "4": "/Health and Medical/",
        "5": "/Energy/",
        "6": "/Other including Finance/",
    }
    if farma:
        directory += farma_maps[farma]

    tickers = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                ticker = file.replace('.csv', '')
                tickers.append(ticker)

    # print(tickers)
    return jsonify({"tickers": tickers})

@app.route('/get-files', methods=['GET'])
def get_files():
    farma = request.args.get('farma', default=None, type=str)
    search = request.args.get('search', default=None, type=str)
    if search:
        search = search.upper()

    
    directory = "./companies"


    farma_maps = {
        "1": ("/Consumer/", "Consumer"),
        "2": ("/Manufacturing/", "Manufacturing"),
        "3": ("/HiTec/", "HiTec"),
        "4": ("/Health and Medical/", "Health and Medical"),
        "5": ("/Energy/", "Energy"),
        "6": ("/Other including Finance/", "Other including Finance"),
    }

    tickers = []
    if farma and farma in farma_maps:
        directory += farma_maps[farma][0]
        sector_name = farma_maps[farma][1]
    else:
        sector_name = None


    for root, dirs, files in os.walk(directory):
        folder_name = os.path.relpath(root, "./companies").replace("/", "")
        for file in files:
            if file.endswith('.csv'):
                ticker = file.replace('.csv', '')
                if search != None and search not in ticker:
                    continue
                    
                if sector_name:
                    tickers.append((ticker, sector_name))
                else:
                    tickers.append((ticker, folder_name))

    return jsonify({"tickers": tickers})

@app.route('/download-csv/', methods=['GET'])
def download_csv():
    sector = request.args.get('sector', type=str)
    ticker = request.args.get('ticker', type=str)

    if not sector or not ticker:
        return "Please provide both sector and ticker parameters.", 400

    directory = "./companies"
    farma_maps = {
        "Consumer": "/Consumer/",
        "Manufacturing": "/Manufacturing/",
        "HiTec": "/HiTec/",
        "Health and Medical": "/Health and Medical/",
        "Energy": "/Energy/",
        "Other including Finance": "/Other including Finance/",
    }

    if sector in farma_maps:
        directory += farma_maps[sector]
    else:
        return "Invalid sector provided.", 400

    filename = f"{ticker}.csv"
    file_path = os.path.join(directory, filename)

    if not os.path.isfile(file_path):
        return f"File '{filename}' not found.", 404

    return send_file(file_path, as_attachment=True)



def find_sector(ticker):
    directory = find_csv_directory(ticker)
    farma_maps = {
        "Consumer": "1",
        "Manufacturing": "2",
        "HiTec": "3",
        "Health and Medical": "4",
        "Energy": "5",
        "Other including Finance": "6"
    }

    if directory is None:
        directory = "Other including Finance"

    return farma_maps.get(os.path.basename(directory), "6"), farma_maps.get(os.path.basename(directory), directory)


@app.route('/api/graph-data')
def get_graph_data():
    min_connections = request.args.get('minConnections', default=2, type=str)
    min_connections = int(min_connections)
    sector_filter = request.args.get('sector', default="All", type=str)
    event_type_filter = request.args.get('type', default="All", type=str)


    sector_colors = {
        "1": "#3498db",
        "2": "#2ecc71",
        "3": "#f39c12",
        "4": "#e74c3c",
        "5": "#9b59b6",
        "6": "#FA8072" 
    }

    event_colors = {
        "General": "#ffd6ba",
        "Weather": "#5DADE2",
        "Political": "#F1C40F",
        "Economy": "#417B5A",
        "Energy": "#E67E22",
        "Business": "#8E44AD"
    }
    
    events_data = pd.read_csv("labeled_events.csv")

    events_data['Parsed_Response'] = events_data['Response'].apply(ast.literal_eval)
    events_data['Parsed_Event_Type'] = events_data['Event Type NLP'].apply(ast.literal_eval)
    # print(events_data['Parsed_Event_Type'])



    # Count how many companies share each event
    event_to_companies = defaultdict(set)
    company_set = defaultdict(set)
    # event_types = defaultdict(set)

    event_type_map = {}

    count = 0
    for _, row in events_data.iterrows():
        for event, event_type in zip(row['Parsed_Response'], row['Parsed_Event_Type']):
            reverse_farma_maps = {
                "1": "Consumer",
                "2": "Manufacturing",
                "3": "HiTec",
                "4": "Health and Medical",
                "5": "Energy",
                "6": "Other including Finance"
            }

            
            event_type_map[event] = event_type
            sector_num, farma = find_sector(row['Ticker'])

            if not row['Company Name'] in company_set[event]:
                # Sector = reverse_farma_maps[farma]
                if sector_filter == "All" or reverse_farma_maps[farma] == sector_filter:
                    event_to_companies[event].add((row['Company Name'], f"{count}", row['Ticker'], sector_colors[sector_num], reverse_farma_maps[farma], row["Response"], row['Year']))
                    company_set[event].add(row['Company Name'])

            count += 1

    # Keep only events shared by multiple companies
    shared_events = {event: companies for event, companies in event_to_companies.items() if len(companies) >= min_connections and (event_type_filter == "All" or event_type_map[event] == event_type_filter)}

    # Create a bipartite graph for shared events
    B_shared = nx.Graph()
    shared_company_nodes = set(chain.from_iterable(shared_events.values()))
    B_shared.add_nodes_from(shared_company_nodes, bipartite=0)
    B_shared.add_nodes_from(shared_events.keys(), bipartite=1)
    # print(shared_events)
    shared_edges = [(company[0] + company[1], event) for event, companies in shared_events.items() for company in companies]
    B_shared.add_edges_from(shared_edges)

    graph_data = {
        "nodes": [
            {
                "id": company[0] + company[1],
                "label": company[0], 
                "shape": "circle", 
                "color": company[3],
                "sector": f"{company[4]}",
                "ticker": f"{company[2]}",
                "year": f"{company[6]}",
                "response": f"{company[5]}"
            }
            for company in shared_company_nodes 
            # if sector_filter == "All" or company[4] == sector_filter
        ] + [
            {
                "id": event, 
                "label": event, 
                "shape": "square", 
                "color": event_colors[event_type_map[event]], 
                "title": "Event",
                "connected_companies": [company[0] for company in shared_events[event]],
                "event_type": event_type_map[event]
                }
            for event in shared_events.keys() 
            # if event_type_filer == "All" or event_type_map[event] == event_type_filer
        ],
        "edges": [{"from": u, "to": v} for u, v in B_shared.edges]
    }

    return jsonify(graph_data)


@app.route('/api/graph-data2')
def get_graph_data2():
    import pandas as pd
    import os
    import ast
    import networkx as nx
    from collections import defaultdict
    from flask import request, jsonify

    min_connections = int(request.args.get('minConnections', default=2))
    sector_filter = request.args.get('sector', default="All")
    event_type_filter = request.args.get('type', default="All")

    sector_colors = {
        "1": "#3498db",  # Consumer - Blue
        "2": "#2ecc71",  # Manufacturing - Green
        "3": "#f39c12",  # HiTec - Orange
        "4": "#e74c3c",  # Health and Medical - Red
        "5": "#9b59b6",  # Energy - Purple
        "6": "#FA8072"   # Other including Finance - Salmon
    }

    event_colors = {
        "General": "#ffd6ba",
        "Weather": "#5DADE2",
        "Political": "#F1C40F",
        "Economy": "#417B5A",
        "Energy": "#E67E22",
        "Business": "#8E44AD"
    }

    reverse_farma_maps = {
        "1": "Consumer",
        "2": "Manufacturing",
        "3": "HiTec",
        "4": "Health and Medical",
        "5": "Energy",
        "6": "Other including Finance"
    }

    # Load the CSV file
    events_data = pd.read_csv("labeled_events.csv")
    events_data['Parsed_Response'] = events_data['Response'].apply(ast.literal_eval)
    events_data['Parsed_Event_Type'] = events_data['Event Type NLP'].apply(ast.literal_eval)

    event_to_companies = defaultdict(set)
    company_details = {}
    event_type_map = {}

    for _, row in events_data.iterrows():
        for event, event_type in zip(row['Parsed_Response'], row['Parsed_Event_Type']):
            sector_num, farma = find_sector(row['Ticker'])
            
            # print("Farma:", farma)
            # print("Sector Filter:", sector_filter)
            # print("Event:", event_type)
            # print("event_type_filter:", event_type_filter)
            # print((sector_filter == "All" or farma == sector_filter))
            # print((event_type_filter == "All" or event_type == event_type_filter))

            if (sector_filter == "All" or reverse_farma_maps[farma] == sector_filter) and (event_type_filter == "All" or event_type == event_type_filter):
                company_id = f"{row['Company Name']}_{sector_num}"
                company_details[company_id] = (row['Company Name'], sector_colors[sector_num], farma, row['Ticker'], row["Response"])
                event_to_companies[event].add(company_id)
                event_type_map[event] = event_type

    
    shared_events = {event: companies for event, companies in event_to_companies.items() if len(companies) >= min_connections}

    
    involved_companies = set(chain.from_iterable(shared_events.values()))
    company_details = {k: v for k, v in company_details.items() if k in involved_companies}

    B_shared = nx.Graph()
    B_shared.add_nodes_from(company_details.keys(), bipartite=0)
    B_shared.add_nodes_from(shared_events.keys(), bipartite=1)
    for event, companies in shared_events.items():
        for company_id in companies:
            B_shared.add_edge(company_id, event)

    graph_data = {
        "nodes": [
            {
                "id": company_id,
                "label": details[0],
                "shape": "circle",
                "color": details[1],
                "sector": details[2],
                "ticker": details[3],
                "response": details[4]
            }
            for company_id, details in company_details.items()
        ] + [
            {
                "id": event,
                "label": event,
                "shape": "square",
                "color": event_colors[event_type_map[event]],
                "title": "Event",
                "connected_companies": list(shared_events[event]),
                "event_type": event_type_map[event]
            }
            for event in shared_events
        ],
        "edges": [{"from": company_id, "to": event} for event, companies in shared_events.items() for company_id in companies]
    }

    return jsonify(graph_data)



@app.route('/')
def index():
    return "API is Online!"

if __name__ == '__main__':
    app.run(debug=True)
