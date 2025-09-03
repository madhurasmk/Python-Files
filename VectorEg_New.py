import faiss
import os
import fitz
from sentence_transformers import SentenceTransformer
import numpy as np
import openai  # You need your OpenAI key set in env var OPENAI_API_KEY
# import ollama
# 1. Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Extract text from PDF
def extract_text_from_pdf(filePath):
    text = ""
    with fitz.open(filePath) as doc:
        for page in doc:
            text += page.get_text() + ' '
    return text

# 3. Load and parse PDFs
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
            print(f"Error reading {filename}: {e}")
    return docs, fileNames

# 4. Load documents and index
docs, filenames = load_docs_from_folder("C://0Madhura/InfoWebPages/PyWeb/docs")
embeddings = model.encode(docs)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# 5. Search and generate answers
def search_and_answer(query, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    top_chunks = [docs[i] for i in indices[0]]
    # context = "\n\n".join(top_chunks)
    # Reduce context size if it exceeds token limit
    context = ""
    token_count = 0
    for chunk in top_chunks:
        chunk_tokens = len(chunk.split())  # Estimate token count based on word count
        if token_count + chunk_tokens > 14000:
            break
        context += chunk + "\n\n"
        token_count += chunk_tokens
        prompt = f"""Answer the following question based on the context below.
        Context:
        {context}
        Question: {query}
        Answer:"""
        response = openai.Completion.create(
            engine="text-davinci-003",  # or any model you are using
            prompt=chunk,
            max_tokens=100,  # Adjust according to your needs
        )
    print(response['choices'][0]['text'].strip())
    import tiktoken

    def count_tokens(text):
        """Count the number of tokens in a string."""
        encoding = tiktoken.get_encoding("gpt-3.5-turbo")  # Adjust to your model version
        tokens = encoding.encode(text)
        return len(tokens)

    input_text = "Your very large input text here"
    token_count = count_tokens(input_text)

    print(f"Token count: {token_count}")

    from openai import OpenAI
    client = OpenAI(api_key='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')
    # client = OpenAI(api_key='sk-proj-uQSDdU85medcLVniY9zyT3BlbkFJeCmlqDo8iSgoHkJBcDiP')  # Assumes OPENAI_API_KEY is set in your environment

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.2
    )
    # response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}], max_tokens = 100)

    answer = response['text'].strip()
    return answer
    # answer = response.choices[0].message.content.strip()
    # return  answer #response['choices'][0]['message']['content'].strip()

# 6. Ask user
query = input("Enter your question: ")
answer = search_and_answer(query)
print(f"\n Answer:\n{answer}")
