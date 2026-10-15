# Intelligent Traffic Weaving System — Analytics Prototype

Analyzes sample traffic-flow patterns by road segment and hour. Includes input validation, a utilization ratio (vehicle count / illustrative capacity), segment/hour summaries, and a chart.

## Run
`pip install -r requirements.txt` then `python main.py`

Outputs: `outputs/traffic_by_segment.csv`, `outputs/hourly_traffic.csv`, and `outputs/congestion_by_segment.png`.

**Limitations:** CSV data is synthetic. This starter does not run SUMO or fetch OpenStreetMap data. A next step is to export detector observations from SUMO and map segment IDs to OSM road attributes, then validate thresholds using real observations.
