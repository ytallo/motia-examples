import sys
import pathlib
import json
import google.generativeai as genai
import faiss
import os
import numpy as np
import yaml

chunks = []
faiss_index = None

GOOGLE_API_KEY = os.environ.get('GOOGLE_DEV_API')

def load_config(config_file="rag_config.yml"):
    """
    Loads configuration from a YAML file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The configuration parameters.
    """
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
llm_model = config["llm_model"]
embedding_model = config["embedding_model"]
prompt_template = config["prompt"]
num_retrievals = config["num_retrival"]

def embed_text(text, model_name=embedding_model):
    """
    Embeds the given text using the specified model.

    Args:
        text (List[str]): The text to embed.
        model_name (str): The name of the embedding model.

    Returns:
        np.ndarray: The embeddings as a NumPy array.
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    embeddings = genai.embed_content(model=model_name, content=text)
    return np.array(embeddings["embedding"])

def startup_event():
    """
    Loads chunks and Faiss index from files.
    """
    global chunks, faiss_index

    current_dir = pathlib.Path().parent.resolve()
    chunks_file = str(current_dir / "temp" / "chunks" / "output.json")
    index_file = str(current_dir / "temp" / "faiss_files" / "vector_index.bin")

    try:
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        faiss_index = faiss.read_index(index_file)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")

def rag_reponse(query: str,num_retrievals = num_retrievals, model_name: str = embedding_model):
    """
    Performs retrieval-augmented generation (RAG) for a given query.

    Args:
        query (str): The query to process.
        model_name (str): The name of the embedding model.

    Returns:
        Dict[str, Any]: The RAG response or an error message.
    """
    startup_event()
    global chunks, faiss_index

    if not chunks or faiss_index is None:
        return {"error": "Data not loaded. Check server logs."}

    try:
        query_embedding = embed_text(query, model_name)
        retrieved_chunks = knn_search_with_text_retrieval(faiss_index, query_embedding, num_retrievals, chunks)

        if not retrieved_chunks:
            return {"error": "No relevant information found for your query."}

        # Format retrieved chunks for the prompt:
        formatted_chunks = "\n---\n".join(retrieved_chunks)

        gemini_response = generate_response(formatted_chunks, query)

        return {"result": gemini_response}
    except Exception as e:
        print(f"Error during search: {e}")
        return {"error": str(e)}

def knn_search_with_text_retrieval(index, query_vector, k, chunks):
    """
    Performs k-NN search and retrieves the corresponding text chunks.

    Args:
        index (faiss.Index): The Faiss index.
        query_vector (np.ndarray): The query vector.
        k (int): The number of nearest neighbors to retrieve.
        chunks (List[str]): The list of text chunks.

    Returns:
        List[str]: The retrieved text chunks.
    """
    try:
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        D, I = index.search(query_vector, k)
        results = []

        for i in range(len(I[0])):
            index_val = I[0][i]
            try:
                text = chunks[index_val]
                results.append(text)
            except KeyError:
                print(f"Warning: Index {index_val} not found in the chunks dictionary.")

        return results
    except Exception as e:
        print(f"Error during k-NN search: {e}")
        return []

def generate_gemini_prompt(query, responses, prompt_template=prompt_template):
    """
    Generates a prompt for the Gemini model.

    Args:
        query (str): The user's query.
        responses (str): The retrieved information.

    Returns:
        str: The generated prompt.
    """
    prompt = prompt_template.format(query=query, responses=responses)
    return prompt

def generate_response(retrived_chunks, query, model_name=llm_model):
    """
    Generates a response using the Gemini model.

    Args:
        retrived_chunks (str): The retrieved text chunks.
        query (str): The user's query.
        model_name (str): The name of the Gemini model.

    Returns:
        str: The generated response.
    """
    prompt = generate_gemini_prompt(query, retrived_chunks)
    genai.configure(api_key=GOOGLE_API_KEY)
    response = genai.GenerativeModel(model_name).generate_content(prompt)
    return response.text



