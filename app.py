from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer, util

from json import load
import pinecone
from dotenv import load_dotenv
import os

load_dotenv()
model = SentenceTransformer(os.environ['MODEL_NAME']) 

pinecone.init(api_key=os.environ['PINECONE_API'], environment="us-west4-gcp-free")

pinecone.list_indexes()
pinecone_index = pinecone.Index(os.environ['IDX_NAME'])


app = Flask(__name__)

def filter_by_threshold(matches, threshold=0.3):
    """Filter matches by a given threshold."""
    return [match for match in matches if match.score > threshold]

def extract_metadata(matches):
    """Extract metadata from matches."""
    res_lines = []
    for match in matches:
        metdat = match.metadata
        res_line = metdat['BRAND'] if metdat['RETAILER'] == "" else f"{metdat['RETAILER']}, {metdat['BRAND']}"
        res_lines.append(res_line)
    return res_lines

def extract_scores(matches):
    """Extract scores from matches."""
    return [round(match.score, 2) for match in matches]

def extract_offers(matches):
    """Extract offer IDs from matches."""
    return [match.id for match in matches]

def nearest_search(user_input: str):
    res = pinecone_index.query(
        vector=model.encode([user_input]).tolist(),
        top_k=20,
        include_metadata=True
    )
    
    # Filter by threshold
    filtered_matches = filter_by_threshold(res['matches'])
    
    # Extract information
    offers = extract_offers(filtered_matches)
    res_lines = extract_metadata(filtered_matches)
    scores = extract_scores(filtered_matches)
    
    return offers, res_lines, scores


@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = []
    if request.method == 'POST':
        query = request.form['search']
        print(query)
        
        offers, res_lines, scores  = nearest_search(query)
        print(scores)
        # Simulated search results
        search_results = [{'title': f'{res_lines[i]}', 'content': f'{offers[i]}','score':f'{scores[i]}'} for i in range(len(scores))]
            # Add more results as needed
       
    return render_template('index.html', search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
