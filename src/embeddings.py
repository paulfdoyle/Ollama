from sentence_transformers import SentenceTransformer
import os
import numpy as np

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Directory where chapter files are saved
chapter_directory = './outputdir'

embeddings = {}
for filename in os.listdir(chapter_directory):
    if filename.endswith('.txt'):
        with open(os.path.join(chapter_directory, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            embedding = model.encode(text)
            embeddings[filename] = embedding

# Save the embeddings (optional)
np.save('chapter_embeddings.npy', embeddings)

