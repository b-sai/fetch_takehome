# Fetch App

### By Sai Shreyas Bhavanasi

To view the app goto: [https://fetchdemo.bsai.app/](https://fetchdemo.bsai.app/)

- Search
  - I used semantic similarity approach to retrieve values most similar to what the user searches for
  - I get 20 most similar items and then filter on a threshold above .3 which I found through experimentation
  - I used pinecone vector database to store and retrieve the embeddings. This was don’t to make it similar to a production setting
- Embedding
  - Used an embedding model (multi-qa-MiniLM-L6-cos-v1) from sentence-transformer
  - Chose a lightweight model so that it uses less RAM and to ensure it had a smaller embedding size to reduce storage size
  - Model is trained for semantic search on 215M question, answer pairs
- Website
  - Used Flask for frontend and backend for creating API routes. Flask was lightweight enough to approach this problem
- Deployment
  - Deployed app using railway.app

## Demo

![Alt text](image.png)
