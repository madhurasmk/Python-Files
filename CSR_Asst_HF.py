import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Load documents from folder
def load_documents(folder_path):
    # Ensure folder path is clean and doesn't contain null characters
    if '\x00' in folder_path:
        raise ValueError("Folder path contains an embedded null character.")

    folder_path = folder_path.strip().replace('\x00', '')

    if not os.path.isdir(folder_path):
        raise ValueError(f"Invalid folder path: {folder_path}")

    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return documents

# 2. Split documents into chunks
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

# 3. Embed and index documents
def embed_documents(chunks):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embedding_model)
    return vectordb


# 4. Setup QA system
def create_qa_system(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever)
    return qa


# Main execution
if __name__ == "__main__":
    folder_path = r"C:\0Madhura\InfoWebPages\PyWeb\docs"
    print("Loading documents...")
    documents = load_documents(folder_path)
    print(" Splitting documents...")
    chunks = split_documents(documents)
    print(" Embedding and indexing...")
    vectordb = embed_documents(chunks)
    print("Setting up QA system...")
    qa_system = create_qa_system(vectordb)

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == 'exit':
            break
        answer = qa_system.run(query)
        print(f"\n Answer: {answer}")
