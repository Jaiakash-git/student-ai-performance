import os


# ==========================================
# CONFIGURATION
# ==========================================

DOCUMENTS_PATH = os.path.join(
    os.path.dirname(__file__),
    "documents"
)


# ==========================================
# LOAD DOCUMENT
# ==========================================

def load_document(filename):

    file_path = os.path.join(
        DOCUMENTS_PATH,
        filename
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ==========================================
# SPLIT DOCUMENT INTO CHUNKS
# ==========================================
def create_chunks(text):

    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    chunks = []

    current_chunk = ""

    for section in sections:

        # If the section is a heading,
        # keep it with the following content.
        if (
            len(section.split("\n")) == 1
            and not section.endswith(".")
        ):
            current_chunk = section

        else:
            if current_chunk:
                chunks.append(
                    current_chunk + "\n" + section
                )
                current_chunk = ""
            else:
                chunks.append(section)

    # Safety: add any remaining heading
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    document = load_document(
        "academic_guide.txt"
    )

    chunks = create_chunks(document)

    print("\nDocument loaded successfully!")
    print(f"Total chunks: {len(chunks)}")

    print("\n================================")
    print("CHUNKS")
    print("================================")

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"\nChunk {index}:"
        )

        print(chunk)