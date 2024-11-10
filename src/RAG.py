import os
import subprocess
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

# Suppress tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load the model for generating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index
index = faiss.read_index('chapter_index.faiss')

# Directory where chapter files are saved
chapter_directory = './outputdir'

# Filenames of the chapters (ensure this list matches the index order)
filenames = sorted(os.listdir(chapter_directory))

# Create TF-IDF model for better retrieval
# Read all chapter texts
documents = []
for filename in filenames:
    file_path = os.path.join(chapter_directory, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        documents.append(f.read())

# Fit the TF-IDF vectorizer to the documents
tfidf_vectorizer = TfidfVectorizer().fit(documents)

def retrieve_chapters(query, top_k=3):
    # Use FAISS for semantic retrieval
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    retrieved_filenames = [filenames[i] for i in indices[0]]

    # Use TF-IDF to further refine results
    tfidf_query = tfidf_vectorizer.transform([query])
    tfidf_scores = tfidf_vectorizer.transform(documents).dot(tfidf_query.T).toarray().flatten()
    combined_indices = sorted(indices[0], key=lambda x: tfidf_scores[x], reverse=True)[:top_k]
    retrieved_filenames = [filenames[i] for i in combined_indices]

    return retrieved_filenames

# Generate a response based on the retrieved chapters
def generate_response(query):
    retrieved_chapters = retrieve_chapters(query)
    context = ""
    for filename in retrieved_chapters:
        file_path = os.path.join(chapter_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            context += f.read() + "\n\n"

    # Construct a refined prompt for the language model
    prompt = f"""
    You are an assistant who provides specific answers based on the given context. Here is some information extracted from relevant documents:

    {context}

    Based on the above information, please answer the following question:

    {query}

    Be concise and provide only the relevant details available in the provided context.
    """

    # Updated ollama command
    command = ['ollama', 'run', 'llama2']
    try:
        result = subprocess.run(command, input=prompt, stdout=subprocess.PIPE, text=True, timeout=60)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Model loading took too long."

# Interactive console for user input
if __name__ == '__main__':
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        response = generate_response(query)
        print("Response:", response)
        if "not available" in response or "does not provide" in response:
            print("It seems I couldn't find the exact information. Could you please be more specific or rephrase your question?")

