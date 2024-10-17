from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2

from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer  # Example embedding model (open-source)
import uuid

QDRANT_URL = "https://3511caaa-095e-4332-bfa5-c2e9d296a8af.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "gwvKzGhdrGiTEWH-2-J3OyL3poFcrPMxX2HfvlTb4Jtgcc-GwWgfCg" # Use your Qdrant API key
#QDRANT_COLLECTION_NAME = "research-papers-chunk-2"

# Initialize Qdrant client
qdrant_client = QdrantClient(url=QDRANT_URL, prefer_grpc=True, api_key=QDRANT_API_KEY)

def create_QDrant_collection(collectionName):
    """Create Qdrant collection."""
    
    # Define collection parameters
    collection_name = collectionName
    vector_size = 384  # Size of the embedding vectors
    distance_metric = models.Distance.COSINE  # Distance metric for vector similarity

    # Check if the collection already exists
    if qdrant_client.collection_exists(collection_name):
        # Optionally, delete the existing collection if you need to recreate it
        qdrant_client.delete_collection(collection_name)

    # Create the collection with the new method
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=distance_metric)  # Pass as vectors_config
    )

    print(f"Collection '{collection_name}' created successfully.")


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Function to chunk the PDF text
def chunk_pdf_text(pdf_file, chunk_size=1000, chunk_overlap=100):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_file)
    
    # Create a RecursiveCharacterTextSplitter instance
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Perform chunking
    chunks = text_splitter.split_text(text)
    
    return chunks


# Function to upload chunks to Qdrant
def upload_chunks_to_qdrant(chunks,collection_name):
    
    # Load an open-source embedding model (you can use any model)
    embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Vector size = 384

    # Embed and upload chunks as points to the collection
    for i, chunk in enumerate(chunks):
        # Convert chunk to vector
        chunk_embedding = embedder.encode(chunk).tolist()
        
        # Create a unique ID for each chunk
        point = models.PointStruct(id=str(uuid.uuid4()), vector=chunk_embedding, payload={"text": chunk})

        # Upload point to the collection
        qdrant_client .upsert(collection_name=collection_name, points=[point])
    
    print(f"Uploaded {len(chunks)} chunks to collection '{collection_name}'.")

# Example usage

def collection_create(pdf_path,collection_name):
    create_QDrant_collection(collection_name)
    #pdf_file_path = "research-papers/20-074.pdf"
    pdf_file_path = pdf_path
    chunks = chunk_pdf_text(pdf_file_path)
    # Upload the chunks to Qdrant
    upload_chunks_to_qdrant(chunks,collection_name)

'''
# Print all chunks
for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:")
    print(chunk)
    print("\n" + "-" * 50 + "\n")
'''

#create_QDrant_collection()
