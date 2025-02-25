import os
import pathlib
import numpy as np
import faiss
from typing import Optional

def read_embeddings() -> Optional[np.ndarray]:
    """
    Reads embeddings from a file and returns them as a NumPy array.

    Returns:
        Optional[np.ndarray]: The embeddings as a NumPy array, or None if an error occurs.
    """
    current_dir = pathlib.Path().parent.resolve()
    embeddings_dir = current_dir / "temp" / "embeddings"
    embeddings_dir.mkdir(parents=True, exist_ok=True) # Ensure the directory exists
    filepath = embeddings_dir / "embeddings_file.npy"
    
    try:
        arr = np.load(filepath)  # Use np.load to read binary format
        print(f"ndarray successfully read from: {filepath}")
        return arr
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading ndarray from {filepath}: {e}")
        return None

def index_embeddings() -> None:
    """
    Reads embeddings, creates a Faiss index, and saves the index to a file.
    """
    current_dir = pathlib.Path().parent.resolve()
    faiss_dir = current_dir / "temp" / "faiss_files"
    faiss_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    filepath = faiss_dir / "vector_index.bin"
    
    embeddings = read_embeddings()
    if embeddings is None:
        print("No embeddings to index.")
        return
    
    n, dim = embeddings.shape
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    
    try:
        faiss.write_index(index, str(filepath))
        print(f"Index saved to {filepath}")
    except Exception as e:
        print(f"Error saving index to {filepath}: {e}")

if __name__ == "__main__":
    try:
        index_embeddings()
    except Exception as e:
        print(f"Indexing Failed: {e}")