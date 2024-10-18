# QA bot for Research Papers 


The Research Paper QA Bot is a solution designed to provide accurate, real-time answers to user queries based on a collection of research papers. It leverages Retrieval-Augmented Generation (RAG) with two levels of filtering and a generative AI model to generate human-readable responses.

The system processes PDF research papers, uploads them to a Qdrant vector database, and uses vector embeddings to find relevant documents and chunks. The final context is used to formulate an easy to understand response to user queries.

The Presentation link can be found [Here](https://docs.google.com/presentation/d/1-UhhAVaiSm8UruCOQ3TtOaMo6URJLq8JZ6zdt-48tto/edit?usp=sharing) 

The Demo video link can be found [Here](https://drive.google.com/drive/folders/1e-IBFTprwMhcWZdneDzkZwLELCq0VDAm?usp=sharing)

## Architecture
![diagram](https://github.com/user-attachments/assets/4ca8851b-6e68-44bc-a2a4-df70b34e1984)


## Workflow

### Data Ingestion:
- **PDF Handling**: 
  - The solution ingests research papers in PDF format.
  - Each PDF is processed to extract its text and is stored as Document objects.
- **Chunking**:
  - The extracted text is split into smaller, meaningful chunks to ensure efficient retrieval and accurate responses.

### Qdrant Vector Store:
- The first collection comprises all the research paper PDFs as points.
- Each PDF is also stored as individual collections with text chunks as points.
- **Vector Embeddings**:
  - Text chunks are converted into vector embeddings using the **Cohere** model (`embed-english-v3.0`) and stored in a Qdrant collection.
  - Each chunk represents a specific point in the Qdrant collection.

### Two-Level RAG Filtering:
- **Level 1: PDF Selection**:
  - A vector search identifies the top 5 most similar research papers (PDFs) based on the user query.
- **Level 2: Chunk Selection**:
  - From the selected PDFs, the most relevant chunks (8 from each PDF) are identified using vector search again, creating a context of 40 chunks.
  - These chunks are used to generate a consolidated answer for the user’s query.

### Generative AI Integration:
- A generative AI model (**Gemini**) processes the context (40 chunks) along with the user query to generate a coherent and accurate response.
- This ensures that the answer is both contextually relevant and human-readable.

### Web Application:
- The solution includes a web-based chatbot interface for user interaction, allowing users to:
  - Submit queries and receive responses.
  - The chatbot also provides suggestions for follow-up questions based on the user input dynamically.

- **Current Limitations**:
  - Due to resource limitations, the solution is optimized to work with 20 PDFs.
- **Scalability**:
  - The architecture is designed to be easily scalable, allowing for an increase in the database size as additional resources become available.
  - The integration with Qdrant and Cohere embeddings ensures smooth handling of larger datasets without significant structural changes.
HOw do glu varience improve transformers
techniques to prune depp nural networks

## API Endpoint
```
import requests
import json

url = "https://57d6-2401-4900-7b9d-2663-c492-2676-220e-1617.ngrok-free.app/api/chat"

payload = json.dumps({
  "prompt": "How do GLU variants improve transformer?"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

## How to Run
Clone the repo , traverse to the repo directory
Run the following commands
```
cd chatbot_frontend
python suggesstions.py
python app.py
npm start
cd chatbot
json-server -p 3500 -w src\Data\messages.json
```
The web app will run on localhost:3000 

### Tech Stack Used

- **Front End**:
  - React JS

- **Back End**:
  - Flask

- **LLM Stack**:
  - Gemini APIs
  - Cohere API
  - Qdrant Vector DB

### Future Enhancements

- **Implementing Advanced Chunking Techniques**:
  - Explore more sophisticated methods for chunking text to improve the accuracy of retrieval and response generation.

- **Semantic Caching**:
  - Implement semantic caching to reduce response time for frequently queried topics by storing and reusing previous results.

- **Integrating Batch Processing**:
  - Incorporate batch processing to handle multiple queries and large datasets simultaneously, increasing efficiency and scalability.

- **Integrating Knowledge Graphs**:
  - Leverage knowledge graphs to provide more semantically aware responses by incorporating structured relationships between concepts.

- **Enhancing Contextual Understanding**:
  - Implement a mechanism to send previously generated queries along with the current user query, improving the chatbot’s ability to maintain context across multi-turn conversations.
