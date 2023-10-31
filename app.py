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

def nearest_search(user_input: str):
    res = pinecone_index.query(
    vector=model.encode([user_input]).tolist(),
    top_k=3,
    include_values=True
    )
    return [res['matches'][x].id for x in range(len(res['matches']))]

@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = []
    if request.method == 'POST':
        query = request.form['search']
        print(query)
        
        coupons  = nearest_search(query)
        # Simulated search results
        search_results = [{'title': f'Result {_+1}', 'content': f'{coupons[_]}'} for _ in range(3)]
            # Add more results as needed
       
    return render_template('index.html', search_results=search_results)

if __name__ == '__main__':
    app.run(debug=False)
