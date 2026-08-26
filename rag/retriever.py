import os
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# CONFIGURATION
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "rag_index.pkl"
)


# ==========================================
# LOAD MODELS + RAG INDEX
# ==========================================

model = SentenceTransformer(MODEL_NAME)

rag_index = joblib.load(DATA_PATH)

chunks = rag_index["chunks"]
embeddings = rag_index["embeddings"]


# ==========================================
# RETRIEVE RELEVANT CHUNKS
# ==========================================

def retrieve_chunks(question, top_k=2):

    question_embedding = model.encode(
        [question]
    )

    similarities = cosine_similarity(
        question_embedding,
        embeddings
    )[0]

    top_indices = similarities.argsort()[
        ::-1
    ][:top_k]

    results = []

    for index in top_indices:

        results.append({
            "chunk": chunks[index],
            "score": float(
                similarities[index]
            )
        })

    return results


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    results = retrieve_chunks(
        question
    )

    print("\n================================")
    print("RETRIEVED CHUNKS")
    print("================================")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {i}")
        print(
            f"Similarity Score: "
            f"{result['score']:.4f}"
        )

        print("--------------------------------")

        print(result["chunk"])