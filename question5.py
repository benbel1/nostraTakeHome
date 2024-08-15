import json
import matplotlib.pyplot as plt

# Function to calculate the core web metrics I've chosen for each payload including the 3 we calculated earlier in Q2
def gather_metrics(payload):
    metrics = {
        "TTFB": payload["responseStart"] - payload["navigationStart"],
        "DOM Content Loaded Time": payload["domContentLoadedEventEnd"] - payload["navigationStart"],
        "Page Load Time": payload["loadEventEnd"] - payload["navigationStart"],
        "Response Duration": payload["responseEnd"] - payload["responseStart"],
        "Time To Interactive": payload["domInteractive"] - payload["navigationStart"]
    }
    return metrics

# Main function to process the JSONL file
def process_jsonl_file(file):
    metrics_by_assignment = {}
    
    with open(file, 'r') as file:
        for line in file:
            payload = json.loads(line)
            assignment = payload["_edge_assignment"]
            
            metrics = gather_metrics(payload)
            
            if assignment not in metrics_by_assignment:
                metrics_by_assignment[assignment] = {metric: [] for metric in metrics}
            
            for metric, value in metrics.items():
                metrics_by_assignment[assignment][metric].append(value)
    
    return metrics_by_assignment

file = 'payload.jsonl'
metrics_by_assignment = process_jsonl_file(file)

# Visualization
def plot_histograms(metrics_by_assignment):
    for metric_name in metrics_by_assignment[next(iter(metrics_by_assignment))]:
        plt.figure(figsize=(12, 6))
        
        for assignment, metrics in metrics_by_assignment.items():
            plt.hist(metrics[metric_name], bins=30, alpha=0.5, label=f'{assignment} ({metric_name})')
        
        plt.title(f'Distribution of {metric_name} by Edge Assignment')
        plt.xlabel(f'{metric_name} (ms)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

plot_histograms(metrics_by_assignment)
