# Git Setup Instructions

This document explains how to connect your local repository to the GitHub remote repository.

## Prerequisites

- Git installed on your local machine
- Terminal or Command Prompt access

## Instructions

1. **Navigate to your project directory**
   
   ```bash
   cd /Users/goose/Downloads/mcp-rag-chatbot
   ```

2. **Initialize the local Git repository**
   
   ```bash
   git init
   ```

3. **Configure your repository to use the main branch (optional if you already have commits)**
   
   ```bash
   git checkout -b main
   ```

4. **Add all the files to the repository**
   
   ```bash
   git add .
   ```

5. **Commit the files**
   
   ```bash
   git commit -m "Initial commit"
   ```

6. **Add the remote GitHub repository**
   
   ```bash
   git remote add origin https://github.com/Goose4500/mcp-rag-chatbot.git
   ```

7. **Pull the remote repository first to avoid conflicts**
   
   ```bash
   git pull origin main --allow-unrelated-histories
   ```

8. **Push your local repository to GitHub**
   
   ```bash
   git push -u origin main
   ```

Now your local repository is connected to GitHub and all your code is backed up!

## Troubleshooting

If you encounter conflicts during the pull or push:

1. Resolve the conflicts in the affected files
2. Add the resolved files:
   ```bash
   git add <resolved-file-paths>
   ```
3. Commit the resolution:
   ```bash
   git commit -m "Resolve merge conflicts"
   ```
4. Try pushing again:
   ```bash
   git push -u origin main
   ```

If you have authentication issues, you might need to use a personal access token instead of a password when prompted.