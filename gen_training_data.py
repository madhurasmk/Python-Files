import os
import fitz  # PyMuPDF for PDF parsing
import json
import re
import spacy
from tqdm import tqdm

# Load spaCy tokenizer
nlp = spacy.load('en_core_web_sm')

# Path to your PDFs
PDF_FOLDER = "C://0Madhura/InfoWebPages/PyWeb/docs"
OUTPUT_FILE = "training_data.json"

# Chunk size (number of sentences per chunk)
CHUNK_SIZE = 3

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() + " "
    return text

def clean_text(text):
    # Basic cleaning (remove extra spaces, newlines, etc.)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text_spacy(text, chunk_size=CHUNK_SIZE):
    # Use spaCy tokenizer to split the text into sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def generate_question_from_chunk(chunk):
    # Simple heuristic for generating questions (improvement needed for complex content)
    sentences = chunk.split(".")
    first_sentence = sentences[0]

    # Basic question generation: "What is/are..." for definitions
    if "is" in first_sentence.lower():
        question = "What " + first_sentence.split("is", 1)[0].strip().lower() + "?"
    else:
        question = "Explain: " + first_sentence[:50] + "..."
    return question.capitalize()

# Process all PDFs
training_data = []
for filename in tqdm(os.listdir(PDF_FOLDER)):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(PDF_FOLDER, filename)
        raw_text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text_spacy(cleaned_text)  # Use spaCy-based chunking

        for chunk in chunks:
            if len(chunk.split()) < 5:
                continue  # Skip very short chunks
            question = generate_question_from_chunk(chunk)
            training_data.append({
                "question": question,
                "context": chunk,
                "source": filename
            })

# Save to JSON file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(training_data, f, ensure_ascii=False, indent=4)

print(f"Generated {len(training_data)} question-context pairs.")
print(f"Training data saved to {OUTPUT_FILE}")
