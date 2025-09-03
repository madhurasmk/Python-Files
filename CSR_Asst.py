import os
import fitz  # PyMuPDF
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

# === Step 1: Set your OpenAI API Key ===
openai.api_key = os.environ['MM_API_Key']  # Preferably load this from env
print(openai.api_key)
# === Step 2: Extract Text from PDF ===
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
#Step 3: Chunk the Text ===
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.create_documents([text])
    return docs

# === Step 4: Create Embeddings and FAISS Index ===
def create_vector_index(docs):
    embeddings = OpenAIEmbeddings()  # Uses 'text-embedding-ada-002'
    db = FAISS.from_documents(docs, embeddings)
    return db

# === Step 5: Query the System ===
def query_index(db, user_question):
    relevant_docs = db.similarity_search(user_question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
You are a helpful assistant. Use the following context to answer the question.
If the answer is not found, say "I couldn’t find that in the documents."
Context:
{context}
Question: {user_question}
Answer:
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']

# ===
# # === Step 6: Putting it All Together ===
def main():
    # Load and process both PDFs
    text1 = extract_text_from_pdf("25 Types of RAG.pdf")
    text2 = extract_text_from_pdf("60 Python Interview QA.pdf")
    full_text = text1 + "\n" + text2
    print(full_text)
#
    # Chunk and embed
    chunks = chunk_text(full_text)
    vector_index = create_vector_index(chunks)

    print("Ask your questions!")
    while True:
        question = input("\n Your Question (type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        answer = query_index(vector_index, question)
        print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()
