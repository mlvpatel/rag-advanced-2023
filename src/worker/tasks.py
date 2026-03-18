from .celery_app import celery_app
from src.embeddings.chroma_utils import index_document_to_chroma
from src.api.db_utils import insert_document_record
import os
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_document(self, file_path: str, filename: str):
    """
    Background task to process and index a document.

    Correct order:
      1. Insert a DB record first to obtain a real integer file_id.
      2. Pass that file_id to Chroma so vector chunks carry the correct metadata.
      3. Clean up the temp file after successful indexing.
    """
    try:
        # Step 1: Create DB record and get a real integer file_id
        file_id = insert_document_record(filename)

        # Step 2: Embed and index into ChromaDB using the real file_id
        success = index_document_to_chroma(file_path, file_id)

        if success:
            # Step 3: Clean up temp file to prevent unbounded disk growth
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temp file: {file_path}")

            return {"status": "success", "file_id": file_id, "filename": filename}
        else:
            return {"status": "failed", "error": "Chroma indexing returned False"}

    except Exception as e:
        logger.error(f"process_document failed for {filename}: {e}")
        raise self.retry(exc=e)
