from fastapi import FastAPI, HTTPException
from app.db import collection  # Assuming 'collection' is initialized in db.py
from app.embeddings import embed_text  # Assuming 'embed_text' is defined in embeddings.py

app = FastAPI()

@app.post("/query/")
async def query(query_text: str):
    # Generate embedding for the query text
    query_embedding = embed_text(query_text)

    # Perform a similarity search in ChromaDB
    results = collection.query(query_embeddings=[query_embedding], n_results=5)

    # If no results were found, raise an exception
    if len(results["documents"]) == 0:  # Assuming results is a dict with a "documents" key
        raise HTTPException(status_code=404, detail="No similar documents found")

    return {"results": results["documents"]}
