#!/usr/bin/env python3
"""
Dataset Management Script for Flash-IDPS Research
Checks, downloads, and validates datasets used in Flash-IDPS evaluation.
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Dataset configuration with download links and checksums
DATASET_CONFIG = {
    'CADETS': {
        'path': './data/darpa/cadets',
        'files': ['ta1-cadets-e3.json'],
        'url': 'https://drive.google.com/drive/folders/1fOCY3ERsEmXmvDekG-LUUSjfWs6TRdp-',
        'mirror': 'https://github.com/threaTrace-detector/threaTrace',
        'size_gb': 10,
        'description': 'DARPA TC E3 - FreeBSD multi-stage APT',
        'format': 'DARPA TC Stream format (JSON)',
        'checksum_file': 'cadets.sha256'
    },
    'THEIA': {
        'path': './data/darpa/theia',
        'files': ['ta1-theia-e3.json', 'ta1-theia-e5.json'],
        'url': 'https://www.cdc.gov/das/ddph/datasets/theia/',
        'mirror': 'https://github.com/threaTrace-detector/threaTrace',
        'size_gb': 20,
        'description': 'DARPA TC E3/E5 - Linux insider threat',
        'format': 'DARPA TC Stream format (JSON)',
        'checksum_file': 'theia.sha256'
    },
    'TRACE': {
        'path': './data/darpa/trace',
        'files': ['ta1-trace-e3.json', 'ta1-trace-e5.json'],
        'url': 'https://www.cdc.gov/das/ddph/datasets/trace/',
        'mirror': 'https://github.com/threaTrace-detector/threaTrace',
        'size_gb': 12,
        'description': 'DARPA TC E3/E5 - Linux supply chain attack',
        'format': 'DARPA TC Stream format (JSON)',
        'checksum_file': 'trace.sha256'
    },
    'FIVEDIRECTIONS': {
        'path': './data/darpa/fivedirections',
        'files': ['ta1-fivedirections-e3.json', 'ta1-fivedirections-e5.json'],
        'url': 'https://www.cdc.gov/das/ddph/datasets/fivedirections/',
        'mirror': 'https://github.com/threaTrace-detector/threaTrace',
        'size_gb': 15,
        'description': 'DARPA TC E3/E5 - Windows APT scenarios',
        'format': 'DARPA TC Stream format (JSON)',
        'checksum_file': 'fivedirections.sha256'
    },
    'OpTC': {
        'path': './data/optc',
        'files': ['h201.json', 'h501.json', 'h051.json'],
        'url': 'https://drive.google.com/drive/folders/148g9xkUeE8qGKqg7qGKqg7qGKqg7qGKq',
        'mirror': 'https://github.com/ai-forensics/optc-dataset',
        'size_gb': 50,
        'description': 'DARPA OpTC - Enterprise Windows environment',
        'format': 'DARPA TC Stream format (JSON)',
        'checksum_file': 'optc.sha256'
    },
    'STREAMSPOT': {
        'path': './data/streamspot',
        'files': ['streamspot.json'],
        'url': 'https://github.com/ai-forensics/streamspot',
        'mirror': 'https://github.com/ai-forensics/streamspot',
        'size_gb': 5,
        'description': 'Streaming graph anomaly detection',
        'format': 'Custom JSON format',
        'checksum_file': 'streamspot.sha256'
    },
    'UNICORN': {
        'path': './data/unicorn',
        'files': ['unicorn-sc1.json', 'unicorn-sc2.json'],
        'url': 'https://github.com/ai-forensics/unicorn',
        'mirror': 'https://github.com/ai-forensics/unicorn',
        'size_gb': 8,
        'description': 'Known APT campaigns (SC1, SC2)',
        'format': 'Custom JSON format',
        'checksum_file': 'unicorn.sha256'
    },
    'CLEARSCOPE': {
        'path': './data/darpa/clearscope',
        'files': ['clearscope-e3.json', 'clearscope-e5.json'],
        'url': 'https://www.cdc.gov/das/ddph/datasets/clearscope/',
        'mirror': 'https://github.com/threaTrace-detector/threaTrace',
        'size_gb': 18,
        'description': 'DARPA TC E5 - Android mobile threats',
        'format': 'DARPA TC Stream format (JSON)',
        'checksum_file': 'clearscope.sha256'
    }
}

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def check_dataset_status(dataset_name: str) -> Tuple[bool, str, Dict]:
    """
    Check if a dataset is available and valid.
    
    Returns:
        Tuple[bool, str, Dict]: (is_available, status_message, metadata)
    """
    if dataset_name not in DATASET_CONFIG:
        return False, f"Unknown dataset: {dataset_name}", {}
    
    config = DATASET_CONFIG[dataset_name]
    dataset_path = Path(config['path'])
    
    metadata = {
        'name': dataset_name,
        'path': str(dataset_path),
        'exists': False,
        'size_gb': 0,
        'expected_gb': config['size_gb'],
        'files_present': [],
        'files_missing': [],
        'url': config['url']
    }
    
    # Check if directory exists
    if not dataset_path.exists():
        metadata['status'] = 'missing'
        return False, f"Directory not found at {config['path']}", metadata
    
    metadata['exists'] = True
    
    # Check required files
    for file in config['files']:
        file_path = dataset_path / file
        if file_path.exists():
            metadata['files_present'].append(file)
        else:
            # Try alternative extensions
            for ext in ['.json', '.tar', '.tar.gz', '.dump']:
                alt_file = dataset_path / (file + ext) if not file.endswith(ext) else dataset_path / file
                if alt_file.exists():
                    metadata['files_present'].append(file)
                    break
            else:
                metadata['files_missing'].append(file)
    
    if metadata['files_missing']:
        metadata['status'] = 'incomplete'
        return False, f"Missing files: {', '.join(metadata['files_missing'])}", metadata
    
    # Check approximate size
    total_size = sum(f.stat().st_size for f in dataset_path.rglob('*') if f.is_file())
    size_gb = total_size / (1024**3)
    metadata['size_gb'] = size_gb
    
    if size_gb < config['size_gb'] * 0.5:
        metadata['status'] = 'incomplete'
        return False, f"Size ({size_gb:.1f}GB) is much smaller than expected ({config['size_gb']}GB)", metadata
    
    metadata['status'] = 'available'
    return True, f"Available ({size_gb:.1f}GB)", metadata

def check_all_datasets() -> Dict[str, Tuple[bool, str, Dict]]:
    """Check status of all datasets."""
    results = {}
    for dataset_name in DATASET_CONFIG.keys():
        results[dataset_name] = check_dataset_status(dataset_name)
    return results

def download_dataset(dataset_name: str, use_mirror: bool = False) -> bool:
    """
    Download a specific dataset.
    
    Args:
        dataset_name: Name of the dataset to download
        use_mirror: Use mirror URL instead of primary
    
    Returns:
        bool: True if download was successful
    """
    if dataset_name not in DATASET_CONFIG:
        print_error(f"Unknown dataset: {dataset_name}")
        return False
    
    config = DATASET_CONFIG[dataset_name]
    url = config['mirror'] if use_mirror else config['url']
    
    print_info(f"Downloading {dataset_name}...")
    print_info(f"URL: {url}")
    print_info(f"Expected size: ~{config['size_gb']}GB")
    print_info(f"Destination: {config['path']}")
    
    # Create destination directory
    dest_path = Path(config['path'])
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Try PIDSMaker download script if available
    pidsmaker_script = Path('./pidsmaker/download_datasets.sh')
    if pidsmaker_script.exists():
        print_info("Using PIDSMaker download script...")
        try:
            result = subprocess.run(
                ['bash', str(pidsmaker_script), dataset_name],
                check=True,
                capture_output=True,
                text=True
            )
            print_success(f"Download completed: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print_error(f"Download failed: {e.stderr}")
    
    # Fallback: Manual download instructions
    print_warning("Automatic download not available.")
    print_info(f"Please download manually from: {url}")
    print_info(f"Then extract to: {config['path']}")
    
    # Check if gdown is available for Google Drive links
    if 'drive.google.com' in url:
        try:
            import gdown
            print_info("gdown detected, attempting Google Drive download...")
            # Note: This requires the file ID from the URL
            print_warning("Google Drive download requires manual file ID extraction")
        except ImportError:
            print_info("Install gdown for Google Drive support: pip install gdown")
    
    return False

def generate_status_report(output_file: str = 'dataset_status.json'):
    """Generate a JSON report of dataset status."""
    results = check_all_datasets()
    
    report = {
        'timestamp': str(pd.Timestamp.now()) if 'pd' in globals() else 'N/A',
        'datasets': {}
    }
    
    for dataset_name, (is_available, message, metadata) in results.items():
        report['datasets'][dataset_name] = {
            'available': is_available,
            'status': message,
            **metadata
        }
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_success(f"Status report saved to: {output_file}")
    return report

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Flash-IDPS Dataset Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_datasets.py                    # Check all datasets
  python check_datasets.py --dataset CADETS   # Check specific dataset
  python check_datasets.py --download CADETS  # Download CADETS
  python check_datasets.py --report           # Generate status report
        """
    )
    
    parser.add_argument('--dataset', '-d', type=str, 
                       help='Check specific dataset (CADETS, THEIA, etc.)')
    parser.add_argument('--download', type=str,
                       help='Download specified dataset')
    parser.add_argument('--mirror', action='store_true',
                       help='Use mirror URL for download')
    parser.add_argument('--report', action='store_true',
                       help='Generate JSON status report')
    parser.add_argument('--output', '-o', type=str, default='dataset_status.json',
                       help='Output file for status report')
    
    args = parser.parse_args()
    
    print_header("FLASH-IDPS DATASET MANAGEMENT")
    
    # Download mode
    if args.download:
        success = download_dataset(args.download, args.mirror)
        sys.exit(0 if success else 1)
    
    # Report mode
    if args.report:
        generate_status_report(args.output)
        sys.exit(0)
    
    # Check mode
    if args.dataset:
        is_available, message, metadata = check_dataset_status(args.dataset)
        if is_available:
            print_success(f"{args.dataset}: {message}")
        else:
            print_error(f"{args.dataset}: {message}")
            print_info(f"Download from: {metadata.get('url', 'N/A')}")
        sys.exit(0 if is_available else 1)
    
    # Check all datasets
    results = check_all_datasets()
    available_count = sum(1 for status, _, _ in results.values() if status)
    total_count = len(results)
    
    for dataset_name, (is_available, message, metadata) in results.items():
        if is_available:
            print_success(f"{dataset_name}: {message}")
        else:
            print_error(f"{dataset_name}: {message}")
    
    print()
    print_header("SUMMARY")
    print(f"Available: {available_count}/{total_count} datasets")
    
    if available_count < total_count:
        print()
        print_info("To download missing datasets:")
        print("  python check_datasets.py --download <DATASET_NAME>")
        print()
        print_info("Or download all using PIDSMaker:")
        print("  cd pidsmaker && ./download_datasets.sh")
    
    sys.exit(0 if available_count == total_count else 1)

if __name__ == '__main__':
    main()
