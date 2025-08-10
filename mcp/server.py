from mcp.indexer import FileIndexer

class ContextWebMCP:
    def __init__(self):
        self.name = "context-web"
        self.version = "0.0.1"
        print(f"ContextWebMCP initialized with name: {self.name} and version: {self.version}")
        
    def handle_request(self, request):
        """Handle incoming requests"""
        print(f"Handling request: {request}")
        method = request.get('method', 'unknown')
        print(f" Received method: {method}")
        if method == "ping":
            return {
                "status": "pong", 
                "server": self.name, 
                "version": self.version
                }
        elif method == "scan_directory":
            path = request.get("path", ".")
            return self.handle_scan_request(path)
        else:
            return {
                "status": "error", 
                "message": f"Method {method} not supported"
            }
            
    def handle_scan_request(self, path):
        """Handle directory scan requests"""
        indexer = FileIndexer()
        try:
            files = indexer.scan_directory(path)
            return {
                "method": "scan_directory",
                "files_found": len(files),
                "directory": path,
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }

if __name__ == "__main__":
    mcp = ContextWebMCP()
    print(f"Running {mcp.name} version {mcp.version}")