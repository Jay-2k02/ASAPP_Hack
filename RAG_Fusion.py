import os
from itertools import chain
from operator import itemgetter
import pathlib
import fitz
import time
from langchain.schema import Document
from langchain.load import dumps, loads
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Cohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents.base import Document
from langchain_cohere import CohereEmbeddings  # Update this line
from langchain_community.vectorstores import Qdrant
from langchain_core.runnables import RunnableLambda
from qdrant_client import models, QdrantClient
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Qdrant
import pdfplumber

# Constants
TOP_K = 5
MAX_DOCS_FOR_CONTEXT = 10
QDRANT_URL = "https://3511caaa-095e-4332-bfa5-c2e9d296a8af.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "gwvKzGhdrGiTEWH-2-J3OyL3poFcrPMxX2HfvlTb4Jtgcc-GwWgfCg" # Use your Qdrant API key
QDRANT_COLLECTION_NAME = "RESEARCH-PAPERS"

# Set the Cohere API key as an environment variable
COHERE_API_KEY = "lb5TT3QgjdHf8yqcIxoFIXtFc5pysCxS2EmfUFFj"  # Use your Cohere API key
embedding_model = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=COHERE_API_KEY)
semantic_chunker_embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# Initialize Qdrant client
qdrant_client = QdrantClient(url=QDRANT_URL, prefer_grpc=True, api_key=QDRANT_API_KEY)

def read_pdf_files(directory: str) -> list[Document]:
    """Reads all .pdf files in a given directory and returns a list of Document objects.

    Args:
        directory (str): The path to the directory containing .pdf files.

    Returns:
        list[Document]: A list of Document objects containing the content of the .pdf files.
    """
    documents = []
    for pdf_file in pathlib.Path(directory).glob('*.pdf'):
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""  # Extract text from each page
            metadata = {"filename": pdf_file.stem}  # Store metadata like filename
            documents.append(Document(page_content=text, metadata=metadata))
    return documents

def upload_chunks_to_qdrant(documents):
    records_to_upload = []
    
    # Extract the page content from documents to generate embeddings
    contents = [doc.page_content for doc in documents]
    
    # Get embeddings for all documents in one call
    embeddings = embedding_model.embed_documents(contents)

    for idx, (content, vector) in enumerate(zip(contents, embeddings)):
        # Create Qdrant point structure for each document with its embedding
        record = models.PointStruct(
            id=idx,
            vector=vector,
            payload={"page_content": content}  # Include other metadata if needed
        )
        records_to_upload.append(record)

    # Upload points to Qdrant collection
    qdrant_client.upload_points(
        collection_name=QDRANT_COLLECTION_NAME,
        points=records_to_upload
    )
    
    return

def reciprocal_rank_fusion(results: list[list], k=60) -> list[Document]:
    """Rerank docs (Reciprocal Rank Fusion)

    Args:
        results (list[list]): Retrieved documents
        k (int, optional): Parameter k for RRF. Defaults to 60.

    Returns:
        ranked_results: List of documents reranked by RRF
    """
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    return [x[0] for x in reranked_results[:MAX_DOCS_FOR_CONTEXT]]

def query_generator(original_query: dict) -> list[str]:
    """Generate queries from original query

    Args:
        original_query (dict): Original query

    Returns:
        list[str]: List of generated queries
    """
    query = original_query.get("query")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that generates multiple search queries based on a single input query.",
            ),
            (
                "user",
                "Generate multiple search queries related to: {original_query}. When creating queries, please refine or add closely related contextual information, without significantly altering the original query's meaning.",
            ),
            ("user", "OUTPUT (3 queries):"),
        ]
    )

    model = Cohere(cohere_api_key=COHERE_API_KEY)
    query_generator_chain = (
        prompt | model | StrOutputParser() | (lambda x: x.split("\n"))
    )

    queries = query_generator_chain.invoke({"original_query": query})
    queries.insert(0, "0. " + query)

    return queries


def create_QDrant_collection():
    """Create Qdrant collection."""
    # Instantiate embeddings (Cohere in this case)
    embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=COHERE_API_KEY)
    
    # Define collection parameters
    collection_name = QDRANT_COLLECTION_NAME
    vector_size = 1024  # Size of the embedding vectors
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


'''
def upload_chunks_to_QDrant(documents):
    """Upload document chunks to Qdrant."""
    records_to_upload = []
    for idx, chunk in enumerate(documents):
        content = chunk.page_content
        vector = embedding_model.encode(content).tolist()

        record = models.PointStruct(
            id=idx,
            vector=vector,
            payload={"page_content": content}
        )
        records_to_upload.append(record)

    qdrant_client.upload_points(
        collection_name=QDRANT_COLLECTION_NAME,
        points=records_to_upload
    )
    return
'''
# def upload_chunks_to_QDrant(documents):
#     records_to_upload = []
#     for idx, chunk in enumerate(documents):
#         content = chunk.page_content
#         # Change how you call to get the embedding
#         vector = embedding_model.embed_documents([content])[0]  # Check if this is the correct call

#         record = models.PointStruct(
#             id=idx,
#             vector=vector,
#             payload={"page_content": content}
#         )
#         records_to_upload.append(record)

#     qdrant_client.upload_points(
#         collection_name=QDRANT_COLLECTION_NAME,
#         points=records_to_upload
#     )
#     return

# def upload_chunks_to_QDrant(documents: list[Document]):
#     """Uploads chunked documents to Qdrant for vector search.
    
#     Args:
#         documents (list[Document]): List of chunked Document objects.
#     """
#     records_to_upload = []
    
#     for idx, chunk in enumerate(documents):
#         content = chunk.page_content
#         metadata = chunk.metadata
        
#         # Get vector embedding for the chunk content
#         vector = embedding_model.embed_documents([content])[0]  # Ensure embedding is a list
        
#         # Create a record for Qdrant
#         record = models.PointStruct(
#             id=idx,  # Use idx or a unique identifier
#             vector=vector,
#             payload={
#                 "page_content": content,
#                 "filename": metadata.get("filename")
#             }  # You can add more metadata here if needed
#         )
#         records_to_upload.append(record)
    
#     # Upload records in batches to Qdrant
#     qdrant_client.upload_points(
#         collection_name=QDRANT_COLLECTION_NAME,
#         points=records_to_upload
#     )
#     return

def ans_retriever(query: str) -> list[Document]:
    """RRF retriever

    Args:
        query (str): Query string
        directory (str): Directory containing the .txt files

    Returns:
        list[Document]: Retrieved documents
    """
    # Read documents from the directory

    # Initialize Qdrant vector store
    qdrant = Qdrant(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embedding_model,
    )

    # Set up the retriever with search kwargs
    retriever = qdrant.as_retriever(search_kwargs={"k": TOP_K})

    # RRF chain setup
    chain = (
        {"query": itemgetter("query")}
        | RunnableLambda(query_generator)
        | retriever.map()  # Use the Qdrant retriever
        | reciprocal_rank_fusion
    )

    # Invoke the chain with the query
    result = chain.invoke({"query": query})

    # Print the top K matched documents
    print("Top K Matched Documents:")
    for idx, document in enumerate(result[:TOP_K]):
        print(f"Document {idx + 1}:\nFilename: {document.metadata.get('filename', 'N/A')}, Content: {document.page_content[:500]}...\n")

    return result


if __name__ == "__main__":
    
    #create_QDrant_collection()

    # Example usage
    # directory = 'papers'  # Directory containing the .txt files
    # documents = read_pdf_files(directory)
    # print("files read successfully")
    # upload_chunks_to_qdrant(documents)
    # print("Documents uploaded successfully")

 
    query = """
        What are the paper related to sequence to sequence learning
    """
   
    retrieved_documents = ans_retriever(query)

    '''
    # Print the retrieved documents
    for doc in retrieved_documents:
        print(doc)
        # print(f"Filename: {doc.metadata['filename']}, Content: {doc.page_content[:100]}...")  # Print first 100 characters
'''