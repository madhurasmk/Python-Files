from sentence_transformers import SentenceTransformer, InputExample, losses, models
from torch.utils.data import DataLoader
import os

# Sample training data: List of InputExample objects with (anchor, positive)
train_samples = [
    InputExample(texts=["What is AI?", "Artificial Intelligence is..."]),
    InputExample(texts=["Define RAG", "RAG stands for Retrieval-Augmented Generation"]),
    # Add more pairs based on your document questions and ideal answers
]

# Initialize the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# DataLoader and loss function
train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=4)
word_embedding_model = models.Transformer('all-MiniLM-L6-v2')
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
# Loss function
train_loss = losses.CosineSimilarityLoss(model)
# train_loss = losses.MultipleNegativesRankingLoss(model)

# Fine-tune the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          epochs=1,
          warmup_steps=10
          )
          # output_path='./trained_embedding_model')
model.save("fine_tuned_model1")
print("Fine-tuned Model saved successfully")