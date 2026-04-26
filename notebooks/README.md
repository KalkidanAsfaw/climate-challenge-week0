# Notebooks

This folder contains Jupyter notebooks for exploratory data analysis (EDA) of African climate data across five countries.

## Notebooks

| Notebook | Country | Description |
|---|---|---|
| `ethiopia_eda.ipynb` | Ethiopia | Data cleaning, outlier detection, time series and correlation analysis |
| `kenya_eda.ipynb` | Kenya | Data cleaning, visualizations, statistical commentary |
| `nigeria_eda.ipynb` | Nigeria | Data cleaning, visualizations, statistical commentary |
| `sudan_eda.ipynb` | Sudan | Data cleaning, outlier detection, time series, correlation, and distribution analysis |
| `tanzania_eda.ipynb` | Tanzania | Data cleaning, visualizations, statistical commentary |

## Running the Notebooks

1. Install dependencies from the project root:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch Jupyter:
   ```bash
   jupyter notebook
   ```

3. Place country CSV files in the `data/` directory before running (see project README for data sources).
