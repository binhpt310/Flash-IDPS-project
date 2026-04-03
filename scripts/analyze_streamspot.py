#!/usr/bin/env python3
"""
Quick analyzer for StreamSpot dataset - helps you understand and prepare the data
for use with Flash IDS in PIDSMaker
"""

import pandas as pd
from pathlib import Path
from collections import Counter
import json
from datetime import datetime, timedelta

STREAMSPOT_DIR = Path('data/streamspot')
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)

def analyze_streamspot():
    """Analyze StreamSpot dataset and generate configuration"""
    
    print("=" * 70)
    print("StreamSpot Dataset Analyzer")
    print("=" * 70)
    
    streamspot_files = sorted(STREAMSPOT_DIR.glob('*.txt'))
    print(f"\n✓ Found {len(streamspot_files)} graph files in {STREAMSPOT_DIR}")
    
    if not streamspot_files:
        print("✗ No StreamSpot files found!")
        return
    
    # Collect statistics
    all_src_types = Counter()
    all_dst_types = Counter()
    all_edge_types = Counter()
    all_labels = Counter()
    edge_counts = []
    node_counts = []
    avg_degree = []
    
    print("\nAnalyzing graph statistics...")
    for i, graph_file in enumerate(streamspot_files):
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{len(streamspot_files)}")
        
        df = pd.read_csv(graph_file, sep='\t', header=None)
        df.columns = ['src_node', 'src_type', 'dst_node', 'dst_type', 'edge_type', 'label']
        
        all_src_types.update(df['src_type'].unique())
        all_dst_types.update(df['dst_type'].unique())
        all_edge_types.update(df['edge_type'].unique())
        all_labels.update(df['label'].unique())
        
        edge_counts.append(len(df))
        nodes = set(df['src_node'].unique()) | set(df['dst_node'].unique())
        node_counts.append(len(nodes))
        avg_degree.append(len(df) / len(nodes) if len(nodes) > 0 else 0)
    
    # Print analysis results
    print("\n" + "=" * 70)
    print("Dataset Statistics")
    print("=" * 70)
    
    print(f"\nGraphs: {len(streamspot_files)}")
    print(f"Edges per graph: {min(edge_counts)} - {max(edge_counts)} (avg: {sum(edge_counts) // len(edge_counts)})")
    print(f"Nodes per graph: {min(node_counts)} - {max(node_counts)} (avg: {sum(node_counts) // len(node_counts)})")
    print(f"Avg degree: {sum(avg_degree) / len(avg_degree):.2f}")
    
    print(f"\nNode Types:")
    all_node_types = set(all_src_types.keys()) | set(all_dst_types.keys())
    for node_type in sorted(all_node_types):
        src_count = all_src_types.get(node_type, 0)
        dst_count = all_dst_types.get(node_type, 0)
        print(f"  {node_type}: src_count={src_count}, dst_count={dst_count}")
    
    print(f"\nEdge Types: {list(sorted(all_edge_types.keys()))}")
    print(f"  Count: {len(all_edge_types)}")
    for edge_type, count in sorted(all_edge_types.items()):
        print(f"    {edge_type}: {count}")
    
    print(f"\nLabels: {dict(all_labels)}")
    
    # Generate config entry
    config_entry = {
        "STREAMSPOT": {
            "raw_dir": "",
            "database": "streamspot",
            "database_all_file": "streamspot",
            "num_node_types": len(all_node_types),
            "num_edge_types": len(all_edge_types),
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "train_dates": generate_train_dates(len(streamspot_files), 0, 0.6),
            "val_dates": generate_train_dates(len(streamspot_files), 0.6, 0.8),
            "test_dates": generate_train_dates(len(streamspot_files), 0.8, 1.0),
            "unused_dates": [],
            "ground_truth_relative_path": [],
            "attack_to_time_window": [],
        }
    }
    
    # Save config
    config_path = OUTPUT_DIR / 'streamspot_config.json'
    with open(config_path, 'w') as f:
        json.dump(config_entry, f, indent=2, default=str)
    
    print("\n" + "=" * 70)
    print("Configuration Entry for PIDSMaker")
    print("=" * 70)
    print(f"\nSave this to: PIDSMaker/pidsmaker/config/config.py")
    print("\nAdd to DATASET_DEFAULT_CONFIG dictionary:\n")
    print(json.dumps(config_entry, indent=4, default=str))
    print(f"\n✓ Config also saved to: {config_path}")
    
    # Generate date mapping
    print("\n" + "=" * 70)
    print("Graph-to-Date Mapping")
    print("=" * 70)
    
    graph_to_date = {}
    start_date = datetime(2024, 1, 1)
    graphs_per_day = max(1, len(streamspot_files) // 30)  # Spread over 30 days
    
    for graph_id in range(len(streamspot_files)):
        day_offset = graph_id // graphs_per_day
        date = (start_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        graph_to_date[f"graph_{graph_id:03d}.txt"] = date
    
    mapping_path = OUTPUT_DIR / 'graph_date_mapping.json'
    with open(mapping_path, 'w') as f:
        json.dump(graph_to_date, f, indent=2)
    
    print(f"✓ Date mapping saved to: {mapping_path}")
    print(f"\nSample mappings:")
    for key in list(graph_to_date.keys())[:5]:
        print(f"  {key} -> {graph_to_date[key]}")
    
    # Generate tips
    print("\n" + "=" * 70)
    print("Next Steps")
    print("=" * 70)
    print("""
1. Copy the config entry above to PIDSMaker/pidsmaker/config/config.py
   
2. In a Python/Jupyter cell, verify the registration:
   from pidsmaker.config import DATASET_DEFAULT_CONFIG
   print("STREAMSPOT" in DATASET_DEFAULT_CONFIG)  # Should be True
   
3. Run Flash IDS:
   cd PIDSMaker
   python pidsmaker/main.py flash STREAMSPOT
   
4. Monitor with W&B:
   python pidsmaker/main.py flash STREAMSPOT --wandb
   
5. Fine-tune parameters:
   python pidsmaker/main.py flash STREAMSPOT \\
       --training.num_epochs=20 \\
       --featurization.emb_dim=64
    """)

def generate_train_dates(total_graphs, start_ratio, end_ratio):
    """Generate date list for graphs"""
    dates = []
    start_date = datetime(2024, 1, 1)
    start_idx = int(total_graphs * start_ratio)
    end_idx = int(total_graphs * end_ratio)
    
    for i in range(start_idx, end_idx):
        day_offset = i // max(1, (end_idx - start_idx) // 30)
        date = (start_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        if date not in dates:
            dates.append(date)
    
    return dates[:10]  # Limit to 10 dates per split

if __name__ == '__main__':
    analyze_streamspot()
