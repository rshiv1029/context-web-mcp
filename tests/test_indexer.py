import os, sqlite3

from mcp.indexer import FileIndexer
from mcp.database import ContextDatabase

def test_indexer_creation():
    indexer = FileIndexer()
    assert indexer is not None

def test_scan_current_directory():
    """Test scanning the current directory for files."""
    indexer = FileIndexer()
    files = indexer.scan_directory(".")
    
    assert isinstance(files, list)
    for file in files:
        assert "name" in file
        assert "path" in file
        assert "size" in file
        assert "modified_time" in file

def test_index_and_save_files():
    """ Test indexer can save files to the database """
    test_db_path = "data/test_indexer.db"
    
    # Clean up if exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Create indexer and database
    db = ContextDatabase(test_db_path)
    indexer = FileIndexer()
    
    saved_response = indexer.index_and_save_files(".", db)
    assert "files_found" in saved_response
    assert "files_saved" in saved_response
    assert "directory" in saved_response
    assert saved_response["files_found"] >= 0
    assert saved_response["files_saved"] >= 0
    assert saved_response["directory"] == "."
    
    # Clean up
    os.remove(test_db_path)

def test_read_file_content():
    """Test reading file content"""
    indexer = FileIndexer()
    
    # Test with a file we know exists
    content = indexer.read_file_content("tests/test_indexer.py")
    
    assert isinstance(content, str)
    assert len(content) > 0
    assert "def test_" in content  # Should contain test functions

def test_pipeline():
    """Test the full pipeline of scanning, indexing, and saving files."""
    test_db_path = "data/test_pipeline.db"
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Create indexer and database
    indexer = FileIndexer()
    database = ContextDatabase(test_db_path)
    
    # Index current directory (should include our test files)
    result = indexer.index_and_save_files(".", database)
    
    assert result['files_found'] > 0
    assert result['files_saved'] > 0
    
    # Check that content was actually saved
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM files WHERE content IS NOT NULL AND content != ''")
    files_with_content = cursor.fetchall()
    conn.close()
    
    assert len(files_with_content) > 0
    
    # Check that at least one file was indexed with content
    python_files = [f for f in files_with_content if f[0].endswith('.py')]
    text_files = [f for f in files_with_content if f[0].endswith('.txt')]
    markdown_files = [f for f in files_with_content if f[0].endswith('.md')]
    assert len(python_files) == 0
    assert len(text_files) == 1
    assert len(markdown_files) == 1
    
    os.remove(test_db_path)