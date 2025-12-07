# CI/CD Pipeline & Deployment Guide
## Group-Saisys Project

**Document Version**: 1.0  
**Last Updated**: December 7, 2025  
**Status**: ACTIVE

---

## Table of Contents

1. [Overview](#overview)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Getting Started](#getting-started)
4. [Development Workflow](#development-workflow)
5. [CI/CD Pipeline Details](#cicd-pipeline-details)
6. [Deployment Process](#deployment-process)
7. [Troubleshooting](#troubleshooting)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Overview

The Group-Saisys project uses **GitHub Actions** for continuous integration and deployment. This automated pipeline ensures code quality, runs comprehensive tests, and automatically deploys validated code to production.

### Key Benefits:

- ✅ **Automated Testing**: Runs on every commit/PR
- ✅ **Code Quality Enforcement**: Black formatting, Flake8 linting
- ✅ **Security Scanning**: Vulnerability detection before deployment
- ✅ **Multi-Version Testing**: Python 3.8-3.11 compatibility
- ✅ **Coverage Tracking**: Maintains code coverage metrics
- ✅ **Automatic Deployment**: Deploys to production on main branch

---

## Pipeline Architecture

### Workflow Overview:

```
┌─────────────────┐
│ Developer Commit│
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Git Push  │
    └────┬─────┘
         │
    ┌────▼──────────────┐
    │ GitHub Actions    │
    │ CI/CD Pipeline    │
    └────┬──────────────┘
         │
    ┌────▼────────────────────────────────┐
    │ Job 1: Code Quality Checks          │
    │ - Black formatter                   │
    │ - Flake8 linting                    │
    │ - isort import checking             │
    └────┬─────────────────────────────────┘
         │
    ┌────▼────────────────────────────────┐
    │ Job 2: Unit Tests & Coverage        │
    │ - Test on Python 3.8-3.11           │
    │ - Generate coverage reports         │
    │ - Upload to Codecov                 │
    └────┬─────────────────────────────────┘
         │
    ┌────▼────────────────────────────────┐
    │ Job 3: Security Scanning            │
    │ - Bandit vulnerability scan         │
    │ - Safety dependency check           │
    └────┬─────────────────────────────────┘
         │
    ┌────▼────────────────────────────────┐
    │ Job 4: Build & Integration Check    │
    │ - Verify imports                    │
    │ - Syntax validation                 │
    └────┬─────────────────────────────────┘
         │
    ┌────▼────────────────────────────────┐
    │ All Jobs Passed?                    │
    └────┬──────────────┬──────────────────┘
         │ YES         │ NO
    ┌────▼──────┐  ┌──▼──────────────┐
    │ Deploy     │  │ Block Merge     │
    │ (Main)     │  │ Show Error      │
    └───────────┘  └─────────────────┘
```

### Parallel Jobs:

The pipeline runs multiple jobs in parallel to save time:
- **Code Quality** and **Security** checks run first (fast)
- **Tests** run independently on all Python versions
- **Build** check runs after quality/tests pass
- **Deployment** only runs on main branch after all checks pass

**Total Time**: ~3-5 minutes for complete pipeline

---

## Getting Started

### 1. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/ragi0313/Group-Saisys.git
cd Group-Saisys

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 2. Configure Git

```bash
# Set up git configuration for consistent commits
git config user.name "Your Name"
git config user.email "your.email@example.com"

# (Optional) Set up SSH for GitHub authentication
# See: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### 3. Verify Setup

```bash
# Test that all tools are installed
python -m pytest --version
black --version
flake8 --version
pre-commit --version

# Run tests locally
pytest tests/ -v

# Run code quality checks
black --check graphhopper.py tests/
flake8 graphhopper.py tests/
isort --check-only graphhopper.py tests/
```

---

## Development Workflow

### Standard Development Process:

#### Step 1: Create Feature Branch

```bash
# Pull latest changes
git pull origin main

# Create feature branch (use descriptive name)
git checkout -b feature/add-new-route-option
# or
git checkout -b bugfix/fix-api-timeout-issue
```

#### Step 2: Make Changes

```bash
# Edit files, add features, or fix bugs
# Example:
echo "# New feature" >> graphhopper.py

# Run tests locally to verify changes
pytest tests/ -v --cov

# Pre-commit hooks will run before commit
git add graphhopper.py
git commit -m "[feat]: Add new route option"
```

#### Step 3: Pre-commit Hook Execution

**Automatic checks that run before your commit:**

```
→ Checking trailing whitespace
→ Fixing end-of-file issues
→ Checking YAML syntax
→ Running Black formatter
→ Sorting imports with isort
→ Running Flake8 linter
→ Type checking with mypy
→ Checking docstring coverage
```

If any check fails:
- Fix the issues (Black/isort will auto-fix formatting)
- Stage the changes: `git add .`
- Try commit again

#### Step 4: Push to GitHub

```bash
# Push feature branch
git push origin feature/add-new-route-option
```

**GitHub Actions will automatically:**
1. Run code quality checks
2. Execute unit tests on Python 3.8-3.11
3. Perform security scanning
4. Generate coverage reports
5. Post results on your PR

#### Step 5: Create Pull Request

```
On GitHub:
1. Create Pull Request from your feature branch to main
2. Add description of changes
3. Request code review from team
4. GitHub Actions checks will appear in PR
```

**Branch Protection Rules:**
- ✅ All CI/CD checks must pass
- ✅ At least 1 code review required
- ✅ Cannot merge with failing tests

#### Step 6: Code Review & Merge

```
After approval and all checks pass:
1. Squash and merge PR
2. Delete feature branch
3. Pull updated main locally
```

---

## CI/CD Pipeline Details

### Job 1: Code Quality Checks

**Purpose**: Enforce consistent code style across the team

**Tools**:
- **Black**: Auto-formatting (removes style debates)
- **Flake8**: Linting (catches bugs and style violations)
- **isort**: Import organization (consistent ordering)

**Configuration**:
- Max line length: 100 characters
- Python versions: 3.8+
- See `.flake8` and `pyproject.toml` for detailed config

**Exit Condition**: ❌ Fails if code doesn't match style guidelines

### Job 2: Unit Tests & Coverage

**Purpose**: Verify code functionality and catch regressions

**Scope**:
- Runs on Python 3.8, 3.9, 3.10, 3.11
- Tests location: `tests/` directory
- Framework: pytest
- Mocking: unittest.mock

**Coverage Requirements**:
- Minimum 80% code coverage
- Reports uploaded to Codecov
- HTML coverage report generated

**Test Categories**:
```
├── test_graphhopper.py
│   ├── Helper Functions (km_to_miles, formatting, etc.)
│   ├── Geocoding (location lookup and error handling)
│   ├── Route Calculations (distance, time, waypoints)
│   ├── Cost Calculations (fuel, calories, e-bike)
│   ├── Error Handling (API errors, timeouts, malformed data)
│   └── Integration Tests (end-to-end workflows)
```

**Exit Condition**: ❌ Fails if any test fails or coverage < 80%

### Job 3: Security Scanning

**Purpose**: Detect security vulnerabilities before deployment

**Tools**:
- **Bandit**: Scans for security issues in Python code
- **Safety**: Checks dependencies for known vulnerabilities

**Checks**:
- Hardcoded passwords/secrets (fails loudly)
- Unsafe functions usage
- SQL injection risks
- Known CVEs in dependencies

**Exit Condition**: ⚠️ Warnings reported (doesn't fail, for now)

### Job 4: Build & Integration Check

**Purpose**: Verify application builds and imports correctly

**Checks**:
- Python syntax validation
- Module imports work
- No circular dependencies

**Exit Condition**: ❌ Fails if app doesn't import properly

### Job 5: Test Report Generation

**Purpose**: Publish test results visible on GitHub

**Output**:
- Results appear in PR as comment
- Artifact download of detailed reports
- Coverage badges in README

### Job 6: Deployment (Main Branch Only)

**Purpose**: Automatically deploy validated code

**Conditions**:
- ✅ Only runs when pushed to `main` branch
- ✅ All previous jobs must pass
- ✅ Cannot be run on PRs

**Deployment Steps**:
1. Verify all checks passed
2. Package application files
3. Archive deployment artifact (30-day retention)
4. Post deployment notification

---

## Deployment Process

### Automatic Deployment

**Trigger**: When code is merged to `main` branch

```
main branch update → All tests pass → Auto-deployment
```

**Deployment Package Contents**:
```
dist/
├── graphhopper.py
├── requirements.txt
└── README.md
```

**Deployment Steps**:
1. Extract deployment package
2. Install dependencies: `pip install -r requirements.txt`
3. Verify imports and syntax
4. Application ready for use

### Manual Deployment (if needed)

```bash
# Download artifact from GitHub Actions
# Or manually run:

cd dist/
pip install -r requirements.txt
python graphhopper.py
```

### Rollback Process

If deployment has issues:

```bash
# Revert to previous commit
git revert <commit-hash>
git push origin main

# This will trigger automated rollback deployment
```

---

## Troubleshooting

### Scenario 1: Pre-commit Hook Failing

**Problem**: Cannot commit changes due to pre-commit hook failure

**Solution**:
```bash
# Check which hook failed
pre-commit run --all-files

# Auto-fix formatting issues
black graphhopper.py tests/
isort graphhopper.py tests/

# Try commit again
git add .
git commit -m "Your message"

# If still failing, check .flake8 config
# May need to manually fix linting issues
```

### Scenario 2: GitHub Actions Tests Failing

**Problem**: Tests pass locally but fail on GitHub Actions

**Common Causes**:
- Different Python version
- Environment variables missing
- Timing/race condition in tests
- Mock setup incomplete

**Solution**:
```bash
# Test on all Python versions locally
python3.8 -m pytest tests/
python3.9 -m pytest tests/
python3.10 -m pytest tests/
python3.11 -m pytest tests/

# Check for API key or secrets
echo $GRAPHHOPPER_API_KEY  # Should print your key

# Check test isolation
pytest tests/ -v --tb=long
```

### Scenario 3: Coverage Below Threshold

**Problem**: Code coverage is below 80% requirement

**Solution**:
```bash
# Generate coverage report with missing lines
pytest tests/ --cov --cov-report=html --cov-report=term-missing

# Open htmlcov/index.html to see which lines need coverage
# Add tests for uncovered code in tests/

# Re-run coverage check
pytest tests/ --cov --cov-fail-under=80
```

### Scenario 4: Flake8 Complains About Valid Code

**Problem**: Flake8 reports false positive

**Solution**:
```bash
# Add exception to .flake8 config
# Example: Add E501 (line too long) to ignore list

# Or add comment to specific line:
long_line = "..." # noqa: E501

# Or disable for entire file:
# flake8: noqa

# See .flake8 file for configuration
```

### Scenario 5: Dependency Conflicts

**Problem**: `pip install -r requirements-dev.txt` fails

**Solution**:
```bash
# Create fresh virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Check for conflicts
pip check
```

---

## Monitoring & Maintenance

### View Pipeline Status

**GitHub Actions Dashboard**:
```
https://github.com/ragi0313/Group-Saisys/actions
```

**View Results**:
- Click on workflow run
- See detailed logs for each job
- Download artifacts (test reports, coverage, security)

### Code Coverage Tracking

**Codecov Integration**:
```
https://codecov.io/github/ragi0313/Group-Saisys
```

**Coverage Badge**:
```markdown
![Coverage](https://codecov.io/gh/ragi0313/Group-Saisys/branch/main/graph/badge.svg)
```

### Test Artifacts Retention

- **Test Results**: Retained for 90 days
- **Deployment Package**: Retained for 30 days
- **Security Reports**: Retained for 60 days

### Periodic Maintenance

**Weekly**:
- Review failed test results
- Check for security warnings
- Monitor coverage trends

**Monthly**:
- Update dependencies: `pip install --upgrade -r requirements-dev.txt`
- Review and update pre-commit hooks: `pre-commit autoupdate`
- Check Python version compatibility

**Quarterly**:
- Review and optimize CI/CD configuration
- Update test suite for new features
- Audit security scanning rules

### Performance Optimization

**Current Pipeline Time**: ~3-5 minutes

**Optimization Opportunities**:
- Cache pip dependencies (already enabled)
- Parallelize tests across workers
- Skip unnecessary jobs based on file changes
- Use faster linting checks on PRs vs main

---

## Best Practices

### Commit Messages

```
Format: [type]: description

Types:
- [feat]: New feature
- [bugfix]: Bug fix
- [docs]: Documentation
- [test]: Test addition/update
- [refactor]: Code refactoring
- [perf]: Performance improvement
- [chore]: Dependency/config update

Example:
[feat]: Add route optimization algorithm
[bugfix]: Fix timezone handling in duration calculation
[test]: Add tests for calorie calculation
```

### Pull Request Guidelines

1. **Descriptive Title**: What does this PR do?
2. **Clear Description**: Why is this change needed?
3. **Linked Issues**: Reference related issues (#123)
4. **Tests Added**: New features must include tests
5. **Update Docs**: Update README if behavior changes

### Testing Standards

1. **Test Coverage**: Minimum 80% for new code
2. **Meaningful Tests**: Test behavior, not implementation
3. **Clear Names**: Test names should describe what they test
4. **Fixtures**: Use conftest.py for shared test utilities
5. **Mocking**: Mock external dependencies (APIs)

### Code Review Checklist

- [ ] Code passes all CI/CD checks
- [ ] Tests are added for new features
- [ ] Documentation is updated
- [ ] No hardcoded secrets/keys
- [ ] Code follows style guidelines
- [ ] Performance impact acceptable
- [ ] Security implications reviewed

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [Pre-commit Framework](https://pre-commit.com/)
- [Codecov Documentation](https://docs.codecov.io/)

---

**End of CI/CD Pipeline Documentation**

For questions or issues, contact the DevOps team or create a GitHub issue.
