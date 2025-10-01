import os
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # use non-GUI backend to avoid Tk/Tcl errors
import matplotlib.pyplot as plt


# ------------ Paths ------------
BASE = Path(__file__).resolve().parents[1]      # the 'customer-churn-analysis' folder
DATA = BASE / "data"
IMAGES = BASE / "images"
IMAGES.mkdir(exist_ok=True)

# default CSV name (change here if your file is named differently)
CSV_PATH = DATA / "customer_churn.csv"


# ------------ Helpers ------------
def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Couldn't find {csv_path}.\n"
            f"Make sure your dataset is here: {csv_path.as_posix()}\n"
            f"Expected columns include: CustomerID, Churn, Contract, Tenure, MonthlyCharges"
        )
    df = pd.read_csv(csv_path)
    return df


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names (lowercase, underscores)
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Common column aliases from Telco churn datasets
    # We'll try to align to: churn, contract, tenure, monthly_charges
    rename_map = {
        "customerid": "customer_id",
        "monthlycharges": "monthly_charges",
    }
    df.rename(columns=rename_map, inplace=True)

    # Coerce churn to Yes/No strings if it's True/False or 1/0
    if "churn" in df.columns:
        df["churn"] = df["churn"].astype(str).str.strip().str.title()  # e.g., "Yes"/"No"
        df["churn"] = df["churn"].replace({"1": "Yes", "0": "No", "True": "Yes", "False": "No"})
    else:
        raise KeyError("Expected a 'churn' column (values like Yes/No).")

    # Make sure key numeric fields are numeric if present
    for col in ["tenure", "monthly_charges"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def compute_metrics(df: pd.DataFrame) -> dict:
    results = {}

    # Overall churn rate
    churn_counts = df["churn"].value_counts(dropna=False)
    yes = churn_counts.get("Yes", 0)
    total = churn_counts.sum()
    churn_rate = yes / total if total else 0.0
    results["overall_churn_rate"] = churn_rate

    # Churn by contract
    if "contract" in df.columns:
        contract_churn = (
            df.groupby("contract")["churn"]
              .value_counts(normalize=True)
              .rename("rate")
              .reset_index()
              .pivot(index="contract", columns="churn", values="rate")
              .fillna(0.0)
        )
        results["churn_by_contract"] = contract_churn
    else:
        results["churn_by_contract"] = None

    # Simple stats (optional)
    if "tenure" in df.columns:
        results["avg_tenure"] = df["tenure"].mean()
    if "monthly_charges" in df.columns:
        results["avg_monthly_charges"] = df["monthly_charges"].mean()

    return results


def plot_churn_distribution(df: pd.DataFrame, outpath: Path) -> Path:
    ax = df["churn"].value_counts().plot(kind="bar", title="Churn Distribution")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Count")
    fig = ax.get_figure()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    return outpath


def main():
    print(f"Loading data from: {CSV_PATH}")
    df_raw = load_data(CSV_PATH)
    df = basic_clean(df_raw)

    metrics = compute_metrics(df)

    print("\n=== RESULTS ===")
    print(f"Overall churn rate: {metrics['overall_churn_rate'] * 100:.2f}%")
    if metrics["churn_by_contract"] is not None:
        print("\nChurn by contract type (rates):")
        # Multiply by 100 for readability
        display_df = (metrics["churn_by_contract"] * 100).round(2)
        print(display_df)
    if "avg_tenure" in metrics:
        print(f"\nAverage tenure (months): {metrics['avg_tenure']:.2f}")
    if "avg_monthly_charges" in metrics:
        print(f"Average monthly charges: ${metrics['avg_monthly_charges']:.2f}")

    # Save a simple chart
    out_img = IMAGES / "churn_distribution.png"
    plot_churn_distribution(df, out_img)
    print(f"\nSaved chart to: {out_img.as_posix()}")


if __name__ == "__main__":
    main()
