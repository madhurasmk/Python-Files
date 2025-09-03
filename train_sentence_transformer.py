from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers import models  # ✅ Import this to access models
from torch.utils.data import DataLoader

try:
    model = SentenceTransformer('C:/Users/Sangmesh/.cache/torch/sentence_transformers', use_auth_token='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')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error: {e}")

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# --- 1. Define training data ---
# Replace these with your own question-context pairs from your PDFs
train_examples = [
    InputExample(texts=["What is RAG?", "RAG stands for Retrieval Augmented Generation."], label=1.0),
    InputExample(texts=["What is a graph?", "A graph is a mathematical structure used to model pairwise relations."]),
    InputExample(texts=["Define document embedding.", "Document embedding is the vector representation of document content."]),
]
#


# # --- 2. Create DataLoader ---
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=4)
#
# # --- 3. Build the model ---
# # Use the base model and add a pooling layer
word_embedding_model =models.Transformer('sentence-transformers/all-MiniLM-L6-v2')
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
#
# # --- 4. Define the loss function ---
train_loss = losses.CosineSimilarityLoss(model)
#
# # --- 5. Fine-tune the model ---
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,  # Increase for better tuning if you have more data
    warmup_steps=10
)
#
# # --- 6. Save your trained model ---
model.save("fine_tuned_model1")
print("Model saved to 'fine_tuned_model1'")
