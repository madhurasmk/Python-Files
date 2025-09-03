import faiss
import os
import fitz
from sentence_transformers import SentenceTransformer
import numpy as np
## 1
model = SentenceTransformer('all-MiniLM-L6-v2')

# ## 2
# documents = [
# "The Eiffel Tower is located in Paris.",
#     "Mount Everest is the tallest mountain in the world.",
#     "The Great Wall of China is visible from space.",
#     "Python is a popular programming language.",
#     "Pandas and NumPy are useful libraries for data science."
# ]
#
# ## 3
# doc_embeddings = model.encode(documents)
#
# ## 4
# dimension = doc_embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)
# index.add(doc_embeddings)
# print(f"FAISS index contains {index.ntotal} vectors." )
#
# ## 5
# query = "What is  the tallest peak on Earth?"
# query_embedding = model.encode(['query'])
# k = 2
# D, I = index.search(query_embedding, k)
# print("Query: ", query)
# print("Top results:")
# for i in I[0]:
#     print(f" - {documents[i]}")


def extract_text_from_pdf(filePath):
    text = ""
    with fitz.open(filePath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def load_docs_from_folder(folder_path):
    docs = []
    fileNames = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        ext = filename.lower().split(".")[-1]
        try:
            if ext == "pdf":
                content = extract_text_from_pdf(filepath)
            else:
                continue
            if content.strip():
                docs.append(content.strip())
                fileNames.append(filename)
        except Exception as e:
            print (f"Error reading {filename}: {e}")
    return docs, fileNames

docs, filenames = load_docs_from_folder("C://0Madhura/InfoWebPages/PyWeb")
embeddings = model.encode(docs)
dim1 = embeddings.shape[1]
index = faiss.IndexFlatL2(dim1)
index.add(np.array(embeddings))

def search(query, top_k = 3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = [(filenames[i], docs[i]) for i in indices[0]]
    return  results

query = input("Enter a query: ")
results = search(query)
print(f"\nQuery : {query} \n Top Matches: ")
for fname, content in results:
    print(f"\n From: {fname} \n Excerpt:\n{content[:300]}...\n")