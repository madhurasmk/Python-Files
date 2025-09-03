import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# === Step 1: PDF Parsing ===
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

# === Step 2: Chunk Text ===
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.create_documents([text])

# === Step 3: Create Embeddings & Index ===
def build_vector_index(docs):
    embeddings = OllamaEmbeddings(model="llama2")  # use "llama2", "gemma", etc.
    db = FAISS.from_documents(docs, embeddings)
    return db

# === Step 4: Question Answering with Ollama ===
def create_qa_chain(vector_db):
    llm = Ollama(model="llama2")  # or llama2, gemma, etc.
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_db.as_retriever())
    return qa_chain

# === Step 5: Main ===
def main():
    text1 = extract_text_from_pdf("25 Types of RAG.pdf")
    text2 = extract_text_from_pdf("60 Python Interview QA.pdf")
    combined_text = text1 + "\n" + text2

    docs = chunk_text(combined_text)
    vector_db = build_vector_index(docs)
    qa = create_qa_chain(vector_db)

    print("Ollama-powered Q&A is ready!")
    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        answer = qa.run(query)
        print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()
