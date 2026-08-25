import os

from sentence_transformers import SentenceTransformer

from rag.ingest import load_document, create_chunks


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# GENERATE EMBEDDINGS
# ==========================================

def generate_embeddings(chunks):

    embeddings = model.encode(
        chunks
    )

    return embeddings


# ==========================================
# MAIN
# ==========================================

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    document = load_document(
        "academic_guide.txt"
    )

    chunks = create_chunks(
        document
    )

    embeddings = generate_embeddings(
        chunks
    )

    # ======================================
    # SAVE CHUNKS + EMBEDDINGS
    # ======================================

    data_path = os.path.join(
        os.path.dirname(__file__),
        "data"
    )

    os.makedirs(
        data_path,
        exist_ok=True
    )

    index_path = os.path.join(
        data_path,
        "rag_index.pkl"
    )

    import joblib

    joblib.dump(
        {
            "chunks": chunks,
            "embeddings": embeddings
        },
        index_path
    )

    # ======================================
    # OUTPUT
    # ======================================

    print("\nEmbedding generation successful!")

    print(
        f"Total chunks: {len(chunks)}"
    )

    print(
        f"Embedding dimensions: "
        f"{embeddings.shape[1]}"
    )

    print(
        f"\nRAG index saved to:\n"
        f"{index_path}"
    )

    print("\n================================")
    print("FIRST CHUNK")
    print("================================")

    print(chunks[0])

    print("\n================================")
    print("FIRST 10 VALUES")
    print("================================")

    print(
        embeddings[0][:10]
    )