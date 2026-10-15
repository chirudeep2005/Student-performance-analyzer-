from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

def clean_data(path=HERE / "sales_sample.csv"):
    df = pd.read_csv(path)
    required = {"order_id", "order_date", "region", "category", "quantity", "unit_price"}
    missing = required - set(df.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    df["order_date"] = pd.to_datetime(df.order_date, errors="coerce")
    df["quantity"] = pd.to_numeric(df.quantity, errors="coerce")
    df["unit_price"] = pd.to_numeric(df.unit_price, errors="coerce")
    df = df.dropna(subset=list(required)).drop_duplicates(subset=["order_id"])
    df = df[(df.quantity > 0) & (df.unit_price >= 0)].copy()
    df["revenue"] = df.quantity * df.unit_price
    df["month"] = df.order_date.dt.to_period("M").astype(str)
    return df

def main():
    df = clean_data()
    if df.empty: raise SystemExit("No valid rows remain after cleaning.")
    monthly = df.groupby("month", as_index=False).agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"), average_order_value=("revenue", "mean"))
    category = df.groupby("category", as_index=False).agg(orders=("order_id", "nunique"), revenue=("revenue", "sum")).sort_values("revenue", ascending=False)
    OUT.mkdir(exist_ok=True); df.to_csv(OUT / "cleaned_sales.csv", index=False); monthly.to_csv(OUT / "monthly_summary.csv", index=False); category.to_csv(OUT / "category_summary.csv", index=False)
    plt.figure(figsize=(8, 4.5)); plt.plot(monthly.month, monthly.revenue, marker="o"); plt.xlabel("Month"); plt.ylabel("Revenue (sample units)"); plt.title("Monthly revenue — synthetic demo data"); plt.xticks(rotation=35, ha="right"); plt.tight_layout(); plt.savefig(OUT / "monthly_revenue.png", dpi=160); plt.close()
    print("Analytics demo — synthetic data only")
    print(f"Rows after cleaning: {len(df)} | Unique orders: {df.order_id.nunique()} | Total revenue: {df.revenue.sum():.2f}")
    print("Monthly summary:\n", monthly.round(2).to_string(index=False)); print("Category summary:\n", category.round(2).to_string(index=False))

if __name__ == "__main__": main()
