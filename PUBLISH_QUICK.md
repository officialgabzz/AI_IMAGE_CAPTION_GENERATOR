# Quick Publishing Reference

## ✅ BUILD SUCCESSFUL!

Your package has been built and is ready for publishing!

**Created Files:**
- `dist/ai_image_caption_generator-1.0.0.tar.gz` (20KB) - Source distribution
- `dist/ai_image_caption_generator-1.0.0-py3-none-any.whl` (14KB) - Wheel distribution

---

## 📦 Publishing to PyPI

### 1. Test on TestPyPI First (Recommended)

```bash
# Create account at https://test.pypi.org/account/register/

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# You'll be asked for:
# Username: __token__
# Password: (your TestPyPI API token - create one in account settings)

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ ai-image-caption-generator
```

### 2. Publish to Real PyPI

```bash
# Create account at https://pypi.org/account/register/

# Upload to PyPI
python -m twine upload dist/*

# You'll be asked for:
# Username: __token__
# Password: (your PyPI API token - create one in account settings)
```

**After publishing, anyone can install with:**
```bash
pip install ai-image-caption-generator
```

---

## 🔄 For Future Releases

When you want to publish updates:

```bash
# 1. Update version in src/__version__.py
# Edit: __version__ = "1.0.1"

# 2. Update CHANGELOG.md with changes

# 3. Clean old builds
rm -rf dist/ build/ *.egg-info

# 4. Rebuild
python -m build

# 5. Upload
python -m twine upload dist/*

# 6. Create git tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```

---

## 🐳 Docker Publishing

```bash
# Build image
docker build -t yourusername/ai-caption-generator:1.0.0 .

# Test locally
docker run -p 5000:5000 yourusername/ai-caption-generator:1.0.0

# Login to Docker Hub
docker login

# Push
docker push yourusername/ai-caption-generator:1.0.0
docker tag yourusername/ai-caption-generator:1.0.0 yourusername/ai-caption-generator:latest
docker push yourusername/ai-caption-generator:latest
```

---

## 🐙 GitHub Release

```bash
# 1. Commit everything
git add .
git commit -m "Release v1.0.0"
git push

# 2. Create tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 3. Create release on GitHub
# Go to: https://github.com/YOUR_USERNAME/REPO/releases/new
# - Choose tag: v1.0.0
# - Release title: "v1.0.0 - Initial Release"
# - Attach: dist/ai_image_caption_generator-1.0.0.tar.gz
# - Copy changelog from CHANGELOG.md
```

---

## 🔑 Getting PyPI API Tokens

### TestPyPI:
1. Go to https://test.pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: "ai-caption-generator"
4. Scope: "Entire account" (or specific project after first upload)
5. Copy token (starts with `pypi-`)
6. Save it securely!

### Real PyPI:
1. Go to https://pypi.org/manage/account/token/
2. Same steps as above

**Using tokens with twine:**
```bash
# Option 1: Interactive (paste when prompted)
python -m twine upload dist/*
# Username: __token__
# Password: pypi-YOURTOKENHERE

# Option 2: Using .pypirc file
# Create ~/.pypirc:
cat > ~/.pypirc << EOF
[pypi]
  username = __token__
  password = pypi-YOURTOKENHERE

[testpypi]
  username = __token__
  password = pypi-YOURTESTTOKENHERE
EOF

chmod 600 ~/.pypirc
```

---

## 📊 Post-Publishing Checklist

- [ ] Package appears on PyPI: https://pypi.org/project/ai-image-caption-generator/
- [ ] Test installation: `pip install ai-image-caption-generator`
- [ ] Update README badges with PyPI link
- [ ] Announce on social media
- [ ] Submit to Product Hunt, Hacker News, Reddit
- [ ] Write blog post about your project
- [ ] Monitor GitHub issues and PyPI downloads

---

## 🎯 What You Have Now

**Files Ready:**
- ✅ `pyproject.toml` - Modern Python packaging config
- ✅ `setup.py` - Backwards compatibility wrapper
- ✅ `MANIFEST.in` - Package file inclusion rules
- ✅ `Dockerfile` - Container image
- ✅ `docker-compose.yml` - Easy deployment
- ✅ `dist/` - Built distributions ready to upload
- ✅ `PUBLISHING_GUIDE.md` - Complete publishing guide
- ✅ `CHANGELOG.md` - Version history

**Files Renamed:**
- `setup.py` (old) → `setup_script.py` (interactive setup script)
- `setup.py` (new) → Minimal package configuration

---

## 💡 Quick Commands Summary

```bash
# Build package
python -m build

# Test upload
python -m twine upload --repository testpypi dist/*

# Real upload
python -m twine upload dist/*

# Docker build & push
docker build -t USERNAME/ai-caption-generator:1.0.0 .
docker push USERNAME/ai-caption-generator:1.0.0

# Run your setup script
python setup_script.py

# Run the app
python app.py
```

---

For complete details, see **PUBLISHING_GUIDE.md**! 🚀
