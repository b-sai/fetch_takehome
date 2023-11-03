import pandas as pd
import pinecone
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import time

df = pd.read_csv('data/offer_retailer.csv')

def keep_ascii(text):
    return ''.join(c for c in text if c.isascii())
df['OFFER'] = df['OFFER'].apply(keep_ascii)

df = df.fillna("")

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')


# load env vars
load_dotenv()

# create an index in pinecone
idxs = pinecone.list_indexes()

if 'fetchapp' not in idxs:
    pinecone.init(api_key=os.environ['PINECONE_API'], environment="us-west4-gcp-free")
    time.sleep(120) # wait for index to be created
    
index = pinecone.Index("fetchapp")

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