import pandas as pd
import pinecone
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import time

df = pd.read_csv('data/offer_retailer.csv')

# load env vars
load_dotenv()

def keep_ascii(text):
    return ''.join(c for c in text if c.isascii())
df['OFFER'] = df['OFFER'].apply(keep_ascii)

df = df.fillna("")

model = SentenceTransformer(os.environ['MODEL_NAME'])
dim = model.encode(["text"])[0].shape[0]



pinecone.init(api_key=os.environ['PINECONE_API'], environment=os.environ['PINECONE_ENV'])

# create an index in pinecone
idxs = pinecone.list_indexes()

if os.environ['IDX_NAME'] not in idxs:
    pinecone.create_index(os.environ['IDX_NAME'], dimension=dim, metric = 'cosine')
    time.sleep(120) # wait for index to be created
    
index = pinecone.Index(os.environ['IDX_NAME'])

res = model.encode(df['OFFER']).tolist()

pinecone_data = []
for idx, row in df.iterrows():
    pinecone_data.append((df['OFFER'][idx], res[idx], {'BRAND': row['BRAND'], 'RETAILER': row['RETAILER']}))

index.upsert(pinecone_data)

print(index.describe_index_stats())

res = index.query(
  vector=model.encode(["Aldi eggs"]).tolist(),
  top_k=3,
  include_values=False,
  include_metadata=True

)
print([res['matches'][x].id for x in range(len(res['matches']))])