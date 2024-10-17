from RAG_Fusion import getTopKDocs
from query_db import getTopChunks
from query_db import gemini

def getFinalAnswer(query):

    doc_ids = getTopKDocs(query)
    totalChunks = []
    collectionName = "research-paper-"
    for id in doc_ids:
        topChunks = getTopChunks(query, collectionName + str(id))
        # print(id)
        # print("---------")
        # print(topChunks)
        totalChunks.extend(topChunks)
    
    finalResult = gemini(query, totalChunks)
    return finalResult

print("--------------------------")
print("FINAL ANSWER")
#ans = getFinalAnswer("What are Transformers?")
ans = getFinalAnswer("How do GLU variants improve transformer?")
#ans = getFinalAnswer("Techniques to prune deep neural networks")
print(ans)