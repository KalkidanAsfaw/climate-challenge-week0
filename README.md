# climate-challenge-week0

KAIM Climate Challenge — Week 0 project.

## Reproducing the Environment

### Prerequisites
- Python 3.10+
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/KalkidanAsfaw/climate-challenge-week0.git
   cd climate-challenge-week0
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
├── .vscode/          # VS Code settings
├── .github/
│   └── workflows/
│       └── unittests.yml   # CI pipeline
├── .gitignore
├── requirements.txt
├── README.md
├── src/              # Source code
├── notebooks/        # Jupyter notebooks
├── tests/            # Unit tests
└── scripts/          # Utility scripts
```

## Running Tests

```bash
pytest tests/ --verbose
```
