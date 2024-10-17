from chunkPapers import collection_create
import os

folder_path = 'C:\\Users\kishore\OneDrive\Desktop\papers-20241017T051416Z-001\papers' # path to paper folder here
collection_name = "research-paper-"
# Loop through all files in the folder
def create_collections():
    i = 0
    for pdf_file in os.listdir(folder_path):
        col_name = collection_name+f"{i}"
        collection_create(os.path.join(folder_path,pdf_file),col_name)
        i += 1

create_collections()




