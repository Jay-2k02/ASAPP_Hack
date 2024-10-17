from sentence_transformers import SentenceTransformer
from qdrant_client import models, QdrantClient
import google.generativeai as genai

# Qdrant details
QDRANT_URL = "https://3511caaa-095e-4332-bfa5-c2e9d296a8af.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "gwvKzGhdrGiTEWH-2-J3OyL3poFcrPMxX2HfvlTb4Jtgcc-GwWgfCg"
QDRANT_COLLECTION_NAME = "research-papers-chunk-2"

# Store the API key as a variable
GEMINI_API_KEY = "AIzaSyAi1jAyprJ-yyjKzBFgQXoGkfORQ1avvvg"
# Configure the library with your API key
genai.configure(api_key=GEMINI_API_KEY)

# Create an instance of the GenerativeModel using a model like "gemini-1.5-flash"
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Qdrant client
qdrant_client = QdrantClient(url=QDRANT_URL, prefer_grpc=True, api_key=QDRANT_API_KEY)

# Load the same embedding model used for chunking
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Vector size = 384

def vector_search(query, collection_name, top_k=8):
    """
    Perform a vector search on the Qdrant collection using an input query.
    
    :param query: The input query as a string.
    :param top_k: The number of top chunks to return based on similarity.
    :return: List of the top relevant chunks.
    """
    # Convert query into a vector
    query_vector = embedder.encode(query).tolist()

    # Perform a vector search on the collection
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k  # Get top_k results
    )

    # Process and return the results
    results = []
    for result in search_result:
        # Extract the relevant chunk (text)
        chunk_text = result.payload.get('text', 'No text found')
        results.append(chunk_text)
    
    return results




def gemini(query, chunks):
    """Generates an answer using Google's Generative AI (Gemini) based on input query and context chunks."""

    # Join the top_chunks into a single context string
    context = "\n".join([f"{i+1}. {chunk}" for i, chunk in enumerate(chunks)])
    
    # Define the prompt with clear instructions for a paragraph answer
    prompt = f"""
    You are a highly knowledgeable assistant. Based on the given context, please provide a well-crafted answer to the query below. Use the provided information from the context as reference material.
    
    ### Context:
    {context}
    
    ### Query:
    {query}
    
    Provide a concise, clear, and informative response as a single paragraph of text.
    """
    
    # Make the request to generate text
    response = model.generate_content(prompt)

    # Check if the response contains valid content
    if response.candidates and len(response.candidates) > 0:
        return response.text    # Return the generated text as a string
    else:
        return "No valid content was returned. Please adjust your prompt or try again."



def getTopChunks(query, collectionName):
    # # Example usage
    # input_query = "What is the goal of LSTM?"
    top_chunks = vector_search(query, collectionName, top_k=8)
    return top_chunks

# input_query = "What is the goal of LSTM?"
# top_chunks = vector_search(input_query, "research-papers-chunk-2", top_k=8)
# result = gemini(input_query, top_chunks)
# print(result)


