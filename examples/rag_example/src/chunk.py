import json
import pathlib
from typing import List, Optional
import yaml

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
chunk_size = config["chunk_size"]
chunk_overlap = config["chunk_overlap"]

def read_text_from_file() -> Optional[str]:
    """Reads text from a file and returns it as a string."""
    current_dir = pathlib.Path().parent.resolve()
    filepath = current_dir / "temp" / "text" / "parsed.txt"
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
        print(f"Text read from {filepath}")
        return text
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading text from file: {e}")
        return None

def chunk_text(text: str, chunk_size: int = chunk_size, overlap: int = chunk_overlap) -> List[str]:
    """Chunks the input text into smaller pieces with optional overlap."""
    words = text.split()
    chunks = []
    if not words:
        return []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i: min(i + chunk_size, len(words))])
        chunks.append(chunk)
    return chunks

def save_chunks(output_file: str = "output.json") -> None:
    """Reads text from a file, chunks it, and saves the chunks to a JSON file."""
    text = read_text_from_file()
    if text is None:
        print("No text to chunk.")
        return
    chunks = chunk_text(text)
    current_dir = pathlib.Path().parent.resolve()
    chunks_dir = current_dir / "temp" / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    output_path = chunks_dir / output_file
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(chunks, file, indent=4)
        print(f"Chunks saved to {output_path}")
    except Exception as e:
        print(f"Error saving chunks to file: {e}")

if __name__ == "__main__":
    try:
        save_chunks()
    except Exception as e:
        print(f"Chunking failed: {e}")