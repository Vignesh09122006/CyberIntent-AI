# Contributing to CyberIntent-AI 🤝

We appreciate your interest in contributing to CyberIntent-AI! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/CyberIntent-AI.git
cd CyberIntent-AI
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

### 3. Setup Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Development Workflow

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import ordering
- Use mypy for type checking

### Before Committing
```bash
# Format code
black src/ models/ app/ api/ tests/

# Sort imports
isort src/ models/ app/ api/ tests/

# Check code quality
flake8 src/ models/ app/ api/ tests/

# Type checking
mypy src/ models/ app/ api/

# Run tests
pytest tests/ -v --cov
```

### Writing Tests
- Write unit tests for new features
- Aim for >80% code coverage
- Use pytest for testing
- Name test files as `test_*.py`

Example:
```python
def test_anomaly_detector_initialization():
    detector = AnomalyDetector()
    assert detector is not None

def test_anomaly_detection_with_valid_data(sample_data):
    detector = AnomalyDetector()
    scores = detector.predict(sample_data)
    assert len(scores) == len(sample_data)
```

## Commit Guidelines

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Build process, dependencies, or tooling changes

### Examples
```
feat: add intent predictor model

Implement ensemble-based intent prediction model using gradient boosting
and neural networks. Includes feature engineering and training pipeline.

Closes #42
```

```
fix: resolve memory leak in stream processor

Fix circular reference in event processor that was preventing garbage
collection of large event batches.

Fixes #38
```

## Pull Request Process

### Before Creating PR
1. Ensure all tests pass: `pytest tests/ -v`
2. Update documentation if needed
3. Add entry to CHANGELOG if applicable
4. Ensure code follows style guidelines

### Creating a PR
1. Push your branch to your fork
2. Create a pull request with a clear title
3. Describe the changes made
4. Reference any related issues (#123)
5. Ensure CI/CD checks pass

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added
- [ ] All tests passing
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Code is documented
- [ ] No breaking changes
```

## Documentation

### Code Documentation
```python
def predict_anomaly(data: np.ndarray, threshold: float = 0.7) -> np.ndarray:
    """
    Detect anomalies in the input data.
    
    Args:
        data: Input feature matrix of shape (n_samples, n_features)
        threshold: Anomaly detection threshold (0-1)
    
    Returns:
        Anomaly scores for each sample
    
    Raises:
        ValueError: If threshold is not in range [0, 1]
        
    Example:
        >>> detector = AnomalyDetector()
        >>> scores = detector.predict(data)
    """
```

### File Documentation
Add docstrings to modules:
```python
"""
Anomaly detection module.

This module provides anomaly detection capabilities using Isolation Forest
and other unsupervised learning techniques.
"""
```

## Creating Issues

### Bug Reports
```markdown
## Description
Clear description of the bug

## Reproduction Steps
1. Step one
2. Step two
3. Bug occurs

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: 
- Python Version:
- CyberIntent-AI Version:
```

### Feature Requests
```markdown
## Description
Clear description of the feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches
```

## Development Tips

### Running Specific Tests
```bash
# Single test file
pytest tests/test_models.py -v

# Single test function
pytest tests/test_models.py::test_anomaly_detection -v

# Tests matching pattern
pytest -k "anomaly" -v
```

### Debugging
```python
# Use ipdb for debugging
import ipdb; ipdb.set_trace()

# Or pytest debugging
pytest --pdb tests/test_models.py
```

### Performance Profiling
```bash
# Memory profiling
python -m memory_profiler scripts/train_models.py

# CPU profiling
py-spy record -o profile.svg python api/main.py
```

## Project Structure Guidelines

When adding new features:
- Models go in `models/`
- Data processing in `src/`
- API endpoints in `api/routes/`
- UI components in `app/components/`
- Tests mirror source structure in `tests/`

## Release Process

Only maintainers handle releases, following semantic versioning:
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

## Questions?

- 📧 Open an issue with [question] tag
- 💬 Start a discussion
- 📖 Check existing documentation

## Recognition

Contributors will be recognized in:
- Repository README
- Release notes
- Contributors list

Thank you for contributing to CyberIntent-AI! 🎉
