import json
import os
import pathlib
import numpy as np
import google.generativeai as genai
from typing import List
import yaml

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
embedding_model = config["embedding_model"]

def embed_text(text: List[str], model_name: str = embedding_model) -> np.ndarray:
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

def read_embed_chunks(json_name: str = "output.json", embedding_file: str = "embeddings_file.npy", model_name: str = embedding_model) -> None:
    """
    Reads chunks from a JSON file, embeds them, and saves the embeddings to a file.

    Args:
        json_name (str): The name of the JSON file containing the chunks.
        embedding_file (str): The name of the file to save the embeddings.
        model_name (str): The name of the embedding model.
    """
    current_dir = pathlib.Path().parent.resolve()
    json_file = current_dir / "temp" / "chunks" / json_name
    e_file = current_dir / "temp" / "embeddings" / embedding_file

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {json_file}: {e}")
        return
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
        return

    try:
        embeddings = embed_text(chunks, model_name)
        np.save(e_file, embeddings, allow_pickle=False)  # Use np.save for binary format (recommended)
        print(f"ndarray successfully written to: {e_file}")
    except Exception as e:
        print(f"Error writing ndarray to {e_file}: {e}")

if __name__ == "__main__":
    try:
        read_embed_chunks()
    except Exception as e:
        print(f"Embedding Failed: {e}")