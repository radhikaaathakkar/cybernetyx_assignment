from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from pathlib import Path

# Initialize FastAPI app
app = FastAPI()

# Directory to store uploaded files temporarily
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/ingest/")
async def ingest(file: UploadFile = File(...)):
    from app.ingest import ingest_document  # Local import to avoid circular import
    
    try:
        # Save the uploaded file temporarily to disk
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Determine file type based on extension
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension not in ["pdf", "docx", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Call the ingest_document function to process the file and ingest it
        ingest_document(file_path=str(file_path), file_type=file_extension)

        # Return success message
        return {"message": f"Document '{file.filename}' ingested successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optionally, remove the file after ingestion
        if os.path.exists(file_path):
            os.remove(file_path)
