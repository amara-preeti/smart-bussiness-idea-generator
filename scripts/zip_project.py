import os
import zipfile

def zip_project(output_filename):
    # Directories to exclude
    exclude_dirs = {'.venv', 'node_modules', '__pycache__', '.pytest_cache', '.vscode'}
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Exclude directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not any(ex in os.path.join(root, d) for ex in exclude_dirs)]
            
            for file in files:
                # Exclude any existing or output zip files
                if file.endswith('.zip') or file == output_filename:
                    continue
                file_path = os.path.join(root, file)
                # Ensure no excluded directory is part of the path
                parts = os.path.normpath(file_path).split(os.sep)
                if any(p in exclude_dirs for p in parts):
                    continue
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    zip_project('project_submission.zip')
    print('Project zipped successfully to project_submission.zip')

