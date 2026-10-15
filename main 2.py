from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
THRESHOLD = 0.80  # illustrative only; validate before real-world use

def load_data(path=HERE / "traffic_sample.csv"):
    df = pd.read_csv(path)
    required = ["timestamp", "road_segment", "vehicle_count", "avg_speed_kmph", "capacity_vehicles"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    for col in ["vehicle_count", "avg_speed_kmph", "capacity_vehicles"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=required)
    df = df[(df.vehicle_count >= 0) & (df.avg_speed_kmph >= 0) & (df.capacity_vehicles > 0)].copy()
    return df

def analyze(df):
    df["utilization"] = df.vehicle_count / df.capacity_vehicles
    df["hour"] = df.timestamp.dt.hour
    df["high_utilization"] = df.utilization >= THRESHOLD
    segments = df.groupby("road_segment", as_index=False).agg(
        observations=("vehicle_count", "size"), avg_vehicle_count=("vehicle_count", "mean"),
        avg_speed_kmph=("avg_speed_kmph", "mean"), avg_utilization=("utilization", "mean"),
        high_utilization_pct=("high_utilization", lambda s: 100 * s.mean()))
    hourly = df.groupby("hour", as_index=False).agg(avg_vehicle_count=("vehicle_count", "mean"), avg_speed_kmph=("avg_speed_kmph", "mean"), avg_utilization=("utilization", "mean"))
    return segments.sort_values("avg_utilization", ascending=False), hourly.sort_values("hour")

def main():
    df = load_data()
    if df.empty:
        raise SystemExit("No valid sample observations found.")
    segments, hourly = analyze(df)
    OUT.mkdir(exist_ok=True)
    segments.to_csv(OUT / "traffic_by_segment.csv", index=False)
    hourly.to_csv(OUT / "hourly_traffic.csv", index=False)
    chart = segments.sort_values("avg_utilization")
    plt.figure(figsize=(8, 4.5)); plt.barh(chart.road_segment, chart.avg_utilization)
    plt.axvline(THRESHOLD, linestyle="--", label="Illustrative threshold")
    plt.xlabel("Vehicle count / illustrative capacity"); plt.title("Sample traffic utilization by segment"); plt.legend(); plt.tight_layout()
    plt.savefig(OUT / "congestion_by_segment.png", dpi=160); plt.close()
    print("Traffic analytics prototype — synthetic sample data only")
    print(segments.round(2).to_string(index=False)); print(f"Outputs saved in {OUT}")

if __name__ == "__main__": main()
