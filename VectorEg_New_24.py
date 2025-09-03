import faiss
import os
import fitz
from sentence_transformers import SentenceTransformer
import numpy as np
import openai
import tiktoken  # New: for accurate token count
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from openai.error import RateLimitError, OpenAIError
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# 1. Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
# model = SentenceTransformer('./trained_embedding_model')
# model = SentenceTransformer('fine_tuned_model')

# openai.api_key = 'sk-proj-uQSDdU85medcLVniY9zyT3BlbkFJeCmlqDo8iSgoHkJBcDiP'
apiKey = "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"

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

# Token counter using tiktoken
def count_tokens(text, model_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

# 4. Load documents and index
docs, filenames = load_docs_from_folder("C://0Madhura/InfoWebPages/PyWeb/docs")
embeddings = model.encode(docs)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

# Load GPT-Neo model and tokenizer for fallback when OpenAI API quota is exceeded
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # GPT-2 tokenizer (works with GPT-Neo)
model_gpt_neo = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")

# Function to generate text using GPT-Neo when OpenAI API quota is exceeded
def generate_text_with_gpt_neo(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model_gpt_neo.generate(inputs['input_ids'], max_length=1200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 5. Search and generate answers
def search_and_answer(query, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    top_chunks = [docs[i] for i in indices[0]]

    context = ""
    token_budget = 4096 - 500
    total_tokens = 0

    for chunk in top_chunks:
        chunk_tokens = count_tokens(chunk)
        if total_tokens + chunk_tokens > token_budget:
            break
        context += chunk + "\n\n"
        total_tokens += chunk_tokens

    system_prompt = "You are a helpful assistant. Use only the provided documents to answer questions. If questions are out of context, say so. Do not give any other information unless asked. Do not be verbose. Be concise"
    user_prompt = f"""You must answer using only the context provided below. Each document chunk is labeled with its source filename. When you answer, mention which source(s) the information came from.
                                Context: {context}
                                Question: {query}"""

    if count_tokens(system_prompt + user_prompt) > 4096:
        print("Prompt too long. Try with a shorter query or fewer documents.")
        return ""

    try:
        # Attempt OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1200,
            temperature=0.2
        )
        answer = response['choices'][0]['message']['content'].strip()

    except RateLimitError:
        # If OpenAI API quota is exceeded, use GPT-Neo instead
        print("Rate limit exceeded. Using GPT-Neo as fallback.")
        answer = generate_text_with_gpt_neo(user_prompt)

    except OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        answer = "An error occurred while calling the OpenAI API."
    return answer

# 6. Ask user
query = input("Enter your question: ")
answer = search_and_answer(query)
print(f"\nAnswer:\n{answer}")
