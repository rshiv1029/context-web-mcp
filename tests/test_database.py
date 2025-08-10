import os, sqlite3
from mcp.database import ContextDatabase

def test_database_initialization():
    """ Test database initialization and table creation """
    test_db_path = "data/test.db"
    
    # Clean up any existing test database if needed
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = ContextDatabase(db_path=test_db_path)
    assert os.path.exists(test_db_path), "Database file should be created"
    
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(files)")
    columns = cursor.fetchall()
    conn.close()
    
    # Should have 8 columns
    assert len(columns) == 8
    
    # Check column names
    column_names = [col[1] for col in columns]  # col[1] is the column name
    expected_columns = ['id', 'path', 'name', 'size', 'modified_time', 'indexed_at', 'content_hash', 'content']
    
    for expected_col in expected_columns:
        assert expected_col in column_names
        
    # Clean up
    os.remove(test_db_path)
    
def test_save_file():
    """Test saving a file to database"""
    test_db_path = "data/test_save.db"
    
    # Clean up if exists
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = ContextDatabase(test_db_path)
    
    # Test file info
    file_info = {
        'path': '/test/file.txt',
        'name': 'file.txt',
        'size': 1024,
        'modified_time': '2025-01-01T12:00:00',
        'content': 'This is a test file content.'
    }
    
    file_id = db.save_file(file_info)
    assert file_id is not None
    assert file_id > 0
    
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM files WHERE id = ?", (file_id,))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    assert result[0] == 'This is a test file content.'
    
    # Clean up
    os.remove(test_db_path)