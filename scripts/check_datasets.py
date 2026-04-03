#!/usr/bin/env python3
"""
Dataset Management Script for Flash-IDPS
Checks and validates datasets used in Flash-IDPS evaluation.

Official Flash-IDPS: https://github.com/DART-Laboratory/Flash-IDS
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Dataset configuration with download links
# Updated for 6 official datasets from Flash-IDPS paper (no CLEARSCOPE)
DATASET_CONFIG = {
    'CADETS': {
        'path': './data/darpa/cadets',
        'files': ['ta1-cadets-e3-official-1.bin'],  # Raw file before parsing
        'url': 'https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-',
        'size_gb': 5,
        'description': 'DARPA TC E3 - FreeBSD multi-stage APT'
    },
    'THEIA': {
        'path': './data/darpa/theia',
        'files': ['ta1-theia-e3.json'],
        'url': 'https://github.com/darpa-i2o/Transparent-Computing',
        'size_gb': 20,
        'description': 'DARPA TC E3/E5 - Linux insider threat'
    },
    'TRACE': {
        'path': './data/darpa/trace',
        'files': ['ta1-trace-e3.json'],
        'url': 'https://github.com/darpa-i2o/Transparent-Computing',
        'size_gb': 12,
        'description': 'DARPA TC E3/E5 - Linux supply chain attack'
    },
    'FIVEDIRECTIONS': {
        'path': './data/darpa/fivedirections',
        'files': ['ta1-fivedirections-e3.json'],
        'url': 'https://github.com/darpa-i2o/Transparent-Computing',
        'size_gb': 15,
        'description': 'DARPA TC E3/E5 - Windows APT scenarios'
    },
    'OpTC': {
        'path': './data/optc',
        'files': ['bro'],  # Check for bro directory with log files
        'url': 'https://drive.google.com/drive/u/0/folders/1n3kkS3KR31KUegn42yk3-e6JkZvf0Caa',
        'size_gb': 1000,  # Full dataset ~1TB, but we use subset
        'description': 'DARPA OpTC - Enterprise Windows environment'
    },
    'STREAMSPOT': {
        'path': './data/streamspot',
        'files': ['all.tsv'],  # Raw TSV file before parsing
        'url': 'https://github.com/sbustreamspot/sbustreamspot-data',
        'size_gb': 3,
        'description': 'Streaming graph anomaly detection'
    }
}


def check_dataset_status(dataset_name: str) -> Tuple[bool, str]:
    """
    Check if a dataset is available and valid.

    Returns:
        Tuple[bool, str]: (is_available, status_message)
    """
    if dataset_name not in DATASET_CONFIG:
        return False, f"Unknown dataset: {dataset_name}"

    config = DATASET_CONFIG[dataset_name]
    dataset_path = Path(config['path'])

    # Check if directory exists
    if not dataset_path.exists():
        return False, f"Directory not found at {config['path']}"

    # Check required files
    missing_files = []
    for file in config['files']:
        # Special handling for OpTC - check for bro directory with files
        if file == 'bro':
            bro_path = dataset_path / 'bro'
            if not bro_path.exists():
                missing_files.append('bro/')
            else:
                # Count bro log files
                log_files = list(bro_path.rglob('*.log.gz'))
                if len(log_files) == 0:
                    missing_files.append('bro/*.log.gz')
        elif not (dataset_path / file).exists():
            missing_files.append(file)

    if missing_files:
        return False, f"Missing files: {', '.join(missing_files)}"

    # Check approximate size
    total_size = sum(f.stat().st_size for f in dataset_path.rglob('*') if f.is_file())
    size_gb = total_size / (1024**3)
    expected_gb = config['size_gb']

    # Skip size check for OpTC (we use subset)
    if dataset_name != 'OpTC' and size_gb < expected_gb * 0.1:
        return False, f"Size ({size_gb:.1f}GB) smaller than expected ({expected_gb}GB)"

    return True, f"Available ({size_gb:.2f}GB)"


def check_all_datasets() -> Dict[str, Tuple[bool, str]]:
    """Check status of all datasets."""
    results = {}
    for dataset_name in DATASET_CONFIG.keys():
        results[dataset_name] = check_dataset_status(dataset_name)
    return results


def print_dataset_table():
    """Print dataset information table."""
    print("\n" + "="*80)
    print("FLASH-IDPS DATASETS (6 Official from Paper)")
    print("="*80)
    print(f"{'Dataset':<15} {'OS':<12} {'Size':<10} {'Description':<40}")
    print("-"*80)

    dataset_info = {
        'CADETS': ('FreeBSD', '~5GB', 'DARPA TC E3 - Multi-stage APT'),
        'THEIA': ('Linux', '~20GB', 'DARPA TC E3/E5 - Insider threat'),
        'TRACE': ('Linux', '~12GB', 'DARPA TC E3/E5 - Supply chain attack'),
        'FIVEDIRECTIONS': ('Windows', '~15GB', 'DARPA TC E3/E5 - Windows APT'),
        'OpTC': ('Windows', '~1TB', 'DARPA - Enterprise environment'),
        'STREAMSPOT': ('Linux', '~3GB', 'Streaming graph anomalies')
    }

    for name, (os, size, desc) in dataset_info.items():
        print(f"{name:<15} {os:<12} {size:<10} {desc:<40}")

    print("="*80)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Flash-IDPS Dataset Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_datasets.py                    # Check all datasets
  python check_datasets.py --dataset CADETS   # Check specific dataset
  python check_datasets.py --table            # Show dataset table

Download datasets from:
  - CADETS:     https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-
  - THEIA:      https://github.com/darpa-i2o/Transparent-Computing
  - TRACE:      https://github.com/darpa-i2o/Transparent-Computing
  - FIVEDIRECTIONS: https://github.com/darpa-i2o/Transparent-Computing
  - OpTC:       https://drive.google.com/drive/u/0/folders/1n3kkS3KR31KUegn42yk3-e6JkZvf0Caa
  - STREAMSPOT: https://github.com/sbustreamspot/sbustreamspot-data
        """
    )

    parser.add_argument('--dataset', '-d', type=str,
                       help='Check specific dataset (CADETS, THEIA, etc.)')
    parser.add_argument('--table', '-t', action='store_true',
                       help='Show dataset information table')

    args = parser.parse_args()

    print("\n" + "="*70)
    print("FLASH-IDPS DATASET STATUS CHECK")
    print("="*70 + "\n")

    # Show table mode
    if args.table:
        print_dataset_table()
        sys.exit(0)

    # Check specific dataset
    if args.dataset:
        is_available, message = check_dataset_status(args.dataset)
        config = DATASET_CONFIG.get(args.dataset, {})
        
        if is_available:
            print(f"✅ {args.dataset}: {message}")
        else:
            print(f"❌ {args.dataset}: {message}")
            if config:
                print(f"   Download from: {config.get('url', 'N/A')}")
        sys.exit(0 if is_available else 1)

    # Check all datasets
    results = check_all_datasets()
    available_count = sum(1 for status, _ in results.values() if status)
    total_count = len(results)

    for dataset_name, (is_available, message) in results.items():
        config = DATASET_CONFIG[dataset_name]
        if is_available:
            print(f"✅ {dataset_name}: {message}")
        else:
            print(f"❌ {dataset_name}: {message}")
            print(f"   Download: {config['url']}")

    print()
    print("="*70)
    print(f"Summary: {available_count}/{total_count} datasets available")
    print("="*70)

    if available_count < total_count:
        print("\n💡 To download missing datasets:")
        print("   1. Visit the URLs listed above")
        print("   2. Download and extract to the specified paths")
        print("   3. Re-run this script to verify")

    sys.exit(0 if available_count == total_count else 1)


if __name__ == '__main__':
    main()
