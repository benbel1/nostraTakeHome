import json
import numpy as np
from statistics import mean, median

# Function to calculate the metrics for each payload
def calculate_metrics(payload):
    ttfb = payload["responseStart"] - payload["navigationStart"]
    dom_content_loaded_time = payload["domContentLoadedEventEnd"] - payload["navigationStart"]
    page_load_time = payload["loadEventEnd"] - payload["navigationStart"]
    
    return ttfb, dom_content_loaded_time, page_load_time

# Function to compute the 75th percentile
def percentile_75th(data):
    return np.percentile(data, 75)

# Function to aggregate metrics by _edge_assignment
def aggregate_metrics_by_assignment(metrics_by_assignment):
    aggregated_results = {}
    
    for assignment, metrics in metrics_by_assignment.items():
        ttfb_list, dom_list, load_list = zip(*metrics)
        
        aggregated_results[assignment] = {
            "TTFB": {
                "mean": mean(ttfb_list),
                "median": median(ttfb_list),
                "75th_percentile": percentile_75th(ttfb_list)
            },
            "DOM Content Loaded Time": {
                "mean": mean(dom_list),
                "median": median(dom_list),
                "75th_percentile": percentile_75th(dom_list)
            },
            "Page Load Time": {
                "mean": mean(load_list),
                "median": median(load_list),
                "75th_percentile": percentile_75th(load_list)
            }
        }
    
    return aggregated_results

# Main function to process the JSONL file
def process_jsonl_file(file):
    metrics_by_assignment = {}
    
    with open(file, 'r') as file:
        for line in file:
            payload = json.loads(line)
            assignment = payload["_edge_assignment"]
            
            ttfb, dom_time, load_time = calculate_metrics(payload)
            
            if assignment not in metrics_by_assignment:
                metrics_by_assignment[assignment] = []
            
            metrics_by_assignment[assignment].append((ttfb, dom_time, load_time))
    
    aggregated_results = aggregate_metrics_by_assignment(metrics_by_assignment)
    
    return aggregated_results

# Define the file path and process the file
file = 'payload.jsonl'
aggregated_metrics = process_jsonl_file(file)

# Display the results
for assignment, metrics in aggregated_metrics.items():
    print(f"Assignment: {assignment}")
    for metric_name, stats in metrics.items():
        print(f"  {metric_name}:")
        print(f"    Mean: {stats['mean']} ms")
        print(f"    Median: {stats['median']} ms")
        print(f"    75th Percentile: {stats['75th_percentile']} ms")
    print()
