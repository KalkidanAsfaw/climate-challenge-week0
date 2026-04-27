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

## Interactive Dashboard

An interactive Streamlit dashboard is available in `app/main.py`.
It visualises climate trends across five African countries to support
Ethiopia's COP32 position paper.

### Features

- **Country multi-select** — filter all charts by one or more countries
- **Year range slider** — zoom into any sub-period between 2015 and 2026
- **Variable selector** — switch between T2M, T2M_MAX, PRECTOTCORR, RH2M, WS2M
- **Trend chart** — interactive monthly-average line chart (Plotly)
- **Distribution boxplot** — side-by-side boxplots per country
- **Summary statistics** — mean / median / std tables and extreme-heat bar chart

### Running Locally

1. Install dependencies (streamlit and plotly are included):
   ```bash
   pip install -r requirements.txt
   ```

2. Place the cleaned CSV files in `data/` (gitignored):
   ```
   data/ethiopia_clean.csv
   data/kenya_clean.csv
   data/nigeria_clean.csv
   data/sudan_clean.csv
   data/tanzania_clean.csv
   ```

3. Launch the app from the project root:
   ```bash
   streamlit run app/main.py
   ```

4. Open the URL printed in the terminal (default: `http://localhost:8501`).

### Deploying to Streamlit Community Cloud

1. Push this branch to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select the repository, branch `dashboard-dev`, and set **Main file path** to `app/main.py`.
4. Add any required secrets in the **Advanced settings** if needed.
5. Click **Deploy** — the app will be live at a public URL within minutes.

> **Note:** The `data/` directory is gitignored. For the cloud deployment, upload the
> cleaned CSV files via Streamlit's **Secrets** or a connected cloud storage bucket,
> and update `utils.py` to read from that source.
