from chunkPapers import collection_create
import os

folder_path = 'C:\\Users\kishore\OneDrive\Desktop\papers-20241017T051416Z-001\papers' # path to paper folder here
collection_name = "research-paper-"
i = 0
# Loop through all files in the folder
def create_collections():
    for pdf_file in os.listdir(folder_path):
        col_name = collection_name+f"{i}"
        collection_create(os.join(folder_path,pdf_file),col_name)




