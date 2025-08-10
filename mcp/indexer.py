import os

from datetime import datetime

class FileIndexer:
    def scan_directory(self, path):
        """
        Scans the given directory and returns file info.
        """
        files_found = []
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a valid directory.")
        
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                files_found.append({
                    "name": filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "modified_time": datetime.fromtimestamp(os.path.getmtime(file_path)),
                    "content": self.read_file_content(file_path)
                })
        
        return files_found

    def index_and_save_files(self, path, database):
        """
        Indexes and saves file information to the database.
        """
        files = self.scan_directory(path)
        saved_count = 0
        
        for file_info in files:
            try:
                file_id = database.save_file(file_info)
                if file_id:
                    saved_count += 1
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e)
                }
        return {
            "files_found": len(files),
            "files_saved": saved_count,
            "directory": path
        }
        
    def read_file_content(self, file_path: str) -> str:
        """Read content from a file safely"""
        try:
            # Only read text-based files
            if file_path.lower().endswith(('.txt', '.py', '.md', '.json', '.csv', '.yml', '.yaml')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"[Binary file: {os.path.basename(file_path)}]"
        except Exception as e:
            return f"[Error reading file: {str(e)}]"