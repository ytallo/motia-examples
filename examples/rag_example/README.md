# My Motia Project

This project demonstrates the use of Motia for performing retrieval-augmented generation (RAG) on Confluence pages. It includes steps for parsing, chunking, embedding, and indexing data, as well as an API for performing RAG on indexed data. The provided version is using Google's Gemini model endpoints for embeddings and generation. You can change the models, prompt, chunking parameters in the rag_config.yml. Please select embedding and LLM models that are availbale for your Gemini API key.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Setting Environment Variables](#setting-environment-variables)
  - [Launching Motia Service](#launching-motia-service)
  - [Indexing New Webpage](#indexing-new-webpage)
  - [Performing RAG](#performing-rag)
- [Configuration](#configuration)
- [src](#src)
- [License](#license)

## Installation

### Using Conda

1. **Ensure Conda is installed**:

    ```sh
    conda --version
    ```

2. **Create a Conda environment named `motia_rag` with Python 3.10**:

    ```sh
    conda create --name motia_rag python=3.10
    ```

3. **Activate the Conda environment**:

    ```sh
    conda activate motia_rag
    ```

4. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

### Using Python Virtual Environment

1. **Ensure Python 3.10 is installed**:

    ```sh
    python --version
    ```

2. **Create a virtual environment named `motia_rag` with Python 3.10**:

    ```sh
    python3.10 -m venv motia_rag
    ```

3. **Activate the virtual environment**:

    - On macOS and Linux:

        ```sh
        source motia_rag/bin/activate
        ```

    - On Windows:

        ```sh
        .\motia_rag\Scripts\activate
        ```

4. **Upgrade pip**:

    ```sh
    pip install --upgrade pip
    ```

5. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Setting Environment Variables

Set Gemini API Key as an environment variable. Free developer tier is available from google:

```sh
export GOOGLE_DEV_API= "your Google Gemini Key"
```
### Launching Motia Service

Start the Motia service using the provided scripts:

```sh
npx motia dev
```
### Indexing New Webpage

Parse, embed, and index a Confluence webpage using the following command:

```sh
curl -X POST http://localhost:3000/api/parse -H "Content-Type:application/json" -d '{"url":"https://confluence.atlassian.com/doc/installing-confluence-on-linux-143556824.html"}'
```

### Performing RAG

Query the indexed data using the following command:

```sh
curl -X POST http://localhost:3000/api/rag -H "Content-Type:application/json" -d '{"query":"how can i update my confluence "}'
```

## Configuration

The `rag_config.yml` file contains various parameters that you can modify to customize the behavior of the Motia project. Here are the parameters you can change:

- `llm_model`: The language model used for generating responses. You can specify different models to see how they perform.
- `embedding_model`: The model used for embedding text. Changing this can affect the quality and speed of text embeddings.
- `chunk_size`: The size of each chunk of text. Larger chunks may capture more context but could be less efficient.
- `chunk_overlap`: The overlap between consecutive chunks. Increasing this can help capture more context but may result in redundant information.
- `prompt`: The template used to generate prompts for the language model. You can modify this to change how the model interprets and responds to queries.
- `num_retrival`: The number of nearest neighbors to retrieve during the k-NN search. Increasing this can provide more context but may also include less relevant information.

## Src
The functionality of the respective step.py files are defined in their corresponding .py files in src, you can modify these to better suit your needs,

- `parse.py`: This file contains functions for parsing the provided website url and and saving it to a text file.

- `chunk.py`: This file contains functions for chunking text into smaller pieces. You can modify the chunk_size and chunk_overlap parameters in rag_config.yml to change how the text is chunked.

- `embed.py`: This file contains functions for embedding text using a specified model. You can modify the embedding_model parameter in rag_config.yml to change the embedding model used.

- `index.py`: This file contains functions for indexing the embedded text using FAISS. You can modify this file to change how the embeddings are indexed and stored.

- `rag.py`: This file contains the main functions for performing retrieval-augmented generation (RAG). You can modify the llm_model, num_retrival, and prompt parameters in rag_config.yml to change the behavior of the RAG process.



## License

This example is provided under the MIT License. See [LICENSE](LICENSE) file for details.

🚨 **Cost Disclaimer** 🚨

Please note that executing the flows in this example will incur API costs:
- Gemini is a paid service with a free developer api available for deveopment and experiemntation.
- Please be aware that there could be some cost associate with using a paid subscription.
- FAISS is a free vectorDB for experimentation and development.
- Please refer to Gemini's and Faiss's policies for use beyond experiemntation.

