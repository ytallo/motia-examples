#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 19:39:20 2025

@author: ash
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:54:52 2025

@author: ash
"""


import json
import pathlib
import google.generativeai as genai
import faiss
import os
import numpy as np





chunks = []
faiss_index = None

GOOGLE_API_KEY = os.environ.get('GOOGLE_DEV_API')

def embed_text(text, model_name = "models/embedding-001"):
    genai.configure(api_key = GOOGLE_API_KEY)
    embeddings = genai.embed_content(model = model_name, content = text)
    return np.array(embeddings["embedding"])

def startup_event():
    global chunks, faiss_index

    current_dir = pathlib.Path(__file__).parent.resolve()
    chunks_file = current_dir.parent / "temp" / "chunks" / "output.json"
    index_file = current_dir.parent / "temp" / "faiss_files" / "vector_index.bin"

    try:
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        faiss_index = faiss.read_index(str(index_file))
        print("Data loaded successfully.") 
    except Exception as e:
        print(f"Error loading data: {e}")
       


def search(query: str, k: int = 3, model_name: str = "models/embedding-001"):
    global chunks, faiss_index

    if not chunks or faiss_index is None:
        return {"error": "Data not loaded. Check server logs."}

    try:
        query_embedding = embed_text(query, model_name)
        retrieved_chunks = knn_search_with_text_retrieval(faiss_index, query_embedding, k, chunks)

        if not retrieved_chunks:  # Handle the case where no chunks are found
            return {"error": "No relevant information found for your query."}


        # Format retrieved chunks for the prompt:
        formatted_chunks = "\n---\n".join(retrieved_chunks)  # Clearer separator

        gemini_response = generate_response(formatted_chunks, query)  # Call generate_response

        return {"result": gemini_response} # Return the summarized response


    except Exception as e:
        print(f"Error during search: {e}")
        return {"error": str(e)}
    

def knn_search_with_text_retrieval(index, query_vector, k, chunks):
   
    try:
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        D, I = index.search(query_vector, k)

        results = []
        for i in range(len(I[0])): # Iterate through k neighbors for single query
            index_val = I[0][i]
            try:  # Handle potential KeyError if index isn't in chunks
                text = chunks[index_val]
                results.append(text)
            except KeyError:
                print(f"Warning: Index {index_val} not found in the chunks dictionary.")


        return results

    except Exception as e:  # Broad exception handling for debugging
        print(f"Error during k-NN search: {e}")
        return []  # Return empty list on error

def generate_gemini_prompt(query, responses):

    prompt = f"""
        
        You are an AI assistant tasked with answering a user's query based on retrieved information.  
        read the provided retrived information to best answers the user's query.  If the response is not sufficient, supplyment the retrived infromation with you knowledge.  Then, summarize the provided retrived infromation  in the context of the query, making your answer sound like a natural, human response. Focus on clarity and conciseness.
        
        
        ### Query:
        
        {query}
        
        
        ### Retrived information:

        {responses}
        
        
        """  #
    return prompt



def generate_response(retrived_chunks, query, model_name ="gemini-1.5-pro-latest"):
    prompt = generate_gemini_prompt(query, retrived_chunks)
    genai.configure(api_key = GOOGLE_API_KEY)
    response = genai.GenerativeModel(model_name).generate_content(prompt)
    return response.text



