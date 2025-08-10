from mcp.server import ContextWebMCP

def test_server_creation():
    """Test that the MCP server can be created"""
    mcp = ContextWebMCP()
    assert mcp.name == "context-web"
    assert mcp.version == "0.0.1"

def test_ping_request():
    """Test with a ping request"""
    mcp = ContextWebMCP()    
    test_request = {"method": "ping"}
    response = mcp.handle_request(test_request)
    assert response["status"] == "pong"
    assert response["server"] == "context-web"
    assert response["version"] == "0.0.1"

def test_scan_directory_request():
    """Test scanning a directory"""
    mcp = ContextWebMCP()
    test_request = {"method": "scan_directory", "path": "."}
    response = mcp.handle_request(test_request)
    
    assert response["method"] == "scan_directory"
    assert response["files_found"] >= 0  # Expecting at least 0 files
    assert response["directory"] == "."

def test_unknown_request():
    """Test with unknown request"""
    mcp = ContextWebMCP()
    unknown_request = {"method": "dance"}
    response = mcp.handle_request(unknown_request)
    assert response["status"] == "error"
    assert "not supported" in response["message"]