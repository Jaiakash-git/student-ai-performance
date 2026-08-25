import os
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# CONFIGURATION
# ==========================================

RAG_INDEX_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "rag_index.pkl"
)


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# LOAD RAG INDEX
# ==========================================

rag_index = joblib.load(
    RAG_INDEX_PATH
)

chunks = rag_index["chunks"]
embeddings = rag_index["embeddings"]


# ==========================================
# RETRIEVE RELEVANT CHUNKS
# ==========================================

def retrieve(query, top_k=2):

    # Convert user question into embedding
    query_embedding = model.encode(
        [query]
    )

    # Compare query with stored embeddings
    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # Get most relevant chunks
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
# TEST RETRIEVER
# ==========================================

if __name__ == "__main__":

    query = input(
        "\nEnter your question: "
    )

    results = retrieve(
        query,
        top_k=2
    )

    print(
        "\n================================"
    )
    print(
        "RETRIEVED CHUNKS"
    )
    print(
        "================================"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nResult {index}"
        )

        print(
            f"Similarity Score: "
            f"{result['score']:.4f}"
        )

        print(
            "--------------------------------"
        )

        print(
            result["chunk"]
        )