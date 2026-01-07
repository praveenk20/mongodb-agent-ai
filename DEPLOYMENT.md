# 🚀 Deployment Guide for MongoDB Agent Distribution

This guide provides step-by-step instructions for deploying the MongoDB Agent to GitHub and publishing it as a Python package.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- [x] Git installed and configured
- [x] GitHub account with access to `cisco-it-supply-chain` organization
- [x] Python 3.8+ installed
- [x] PyPI account (for package publishing)
- [x] Co-authors' names and email addresses

---

## 🔧 Step 1: Create New GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to https://github.com/organizations/cisco-it-supply-chain/repositories/new
2. Repository name: `mongodb_agent_distribution_general`
3. Description: "AI-powered agent for querying MongoDB databases using natural language"
4. Visibility: Choose **Public** or **Private** based on your requirements
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### Option B: Using GitHub CLI

```bash
gh repo create cisco-it-supply-chain/mongodb_agent_distribution_general \
  --public \
  --description "AI-powered agent for querying MongoDB databases using natural language"
```

---

## 🔄 Step 2: Update Remote and Push Code

Run these commands in your terminal:

```bash
# Navigate to your project directory
cd /Users/prakalam/mongodb-agent-public

# Remove old remote (if exists)
git remote remove origin

# Add new remote
git remote add origin https://github.com/cisco-it-supply-chain/mongodb_agent_distribution_general.git

# Stage all new files
git add -A

# Commit with co-authors
git commit -m "Initial commit: MongoDB Agent AI v1.0.0

This release includes:
- Natural language MongoDB query support
- Multi-LLM provider support (OpenAI, Anthropic, AWS Bedrock)
- Semantic model templates
- Complete documentation and examples
- Package distribution setup

Co-authored-by: [Co-Author Name 1] <email1@cisco.com>
Co-authored-by: [Co-Author Name 2] <email2@cisco.com>
Co-authored-by: [Co-Author Name 3] <email3@cisco.com>"

# Push to GitHub
git push -u origin main
```

**⚠️ Important:** Replace `[Co-Author Name]` and `<email@cisco.com>` with actual names and emails of your co-authors.

---

## 📦 Step 3: Build and Test Package Locally

Before publishing, test the package build:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# This creates:
# - dist/mongodb_agent_ai-1.0.0-py3-none-any.whl
# - dist/mongodb_agent_ai-1.0.0.tar.gz

# Check the package
twine check dist/*

# Test installation locally
pip install dist/mongodb_agent_ai-1.0.0-py3-none-any.whl
```

---

## 🌐 Step 4: Publish to PyPI

### 4.1 Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Register an account
3. Verify your email

### 4.2 Generate API Token

1. Log in to PyPI
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Token name: `mongodb-agent-ci`
5. Scope: Choose "Entire account" or specific project
6. Copy the token (starts with `pypi-`)

### 4.3 Add Secret to GitHub

1. Go to https://github.com/cisco-it-supply-chain/mongodb_agent_distribution_general/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Paste your PyPI token
5. Click "Add secret"

### 4.4 Manual Publishing (First Time)

```bash
# Upload to PyPI
twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your-pypi-token>
```

### 4.5 Automated Publishing via GitHub Actions

The package will automatically publish when you:

1. Create a new release on GitHub:
   ```bash
   # Tag the release
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. Or manually trigger the workflow:
   - Go to Actions tab in GitHub
   - Select "Publish to PyPI" workflow
   - Click "Run workflow"

---

## 👥 Step 5: Add Co-Authors for Future Commits

### Option A: Using Git Commit Template

```bash
# Set up commit template
git config commit.template .gitmessage

# Now when you commit:
git commit
# Edit the message and add co-authors at the bottom
```

### Option B: Direct Commit with Co-Authors

```bash
git commit -m "Your commit message

Co-authored-by: Name1 <email1@cisco.com>
Co-authored-by: Name2 <email2@cisco.com>"
```

### Option C: Create Git Alias

```bash
# Add to ~/.gitconfig
git config --global alias.cocommit '!f() { git commit -m "$1" -m "Co-authored-by: Name1 <email1@cisco.com>" -m "Co-authored-by: Name2 <email2@cisco.com>"; }; f'

# Usage
git cocommit "Your commit message"
```

---

## 🔐 Step 6: Configure Repository Settings

### Protected Branches

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

### Code Owners

The `CODEOWNERS` file has been created. To activate it:

1. Go to Settings → Code security and analysis
2. Enable "Code owners"

---

## 📊 Step 7: Verify Installation

After publishing, verify users can install:

```bash
# Install from PyPI
pip install mongodb-agent-ai

# Or with extras
pip install mongodb-agent-ai[openai,anthropic]

# Verify installation
mongodb-agent --version
```

---

## 🎉 Post-Deployment Checklist

- [ ] Repository created and code pushed
- [ ] All co-authors credited in initial commit
- [ ] Package built and tested locally
- [ ] PyPI account created and token generated
- [ ] Package published to PyPI
- [ ] GitHub Actions secrets configured
- [ ] CODEOWNERS file activated
- [ ] Branch protection rules set
- [ ] Installation verified from PyPI
- [ ] Documentation reviewed and accessible
- [ ] Team members have access to repository

---

## 🔄 Future Updates

To release new versions:

1. Update version in `setup.py` and `pyproject.toml`
2. Update CHANGELOG (if exists)
3. Commit changes with co-authors
4. Create and push a new tag:
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```
5. GitHub Actions will automatically publish to PyPI

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/cisco-it-supply-chain/mongodb_agent_distribution_general/issues
- Documentation: See `/docs` folder

---

## 📝 Quick Command Reference

```bash
# Push code
git remote add origin https://github.com/cisco-it-supply-chain/mongodb_agent_distribution_general.git
git push -u origin main

# Build package
python -m build

# Publish to PyPI
twine upload dist/*

# Create release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

**Happy Deploying! 🚀**
