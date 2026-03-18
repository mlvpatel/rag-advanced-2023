import pytest
from unittest.mock import MagicMock
from langchain_core.documents import Document

@pytest.fixture
def mock_chroma():
    """Mock ChromaDB vector store."""
    mock = MagicMock()
    # default behavior for similarity search
    mock.similarity_search.return_value = [
        Document(page_content="Test doc 1", metadata={"id": 1}),
        Document(page_content="Test doc 2", metadata={"id": 2})
    ]
    return mock

@pytest.fixture
def mock_documents():
    return [
        Document(page_content="Apple is a fruit", metadata={"category": "fruit"}),
        Document(page_content="Carrot is a vegetable", metadata={"category": "veg"}),
        Document(page_content="Banana is yellow", metadata={"category": "fruit"}),
    ]
