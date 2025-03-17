#!/bin/bash
# Script to sync your local project with GitHub

# Navigate to your project directory
cd /Users/goose/Downloads/mcp-rag-chatbot || { echo "Error: Project directory not found"; exit 1; }

# Check if git is initialized
if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
  git remote add origin https://github.com/Goose4500/mcp-rag-chatbot.git
else
  echo "Git repository already initialized."
fi

# Fetch the latest from GitHub
echo "Fetching latest code from GitHub..."
git fetch origin

# Backup local changes if needed
TIMESTAMP=$(date +%Y%m%d%H%M%S)
mkdir -p .backup
cp -r * .backup/backup_$TIMESTAMP/

# Reset to match GitHub state
echo "Updating local files to match GitHub..."
git checkout -B main
git reset --mixed origin/main

# List any differences
echo -e "\nFiles differing from GitHub version:"
git status

# Instructions for the user
echo -e "\n===== NEXT STEPS ====="
echo "1. Review any untracked or modified files listed above"
echo "2. Add and commit changes you want to keep:"
echo "   git add ."
echo "   git commit -m \"Your message\""
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo "4. Run your application:"
echo "   python app.py"
echo -e "\nA backup of your files is stored in .backup/backup_$TIMESTAMP/"
