import fitz  # PyMuPDF
import docx
import chromadb
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException

# Initialize ChromaDB client
chroma_client = chromadb.Client()

# Initialize SentenceTransformer model for embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Create or get collection
collection = chroma_client.create_collection(name="documents")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path: str) -> str:
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Function to extract text from TXT files
def extract_text_from_txt(txt_path: str) -> str:
    with open(txt_path, 'r') as file:
        return file.read()

# Function to ingest documents into ChromaDB
def ingest_document(file_path: str, file_type: str):
    try:
        # Extract text based on file type
        if file_type == "pdf":
            text = extract_text_from_pdf(file_path)
        elif file_type == "docx":
            text = extract_text_from_docx(file_path)
        elif file_type == "txt":
            text = extract_text_from_txt(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Generate embeddings for the extracted text
        embeddings = model.encode([text])

        # Insert document into the ChromaDB collection
        collection.add(documents=[text], metadatas=[{"file_path": file_path}], embeddings=embeddings)

        print(f"Document {file_path} ingested successfully into the collection")

    except Exception as e:
        print(f"Error ingesting document {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Error during document ingestion")
