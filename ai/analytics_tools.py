
import pandas as pd

from ai.config import DATA_FILE


def load_upi_data():
    """Load the processed UPI monthly dataset."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        raise ValueError("The UPI dataset is empty.")

    return df


def get_project_summary():
    """Calculate important project statistics."""

    df = load_upi_data()

    volume_col = "Volume (In Mn.)"
    value_col = "Value (In Cr.)"
    avg_col = "Average Transaction Value (₹)"

    summary = {
        "records": len(df),
        "first_month": str(df["Month"].iloc[0]),
        "last_month": str(df["Month"].iloc[-1]),
        "total_volume_mn": round(df[volume_col].sum(), 2),
        "total_value_cr": round(df[value_col].sum(), 2),
        "average_monthly_volume_mn": round(
            df[volume_col].mean(), 2
        ),
        "average_monthly_value_cr": round(
            df[value_col].mean(), 2
        ),
        "average_transaction_value": round(
            df[avg_col].mean(), 2
        ),
    }

    return summary


def get_analytics_context():
    """Create factual dataset context for the RAG assistant."""

    df = load_upi_data()
    summary = get_project_summary()

    volume_col = "Volume (In Mn.)"
    value_col = "Value (In Cr.)"

    first_volume = float(df[volume_col].iloc[0])
    last_volume = float(df[volume_col].iloc[-1])

    first_value = float(df[value_col].iloc[0])
    last_value = float(df[value_col].iloc[-1])

    volume_growth = (
        ((last_volume - first_volume) / first_volume) * 100
        if first_volume else 0
    )

    value_growth = (
        ((last_value - first_value) / first_value) * 100
        if first_value else 0
    )

    return f"""
DATASET ANALYTICS:

Number of monthly records: {summary['records']}
First month: {summary['first_month']}
Last month: {summary['last_month']}

Total transaction volume: {summary['total_volume_mn']} million
Total transaction value: {summary['total_value_cr']} crore

Average monthly transaction volume:
{summary['average_monthly_volume_mn']} million

Average monthly transaction value:
{summary['average_monthly_value_cr']} crore

Average transaction value:
₹{summary['average_transaction_value']}

Volume change from first to last record:
{volume_growth:.2f}%

Value change from first to last record:
{value_growth:.2f}%

These are calculations from the available project dataset.
"""
