# Quick Start Guide: Automated Testing & CI/CD
## Group-Saisys Project

**For Team Members** - Get up and running in 5 minutes

---

## 📋 Checklist: Set Up Your Machine (First Time Only)

- [ ] Clone repository: `git clone https://github.com/ragi0313/Group-Saisys.git`
- [ ] Enter directory: `cd Group-Saisys`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate it:
  - **Windows**: `venv\Scripts\activate`
  - **Mac/Linux**: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements-dev.txt`
- [ ] Install git hooks: `pre-commit install`
- [ ] Verify setup: `pytest tests/ -v` (should pass)

---

## 🔄 Daily Development Workflow

### 1️⃣ Pull Latest Code
```bash
git pull origin main
```

### 2️⃣ Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 3️⃣ Make Your Changes
Edit files, write code, add tests

### 4️⃣ Run Tests Locally
```bash
pytest tests/ -v
```

### 5️⃣ Commit Your Changes
```bash
git add .
git commit -m "[feat]: Describe your change"
# Pre-commit hooks automatically run and fix issues
```

### 6️⃣ Push to GitHub
```bash
git push origin feature/your-feature-name
```

### 7️⃣ Create Pull Request
- Go to GitHub.com
- Create PR from your branch to `main`
- GitHub Actions automatically runs tests
- Wait for ✅ all checks to pass

### 8️⃣ Get Code Review & Merge
- Team reviews your code
- After approval, merge PR
- Done! 🎉

---

## ⚡ Quick Commands Reference

| Need | Command |
|------|---------|
| Run all tests | `pytest tests/ -v` |
| Run specific test | `pytest tests/test_graphhopper.py::TestGeocoding -v` |
| Check code style | `black --check graphhopper.py` |
| Auto-fix style | `black graphhopper.py` |
| Run linter | `flake8 graphhopper.py` |
| Check coverage | `pytest tests/ --cov --cov-report=html` |
| Fix imports | `isort graphhopper.py` |
| Run all checks | `pre-commit run --all-files` |

---

## ❌ Something Went Wrong?

### Tests Failing Locally?
```bash
# Pull latest
git pull origin main

# Create fresh environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate

# Reinstall everything
pip install -r requirements-dev.txt

# Run tests again
pytest tests/ -v
```

### Pre-commit Hook Blocking Commit?
```bash
# Let it auto-fix formatting issues
git add .
# Try commit again

# If still blocked, check what's wrong
pre-commit run --all-files

# Manually fix issues, then try again
git add .
git commit -m "message"
```

### GitHub Actions Test Failing But Passes Locally?
```bash
# Test on multiple Python versions
python3.8 -m pytest tests/
python3.9 -m pytest tests/
python3.10 -m pytest tests/
python3.11 -m pytest tests/

# Or check GitHub Actions logs for more details
# Go to: https://github.com/ragi0313/Group-Saisys/actions
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `DEVASC_PROJECT_ACTIVITY_4.md` | Project overview, features, team roles |
| `CI_CD_DEPLOYMENT_GUIDE.md` | Detailed pipeline documentation |
| `TESTING_GUIDE.md` | How to write and run tests |
| `requirements-dev.txt` | All development tools needed |
| `.github/workflows/ci-cd.yml` | GitHub Actions workflow |
| `.flake8` | Linting rules |
| `pyproject.toml` | Code formatting and testing config |
| `.pre-commit-config.yaml` | Local git hooks |

---

## 🚀 What Gets Automated?

### Every Time You Push:
1. ✅ **Code style check** (Black, Flake8, isort)
2. ✅ **Tests on Python 3.8-3.11**
3. ✅ **Security scanning** (Bandit, Safety)
4. ✅ **Import validation**
5. ✅ **Coverage reporting**

### On Main Branch Only:
6. ✅ **Automatic deployment** (if all checks pass)

**If any check fails**: PR is blocked. Fix the issue, push again, and checks re-run.

---

## 💡 Tips & Tricks

### Before Every Commit, Run:
```bash
pytest tests/ -v && black graphhopper.py && flake8 graphhopper.py
```

### See Which Lines Aren't Tested:
```bash
pytest tests/ --cov --cov-report=term-missing
```

### Test Only Your Changes:
```bash
# Test just the test class for your feature
pytest tests/test_graphhopper.py::TestYourFeature -v
```

### Make Tests Run Faster:
```bash
# Run tests in parallel
pytest tests/ -n auto  # Requires: pip install pytest-xdist
```

---

## 📞 Need Help?

1. **Check the docs**:
   - `CI_CD_DEPLOYMENT_GUIDE.md` - Pipeline questions
   - `TESTING_GUIDE.md` - Test writing questions
   - `DEVASC_PROJECT_ACTIVITY_4.md` - Project overview

2. **Check GitHub Actions**:
   - Go to: https://github.com/ragi0313/Group-Saisys/actions
   - See exactly what failed and why

3. **Ask the team**:
   - DevOps Engineer for CI/CD questions
   - QA Lead for testing questions
   - Any team member for general help

---

## ✨ You're Ready!

You now have:
- ✅ Automated testing on every commit
- ✅ Code quality enforcement
- ✅ Security scanning
- ✅ Automatic deployments
- ✅ Peace of mind! 😌

**Happy coding!**

---

**Questions?** See `CI_CD_DEPLOYMENT_GUIDE.md` Troubleshooting section
