import faiss
import numpy as np

# Load the saved embeddings
embeddings = np.load('chapter_embeddings.npy', allow_pickle=True).item()
embedding_list = list(embeddings.values())
filenames = list(embeddings.keys())

# Create FAISS index
dimension = len(embedding_list[0])
index = faiss.IndexFlatL2(dimension)

# Convert embeddings to NumPy array and add to the index
embeddings_np = np.array(embedding_list)
index.add(embeddings_np)

# Save the index
faiss.write_index(index, 'chapter_index.faiss')
print("FAISS index created and saved.")

