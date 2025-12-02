# Git Commands for Project Management

## Initial Setup (One-time)

1. **Initialize Git Repository**
   ```bash
   git init
   ```

2. **Set Up Remote Repository**
   ```bash
   # Add remote origin (choose either HTTPS or SSH)
   git remote add origin https://github.com/your-username/your-repo-name.git
   # OR for SSH
   # git remote add origin git@github.com:your-username/your-repo-name.git
   ```

## Regular Workflow

1. **Check Status**
   ```bash
   git status
   ```

2. **Stage Changes**
   ```bash
   # Stage specific file
   git add path/to/file
   
   # Stage all changes
   git add .
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Your descriptive commit message"
   ```

4. **Pull Latest Changes**
   ```bash
   git pull origin main  # or your branch name
   ```

5. **Push Changes**
   ```bash
   # First push to a new branch
   git push -u origin main
   
   # Subsequent pushes
   git push
   ```

## Branch Management

1. **Create New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Switch Branches**
   ```bash
   git checkout branch-name
   ```

3. **List Branches**
   ```bash
   git branch
   ```

4. **Merge Branches**
   ```bash
   git checkout main
   git merge feature/your-feature-name
   ```

## Common Issues

1. **Undo Local Changes**
   ```bash
   # Discard changes in working directory
   git restore <file>
   
   # Reset to last commit (DANGEROUS: discards all changes)
   git reset --hard HEAD
   ```

2. **Update Remote URL**
   ```bash
   git remote set-url origin new-remote-url
   ```

3. **View Commit History**
   ```bash
   git log --oneline
   ```

## .gitignore Setup (Recommended)
Create a `.gitignore` file in your root directory with these common entries:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env
.venv

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs and databases
*.log
*.sqlite3

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

## First Time Setup (Complete Example)

```bash
# Navigate to project directory
cd "c:\Users\saran\OneDrive\Dokumen\Genai assignment 1"

# Initialize repository
git init

# Add all files (after creating .gitignore)
git add .

# Make first commit
git commit -m "Initial commit"

# Add remote repository
git remote add origin https://github.com/your-username/your-repo-name.git

# Push to main branch
git push -u origin main
```

## Updating Your Repository

```bash
# Add all changes
git add .

# Commit with message
git commit -m "Update: Your descriptive message"

# Push changes
git push
```
