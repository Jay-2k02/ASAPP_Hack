# QA bot for Research Papers 


The Research Paper QA Bot is a solution designed to provide accurate, real-time answers to user queries based on a collection of research papers. It leverages Retrieval-Augmented Generation (RAG) with two levels of filtering and a generative AI model to generate human-readable responses.

The system processes PDF research papers, uploads them to a Qdrant vector database, and uses vector embeddings to find relevant documents and chunks. The final context is used to formulate an easy to understand response to user queries.

## Architecture
![diagram](https://github.com/user-attachments/assets/4ca8851b-6e68-44bc-a2a4-df70b34e1984)

The detailed workflow can be viewed in this [Document](https://docs.google.com/document/d/1gW8atZmKu7whTX7H80x_caCxSoBA6LkQtw1ouB_KJSk/edit?usp=sharing) 
