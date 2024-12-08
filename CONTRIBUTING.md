# Contributing to MemOS AI

First off, thank you for considering contributing to MemOS AI! It's people like you that make MemOS AI such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for MemOS AI. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**How Do I Submit A (Good) Bug Report?**

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots and animated GIFs if possible
* Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for MemOS AI, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**

* Check if there's already a package which provides that enhancement.
* Determine which repository the enhancement should be suggested in.
* Perform a cursory search to see if the enhancement has already been suggested.

**How Do I Submit A (Good) Enhancement Suggestion?**

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful
* List some other text editors or applications where this enhancement exists
* Include screenshots and animated GIFs if relevant

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python styleguide
* Include thoughtfully-worded, well-structured tests
* Document new code based on the Documentation Styleguide
* End all files with a newline

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🐎 `:racehorse:` when improving performance
    * 📝 `:memo:` when writing docs
    * 🐛 `:bug:` when fixing a bug
    * 🔥 `:fire:` when removing code or files
    * 💚 `:green_heart:` when fixing the CI build
    * ✅ `:white_check_mark:` when adding tests
    * 🔒 `:lock:` when dealing with security
    * ⬆️ `:arrow_up:` when upgrading dependencies
    * ⬇️ `:arrow_down:` when downgrading dependencies

### Python Styleguide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use [Black](https://github.com/psf/black) for code formatting
* Use [isort](https://pycqa.github.io/isort/) for import sorting
* Use [mypy](http://mypy-lang.org/) for static type checking
* Use [flake8](https://flake8.pycqa.org/) for linting

### Documentation Styleguide

* Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
* Reference functions, classes, and modules in backticks
* Use section headers: `##` for sections, `###` for subsections
* Place code blocks in triple backticks and specify the language
* Include docstrings for all public modules, functions, classes, and methods

## Development Process

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run the test suite
5. Update documentation
6. Submit a Pull Request

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/nostradamus23/memos-Framework.git
cd memos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=memos tests/

# Run specific test file
pytest tests/test_core.py
```

### Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy memos

# Linting
flake8 memos
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

## Recognition

Contributors who make significant and valuable contributions will be granted commit access to the project. 