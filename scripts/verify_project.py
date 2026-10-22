import os
import re
import subprocess
import glob

def get_files_and_loc(src_dirs):
    loc = 0
    files = []
    for d in src_dirs:
        for root, _, filenames in os.walk(d):
            if "__pycache__" in root or "node_modules" in root or "dist" in root:
                continue
            for f in filenames:
                if f.endswith(('.py', '.ts', '.js', '.html', '.css', '.tsx', '.jsx')):
                    filepath = os.path.join(root, f)
                    files.append(filepath)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                            loc += len([l for l in lines if l.strip()])
                    except:
                        pass
    return len(files), loc

def get_test_files(test_dirs):
    files = []
    for d in test_dirs:
        for root, _, filenames in os.walk(d):
            if "__pycache__" in root or "node_modules" in root:
                continue
            for f in filenames:
                if f.startswith('test_') or f.endswith('.test.ts') or f.endswith('.spec.ts'):
                    files.append(os.path.join(root, f))
    return len(files)

def get_git_commits():
    try:
        output = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], stderr=subprocess.STDOUT)
        return int(output.decode('utf-8').strip())
    except:
        return 0

def check_secrets():
    # Simple heuristic
    patterns = [r'(?i)api[_-]?key', r'(?i)secret', r'(?i)password\s*=', r'(?i)token\s*=']
    found = 0
    for root, dirs, filenames in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules', 'dist', '.venv', '.pytest_cache')]
        for f in filenames:
            if not f.endswith(('.py', '.ts', '.js', '.json', '.env', '.md')): continue
            # Exclude our own scripts
            if "verify_project" in f: continue
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for p in patterns:
                        if re.search(p, content):
                            found += 1
            except:
                pass
    return found

def main():
    src_dirs = ['python_app', 'src', 'dist']
    num_files, loc = get_files_and_loc(src_dirs)
    
    num_test_files = get_test_files(['tests', 'src'])
    
    commits = get_git_commits()
    
    secrets = check_secrets()
    
    print("========================================")
    print("PROJECT EVALUATION")
    print(f"Production LOC: {loc}")
    print(f"Production files: {num_files}")
    print(f"Git commits: {commits}")
    print(f"Test specification files: {num_test_files}")
    print(f"Secrets found: {secrets}")
    print("========================================")

if __name__ == '__main__':
    main()
