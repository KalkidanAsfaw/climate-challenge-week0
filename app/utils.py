import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

COUNTRIES = ["Ethiopia", "Kenya", "Nigeria", "Sudan", "Tanzania"]

COUNTRY_COLORS = {
    "Ethiopia": "#1565C0",
    "Kenya":    "#2E7D32",
    "Nigeria":  "#E65100",
    "Sudan":    "#B71C1C",
    "Tanzania": "#6A1B9A",
}

VARIABLES = {
    "T2M":          "Mean Temperature (°C)",
    "T2M_MAX":      "Max Temperature (°C)",
    "T2M_MIN":      "Min Temperature (°C)",
    "PRECTOTCORR":  "Precipitation (mm/day)",
    "RH2M":         "Relative Humidity (%)",
    "WS2M":         "Wind Speed (m/s)",
}


def load_all_data() -> pd.DataFrame:
    """Load and concatenate clean CSVs for all five countries."""
    frames = []
    for country in COUNTRIES:
        path = os.path.join(DATA_DIR, f"{country.lower()}_clean.csv")
        if not os.path.exists(path):
            continue
        df_c = pd.read_csv(path, parse_dates=["Date"])
        df_c["Country"] = country
        frames.append(df_c)
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def filter_data(df: pd.DataFrame, countries: list, year_range: tuple) -> pd.DataFrame:
    """Return rows matching the selected countries and year range."""
    mask = df["Country"].isin(countries) & df["YEAR"].between(year_range[0], year_range[1])
    return df[mask].copy()


def get_monthly_avg(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Monthly average of *variable* per country, with a proper datetime column."""
    monthly = (
        df.groupby(["Country", df["Date"].dt.to_period("M")])[variable]
        .mean()
        .reset_index()
    )
    monthly.columns = ["Country", "Period", variable]
    monthly["Date"] = monthly["Period"].dt.to_timestamp()
    return monthly


def get_annual_avg(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Annual average of *variable* per country."""
    return (
        df.groupby(["Country", "YEAR"])[variable]
        .mean()
        .reset_index()
        .rename(columns={variable: f"{variable}_mean"})
    )


def get_summary_stats(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Mean, median, and std of *variable* grouped by country."""
    stats = (
        df.groupby("Country")[variable]
        .agg(Mean="mean", Median="median", Std="std")
        .round(3)
        .sort_values("Mean", ascending=False)
    )
    stats.columns = ["Mean", "Median", "Std Dev"]
    return stats


def get_extreme_heat_counts(df: pd.DataFrame, threshold: float = 35.0) -> pd.DataFrame:
    """Average annual days where T2M_MAX exceeds *threshold* per country."""
    counts = (
        df.groupby(["Country", "YEAR"])
        .apply(lambda g: (g["T2M_MAX"] > threshold).sum(), include_groups=False)
        .reset_index(name="heat_days")
    )
    return counts.groupby("Country")["heat_days"].mean().round(1).reset_index()
